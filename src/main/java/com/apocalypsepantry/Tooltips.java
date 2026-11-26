package com.apocalypsepantry;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.item.ItemStack;

/**
 * Tooltip lines of a food: hunger and saturation, effects with durations, chance effects, cures, the crash after
 * Adrenaline and the sleep reset. Called from the loader's tooltip event.
 */
public final class Tooltips {
    private Tooltips() {}

    public static void append(ItemStack stack, List<Component> tooltip) {
        if (!(stack.getItem() instanceof PantryFood item)) return;
        Food food = item.food();
        String id = ApocalypsePantry.MODID;
        List<Component> lines = new ArrayList<>();
        lines.add(Compat.tr("tooltip." + id + ".food", food.nutrition, String.format("%.1f", food.saturationPoints()))
                .withStyle(ChatFormatting.GOLD));
        for (Food.Fx fx : food.effects()) {
            MutableComponent line = effect(fx);
            if (line != null) lines.add(line);
            if (fx.effect().equals(id + ":adrenaline")) {
                MutableComponent crash = effect(new Food.Fx(id + ":crash", EffectLogic.CRASH_TICKS, 0));
                if (crash != null) lines.add(Compat.tr("tooltip." + id + ".then", crash).withStyle(ChatFormatting.RED));
            }
        }
        for (Food.Chance chance : food.chances()) {
            MutableComponent line = effect(chance.fx());
            if (line != null) {
                lines.add(Compat.tr("tooltip." + id + ".chance", Math.round(chance.chance() * 100), line).withStyle(ChatFormatting.RED));
            }
        }
        if (!food.cures().isEmpty()) {
            List<String> names = new ArrayList<>();
            for (String cure : food.cures()) {
                var holder = Compat.effect(ApocalypsePantry.parse(cure));
                if (holder != null) names.add(Compat.tr(Compat.value(holder).getDescriptionId()).getString());
            }
            lines.add(Compat.tr("tooltip." + id + ".cures", String.join(", ", names)).withStyle(ChatFormatting.AQUA));
        }
        if (food.resetsRest()) lines.add(Compat.tr("tooltip." + id + ".rest").withStyle(ChatFormatting.GRAY));
        // Right under the item name
        tooltip.addAll(Math.min(1, tooltip.size()), lines);
    }

    private static MutableComponent effect(Food.Fx fx) {
        var holder = Compat.effect(ApocalypsePantry.parse(fx.effect()));
        if (holder == null) return null;
        MobEffect effect = Compat.value(holder);
        MutableComponent line = Compat.tr(effect.getDescriptionId());
        if (fx.amplifier() > 0) line = Compat.tr("potion.withAmplifier", line, Compat.tr("potion.potency." + fx.amplifier()));
        if (fx.duration() > 20) line = Compat.tr("potion.withDuration", line, duration(fx.duration()));
        return line.withStyle(effect.getCategory().getTooltipFormatting());
    }

    private static String duration(int ticks) {
        int seconds = ticks / 20;
        return String.format("%d:%02d", seconds / 60, seconds % 60);
    }
}
