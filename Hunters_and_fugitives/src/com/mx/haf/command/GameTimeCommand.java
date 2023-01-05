package com.mx.haf.command;

import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.NotNull;

import static com.mx.haf.HuntersAndFugitives.GameTime;

public class GameTimeCommand implements CommandExecutor {

    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, @NotNull String s, String[] args) {
        if (sender instanceof Player) {
            if (args.length < 1) {
                sender.sendMessage(ChatColor.RED + "请输入时间");
            } else {
                try {
                    GameTime = Integer.parseInt(args[0]);
                    sender.sendMessage(ChatColor.GREEN + "游戏时间成功设置为" + args[0]);
                } catch (NumberFormatException e) {
                    sender.sendMessage(ChatColor.RED + "错误：输入的不是整形数字");
                }
            }
        } else {
            if (args.length < 1) {
                Command.broadcastCommandMessage(sender, ChatColor.RED + "请输入时间");
            } else {
                try {
                    GameTime = Integer.parseInt(args[0]);
                    Command.broadcastCommandMessage(sender, ChatColor.GREEN + "游戏时间成功设置为" + args[0]);
                } catch (NumberFormatException e) {
                    Command.broadcastCommandMessage(sender, ChatColor.RED + "错误：输入的不是整形数字");
                }
            }
        }
        return true;
    }
}
