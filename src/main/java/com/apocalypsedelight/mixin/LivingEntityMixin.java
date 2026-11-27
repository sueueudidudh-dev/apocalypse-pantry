package com.apocalypsedelight.mixin;

import com.apocalypsedelight.EffectLogic;
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
    private MobEffectInstance apocalypsedelight$kept;

    @Inject(method = "tick", at = @At("HEAD"))
    private void apocalypsedelight$tick(CallbackInfo ci) {
        EffectLogic.tick((LivingEntity) (Object) this);
    }

    @Inject(method = "setLastHurtByMob", at = @At("HEAD"))
    private void apocalypsedelight$hurtBy(LivingEntity attacker, CallbackInfo ci) {
        EffectLogic.onHurtBy((LivingEntity) (Object) this, attacker);
    }

    @Inject(method = "die", at = @At("HEAD"))
    private void apocalypsedelight$die(DamageSource source, CallbackInfo ci) {
        EffectLogic.onDie((LivingEntity) (Object) this, source);
    }

    @Inject(method = "removeAllEffects", at = @At("HEAD"))
    private void apocalypsedelight$keep(CallbackInfoReturnable<Boolean> cir) {
        apocalypsedelight$kept = EffectLogic.keptOnClear((LivingEntity) (Object) this);
    }

    @Inject(method = "removeAllEffects", at = @At("RETURN"))
    private void apocalypsedelight$restore(CallbackInfoReturnable<Boolean> cir) {
        MobEffectInstance kept = apocalypsedelight$kept;
        apocalypsedelight$kept = null;
        if (kept != null) ((LivingEntity) (Object) this).addEffect(kept);
    }
}
