package com.mx.haf.other;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.GameMode;
import org.bukkit.Location;
import org.bukkit.command.ConsoleCommandSender;
import org.bukkit.entity.Entity;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Player;
import org.bukkit.potion.PotionEffect;
import org.bukkit.potion.PotionEffectType;

import java.util.List;

import static com.mx.haf.HuntersAndFugitives.*;
import static com.mx.haf.event.GetWorldEvent.world;
import static com.mx.haf.other.ExitGame.leaveAllTeams;
import static com.mx.haf.other.LocationTimer.min;
import static com.mx.haf.other.LocationTimer.thread;
import static org.apache.commons.lang.math.RandomUtils.nextInt;
import static org.bukkit.Bukkit.selectEntities;

public class OverGame {
    public static int randomX;
    public static int randomZ;

    public static void clearGame(boolean timerOver) {
        if (timerOver) {
            Bukkit.broadcastMessage(ChatColor.GREEN + "逃亡者" + ChatColor.GOLD + "获胜！");
        }
        min = 0;
        isStart = false;
        Time.setScore(-1);
        ConsoleCommandSender sender = Bukkit.getConsoleSender();
        List<Entity> allPlayer = selectEntities(sender, "@a");
        randomX = nextInt(100000);
        randomZ = nextInt(100000);
        for (Entity e : allPlayer) {
            leaveAllTeams((Player) e);
            Player player = (Player) e;
            setEffect((LivingEntity) e);
            Bukkit.getScheduler().runTask(mainPlugin, () -> {
                player.setGameMode(GameMode.ADVENTURE);
                e.teleport(new Location(world, randomX, 255, randomZ));
            });
        }
        world.setSpawnLocation(new Location(world, randomX, 255, randomZ));
        if (thread.isAlive()) {
            thread.stop();
        }
    }

    public static void setEffect(LivingEntity livingEntity) {
        Bukkit.getScheduler().runTask(mainPlugin, () -> {
            PotionEffect[] effects = {new PotionEffect(PotionEffectType.DAMAGE_RESISTANCE, 999999, 50, false, false), new PotionEffect(PotionEffectType.SATURATION, 999999, 50, false, false), new PotionEffect(PotionEffectType.WEAKNESS, 999999, 50, false, false), new PotionEffect(PotionEffectType.REGENERATION, 999999, 50, false, false)};
            for (PotionEffect effect : effects) {
                livingEntity.addPotionEffect(effect);
            }
        });
    }
}
