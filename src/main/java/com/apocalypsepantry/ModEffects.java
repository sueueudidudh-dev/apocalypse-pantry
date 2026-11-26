package com.apocalypsepantry;

import java.util.List;
import java.util.function.Supplier;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;

/** Ids and factories of the mod's effects, registered by each loader. */
public final class ModEffects {
    public static final List<String> IDS = List.of("infection", "undead_scent", "adrenaline", "crash", "stamina");

    private ModEffects() {}

    public static Supplier<MobEffect> factory(String id) {
        return switch (id) {
            case "infection" -> () -> new ModEffect(MobEffectCategory.HARMFUL, 0x5E8C31, true);
            case "undead_scent" -> () -> new ModEffect(MobEffectCategory.BENEFICIAL, 0x6B7340, false);
            case "adrenaline" -> () -> new ModEffect(MobEffectCategory.BENEFICIAL, 0xF5A623, false);
            case "crash" -> () -> new ModEffect(MobEffectCategory.HARMFUL, 0x6A5A8C, false);
            case "stamina" -> () -> new ModEffect(MobEffectCategory.BENEFICIAL, 0xC95C2C, false);
            default -> throw new IllegalArgumentException(id);
        };
    }
}
