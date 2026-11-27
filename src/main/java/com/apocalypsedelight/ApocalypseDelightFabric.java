package com.apocalypsedelight;

//? if fabric {
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.entity.FakePlayer;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.item.Item;

// Fabric entry point (fabric.mod.json, entrypoints.main). Runs on both sides: no client classes here.
public final class ApocalypseDelightFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        for (String id : ModEffects.IDS) Registry.register(BuiltInRegistries.MOB_EFFECT, ApocalypseDelight.id(id), ModEffects.factory(id).get());
        for (String id : ModItems.EXTRAS) {
            Item item = Registry.register(BuiltInRegistries.ITEM, ApocalypseDelight.id(id), FoodItems.plain(id));
            ModItems.set(id, () -> item);
        }
        for (Food food : Foods.ALL) {
            Item item = Registry.register(BuiltInRegistries.ITEM, ApocalypseDelight.id(food.id), FoodItems.create(food));
            food.item = () -> item;
        }
        Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, ApocalypseDelight.id("main"), FabricTabs.builder()
                .title(Compat.tr("itemGroup." + ApocalypseDelight.MODID))
                .icon(Tab::icon)
                .displayItems((params, output) -> Tab.fill(output::accept))
                .build());
        ServerLifecycleEvents.SERVER_STARTED.register(server -> {
            if (SelfTest.enabled()) SelfTest.run(server, FakePlayer.get(server.overworld()));
        });
        ApocalypseDelight.init();
    }
}
//?}
