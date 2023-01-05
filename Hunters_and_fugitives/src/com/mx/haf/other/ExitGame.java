package com.mx.haf.other;

import org.bukkit.entity.Player;

import static com.mx.haf.HuntersAndFugitives.*;

public class ExitGame {
    public static void leaveAllTeams(Player player) {
        if (Hunters.hasEntry(player.getName())) {
            Hunters.removeEntry(player.getName());
        } else if (Fugitives.hasEntry(player.getName())) {
            Fugitives.removeEntry(player.getName());
        } else if (Audience.hasEntry(player.getName())) {
            Audience.removeEntry(player.getName());
        }
    }
}
