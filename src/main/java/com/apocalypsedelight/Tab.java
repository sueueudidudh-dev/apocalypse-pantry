package com.apocalypsedelight;

import net.minecraft.world.item.ItemStack;

/** What the creative tab shows: the foods, then the containers. */
final class Tab {
    private Tab() {}

    static ItemStack icon() {
        return Foods.byId("canned_stew").item().getDefaultInstance();
    }

    static void fill(java.util.function.Consumer<ItemStack> out) {
        for (Food food : Foods.ALL) out.accept(new ItemStack(food.item()));
        for (String id : ModItems.EXTRAS) out.accept(new ItemStack(ModItems.get(id)));
    }
}
