package com.apocalypsepantry;

import java.util.List;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

/**
 * Self-test for a test server: with -Dapocalypsepantry.selftest=true, after the server starts it checks the recipes,
 * eats every food with a fake player (effects and containers) and checks the mixins: Undead Scent against a zombie,
 * Infection from a zombie hit, Infection surviving removeAllEffects(), Stamina halving exhaustion and the crash after
 * Adrenaline. The result is the SELFTEST DONE line in the log.
 */
public final class SelfTest {
    private static int ok;
    private static int fail;

    private SelfTest() {}

    public static boolean enabled() {
        return Boolean.getBoolean(ApocalypsePantry.MODID + ".selftest");
    }

    private static void check(boolean passed, String what) {
        if (passed) ok++;
        else {
            fail++;
            ApocalypsePantry.LOGGER.error("SELFTEST FAIL {}", what);
        }
    }

    private static MobEffectInstance fx(String id, int duration) {
        return Compat.instance(new Food.Fx(id, duration, 0));
    }

    private static boolean has(ServerPlayer player, String id) {
        var effect = Compat.effect(ApocalypsePantry.parse(id));
        return effect != null && player.hasEffect(effect);
    }

    /** Every effect off, Infection included (removeAllEffects() keeps it on purpose). */
    private static void clear(ServerPlayer player) {
        player.removeAllEffects();
        var infection = Compat.effect(ApocalypsePantry.id("infection"));
        if (infection != null) player.removeEffect(infection);
    }

    public static void run(MinecraftServer server, ServerPlayer player) {
        ok = 0;
        fail = 0;
        ServerLevel level = server.overworld();
        String ap = ApocalypsePantry.MODID + ":";

        // Recipes: at least one per food and per container
        List<String> ids = Compat.recipeIds(server).stream().filter(id -> id.startsWith(ap)).toList();
        List<String> wanted = new java.util.ArrayList<>(ModItems.EXTRAS);
        for (Food food : Foods.ALL) wanted.add(food.id);
        for (String item : wanted) {
            boolean found = ids.stream().map(id -> id.substring(id.lastIndexOf('/') + 1))
                    .anyMatch(name -> name.equals(item) || name.startsWith(item + "_from_"));
            check(found, "no recipe for " + item);
        }
        ApocalypsePantry.LOGGER.info("SELFTEST {} recipes of the mod loaded", ids.size());

        // Foods: effects and what is left in the hand
        for (Food food : Foods.ALL) {
            clear(player);
            ItemStack left = new ItemStack(food.item()).finishUsingItem(level, player);
            int effects = player.getActiveEffects().size();
            Item container = ModItems.container(food.container);
            boolean back = container == null ? left.isEmpty() : left.is(container);
            boolean count = effects >= food.effects().size() && effects <= food.effects().size() + food.chances().size();
            check(back && count, food.id + ": " + effects + " effects (want " + food.effects().size() + "), left " + left);
        }

        // Cures: water clears Nausea
        clear(player);
        player.addEffect(fx("minecraft:nausea", 200));
        new ItemStack(Foods.byId("bottled_water").item()).finishUsingItem(level, player);
        check(!has(player, "minecraft:nausea"), "bottled water does not clear nausea");

        // Undead Scent (Mob mixin) and attacking breaks it (LivingEntity mixin)
        clear(player);
        Mob zombie = Compat.newZombie(level);
        if (zombie == null) check(false, "cannot create a zombie");
        else {
            zombie.setPos(player.getX() + 2, player.getY(), player.getZ());
            player.addEffect(fx(ap + "undead_scent", 1200));
            zombie.setTarget(player);
            check(zombie.getTarget() == null, "a zombie targets a player with Undead Scent");
            zombie.setLastHurtByMob(player);
            check(!has(player, ap + "undead_scent"), "attacking does not break Undead Scent");

            // Infection from a zombie hit (LivingEntity mixin)
            clear(player);
            EffectLogic.forceInfection = true;
            player.setLastHurtByMob(zombie);
            EffectLogic.forceInfection = false;
            check(has(player, ap + "infection"), "a zombie hit does not infect");
            // ... and it survives milk and removeAllEffects() (totems, /effect clear)
            Compat.milk(player);
            check(has(player, ap + "infection"), "milk removes Infection");
            player.removeAllEffects();
            check(has(player, ap + "infection"), "removeAllEffects() removes Infection");
            // ... and only the herbal tea cures it
            new ItemStack(Foods.byId("herbal_tea_canteen").item()).finishUsingItem(level, player);
            check(!has(player, ap + "infection"), "herbal tea does not cure Infection");
            // Zombie loot when a player kills it (LivingEntity mixin)
            EffectLogic.forceLoot = true;
            EffectLogic.lastLoot = null;
            zombie.die(Compat.playerAttack(player));
            EffectLogic.forceLoot = false;
            check(EffectLogic.lastLoot != null && !EffectLogic.lastLoot.isEmpty(), "a zombie killed by a player drops nothing");
            zombie.discard();
        }

        // Stamina halves exhaustion (Player mixin)
        clear(player);
        player.addEffect(fx(ap + "stamina", 1200));
        EffectLogic.lastExhaustion = -1.0F;
        player.causeFoodExhaustion(1.0F);
        float got = EffectLogic.lastExhaustion;
        check(Math.abs(got - 0.5F) < 0.01F, "Stamina: exhaustion " + got + " (want 0.5)");

        // Adrenaline ends in a Crash
        clear(player);
        player.addEffect(fx(ap + "adrenaline", 1));
        EffectLogic.tick(player);
        check(has(player, ap + "crash"), "no Crash after Adrenaline");
        clear(player);

        ApocalypsePantry.LOGGER.info("SELFTEST DONE: {} ok, {} failed", ok, fail);
    }
}
