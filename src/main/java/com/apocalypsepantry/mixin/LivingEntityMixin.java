package com.apocalypsepantry.mixin;

import com.apocalypsepantry.EffectLogic;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.LivingEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Every living entity: effects ticking, being hurt by a mob, zombie loot on death, Infection surviving removeAllEffects(). */
@Mixin(LivingEntity.class)
public abstract class LivingEntityMixin {
    @Unique
    private MobEffectInstance apocalypsepantry$kept;

    @Inject(method = "tick", at = @At("HEAD"))
    private void apocalypsepantry$tick(CallbackInfo ci) {
        EffectLogic.tick((LivingEntity) (Object) this);
    }

    @Inject(method = "setLastHurtByMob", at = @At("HEAD"))
    private void apocalypsepantry$hurtBy(LivingEntity attacker, CallbackInfo ci) {
        EffectLogic.onHurtBy((LivingEntity) (Object) this, attacker);
    }

    @Inject(method = "die", at = @At("HEAD"))
    private void apocalypsepantry$die(DamageSource source, CallbackInfo ci) {
        EffectLogic.onDie((LivingEntity) (Object) this, source);
    }

    @Inject(method = "removeAllEffects", at = @At("HEAD"))
    private void apocalypsepantry$keep(CallbackInfoReturnable<Boolean> cir) {
        apocalypsepantry$kept = EffectLogic.keptOnClear((LivingEntity) (Object) this);
    }

    @Inject(method = "removeAllEffects", at = @At("RETURN"))
    private void apocalypsepantry$restore(CallbackInfoReturnable<Boolean> cir) {
        MobEffectInstance kept = apocalypsepantry$kept;
        apocalypsepantry$kept = null;
        if (kept != null) ((LivingEntity) (Object) this).addEffect(kept);
    }
}
