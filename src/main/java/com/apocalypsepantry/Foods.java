package com.apocalypsepantry;

import java.util.List;

/**
 * All foods in creative-tab order. Effect ids are registry ids, so the list is the same on every version.
 * Comfort and Nourishment come from Farmer's Delight, as on its own soups and meals.
 */
public final class Foods {
    private static final String MC = "minecraft:";
    private static final String FD = "farmersdelight:";
    private static final String AP = ApocalypsePantry.MODID + ":";
    static final int SEC = 20;
    static final int MIN = 60 * SEC;

    public static final List<Food> ALL = List.of(
            new Food("canned_beans", Food.Container.CAN, 6, 0.6F)
                    .fx(AP + "stamina", 3 * MIN, 0),
            new Food("canned_stew", Food.Container.CAN, 8, 0.8F)
                    .fx(MC + "strength", 90 * SEC, 0)
                    .fx(AP + "stamina", 5 * MIN, 0),
            new Food("canned_peaches", Food.Container.CAN, 5, 0.5F)
                    .fx(MC + "speed", MIN, 0)
                    .fx(MC + "regeneration", 10 * SEC, 0),
            new Food("condensed_milk", Food.Container.CAN, 4, 0.4F).always()
                    .fx(MC + "absorption", 2 * MIN, 0)
                    .fx(MC + "haste", MIN, 0),
            new Food("energy_drink", Food.Container.CAN, 1, 0.1F).always().drink().rest()
                    .fx(AP + "adrenaline", 45 * SEC, 0),
            new Food("bottled_water", Food.Container.BOTTLE, 0, 0.0F).always().drink()
                    .cures(AP + "crash", MC + "hunger", MC + "nausea")
                    .fx(MC + "regeneration", 5 * SEC, 0),
            new Food("herbal_tea", Food.Container.BOTTLE, 2, 0.2F).always().drink()
                    .cures(AP + "infection")
                    .fx(FD + "comfort", MIN, 0)
                    .fx(MC + "regeneration", 10 * SEC, 0),
            new Food("mre_ration", Food.Container.NONE, 10, 0.9F).slow(48).stack(8)
                    .fx(AP + "stamina", 8 * MIN, 0)
                    .fx(MC + "resistance", 2 * MIN, 0),
            new Food("protein_bar", Food.Container.NONE, 4, 0.8F).fast()
                    .fx(MC + "strength", 45 * SEC, 0),
            new Food("hardtack", Food.Container.NONE, 3, 0.4F)
                    .fx(AP + "stamina", MIN, 0),
            new Food("instant_noodles", Food.Container.NONE, 6, 0.5F)
                    .fx(FD + "comfort", 2 * MIN, 0)
                    .fx(MC + "regeneration", 15 * SEC, 0)
                    .fx(AP + "stamina", 2 * MIN, 0),
            new Food("jerky", Food.Container.NONE, 6, 0.7F).fast()
                    .fx(MC + "strength", MIN, 0),
            new Food("zombie_jerky", Food.Container.NONE, 4, 0.3F)
                    .fx(AP + "undead_scent", 2 * MIN, 0)
                    .fx(MC + "nausea", 5 * SEC, 0),
            new Food("grilled_rat", Food.Container.STICK, 5, 0.5F)
                    .chance(MC + "poison", 10 * SEC, 0, 0.2F),
            new Food("pickled_cucumbers", Food.Container.BOTTLE, 3, 0.3F)
                    .cures(MC + "poison", MC + "nausea"),
            new Food("survivor_stew", Food.Container.BOWL, 10, 0.8F)
                    .fx(FD + "nourishment", 5 * MIN, 0)
                    .fx(MC + "resistance", 3 * MIN, 0)
                    .fx(MC + "regeneration", 20 * SEC, 0)
                    .fx(AP + "stamina", 6 * MIN, 0),
            new Food("chocolate_ration", Food.Container.NONE, 5, 0.6F)
                    .fx(MC + "speed", 90 * SEC, 0)
                    .fx(MC + "haste", 90 * SEC, 0)
                    .fx(MC + "absorption", MIN, 0));

    private Foods() {}

    public static Food byId(String id) {
        for (Food food : ALL) if (food.id.equals(id)) return food;
        throw new IllegalArgumentException("Unknown food " + id);
    }
}
