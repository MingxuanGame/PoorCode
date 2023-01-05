package com.mx.haf.event;

import com.mx.haf.other.OverGame;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.GameMode;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerQuitEvent;

import static com.mx.haf.HuntersAndFugitives.*;
import static com.mx.haf.other.LocationTimer.thread;

public class PlayerLeaveEvent implements Listener {
    public static boolean isLeave = false;

    @EventHandler
    public void playerJoin(PlayerQuitEvent event) {
        if (isStart) {
            Player player = event.getPlayer();
            Bukkit.getScheduler().runTask(mainPlugin, () -> player.setGameMode(GameMode.SPECTATOR));
            if (Hunters.hasEntry(player.getName())) {
                Hunters.removeEntry(player.getName());
            } else if (Fugitives.hasEntry(player.getName())) {
                Fugitives.removeEntry(player.getName());
            } else if (!Audience.hasEntry(player.getName())) {
                Audience.addEntry(player.getName());
            }
            Bukkit.broadcastMessage(ChatColor.GREEN + player.getName() + ChatColor.GOLD + "已经退出");
            if (Fugitives.getSize() == 0) {
                Bukkit.broadcastMessage(ChatColor.YELLOW + "所有逃亡者死亡，游戏结束！");
                thread.stop();
                OverGame.clearGame(false);
            }
        }
        isLeave = true;
    }
}
