package com.apocalypsepantry;

import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
//? if neoforge {
/*import net.minecraft.world.effect.MobEffectInstance;
*///?}

/**
 * The mod's effects. They do nothing on their own: EffectLogic reads them (called from the mixins), the same way on
 * every loader and version. Infection is milk-proof: only Herbal Tea cures it.
 */
public final class ModEffect extends MobEffect {
    private final boolean milkProof;

    public ModEffect(MobEffectCategory category, int color, boolean milkProof) {
        super(category, color);
        this.milkProof = milkProof;
    }

    //? if forge {
    /*// Forge 1.18-1.20: milk cures the effects that list it as a curative item
    @Override
    public java.util.List<net.minecraft.world.item.ItemStack> getCurativeItems() {
        return milkProof ? new java.util.ArrayList<>() : super.getCurativeItems();
    }
    *///?}

    //? if neoforge {
    /*// NeoForge 1.21.1: milk removes the effects that have EffectCures.MILK
    @Override
    public void fillEffectCures(java.util.Set<net.neoforged.neoforge.common.EffectCure> cures, MobEffectInstance instance) {
        if (!milkProof) super.fillEffectCures(cures, instance);
    }
    *///?}
}
