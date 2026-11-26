package com.apocalypsepantry.mixin;

import com.apocalypsepantry.EffectLogic;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.damagesource.DamageSource;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/** A player who dies infected rises again as a zombie. */
@Mixin(ServerPlayer.class)
public abstract class ServerPlayerMixin {
    @Inject(method = "die", at = @At("HEAD"))
    private void apocalypsepantry$die(DamageSource source, CallbackInfo ci) {
        EffectLogic.onDeath((ServerPlayer) (Object) this);
    }
}
