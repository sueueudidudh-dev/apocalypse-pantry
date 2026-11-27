package com.apocalypsedelight;

import com.mojang.logging.LogUtils;
import net.minecraft.resources.Identifier;
import org.slf4j.Logger;

/**
 * Common constants. Loader entry points: ApocalypseDelightForge, ApocalypseDelightNeoForge, ApocalypseDelightFabric.
 * Code that differs between Minecraft versions is marked with Stonecutter comments (//? if ...).
 */
public final class ApocalypseDelight {
    public static final String MODID = "apocalypsedelight";
    public static final Logger LOGGER = LogUtils.getLogger();

    private ApocalypseDelight() {}

    /** apocalypsedelight:path */
    public static Identifier id(String path) {
        //? if >=1.21 {
        return Identifier.fromNamespaceAndPath(MODID, path);
        //?} else {
        /*return new Identifier(MODID, path);
        *///?}
    }

    /** A full namespace:path id. */
    public static Identifier parse(String id) {
        //? if >=1.21 {
        return Identifier.parse(id);
        //?} else {
        /*return new Identifier(id);
        *///?}
    }

    static void init() {
        LOGGER.info("Apocalypse Delight: {} foods and {} effects loaded", Foods.ALL.size(), ModEffects.IDS.size());
    }
}
