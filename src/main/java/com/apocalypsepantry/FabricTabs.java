package com.apocalypsepantry;

//? if fabric && >=26.1 {
import net.fabricmc.fabric.api.creativetab.v1.FabricCreativeModeTab;
import net.minecraft.world.item.CreativeModeTab;

// Creative tab builder from Fabric API (the module is creative-tab-api since 26.1)
final class FabricTabs {
    private FabricTabs() {}

    static CreativeModeTab.Builder builder() {
        return FabricCreativeModeTab.builder();
    }
}
//?}

//? if fabric && <26.1 {
/*import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.minecraft.world.item.CreativeModeTab;

// Creative tab builder from Fabric API (item-group-api before 26.1)
final class FabricTabs {
    private FabricTabs() {}

    static CreativeModeTab.Builder builder() {
        return FabricItemGroup.builder();
    }
}
*///?}
