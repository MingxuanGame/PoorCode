package com.mx.haf.command;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Location;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.ConsoleCommandSender;
import org.bukkit.entity.Entity;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.NotNull;

import java.util.List;

import static com.mx.haf.HuntersAndFugitives.isStart;
import static com.mx.haf.HuntersAndFugitives.mainPlugin;
import static com.mx.haf.event.GetWorldEvent.world;
import static com.mx.haf.other.OverGame.*;
import static org.apache.commons.lang.math.RandomUtils.nextInt;
import static org.bukkit.Bukkit.selectEntities;

public class RandomTeleportCommand implements CommandExecutor {
    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, @NotNull String label, @NotNull String[] args) {
        if (sender instanceof Player) {
            if (randomTeleport(isStart)) {
                sender.sendMessage(ChatColor.GREEN + "随机切换地点已经完成");
            } else {
                sender.sendMessage(ChatColor.RED + "游戏已经开始，不能随机切换地点");
            }
        } else {
            if (randomTeleport(isStart)) {
                Command.broadcastCommandMessage(sender, ChatColor.GREEN + "随机切换地点已经完成");
            } else {
                Command.broadcastCommandMessage(sender, ChatColor.RED + "游戏已经开始，不能随机切换地点");
            }
        }
        return true;
    }

    private boolean randomTeleport(boolean isStart) {
        if (isStart) {
            return false;
        } else {
            randomX = nextInt(100000);
            randomZ = nextInt(100000);
            ConsoleCommandSender sender = Bukkit.getConsoleSender();
            List<Entity> allPlayer = selectEntities(sender, "@a");
            for (Entity e : allPlayer) {
                setEffect((LivingEntity) e);
                Bukkit.getScheduler().runTask(mainPlugin, () -> {
                    e.teleport(new Location(world, randomX, 255, randomZ));
                });
                world.setSpawnLocation(new Location(world, randomX, 255, randomZ));
            }
            return true;
        }
    }
}
