"""Data generator for Apocalypse Pantry.

Writes:
  * shared assets: item models, item textures (copied from art/textures) and the language files
    (src/main/resources/assets/apocalypsepantry);
  * per Minecraft version + loader (versions/<version>-<loader>/generated): recipes, recipe-unlock advancements,
    item definitions (1.21.4+) and pack.mcmeta (Forge). Formats differ per version, see Target.

  py tools/gen.py
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = 'apocalypsepantry'
RES = os.path.join(ROOT, 'src/main/resources')
ART = os.path.join(ROOT, 'art/textures')

# id: (English, Russian). Foods in the order of Foods.java, then the containers.
ITEMS = {
    'canned_beans': ('Canned Beans', 'Фасоль в томате'),
    'canned_stew': ('Canned Stew', 'Тушёнка'),
    'canned_peaches': ('Canned Peaches', 'Консервированные персики'),
    'condensed_milk': ('Condensed Milk', 'Сгущёнка'),
    'energy_drink': ('Energy Drink', 'Энергетик'),
    'bottled_water': ('Bottled Water', 'Бутылка воды'),
    'mre_ration': ('MRE Ration', 'Сухпаёк (ИРП)'),
    'protein_bar': ('Protein Bar', 'Протеиновый батончик'),
    'hardtack': ('Hardtack', 'Галеты'),
    'instant_noodles': ('Instant Noodles', 'Лапша быстрого приготовления'),
    'jerky': ('Jerky', 'Вяленое мясо'),
    'zombie_jerky': ('Zombie Jerky', 'Вяленая плоть зомби'),
    'grilled_rat': ('Grilled Rat', 'Крыса на палочке'),
    'pickled_cucumbers': ('Pickled Cucumbers', 'Банка солений'),
    'herbal_tea_canteen': ('Herbal Tea Canteen', 'Фляга травяного чая'),
    'survivor_stew': ("Survivor's Stew", 'Похлёбка выжившего'),
    'chocolate_ration': ('Chocolate Ration', 'Армейский шоколад'),
    'empty_can': ('Empty Can', 'Пустая банка'),
    'empty_canteen': ('Empty Canteen', 'Пустая фляга'),
}
EFFECTS = {
    'infection': ('Infection', 'Заражение'),
    'undead_scent': ('Undead Scent', 'Мёртвый запах'),
    'adrenaline': ('Adrenaline', 'Адреналин'),
    'crash': ('Crash', 'Отходняк'),
    'stamina': ('Stamina', 'Запас сил'),
}
TEXT = {
    'itemGroup.' + MOD: ('Apocalypse Pantry', 'Apocalypse Pantry'),
    f'tooltip.{MOD}.food': ('Hunger +%s, Saturation +%s', 'Голод +%s, насыщение +%s'),
    f'tooltip.{MOD}.then': ('Then: %s', 'Затем: %s'),
    f'tooltip.{MOD}.chance': ('%s%% chance: %s', 'Шанс %s%%: %s'),
    f'tooltip.{MOD}.cures': ('Cures: %s', 'Снимает: %s'),
    f'tooltip.{MOD}.rest': ('Resets the time since you last slept', 'Сбрасывает время без сна'),
}

AP = MOD + ':'
CAN = AP + 'empty_can'
# (recipe name, kind, ingredients or input, options). kind: craft (shapeless), smelt, smoke, campfire.
R = [
    ('empty_can', 'craft', ['minecraft:iron_nugget'] * 3, {}),
    ('empty_canteen', 'craft', ['minecraft:iron_ingot', 'minecraft:iron_ingot', 'minecraft:leather'], {}),
    ('iron_nugget_from_empty_can', 'smelt', CAN, {'result': 'minecraft:iron_nugget', 'xp': 0.1}),
    ('canned_beans', 'craft', [CAN, 'minecraft:beetroot', 'minecraft:cocoa_beans', 'minecraft:cocoa_beans'], {}),
    ('canned_stew', 'craft', [CAN, 'minecraft:cooked_beef', 'minecraft:potato'], {}),
    ('canned_stew_from_porkchop', 'craft', [CAN, 'minecraft:cooked_porkchop', 'minecraft:potato'], {'result': AP + 'canned_stew'}),
    ('canned_peaches', 'craft', [CAN, 'minecraft:apple', 'minecraft:apple', 'minecraft:sugar'], {}),
    ('condensed_milk', 'craft', [CAN, 'minecraft:milk_bucket', 'minecraft:sugar', 'minecraft:sugar'], {}),
    ('energy_drink', 'craft', [CAN, 'minecraft:sugar', 'minecraft:sugar', 'minecraft:cocoa_beans', 'minecraft:glowstone_dust'], {}),
    ('bottled_water', 'craft', ['minecraft:glass_bottle', 'minecraft:ice'], {}),
    ('mre_ration', 'craft', ['minecraft:paper', AP + 'hardtack', AP + 'jerky', AP + 'chocolate_ration'], {}),
    ('protein_bar', 'craft', ['minecraft:wheat', 'minecraft:honey_bottle', 'minecraft:pumpkin_seeds', 'minecraft:paper'], {'count': 2}),
    ('hardtack', 'craft', ['minecraft:wheat'] * 3, {'count': 2}),
    ('instant_noodles', 'craft', [AP + 'bottled_water', 'minecraft:wheat', 'minecraft:dried_kelp', 'minecraft:paper'], {}),
    ('jerky', 'craft', ['minecraft:cooked_beef', 'minecraft:sugar'], {'count': 2}),
    ('jerky_from_porkchop', 'craft', ['minecraft:cooked_porkchop', 'minecraft:sugar'], {'count': 2, 'result': AP + 'jerky'}),
    ('zombie_jerky', 'smoke', 'minecraft:rotten_flesh', {'xp': 0.35}),
    ('zombie_jerky_from_campfire', 'campfire', 'minecraft:rotten_flesh', {'xp': 0.35, 'result': AP + 'zombie_jerky'}),
    ('grilled_rat', 'craft', ['minecraft:stick', 'minecraft:cooked_rabbit'], {}),
    ('pickled_cucumbers', 'craft', ['minecraft:glass_bottle', 'minecraft:sea_pickle', 'minecraft:sea_pickle', 'minecraft:sugar'], {}),
    ('herbal_tea_canteen', 'craft', [AP + 'empty_canteen', AP + 'bottled_water', 'minecraft:fern', 'minecraft:sweet_berries'], {}),
    ('survivor_stew', 'craft', ['minecraft:bowl', AP + 'canned_stew', 'minecraft:potato', 'minecraft:carrot', 'minecraft:brown_mushroom'], {}),
    ('chocolate_ration', 'craft', ['minecraft:cocoa_beans', 'minecraft:cocoa_beans', 'minecraft:sugar', 'minecraft:paper'], {'count': 2}),
]
COOK = {'smelt': ('minecraft:smelting', 200), 'smoke': ('minecraft:smoking', 100), 'campfire': ('minecraft:campfire_cooking', 600)}

TARGETS = {
    '1.18.2-forge': (8, 9), '1.19.2-forge': (9, 10), '1.20.1-forge': (15, 15), '1.20.1-fabric': None, '1.21.1-neoforge': None,
    '1.21.1-fabric': None, '1.21.5-fabric': None, '1.21.8-fabric': None, '1.21.10-fabric': None, '1.21.11-fabric': None,
    '26.1-fabric': None, '26.2-fabric': None, '26.3-fabric': None,
}


def ver(s):
    return tuple(int(x) for x in s.split('.'))


class Target:
    def __init__(self, name, pack):
        self.name, self.pack = name, pack
        mc = self.mc = ver(name.split('-')[0])
        self.plural = mc < (1, 21)                  # recipes/, advancements/ before 1.21
        self.result_key = 'item' if mc < (1, 20, 5) else 'id'
        self.string_ingredients = mc >= (1, 21, 2)
        self.holder_predicates = mc >= (1, 20, 5)
        self.unlock_key = 'recipes' if mc >= (26, 3) else 'recipe'
        self.item_models = mc >= (1, 21, 4)
        self.out = os.path.join(ROOT, 'versions', name, 'generated')

    def ingredient(self, s):
        return s if self.string_ingredients else {'item': s}

    def stack(self, item, count=1):
        res = {self.result_key: item}
        if count > 1:
            res['count'] = count
        return res

    def cook_result(self, item):
        return item if self.mc < (1, 20, 5) else {'id': item}

    def predicate(self, s):
        return {'items': s} if self.holder_predicates else {'items': [s]}


def wjson(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')


def write_assets():
    a = os.path.join(RES, 'assets', MOD)
    for sub in ('models/item', 'textures/item'):
        shutil.rmtree(os.path.join(a, sub), ignore_errors=True)
    for i in ITEMS:
        wjson(os.path.join(a, 'models', 'item', i + '.json'), {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'{MOD}:item/{i}'}})
        os.makedirs(os.path.join(a, 'textures', 'item'), exist_ok=True)
        shutil.copyfile(os.path.join(ART, i + '.png'), os.path.join(a, 'textures', 'item', i + '.png'))
    for k, lang in ((0, 'en_us'), (1, 'ru_ru')):
        out = {f'item.{MOD}.{i}': v[k] for i, v in ITEMS.items()}
        out.update({f'effect.{MOD}.{i}': v[k] for i, v in EFFECTS.items()})
        out.update({key: v[k] for key, v in TEXT.items()})
        wjson(os.path.join(a, 'lang', lang + '.json'), out)
    shutil.copyfile(os.path.join(ROOT, 'page', 'docs', 'icon-512.png'), os.path.join(RES, MOD + '_logo.png'))


def write_target(t):
    shutil.rmtree(t.out, ignore_errors=True)
    data = os.path.join(t.out, 'data', MOD)
    rec_dir, adv_dir = ('recipes', 'advancements') if t.plural else ('recipe', 'advancement')
    for name, kind, ings, opt in R:
        result = opt.get('result', AP + name)
        if kind == 'craft':
            obj = {'type': 'minecraft:crafting_shapeless', 'group': MOD,
                   'ingredients': [t.ingredient(x) for x in ings], 'result': t.stack(result, opt.get('count', 1))}
            sub, inputs = 'crafting', ings
        else:
            typ, time = COOK[kind]
            obj = {'type': typ, 'ingredient': t.ingredient(ings), 'result': t.cook_result(result),
                   'experience': opt.get('xp', 0.1), 'cookingtime': time}
            sub, inputs = 'cooking', [ings]
        wjson(os.path.join(data, rec_dir, sub, name + '.json'), obj)
        rec_id = f'{MOD}:{sub}/{name}'
        crit = {'has_the_recipe': {'trigger': 'minecraft:recipe_unlocked', 'conditions': {t.unlock_key: rec_id}}}
        uniq = []
        for x in inputs:
            if x not in uniq and x not in ('minecraft:bowl', 'minecraft:paper', 'minecraft:sugar'):
                uniq.append(x)
        for n, x in enumerate(uniq):
            crit[f'has_ingredient_{n}'] = {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [t.predicate(x)]}}
        wjson(os.path.join(data, adv_dir, 'recipes', sub, name + '.json'), {
            'parent': 'minecraft:recipes/root', 'criteria': crit, 'requirements': [list(crit.keys())],
            'rewards': {'recipes': [rec_id]}, 'sends_telemetry_event': False})
    if t.item_models:
        for i in ITEMS:
            wjson(os.path.join(t.out, 'assets', MOD, 'items', i + '.json'), {'model': {'type': 'minecraft:model', 'model': f'{MOD}:item/{i}'}})
    if t.pack:
        resource, datapack = t.pack
        pack = {'description': 'Apocalypse Pantry resources', 'pack_format': datapack}
        if resource != datapack:
            pack['forge:resource_pack_format'] = resource
            pack['forge:data_pack_format'] = datapack
        wjson(os.path.join(t.out, 'pack.mcmeta'), {'pack': pack})


def main():
    write_assets()
    for name, pack in TARGETS.items():
        write_target(Target(name, pack))
    print(f'OK: {len(ITEMS)} items, {len(R)} recipes, data for {len(TARGETS)} versions')


if __name__ == '__main__':
    main()
