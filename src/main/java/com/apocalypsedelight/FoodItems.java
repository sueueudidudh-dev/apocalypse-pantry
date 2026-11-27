package com.apocalypsedelight;

import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.Item;
//? if >=1.21.2 {
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.component.Consumable;
import net.minecraft.world.item.component.Consumables;
//?}

/** Item properties for every Minecraft version. Effects are applied by FoodLogic when the food is eaten. */
public final class FoodItems {
    private FoodItems() {}

    public static Item create(Food food) {
        Item.Properties properties = properties(food);
        return food.drink ? new PantryDrinkItem(food, properties) : new PantryFoodItem(food, properties);
    }

    /** A plain item (the containers). */
    public static Item plain(String id) {
        return new Item(base(id).stacksTo(16));
    }

    static Item.Properties base(String id) {
        Item.Properties properties = new Item.Properties();
        //? if >=1.21.2 {
        properties.setId(ResourceKey.create(Registries.ITEM, ApocalypseDelight.id(id)));
        //?}
        //? if <1.19.3 {
        /*properties.tab(ModTab.TAB);
        *///?}
        return properties;
    }

    static Item.Properties properties(Food food) {
        FoodProperties.Builder builder = new FoodProperties.Builder().nutrition(food.nutrition);
        //? if >=1.20.5 {
        builder.saturationModifier(food.saturation);
        if (food.alwaysEdible) builder.alwaysEdible();
        //?} else {
        /*builder.saturationMod(food.saturation);
        if (food.alwaysEdible) builder.alwaysEat();
        *///?}
        //? if <1.21.2 {
        /*if (food.fast) builder.fast();
        *///?}

        Item.Properties properties = base(food.id);
        //? if >=1.21.2 {
        // Since 1.21.2 the eating time, animation and sound come from the Consumable component
        Consumable.Builder consumable = food.drink ? Consumables.defaultDrink() : Consumables.defaultFood();
        if (food.fast) consumable.consumeSeconds(0.8F);
        if (food.useTicks > 0) consumable.consumeSeconds(food.useTicks / 20.0F);
        properties.food(builder.build(), consumable.build());
        //?} else {
        /*properties.food(builder.build());
        *///?}

        properties.stacksTo(food.stack);
        // The container also comes back when the food is used in a crafting recipe
        Item remainder = ModItems.container(food.container);
        if (remainder != null) properties.craftRemainder(remainder);
        return properties;
    }
}
