package com.apocalypsepantry;

import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
//? if <1.21.2 {
/*import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.item.UseAnim;
*///?}

/** A food or drink: Minecraft eats it, then FoodLogic applies its effects and the container is handed back. */
public class PantryFoodItem extends Item implements PantryFood {
    private final Food food;

    public PantryFoodItem(Food food, Properties properties) {
        super(properties);
        this.food = food;
    }

    @Override
    public Food food() {
        return food;
    }

    @Override
    public ItemStack finishUsingItem(ItemStack stack, Level level, LivingEntity consumer) {
        Item container = ModItems.container(food.container);
        ItemStack result = super.finishUsingItem(stack, level, consumer);
        FoodLogic.eaten(food, level, consumer);
        if (container == null) return result;
        if (consumer instanceof Player player && player.getAbilities().instabuild) return result;
        ItemStack back = new ItemStack(container);
        if (result.isEmpty()) return back;
        if (consumer instanceof Player player && !level.isClientSide()) Compat.giveBack(player, back);
        return result;
    }

    //? if <1.21.2 {
    /*@Override
    public UseAnim getUseAnimation(ItemStack stack) {
        return food.drink ? UseAnim.DRINK : UseAnim.EAT;
    }

    @Override
    public SoundEvent getEatingSound() {
        return food.drink ? getDrinkingSound() : super.getEatingSound();
    }
    *///?}

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
