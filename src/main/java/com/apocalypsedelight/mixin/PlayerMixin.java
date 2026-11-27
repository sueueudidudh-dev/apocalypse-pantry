package com.apocalypsedelight.mixin;

import com.apocalypsedelight.EffectLogic;
import net.minecraft.world.entity.player.Player;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyVariable;

/** Stamina and Infection change how fast hunger drains. */
@Mixin(Player.class)
public abstract class PlayerMixin {
    @ModifyVariable(method = "causeFoodExhaustion", at = @At("HEAD"), argsOnly = true)
    private float apocalypsedelight$exhaustion(float amount) {
        return EffectLogic.exhaustion((Player) (Object) this, amount);
    }
}
