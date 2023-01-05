package com.mx.haf.command;

import com.mx.haf.HuntersAndFugitives;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.NotNull;

import static com.mx.haf.HuntersAndFugitives.*;

public class SetModeCommand implements CommandExecutor {
    public static int oldGameTime;

    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, @NotNull String label, @NotNull String[] args) {
        if (sender instanceof Player) {
            if (args.length > 0) {
                if (setMode(Boolean.parseBoolean(args[0]))) {
                    if (isRapidly) {
                        sender.sendMessage(ChatColor.GREEN + "设置成功，当前是" + ChatColor.GOLD + "速通模式");
                    } else {
                        sender.sendMessage(ChatColor.GREEN + "设置成功，当前是" + ChatColor.GOLD + "普通模式");
                    }
                } else {
                    sender.sendMessage(ChatColor.RED + "游戏已经开始，不允许设置模式");
                }
            }
        } else {
            if (args.length > 0) {
                if (setMode(Boolean.parseBoolean(args[0]))) {
                    if (isRapidly) {
                        Command.broadcastCommandMessage(sender, ChatColor.GREEN + "设置成功，当前是" + ChatColor.GOLD + "速通模式");
                    } else {
                        Command.broadcastCommandMessage(sender, ChatColor.GREEN + "设置成功，当前是" + ChatColor.GOLD + "普通模式");
                    }
                } else {
                    Command.broadcastCommandMessage(sender, ChatColor.RED + "游戏已经开始，不允许设置模式");
                }
            }
        }
        return true;
    }

    private boolean setMode(boolean isRapidly) {
        if (!isStart) {
            if (isRapidly) {
                oldGameTime = GameTime;
                GameTime = 2147483647;
                HuntersAndFugitives.isRapidly = true;
            } else {
                GameTime = oldGameTime;
                HuntersAndFugitives.isRapidly = false;
            }
            return true;
        }
        return false;
    }
}
