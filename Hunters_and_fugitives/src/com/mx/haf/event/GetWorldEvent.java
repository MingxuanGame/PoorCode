package com.mx.haf.event;

import org.bukkit.World;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;

public class GetWorldEvent implements Listener {

    public static World world;

    @EventHandler
    public void playerJoin(PlayerJoinEvent event) {
        world = event.getPlayer().getWorld();
    }
}
