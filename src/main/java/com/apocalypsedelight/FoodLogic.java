package com.apocalypsedelight;

import net.minecraft.server.level.ServerPlayer;
import net.minecraft.stats.Stats;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.Level;

/** What happens when a food is eaten: cures first, then its effects, its chance effects and the sleep reset. */
final class FoodLogic {
    private FoodLogic() {}

    static void eaten(Food food, Level level, LivingEntity consumer) {
        if (level.isClientSide()) return;
        for (String cure : food.cures()) {
            var effect = Compat.effect(ApocalypseDelight.parse(cure));
            if (effect != null) consumer.removeEffect(effect);
        }
        for (Food.Fx fx : food.effects()) {
            MobEffectInstance instance = Compat.instance(fx);
            if (instance != null) consumer.addEffect(instance);
        }
        for (Food.Chance chance : food.chances()) {
            if (consumer.getRandom().nextFloat() >= chance.chance()) continue;
            MobEffectInstance instance = Compat.instance(chance.fx());
            if (instance != null) consumer.addEffect(instance);
        }
        if (food.resetsRest() && consumer instanceof ServerPlayer player) {
            player.resetStat(Stats.CUSTOM.get(Stats.TIME_SINCE_REST));
        }
    }
}
