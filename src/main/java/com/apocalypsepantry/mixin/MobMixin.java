package com.apocalypsepantry.mixin;

import com.apocalypsepantry.EffectLogic;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** Undead Scent: undead mobs cannot pick the player as a target. */
@Mixin(Mob.class)
public abstract class MobMixin {
    @Inject(method = "setTarget", at = @At("HEAD"), cancellable = true)
    private void apocalypsepantry$scent(LivingEntity target, CallbackInfo ci) {
        if (target != null && EffectLogic.hiddenFrom((Mob) (Object) this, target)) ci.cancel();
    }
}
