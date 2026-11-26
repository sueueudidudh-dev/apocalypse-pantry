package com.apocalypsepantry;

//? if fabric && >=1.20.5 {
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.item.v1.ItemTooltipCallback;

// Fabric client entry point (entrypoints.client): ItemTooltipCallback must not load on a dedicated server
public final class ApocalypsePantryFabricClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        ItemTooltipCallback.EVENT.register((stack, context, flag, lines) -> Tooltips.append(stack, lines));
    }
}
//?}

//? if fabric && <1.20.5 {
/*import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.item.v1.ItemTooltipCallback;

// Fabric client entry point (entrypoints.client): ItemTooltipCallback must not load on a dedicated server
public final class ApocalypsePantryFabricClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        ItemTooltipCallback.EVENT.register((stack, flag, lines) -> Tooltips.append(stack, lines));
    }
}
*///?}
