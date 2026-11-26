package com.apocalypsepantry;

//? if forge && >=1.19.3 {
/*import net.minecraft.core.registries.Registries;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.Item;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.common.util.FakePlayerFactory;
import net.minecraftforge.event.server.ServerStartedEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

// Forge 1.20.1 entry point (and NeoForge 1.20.1: the same jar)
@Mod(ApocalypsePantry.MODID)
public final class ApocalypsePantryForge {
    private static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, ApocalypsePantry.MODID);
    private static final DeferredRegister<MobEffect> EFFECTS = DeferredRegister.create(ForgeRegistries.MOB_EFFECTS, ApocalypsePantry.MODID);
    private static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, ApocalypsePantry.MODID);

    @SuppressWarnings("removal") // FMLJavaModLoadingContext.get() kept for older Forge 47.x builds
    public ApocalypsePantryForge() {
        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
        for (String id : ModEffects.IDS) EFFECTS.register(id, ModEffects.factory(id));
        for (String id : ModItems.EXTRAS) ModItems.set(id, ITEMS.register(id, () -> FoodItems.plain(id)));
        for (Food food : Foods.ALL) food.item = ITEMS.register(food.id, () -> FoodItems.create(food));
        TABS.register("main", () -> CreativeModeTab.builder()
                .title(Compat.tr("itemGroup." + ApocalypsePantry.MODID))
                .withTabsBefore(CreativeModeTabs.FOOD_AND_DRINKS)
                .icon(Tab::icon)
                .displayItems((params, output) -> Tab.fill(output::accept))
                .build());
        EFFECTS.register(modBus);
        ITEMS.register(modBus);
        TABS.register(modBus);
        MinecraftForge.EVENT_BUS.addListener((ServerStartedEvent event) -> {
            if (SelfTest.enabled()) SelfTest.run(event.getServer(), FakePlayerFactory.getMinecraft(event.getServer().overworld()));
        });
        ApocalypsePantry.init();
    }
}
*///?}

//? if forge && <1.19.3 {
/*import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.item.Item;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.common.util.FakePlayerFactory;
import net.minecraftforge.event.server.ServerStartedEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;

// Forge 1.18.2 / 1.19.2 entry point: the creative tab is ModTab (no tab registry yet)
@Mod(ApocalypsePantry.MODID)
public final class ApocalypsePantryForge {
    private static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, ApocalypsePantry.MODID);
    private static final DeferredRegister<MobEffect> EFFECTS = DeferredRegister.create(ForgeRegistries.MOB_EFFECTS, ApocalypsePantry.MODID);

    public ApocalypsePantryForge() {
        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
        for (String id : ModEffects.IDS) EFFECTS.register(id, ModEffects.factory(id));
        for (String id : ModItems.EXTRAS) ModItems.set(id, ITEMS.register(id, () -> FoodItems.plain(id)));
        for (Food food : Foods.ALL) food.item = ITEMS.register(food.id, () -> FoodItems.create(food));
        EFFECTS.register(modBus);
        ITEMS.register(modBus);
        MinecraftForge.EVENT_BUS.addListener((ServerStartedEvent event) -> {
            if (SelfTest.enabled()) SelfTest.run(event.getServer(), FakePlayerFactory.getMinecraft(event.getServer().overworld()));
        });
        ApocalypsePantry.init();
    }
}
*///?}
