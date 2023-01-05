package com.mx.haf.command;

import com.mx.haf.other.OverGame;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.jetbrains.annotations.NotNull;

import static com.mx.haf.HuntersAndFugitives.isStart;

public class OverCommand implements CommandExecutor {
    @Override
    public boolean onCommand(CommandSender commandSender, @NotNull Command command, @NotNull String s, String[] strings) {
        OverGame.clearGame(false);
        commandSender.sendMessage(ChatColor.GREEN + "游戏已经结束");
        isStart = false;
        return true;
    }
}
