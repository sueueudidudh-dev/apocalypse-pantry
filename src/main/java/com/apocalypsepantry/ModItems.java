package com.apocalypsepantry;

import java.util.List;
import java.util.function.Supplier;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;

/** Items that are not food: the containers. They are registered before the foods that leave them behind. */
public final class ModItems {
    public static final List<String> EXTRAS = List.of("empty_can", "empty_canteen");
    static Supplier<Item> emptyCan;
    static Supplier<Item> emptyCanteen;

    private ModItems() {}

    static void set(String id, Supplier<Item> item) {
        if (id.equals("empty_can")) emptyCan = item;
        else emptyCanteen = item;
    }

    public static Item get(String id) {
        return (id.equals("empty_can") ? emptyCan : emptyCanteen).get();
    }

    /** What a food leaves behind, or null. */
    static Item container(Food.Container container) {
        return switch (container) {
            case NONE -> null;
            case BOWL -> Items.BOWL;
            case BOTTLE -> Items.GLASS_BOTTLE;
            case STICK -> Items.STICK;
            case CAN -> emptyCan.get();
            case CANTEEN -> emptyCanteen.get();
        };
    }
}
