package com.mx.haf.command;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.ConsoleCommandSender;
import org.bukkit.entity.Entity;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

import static com.mx.haf.HuntersAndFugitives.*;
import static org.bukkit.Bukkit.selectEntities;

public class SearchCommand implements CommandExecutor {
    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, @NotNull String label, String[] strings) {
        if (sender instanceof Player) {
            if (strings.length > 0) {
                if (Objects.equals(strings[0], "ows")) {
                    sender.sendMessage(ChatColor.GREEN + "你当前所在队伍是：" + ChatColor.GOLD + getPlayerInTeam(sender.getName()));
                } else {
                    if (sender.hasPermission("haf.se.team")) {
                        List<String> players = getPlayers(strings[0]);
                        if (players == null && !Objects.equals(strings[0], "ows")) {
                            sender.sendMessage(ChatColor.RED + "你所查询的队伍不存在，请使用 /help search 查看支持的队伍");
                        } else {
                            assert players != null;
                            sender.sendMessage(ChatColor.GREEN + "你所查询的队伍有" + players.size() + "名玩家");
                            for (String s : players) {
                                sender.sendMessage(ChatColor.GREEN + s);
                            }
                        }
                    } else {
                        sender.sendMessage(ChatColor.RED + "你没有权限");
                    }
                }
            } else {
                sender.sendMessage(ChatColor.RED + "参数不足");
            }
        } else {
            if (strings.length > 0) {
                List<String> players = getPlayers(strings[0]);
                if (players == null && !Objects.equals(strings[0], "ows")) {
                    Command.broadcastCommandMessage(sender, ChatColor.RED + "你所查询的队伍不存在，请使用 /help search 查看支持的队伍");
                } else if (Objects.equals(strings[0], "ows")) {
                    Command.broadcastCommandMessage(sender, ChatColor.RED + "控制台不能查询自己所在的队伍");
                } else {
                    assert players != null;
                    Command.broadcastCommandMessage(sender, ChatColor.GREEN + "你所查询的队伍有" + players.size() + "名玩家");
                    for (String s : players) {
                        Command.broadcastCommandMessage(sender, ChatColor.GREEN + s);
                    }
                }
            } else {
                Command.broadcastCommandMessage(sender, ChatColor.RED + "参数不足");
            }
        }
        return true;
    }

    private List<String> getPlayers(String team) {
        List<String> playerList = new ArrayList<>();
        ConsoleCommandSender sender = Bukkit.getConsoleSender();
        List<Entity> teamPlayers;
        switch (team) {
            case "h":
                teamPlayers = selectEntities(sender, "@a[team=Hunters]");
                break;
            case "f":
                teamPlayers = selectEntities(sender, "@a[team=Fugitives]");
                break;
            case "a":
                teamPlayers = selectEntities(sender, "@a[team=Audience]");
                break;
            default:
                return null;
        }
        for (Entity e : teamPlayers) {
            playerList.add(e.getName());
        }
        return playerList;
    }

    private String getPlayerInTeam(String player) {
        if (Hunters.hasEntry(player)) {
            return "猎人队";
        } else if (Fugitives.hasEntry(player)) {
            return "逃亡者队";
        } else if (Audience.hasEntry(player)) {
            return "观众";
        } else {
            return "无队伍";
        }
    }
}
