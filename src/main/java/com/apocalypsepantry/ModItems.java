package com.apocalypsepantry;

import java.util.List;
import java.util.function.Supplier;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;

/** Items that are not food: the empty can. It is registered before the foods that leave it behind. */
public final class ModItems {
    public static final List<String> EXTRAS = List.of("empty_can");
    static Supplier<Item> emptyCan;

    private ModItems() {}

    static void set(String id, Supplier<Item> item) {
        emptyCan = item;
    }

    public static Item get(String id) {
        return emptyCan.get();
    }

    /** What a food leaves behind, or null. */
    static Item container(Food.Container container) {
        return switch (container) {
            case NONE -> null;
            case BOWL -> Items.BOWL;
            case BOTTLE -> Items.GLASS_BOTTLE;
            case STICK -> Items.STICK;
            case CAN -> emptyCan.get();
        };
    }
}
