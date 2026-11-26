package com.apocalypsepantry;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import vectorwing.farmersdelight.common.item.ConsumableItem;

/**
 * A food. Farmer's Delight's ConsumableItem eats it and hands the container back (bowl, bottle, empty can, stick);
 * FoodLogic adds the effects. No tooltip of its own.
 */
public class PantryFoodItem extends ConsumableItem implements PantryFood {
    private final Food food;

    public PantryFoodItem(Food food, Properties properties) {
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

    //? if >=1.20.5 <1.21.2 {
    /*@Override
    public int getUseDuration(ItemStack stack, LivingEntity entity) {
        return food.useTicks > 0 ? food.useTicks : super.getUseDuration(stack, entity);
    }
    *///?}

    //? if <1.20.5 {
    /*@Override
    public int getUseDuration(ItemStack stack) {
        return food.useTicks > 0 ? food.useTicks : super.getUseDuration(stack);
    }
    *///?}
}
