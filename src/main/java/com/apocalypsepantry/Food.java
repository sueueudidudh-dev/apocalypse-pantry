package com.apocalypsepantry;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.function.Supplier;
import net.minecraft.world.item.Item;

/** One food: what it leaves behind, how filling it is, how it is eaten and what it does. The list is in Foods. */
public final class Food {
    /** What is left after eating: nothing, a bowl, a glass bottle, an empty can or a stick. */
    public enum Container { NONE, BOWL, BOTTLE, CAN, STICK }

    /** An effect: registry id, duration in ticks, amplifier from 0. */
    public record Fx(String effect, int duration, int amplifier) {}

    /** An effect that only happens with the given chance (0..1). */
    public record Chance(Fx fx, float chance) {}

    public final String id;
    public final Container container;
    public final int nutrition;
    /** Saturation modifier, as in FoodProperties.Builder. */
    public final float saturation;
    boolean alwaysEdible;
    boolean drink;
    boolean fast;
    boolean resetsRest;
    int useTicks;
    int stack = 64;
    private final List<Fx> effects = new ArrayList<>();
    private final List<Chance> chances = new ArrayList<>();
    private final List<String> cures = new ArrayList<>();
    /** Set by the loader when the item is registered. */
    Supplier<Item> item;

    Food(String id, Container container, int nutrition, float saturation) {
        this.id = id;
        this.container = container;
        this.nutrition = nutrition;
        this.saturation = saturation;
        if (container != Container.NONE) stack = 16;
    }

    Food always() {
        alwaysEdible = true;
        return this;
    }

    Food drink() {
        drink = true;
        return this;
    }

    /** Eaten in 0.8 s. */
    Food fast() {
        fast = true;
        return this;
    }

    /** Takes this many ticks to eat (default 32). */
    Food slow(int ticks) {
        useTicks = ticks;
        return this;
    }

    Food stack(int size) {
        stack = size;
        return this;
    }

    /** Resets the time since the player last slept (keeps phantoms away). */
    Food rest() {
        resetsRest = true;
        return this;
    }

    Food fx(String effect, int duration, int amplifier) {
        effects.add(new Fx(effect, duration, amplifier));
        return this;
    }

    Food chance(String effect, int duration, int amplifier, float chance) {
        chances.add(new Chance(new Fx(effect, duration, amplifier), chance));
        return this;
    }

    Food cures(String... ids) {
        Collections.addAll(cures, ids);
        return this;
    }

    public List<Fx> effects() {
        return Collections.unmodifiableList(effects);
    }

    public List<Chance> chances() {
        return Collections.unmodifiableList(chances);
    }

    public List<String> cures() {
        return Collections.unmodifiableList(cures);
    }

    public boolean resetsRest() {
        return resetsRest;
    }

    public Item item() {
        return item.get();
    }

    /** Saturation in points, as Minecraft computes it. */
    public float saturationPoints() {
        return nutrition * saturation * 2.0F;
    }
}
