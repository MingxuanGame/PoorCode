package com.mx.haf.command;

import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.NotNull;

import static com.mx.haf.other.ExitGame.leaveAllTeams;

public class LeaveCommand implements CommandExecutor {
    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, @NotNull String s, String[] args) {
        if (sender instanceof Player) {
            leaveAllTeams((Player) sender);
            sender.sendMessage(ChatColor.GREEN + "成功退出所有队伍");
        } else {
            Command.broadcastCommandMessage(sender, ChatColor.RED + "错误：控制台不能参加游戏");
        }
        return true;
    }
}
