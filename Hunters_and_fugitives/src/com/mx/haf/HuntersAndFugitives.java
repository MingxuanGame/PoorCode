package com.mx.haf;

import com.mx.haf.command.*;
import com.mx.haf.event.*;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scoreboard.*;

import java.util.Objects;

import static org.bukkit.scoreboard.Team.Option.COLLISION_RULE;
import static org.bukkit.scoreboard.Team.OptionStatus.FOR_OWN_TEAM;

public class HuntersAndFugitives extends JavaPlugin {
    public static Team Hunters;
    public static Team Fugitives;
    public static Team Audience;
    public static Scoreboard Timer;
    public static Objective Number;
    public static HuntersAndFugitives mainPlugin;
    public static int GameTime = 10;
    public static Score Time;
    public static boolean isStart = false;
    public static boolean isRapidly = false;

    @Override
    public void onEnable() {
        mainPlugin = this;
        Timer = Objects.requireNonNull(Bukkit.getScoreboardManager()).getNewScoreboard();
        Number = Timer.registerNewObjective("Timer", "dummy", "§e猎人追杀计时器");
        Number.setDisplaySlot(DisplaySlot.SIDEBAR);
        Time = Number.getScore("剩余时间（分钟）");
        Time.setScore(-1);
        Hunters = Objects.requireNonNull(getServer().getScoreboardManager()).getMainScoreboard().registerNewTeam("Hunters");
        Fugitives = Objects.requireNonNull(getServer().getScoreboardManager()).getMainScoreboard().registerNewTeam("Fugitives");
        Audience = Objects.requireNonNull(getServer().getScoreboardManager()).getMainScoreboard().registerNewTeam("Audience");
        Fugitives.setColor(ChatColor.GREEN);
        Hunters.setColor(ChatColor.GOLD);
        Fugitives.setOption(COLLISION_RULE, FOR_OWN_TEAM);
        Objects.requireNonNull(this.getCommand("hunter")).setExecutor(new HuntersCommand());
        Objects.requireNonNull(this.getCommand("fugitive")).setExecutor(new FugitivesCommand());
        Objects.requireNonNull(this.getCommand("gametime")).setExecutor(new GameTimeCommand());
        Objects.requireNonNull(this.getCommand("over")).setExecutor(new OverCommand());
        Objects.requireNonNull(this.getCommand("start")).setExecutor(new StartCommand());
        Objects.requireNonNull(this.getCommand("leave")).setExecutor(new LeaveCommand());
        Objects.requireNonNull(this.getCommand("audience")).setExecutor(new AudienceCommand());
        Objects.requireNonNull(this.getCommand("search")).setExecutor(new SearchCommand());
        Objects.requireNonNull(this.getCommand("rt")).setExecutor(new RandomTeleportCommand());
        Objects.requireNonNull(this.getCommand("setmode")).setExecutor(new SetModeCommand());
        getServer().getPluginManager().registerEvents(new EntityDeathEvent(), this);
        getServer().getPluginManager().registerEvents(new FugitivesDeathEvent(), this);
        getServer().getPluginManager().registerEvents(new GetWorldEvent(), this);
        getServer().getPluginManager().registerEvents(new ReSpawnEvent(), this);
        getServer().getPluginManager().registerEvents(new PlayerJoinEvent(), this);
        getServer().getPluginManager().registerEvents(new PlayerLeaveEvent(), this);
        getLogger().info("猎人追杀已经开启");
    }

    public void onDisable() {
        Hunters.unregister();
        Fugitives.unregister();
        Audience.unregister();
        getLogger().info("猎人追杀已经卸载");
    }
}
