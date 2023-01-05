package com.mx.haf.event;

import com.mx.haf.other.OverGame;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.entity.EntityType;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;

import static com.mx.haf.other.LocationTimer.thread;

public class EntityDeathEvent implements Listener {
    @EventHandler
    public void endDragonDeath(org.bukkit.event.entity.EntityDeathEvent event) {
        if (event.getEntity().getType() == EntityType.ENDER_DRAGON) {
            Bukkit.broadcastMessage(ChatColor.YELLOW + "末影龙已死亡，逃亡者胜利！");
            thread.stop();
            OverGame.clearGame(false);
        }
    }
}
