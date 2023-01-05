package com.mx.haf.event;

import com.mx.haf.other.OverGame;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.GameMode;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.PlayerDeathEvent;

import java.util.Objects;

import static com.mx.haf.HuntersAndFugitives.Fugitives;
import static com.mx.haf.other.LocationTimer.thread;

public class FugitivesDeathEvent implements Listener {
    @EventHandler
    public void deathPlayer(PlayerDeathEvent event) {
        if (Fugitives.hasEntry(event.getEntity().getName())) {
            Bukkit.broadcastMessage(ChatColor.GREEN + event.getEntity().getName() + ChatColor.GOLD + "已死亡");
            Objects.requireNonNull(event.getEntity().getPlayer()).setGameMode(GameMode.SPECTATOR);
            Fugitives.removeEntry(event.getEntity().getName());
            if (Fugitives.getSize() == 0) {
                Bukkit.broadcastMessage(ChatColor.YELLOW + "所有逃亡者死亡，游戏结束！");
                thread.stop();
                OverGame.clearGame(false);
            }
        }
    }
}
