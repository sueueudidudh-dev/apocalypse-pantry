package com.apocalypsedelight;

import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.Difficulty;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

/** How the mod's effects work. Called from the mixins (LivingEntity, Mob, Player, ServerPlayer). */
public final class EffectLogic {
    /** Infection lasts an hour unless Herbal Tea cures it; Weakness after 5 minutes, Slowness after 10. */
    public static final int INFECTION_TICKS = 72000;
    static final int WEAKNESS_AFTER = 6000;
    static final int SLOWNESS_AFTER = 12000;
    /** Crash after Adrenaline: 30 seconds. */
    static final int CRASH_TICKS = 600;
    /** SelfTest only: infect on every zombie hit; the last exhaustion the Player mixin passed on. */
    static boolean forceInfection;
    static float lastExhaustion = -1.0F;

    private EffectLogic() {}

    private static boolean has(LivingEntity entity, String id) {
        var effect = Compat.effect(ApocalypseDelight.id(id));
        return effect != null && entity.hasEffect(effect);
    }

    private static MobEffectInstance get(LivingEntity entity, String id) {
        var effect = Compat.effect(ApocalypseDelight.id(id));
        return effect == null ? null : entity.getEffect(effect);
    }

    /** A short effect that is topped up every 10 ticks while its source lasts. */
    private static void topUp(LivingEntity entity, String id, int amplifier, boolean icon) {
        MobEffectInstance instance = Compat.hidden(id, 30, amplifier, icon);
        if (instance != null) entity.addEffect(instance);
    }

    /** Start of LivingEntity.tick(), before the effects tick. */
    public static void tick(LivingEntity entity) {
        Level level = Compat.level(entity);
        if (level.isClientSide()) return;
        if (entity instanceof Mob mob) {
            LivingEntity target = mob.getTarget();
            if (target != null && hiddenFrom(mob, target)) mob.setTarget(null);
        }
        if (entity.getActiveEffects().isEmpty()) return;
        boolean refresh = entity.tickCount % 10 == 0;

        MobEffectInstance infection = get(entity, "infection");
        if (infection != null && refresh) {
            int elapsed = INFECTION_TICKS - infection.getDuration();
            if (elapsed >= WEAKNESS_AFTER) topUp(entity, "minecraft:weakness", 0, true);
            if (elapsed >= SLOWNESS_AFTER) topUp(entity, "minecraft:slowness", 0, true);
        }

        MobEffectInstance adrenaline = get(entity, "adrenaline");
        if (adrenaline != null) {
            if (refresh) {
                topUp(entity, "minecraft:speed", 1, false);
                topUp(entity, "minecraft:jump_boost", 0, false);
            }
            // Last tick of Adrenaline: the crash follows
            if (adrenaline.getDuration() <= 1) {
                MobEffectInstance crash = Compat.instance(new Food.Fx(ApocalypseDelight.MODID + ":crash", CRASH_TICKS, 0));
                if (crash != null) entity.addEffect(crash);
            }
        }

        if (refresh && has(entity, "crash")) {
            topUp(entity, "minecraft:slowness", 0, false);
            topUp(entity, "minecraft:mining_fatigue", 0, false);
        }
    }

    /** Undead Scent: undead mobs do not see the player unless the player hit them. */
    public static boolean hiddenFrom(Mob mob, LivingEntity target) {
        return target instanceof Player && has(target, "undead_scent") && Compat.isUndead(mob)
                && mob.getLastHurtByMob() != target;
    }

    /** LivingEntity.setLastHurtByMob(attacker): called when victim takes damage from attacker. */
    public static void onHurtBy(LivingEntity victim, LivingEntity attacker) {
        if (attacker == null || Compat.level(victim).isClientSide()) return;
        // Attacking breaks the scent
        if (attacker instanceof Player && has(attacker, "undead_scent")) {
            var scent = Compat.effect(ApocalypseDelight.id("undead_scent"));
            attacker.removeEffect(scent);
        }
        if (victim instanceof Player player && Compat.isZombie(attacker) && !player.isCreative() && !player.isSpectator()
                && !has(player, "infection")) {
            Difficulty difficulty = Compat.level(victim).getDifficulty();
            float chance = difficulty == Difficulty.HARD ? 0.25F : difficulty == Difficulty.NORMAL ? 0.10F : 0.0F;
            if (forceInfection || player.getRandom().nextFloat() < chance) {
                MobEffectInstance infection = Compat.instance(new Food.Fx(ApocalypseDelight.MODID + ":infection", INFECTION_TICKS, 0));
                if (infection != null) player.addEffect(infection);
            }
        }
    }

    /** Player.causeFoodExhaustion(amount): Stamina halves it, Infection adds half again. */
    public static float exhaustion(Player player, float amount) {
        float k = 1.0F;
        if (!player.getActiveEffects().isEmpty()) {
            if (has(player, "stamina")) k *= 0.5F;
            if (has(player, "infection")) k *= 1.5F;
        }
        lastExhaustion = amount * k;
        return amount * k;
    }

    /** ServerPlayer.die(): a player who dies infected rises again as a zombie. */
    public static void onDeath(ServerPlayer player) {
        if (has(player, "infection") && Compat.level(player) instanceof ServerLevel level) {
            Compat.spawnZombie(level, player.getX(), player.getY(), player.getZ(), player.getName());
        }
    }

    /** What a killed zombie can drop, 5% chance per kill by a player. */
    static final String[] LOOT = {"canned_beans", "canned_stew", "canned_peaches", "hardtack", "energy_drink", "bottled_water"};
    static final float LOOT_CHANCE = 0.05F;
    /** SelfTest only: always drop; the last dropped stack. */
    static boolean forceLoot;
    static ItemStack lastLoot;

    /** LivingEntity.die(source): zombies killed by a player sometimes drop survival food. */
    public static void onDie(LivingEntity entity, DamageSource source) {
        if (!(Compat.level(entity) instanceof ServerLevel level) || !Compat.isZombie(entity)) return;
        if (!(source.getEntity() instanceof Player)) return;
        if (!forceLoot && entity.getRandom().nextFloat() >= LOOT_CHANCE) return;
        ItemStack stack = new ItemStack(Foods.byId(LOOT[entity.getRandom().nextInt(LOOT.length)]).item());
        lastLoot = stack.copy();
        level.addFreshEntity(new ItemEntity(level, entity.getX(), entity.getY() + 0.5, entity.getZ(), stack));
    }

    /** removeAllEffects() (milk on Fabric, totems, /effect clear): Infection stays. */
    public static MobEffectInstance keptOnClear(LivingEntity entity) {
        MobEffectInstance infection = get(entity, "infection");
        return infection == null ? null : new MobEffectInstance(infection);
    }
}
