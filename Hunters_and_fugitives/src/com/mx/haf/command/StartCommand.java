package com.mx.haf.command;

import com.mx.haf.other.GameTimer;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.GameMode;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Entity;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Player;
import org.bukkit.potion.PotionEffect;
import org.bukkit.potion.PotionEffectType;
import org.jetbrains.annotations.NotNull;

import java.util.List;
import java.util.Objects;

import static com.mx.haf.HuntersAndFugitives.*;
import static org.bukkit.Bukkit.selectEntities;


@SuppressWarnings("ALL")
public class StartCommand implements CommandExecutor {

    private static boolean startValidation(int One, int Two) {
        return Math.max(1.9, One / Two) == Math.min(One / Two, 3.1);
    }

    private static void startGame(CommandSender sender) {
        List<Entity> huntersPlayer = selectEntities(sender, "@a[team=Hunters]");
        List<Entity> fugitivesPlayer = selectEntities(sender, "@a[team=Fugitives]");
        List<Entity> audiencePlayer = selectEntities(sender, "@a[team=Audience]");
        List<Entity> allPlayer = selectEntities(sender, "@a");
        ((Player) sender).performCommand("spreadplayers ~ ~ 5 8 false @a");
        ((Player) sender).performCommand("effect clear @a");
        ((Player) sender).performCommand("clear @a");
        ((Player) sender).performCommand("advancement revoke @a everything");
        for (Entity e : huntersPlayer) {
            Player player = (Player) e;
            player.setGameMode(GameMode.SURVIVAL);
        }
        for (Entity e : fugitivesPlayer) {
            Player player = (Player) e;
            player.setGameMode(GameMode.SURVIVAL);
        }
        for (Entity e : audiencePlayer) {
            Player player = (Player) e;
            player.setGameMode(GameMode.SPECTATOR);
        }
        for (Entity e : allPlayer) {
            ((Player) e).setScoreboard(Timer);
        }
        Bukkit.broadcastMessage(ChatColor.GOLD + "比赛开始！");
        Bukkit.broadcastMessage(ChatColor.GOLD + "逃亡者是：");
        for(Entity e:fugitivesPlayer){
            Bukkit.broadcastMessage(ChatColor.GREEN + e.getName());
        }
        Bukkit.getScheduler().runTask(mainPlugin, () -> {
            PotionEffect effect = new PotionEffect(PotionEffectType.SPEED, 10, 3, false, false);
            for (Entity entity:fugitivesPlayer) {
                ((LivingEntity)entity).addPotionEffect(effect);
            }
        });
        GameTimer.main();
    }

    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, @NotNull String s, String[] strings) {
        if (sender instanceof Player) {
            int HuntersCount = Hunters.getSize();
            int FugitivesCount = Fugitives.getSize();
            boolean validationResults;
            if (FugitivesCount != 0) {
                validationResults = startValidation(HuntersCount, FugitivesCount);
            } else {
                sender.sendMessage(ChatColor.RED + "错误：逃亡者队当前是0人");
                return true;
            }
            if (validationResults) {
                startGame(sender);
            } else if (Objects.equals(strings[0], "f")) {
                startGame(sender);
            } else if (Objects.equals(strings[0], "l")) {
                sender.sendMessage(ChatColor.GREEN + String.format("猎人队共有%s人", HuntersCount));
                sender.sendMessage(ChatColor.GREEN + String.format("逃亡者队共有%s人", FugitivesCount));
            } else {
                sender.sendMessage(ChatColor.RED + "人数比异常");
                sender.sendMessage(ChatColor.BLUE + String.format("猎人队共有%s人", HuntersCount));
                sender.sendMessage(ChatColor.BLUE + String.format("逃亡者队共有%s人", FugitivesCount));
            }
        } else {
            Command.broadcastCommandMessage(sender, ChatColor.RED + "错误：控制台不能开启游戏");
        }
        return true;
    }
}
