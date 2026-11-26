package com.apocalypsepantry;

import java.util.List;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.resources.Identifier;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.level.Level;
//? if >=1.20.5 {
import net.minecraft.core.Holder;
import net.minecraft.tags.EntityTypeTags;
//?} else {
/*import net.minecraft.world.entity.MobType;
*///?}
//? if >=1.21.2 {
import net.minecraft.world.entity.EntitySpawnReason;
//?}
//? if >=26.3 {
import net.minecraft.util.Prediction;
//?}
//? if >=26.2 {
import net.minecraft.world.entity.EntityTypes;
//?}
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
//? if >=1.19.3 {
import net.minecraft.core.registries.BuiltInRegistries;
//?} else {
/*import net.minecraft.core.Registry;
*///?}
//? if <1.19 {
/*import net.minecraft.network.chat.TranslatableComponent;
*///?}

/**
 * Wrappers around API that differs between Minecraft versions and loaders.
 * Inside Stonecutter blocks only line comments are used.
 */
final class Compat {
    private Compat() {}

    // ---- effects: MobEffect before 1.20.5, Holder<MobEffect> since. effect(id) is the effect or null ----

    //? if >=1.21.2 {
    static Holder<MobEffect> effect(Identifier id) {
        return BuiltInRegistries.MOB_EFFECT.get(id).orElse(null);
    }
    //?}

    //? if >=1.20.5 <1.21.2 {
    /*static Holder<MobEffect> effect(Identifier id) {
        return BuiltInRegistries.MOB_EFFECT.getHolder(id).orElse(null);
    }
    *///?}

    //? if >=1.19.3 <1.20.5 {
    /*static MobEffect effect(Identifier id) {
        return BuiltInRegistries.MOB_EFFECT.get(id);
    }
    *///?}

    //? if <1.19.3 {
    /*static MobEffect effect(Identifier id) {
        return Registry.MOB_EFFECT.get(id);
    }
    *///?}

    //? if >=1.20.5 {
    static MobEffect value(Holder<MobEffect> effect) {
        return effect.value();
    }
    //?} else {
    /*static MobEffect value(MobEffect effect) {
        return effect;
    }
    *///?}

    /** An effect instance for a food, or null if the effect does not exist. */
    static MobEffectInstance instance(Food.Fx fx) {
        var effect = effect(ApocalypsePantry.parse(fx.effect()));
        return effect == null ? null : new MobEffectInstance(effect, fx.duration(), fx.amplifier());
    }

    /** A quiet effect instance (ambient, no particles; icon optional) for effects that are topped up. */
    static MobEffectInstance hidden(String id, int duration, int amplifier, boolean icon) {
        var effect = effect(ApocalypsePantry.parse(id));
        return effect == null ? null : new MobEffectInstance(effect, duration, amplifier, true, false, icon);
    }

    // ---- text ----

    //? if >=1.19 {
    static MutableComponent tr(String key, Object... args) {
        return Component.translatable(key, args);
    }
    //?} else {
    /*static MutableComponent tr(String key, Object... args) {
        return new TranslatableComponent(key, args);
    }
    *///?}

    // ---- world and mobs ----

    static Level level(Entity entity) {
        //? if >=1.20 {
        return entity.level();
        //?} else {
        /*return entity.level;
        *///?}
    }

    /** Zombies that can infect: zombie, husk, drowned, zombie villager. */
    static boolean isZombie(Entity entity) {
        EntityType<?> type = entity.getType();
        // 26.2 moved the entity type constants to EntityTypes
        //? if >=26.2 {
        return type == EntityTypes.ZOMBIE || type == EntityTypes.HUSK || type == EntityTypes.DROWNED || type == EntityTypes.ZOMBIE_VILLAGER;
        //?} else {
        /*return type == EntityType.ZOMBIE || type == EntityType.HUSK || type == EntityType.DROWNED || type == EntityType.ZOMBIE_VILLAGER;
        *///?}
    }

    @SuppressWarnings("deprecation") // builtInRegistryHolder(): the one tag check that exists on every version
    static boolean isUndead(LivingEntity entity) {
        //? if >=1.20.5 {
        return entity.getType().builtInRegistryHolder().is(EntityTypeTags.UNDEAD);
        //?} else {
        /*return entity.getMobType() == MobType.UNDEAD;
        *///?}
    }

    /** A new zombie, not yet in the world (or null). */
    static Mob newZombie(ServerLevel level) {
        //? if >=26.2 {
        return EntityTypes.ZOMBIE.create(level, EntitySpawnReason.TRIGGERED);
        //?}
        //? if >=1.21.2 <26.2 {
        /*return EntityType.ZOMBIE.create(level, EntitySpawnReason.TRIGGERED);
        *///?}
        //? if <1.21.2 {
        /*return EntityType.ZOMBIE.create(level);
        *///?}
    }

    static void spawnZombie(ServerLevel level, double x, double y, double z, Component name) {
        Mob zombie = newZombie(level);
        if (zombie == null) return;
        zombie.setPos(x, y, z);
        zombie.setCustomName(name);
        zombie.setPersistenceRequired();
        level.addFreshEntity(zombie);
    }

    /** Put a container back into the player's inventory, or drop it if there is no room. */
    static void giveBack(Player player, ItemStack stack) {
        //? if >=26.3 {
        player.getInventory().placeItemBackInInventory(stack, Prediction.SERVER_ONLY);
        //?} else {
        /*player.getInventory().placeItemBackInInventory(stack);
        *///?}
    }

    /** What drinking milk does to effects on this loader (for SelfTest). */
    static void milk(LivingEntity entity) {
        //? if forge {
        /*entity.curePotionEffects(new ItemStack(net.minecraft.world.item.Items.MILK_BUCKET));
        *///?}
        //? if neoforge {
        /*entity.removeEffectsCuredBy(net.neoforged.neoforge.common.EffectCures.MILK);
        *///?}
        //? if fabric {
        entity.removeAllEffects();
        //?}
    }

    /** Damage dealt by a player's melee attack (for SelfTest). */
    static net.minecraft.world.damagesource.DamageSource playerAttack(Player player) {
        //? if >=1.19.4 {
        return Compat.level(player).damageSources().playerAttack(player);
        //?} else {
        /*return net.minecraft.world.damagesource.DamageSource.playerAttack(player);
        *///?}
    }

    // ---- server recipes (for SelfTest): ids of every loaded recipe ----

    //? if >=1.21.11 {
    static List<String> recipeIds(MinecraftServer server) {
        return server.getRecipeManager().getRecipes().stream().map(h -> h.id().identifier().toString()).toList();
    }
    //?}

    //? if >=1.21.2 <1.21.11 {
    /*static List<String> recipeIds(MinecraftServer server) {
        return server.getRecipeManager().getRecipes().stream().map(h -> h.id().location().toString()).toList();
    }
    *///?}

    //? if >=1.20.2 <1.21.2 {
    /*static List<String> recipeIds(MinecraftServer server) {
        return server.getRecipeManager().getRecipes().stream().map(h -> h.id().toString()).toList();
    }
    *///?}

    //? if <1.20.2 {
    /*static List<String> recipeIds(MinecraftServer server) {
        return server.getRecipeManager().getRecipes().stream().map(r -> r.getId().toString()).toList();
    }
    *///?}
}
