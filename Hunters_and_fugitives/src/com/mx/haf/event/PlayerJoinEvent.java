package com.mx.haf.event;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.GameMode;
import org.bukkit.Location;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;

import static com.mx.haf.HuntersAndFugitives.*;
import static com.mx.haf.event.GetWorldEvent.world;
import static com.mx.haf.event.PlayerLeaveEvent.isLeave;
import static com.mx.haf.other.ExitGame.leaveAllTeams;
import static com.mx.haf.other.OverGame.*;

public class PlayerJoinEvent implements Listener {
    @EventHandler
    public void playerJoin(org.bukkit.event.player.PlayerJoinEvent event) {
        Player player = event.getPlayer();
        if (isStart) {
            Bukkit.getScheduler().runTask(mainPlugin, () -> player.setGameMode(GameMode.SPECTATOR));
            if (Hunters.hasEntry(player.getName())) {
                Hunters.removeEntry(player.getName());
            } else if (Fugitives.hasEntry(player.getName())) {
                Fugitives.removeEntry(player.getName());
            } else if (!Audience.hasEntry(player.getName())) {
                Audience.addEntry(player.getName());
            }
            player.sendMessage(ChatColor.YELLOW + "因为你已经退出，所以自动死亡，已经成为观众");
        } else if (isLeave) {
            Bukkit.getScheduler().runTask(mainPlugin, () -> {
                player.setGameMode(GameMode.ADVENTURE);
                player.teleport(new Location(world, randomX, 255, randomZ));
            });
            leaveAllTeams(player);
            setEffect(player);
            player.sendMessage(ChatColor.YELLOW + "游戏已经结束");
        }
    }
}
