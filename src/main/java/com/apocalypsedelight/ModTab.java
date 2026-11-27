package com.apocalypsedelight;

//? if <1.19.3 {
/*import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;

// Creative tab for Minecraft before 1.19.3, where tabs have no registry yet (Forge 1.18.2 / 1.19.2 only)
public final class ModTab {
    public static final CreativeModeTab TAB = new CreativeModeTab(ApocalypseDelight.MODID) {
        @Override
        public ItemStack makeIcon() {
            return new ItemStack(Foods.byId("canned_stew").item());
        }
    };

    private ModTab() {}
}
*///?}
