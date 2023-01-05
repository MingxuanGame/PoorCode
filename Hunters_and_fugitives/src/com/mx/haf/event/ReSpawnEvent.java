package com.mx.haf.event;

import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerRespawnEvent;

import static com.mx.haf.HuntersAndFugitives.isStart;
import static com.mx.haf.other.OverGame.setEffect;

public class ReSpawnEvent implements Listener {
    @EventHandler
    public void playerReSpawn(PlayerRespawnEvent event) {
        if (!isStart) {
            setEffect(event.getPlayer());
        }
    }
}
