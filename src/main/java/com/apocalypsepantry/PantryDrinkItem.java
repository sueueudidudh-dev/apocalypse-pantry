package com.apocalypsepantry;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
//? if fabric && >=1.21.2 {
import vectorwing.farmersdelight.common.item.ConsumableItem;
//?} else {
/*import vectorwing.farmersdelight.common.item.DrinkableItem;
*///?}

// A drink: Farmer's Delight's DrinkableItem (drinking animation, the bottle or can comes back). Farmer's Delight
// Refabricated for 1.21.2+ has no DrinkableItem: the Consumable component gives the animation (see FoodItems).
//? if fabric && >=1.21.2 {
public class PantryDrinkItem extends ConsumableItem implements PantryFood {
//?} else {
/*public class PantryDrinkItem extends DrinkableItem implements PantryFood {
*///?}
    private final Food food;

    public PantryDrinkItem(Food food, Properties properties) {
        super(properties, false, false);
        this.food = food;
    }

    @Override
    public Food food() {
        return food;
    }

    @Override
    public void affectConsumer(ItemStack stack, Level level, LivingEntity consumer) {
        FoodLogic.eaten(food, level, consumer);
    }
}
