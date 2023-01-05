package com.mx.haf.other;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.GameMode;
import org.bukkit.Location;
import org.bukkit.command.ConsoleCommandSender;
import org.bukkit.entity.Entity;
import org.bukkit.entity.LivingEntity;
import org.bukkit.entity.Player;
import org.bukkit.potion.PotionEffect;
import org.bukkit.potion.PotionEffectType;

import java.util.List;

import static com.mx.haf.HuntersAndFugitives.*;
import static com.mx.haf.event.GetWorldEvent.world;
import static com.mx.haf.other.ExitGame.leaveAllTeams;
import static com.mx.haf.other.OverGame.*;
import static org.bukkit.Bukkit.selectEntities;

@SuppressWarnings("ALL")
public class LocationTimer {
    public static Thread thread;
    public static short min = 0;

    public static void main() {
        thread = new Thread(() -> {
            while (!(min >= GameTime) && isStart && Fugitives.getSize() > 0) {
                Time.setScore(GameTime - min);
                ConsoleCommandSender sender = Bukkit.getConsoleSender();
                List<Entity> PlayerList = selectEntities(sender, "@a[team=Fugitives]");
                Bukkit.broadcastMessage(ChatColor.GOLD + "坐标提供：");
                for (Entity entity : PlayerList) {
                    Bukkit.broadcastMessage(ChatColor.GREEN + entity.getName() + "的坐标：" + ChatColor.AQUA + "X:" + (int) entity.getLocation().getX() + "  Y：" + (int) entity.getLocation().getY() + "  Z：" + (int) entity.getLocation().getZ());
                }
                if(GameTime-min==1){
                    List<Entity> allPlayer = selectEntities(sender, "@a");
                    Bukkit.broadcastMessage(ChatColor.GOLD  + "决斗开始！");
                    for (Entity e : allPlayer) {
                        Player player = (Player) e;
                        setEffect((LivingEntity) e);
                        Bukkit.getScheduler().runTask(mainPlugin, () -> {
                            e.teleport(new Location(world, randomX, 255, randomZ));
                        });
                    }
                    try {
                        Thread.sleep(10000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    for (Entity e : allPlayer) {
                        PotionEffectType[] effectTypes = {PotionEffectType.DAMAGE_RESISTANCE,PotionEffectType.REGENERATION,PotionEffectType.SATURATION,PotionEffectType.WEAKNESS};
                        for(PotionEffectType effect : effectTypes) {
                            ((LivingEntity) e).removePotionEffect(effect);
                        }
                    }
                }
                min++;
                try {
                    Thread.sleep(60000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            if (!(Fugitives.getSize() <= 0) && isStart) {
                Bukkit.broadcastMessage(ChatColor.YELLOW + "时间到！");
                OverGame.clearGame(true);
            }
        });
    }
}
