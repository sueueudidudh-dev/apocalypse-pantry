package com.apocalypsedelight;

//? if neoforge {
/*import net.minecraft.core.registries.Registries;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.common.util.FakePlayerFactory;
import net.neoforged.neoforge.event.server.ServerStartedEvent;
import net.neoforged.neoforge.registries.DeferredRegister;

// NeoForge 1.21.1 entry point (NeoForge 1.20.1 loads the Forge build of the mod)
@Mod(ApocalypseDelight.MODID)
public final class ApocalypseDelightNeoForge {
    private static final DeferredRegister<Item> ITEMS = DeferredRegister.create(Registries.ITEM, ApocalypseDelight.MODID);
    private static final DeferredRegister<MobEffect> EFFECTS = DeferredRegister.create(Registries.MOB_EFFECT, ApocalypseDelight.MODID);
    private static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, ApocalypseDelight.MODID);

    public ApocalypseDelightNeoForge(IEventBus modBus) {
        for (String id : ModEffects.IDS) EFFECTS.register(id, ModEffects.factory(id));
        for (String id : ModItems.EXTRAS) ModItems.set(id, ITEMS.register(id, () -> FoodItems.plain(id)));
        for (Food food : Foods.ALL) food.item = ITEMS.register(food.id, () -> FoodItems.create(food));
        TABS.register("main", () -> CreativeModeTab.builder()
                .title(Compat.tr("itemGroup." + ApocalypseDelight.MODID))
                .withTabsBefore(CreativeModeTabs.FOOD_AND_DRINKS)
                .icon(Tab::icon)
                .displayItems((params, output) -> Tab.fill(output::accept))
                .build());
        EFFECTS.register(modBus);
        ITEMS.register(modBus);
        TABS.register(modBus);
        NeoForge.EVENT_BUS.addListener((ServerStartedEvent event) -> {
            if (SelfTest.enabled()) SelfTest.run(event.getServer(), FakePlayerFactory.getMinecraft(event.getServer().overworld()));
        });
        ApocalypseDelight.init();
    }
}
*///?}
