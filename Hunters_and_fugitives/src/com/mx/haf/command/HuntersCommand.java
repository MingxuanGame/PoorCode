package com.mx.haf.command;

import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.NotNull;

import static com.mx.haf.HuntersAndFugitives.*;


public class HuntersCommand implements CommandExecutor {
    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, @NotNull String s, String[] strings) {
        if (sender instanceof Player) {
            if (Fugitives.hasEntry(sender.getName())) {
                sender.sendMessage(ChatColor.RED + "你已经加入逃亡者队了");
            } else if (Hunters.hasEntry(sender.getName())) {
                sender.sendMessage(ChatColor.RED + "你已经加入猎人队了");
            } else if (Audience.hasEntry(sender.getName())) {
                sender.sendMessage(ChatColor.RED + "你已经成为了观众");
            } else {
                Hunters.addEntry(sender.getName());
                sender.sendMessage(ChatColor.GREEN + "你成功加入猎人队");
            }
        } else {
            Command.broadcastCommandMessage(sender, ChatColor.RED + "控制台不允许参加游戏");
        }
        return true;
    }
}
