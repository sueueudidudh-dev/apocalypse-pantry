"""Data generator for Apocalypse Pantry, a Farmer's Delight add-on.

Writes:
  * shared assets: item models, item textures (copied from art/textures) and the language files
    (src/main/resources/assets/apocalypsepantry);
  * per Minecraft version + loader (versions/<version>-<loader>/generated): recipes (cooking pot, cutting board,
    crafting table, smoker, campfire, furnace), recipe-unlock advancements, Farmer's Delight category tags,
    item definitions (1.21.4+) and pack.mcmeta (Forge).
Tags and the cutting-board tool are written per version exactly as in Stardew Delight (checked against the jars of
Farmer's Delight, Forge/NeoForge and Fabric API of every version). The cooking pot serves a dish into the item it
leaves behind: a bowl, a glass bottle or an empty can.

  py tools/gen.py
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = 'apocalypsepantry'
RES = os.path.join(ROOT, 'src/main/resources')
ART = os.path.join(ROOT, 'art/textures')

# id: (English, Russian, Farmer's Delight category). Foods in the order of Foods.java, then the empty can.
ITEMS = {
    'canned_beans': ('Canned Beans', 'Фасоль в томате', 'meals'),
    'canned_stew': ('Canned Stew', 'Тушёнка', 'meals'),
    'canned_peaches': ('Canned Peaches', 'Консервированные персики', 'sweets'),
    'condensed_milk': ('Condensed Milk', 'Сгущёнка', 'sweets'),
    'energy_drink': ('Energy Drink', 'Энергетик', 'drinks'),
    'bottled_water': ('Bottled Water', 'Бутылка воды', 'drinks'),
    'herbal_tea': ('Herbal Tea', 'Травяной чай', 'drinks'),
    'mre_ration': ('MRE Ration', 'Сухпаёк (ИРП)', 'snacks'),
    'protein_bar': ('Protein Bar', 'Протеиновый батончик', 'snacks'),
    'hardtack': ('Hardtack', 'Галеты', 'snacks'),
    'instant_noodles': ('Instant Noodles', 'Лапша быстрого приготовления', 'meals'),
    'jerky': ('Jerky', 'Вяленое мясо', 'snacks'),
    'zombie_jerky': ('Zombie Jerky', 'Вяленая плоть зомби', 'snacks'),
    'grilled_rat': ('Grilled Rat', 'Крыса на палочке', 'snacks'),
    'pickled_cucumbers': ('Pickled Cucumbers', 'Банка солений', 'snacks'),
    'survivor_stew': ("Survivor's Stew", 'Похлёбка выжившего', 'meals'),
    'chocolate_ration': ('Chocolate Ration', 'Армейский шоколад', 'sweets'),
    'canned_fish': ("Canned Fish", "Рыбные консервы", 'meals'),
    'canned_tomato_soup': ("Canned Tomato Soup", "Томатный суп в банке", 'meals'),
    'canned_mushrooms': ("Canned Mushrooms", "Грибы в банке", 'meals'),
    'canned_ham': ("Canned Ham", "Ветчина в банке", 'meals'),
    'canned_dog_food': ("Canned Dog Food", "Собачий корм в банке", 'meals'),
    'cola': ("Cola", "Газировка", 'drinks'),
    'instant_coffee': ("Instant Coffee", "Растворимый кофе", 'drinks'),
    'kvass': ("Kvass", "Квас", 'drinks'),
    'moonshine': ("Moonshine", "Самогон", 'drinks'),
    'pine_needle_tea': ("Pine Needle Tea", "Хвойный чай", 'drinks'),
    'marrow_soup': ("Marrow Soup", "Похлёбка из костей", 'meals'),
    'game_stew': ("Game Stew", "Рагу из дичи", 'meals'),
    'dandelion_salad': ("Dandelion Salad", "Салат из одуванчиков", 'meals'),
    'porridge': ("Ration Porridge", "Каша из пайка", 'meals'),
    'rice_gruel': ("Rice Gruel", "Рисовая баланда", 'meals'),
    'bunker_chili': ("Bunker Chili", "Чили из бункера", 'meals'),
    'scavenger_soup': ("Scavenger Soup", "Похлёбка мародёра", 'meals'),
    'rice_crackers': ("Rice Crackers", "Рисовые хлебцы", 'snacks'),
    'trail_mix': ("Trail Mix", "Походная смесь", 'snacks'),
    'granola_bar': ("Granola Bar", "Гранола", 'snacks'),
    'dried_fruit': ("Dried Fruit", "Сухофрукты", 'sweets'),
    'fish_jerky': ("Fish Jerky", "Рыбная вяленка", 'snacks'),
    'roasted_spider_eye': ("Roasted Spider Eye", "Жареный паучий глаз", 'snacks'),
    'boiled_eggs': ("Boiled Eggs", "Варёные яйца", 'snacks'),
    'pemmican': ("Pemmican", "Пеммикан", 'snacks'),
    'hard_candy': ("Hard Candy", "Леденцы", 'sweets'),
    'pickled_eggs': ("Pickled Eggs", "Маринованные яйца", 'snacks'),
    'sauerkraut': ("Sauerkraut", "Квашеная капуста", 'snacks'),
    'mystery_meat': ("Mystery Meat", "Мясо неизвестного происхождения", 'snacks'),
    'emergency_ration': ("Emergency Ration", "Аварийный паёк", 'snacks'),
    'mushroom_skewer': ("Mushroom Skewer", "Грибной шашлык", 'snacks'),
    'empty_can': ('Empty Can', 'Пустая банка', None),
}
EFFECTS = {
    'infection': ('Infection', 'Заражение'),
    'undead_scent': ('Undead Scent', 'Мёртвый запах'),
    'adrenaline': ('Adrenaline', 'Адреналин'),
    'crash': ('Crash', 'Отходняк'),
    'stamina': ('Stamina', 'Запас сил'),
}

AP = MOD + ':'
# (recipe name, kind, ingredients or input, options). kind: pot (Farmer's Delight cooking pot), cut (cutting board with
# a knife), craft (shapeless), smelt, smoke, campfire. "#tag" in Forge 1.20.1 names (translated by TAGS), "fd:" =
# farmersdelight, "ap:" = this mod.
R = [
    ('empty_can', 'craft', ['minecraft:iron_nugget'] * 3, {}),
    ('iron_nugget_from_empty_can', 'smelt', 'ap:empty_can', {'result': 'minecraft:iron_nugget', 'xp': 0.1}),
    ('canned_beans', 'pot', ['minecraft:cocoa_beans', 'minecraft:cocoa_beans', 'fd:tomato_sauce'], {}),
    ('canned_stew', 'pot', ['minecraft:beef', '#forge:crops/potato', '#forge:crops/onion'], {}),
    ('canned_peaches', 'pot', ['minecraft:apple', 'minecraft:apple', 'minecraft:sugar'], {}),
    ('condensed_milk', 'pot', ['#forge:milk', 'minecraft:sugar', 'minecraft:sugar'], {}),
    ('energy_drink', 'pot', ['minecraft:sugar', 'minecraft:cocoa_beans', 'minecraft:glowstone_dust'], {'tab': 'drinks'}),
    ('bottled_water', 'pot', ['minecraft:ice'], {'tab': 'drinks'}),
    ('herbal_tea', 'pot', ['minecraft:fern', 'minecraft:sweet_berries', '#forge:salad_ingredients'], {'tab': 'drinks'}),
    ('mre_ration', 'craft', ['minecraft:paper', 'ap:hardtack', 'ap:jerky', 'ap:chocolate_ration'], {}),
    ('protein_bar', 'craft', ['#forge:crops/wheat', 'minecraft:honey_bottle', 'minecraft:pumpkin_seeds', 'minecraft:paper'], {'count': 2}),
    ('hardtack', 'craft', ['#forge:dough', '#forge:crops/wheat'], {'count': 2}),
    ('instant_noodles', 'pot', ['#forge:pasta', 'minecraft:dried_kelp', '#forge:crops/onion'], {}),
    ('jerky', 'cut', ['minecraft:cooked_beef'], {'count': 2}),
    ('jerky_from_porkchop', 'cut', ['minecraft:cooked_porkchop'], {'count': 2, 'result': 'ap:jerky'}),
    ('zombie_jerky', 'smoke', 'minecraft:rotten_flesh', {'xp': 0.35}),
    ('zombie_jerky_from_campfire', 'campfire', 'minecraft:rotten_flesh', {'xp': 0.35, 'result': 'ap:zombie_jerky'}),
    ('grilled_rat', 'craft', ['minecraft:stick', 'minecraft:cooked_rabbit'], {}),
    ('pickled_cucumbers', 'pot', ['minecraft:sea_pickle', 'minecraft:sea_pickle', 'minecraft:sugar'], {}),
    ('survivor_stew', 'pot', ['minecraft:beef', '#forge:crops/potato', '#forge:crops/carrot', 'minecraft:brown_mushroom',
                              '#forge:crops/onion'], {}),
    ('chocolate_ration', 'craft', ['minecraft:cocoa_beans', 'minecraft:cocoa_beans', 'minecraft:sugar', 'minecraft:paper'], {'count': 2}),
    ('canned_fish', 'pot', ["#forge:raw_fishes", "#forge:raw_fishes", "minecraft:kelp"], {}),
    ('canned_tomato_soup', 'pot', ["fd:tomato_sauce", "#forge:crops/tomato", "#forge:crops/onion"], {}),
    ('canned_mushrooms', 'pot', ["minecraft:brown_mushroom", "minecraft:red_mushroom", "#forge:crops/onion"], {}),
    ('canned_ham', 'pot', ["minecraft:porkchop", "minecraft:porkchop", "minecraft:sugar"], {}),
    ('canned_dog_food', 'pot', ["minecraft:rotten_flesh", "minecraft:bone_meal", "#forge:crops/wheat"], {}),
    ('cola', 'pot', ["minecraft:sugar", "minecraft:sugar", "minecraft:sweet_berries"], {"tab": "drinks"}),
    ('instant_coffee', 'pot', ["minecraft:cocoa_beans", "minecraft:cocoa_beans", "minecraft:sugar"], {"tab": "drinks"}),
    ('kvass', 'pot', ["minecraft:bread", "minecraft:sugar", "#forge:crops/wheat"], {"tab": "drinks"}),
    ('moonshine', 'pot', ["#forge:crops/potato", "#forge:crops/potato", "minecraft:sugar"], {"tab": "drinks"}),
    ('pine_needle_tea', 'pot', ["minecraft:spruce_leaves", "minecraft:spruce_leaves", "minecraft:sugar"], {"tab": "drinks"}),
    ('marrow_soup', 'pot', ["minecraft:bone", "minecraft:bone", "#forge:crops/onion"], {}),
    ('game_stew', 'pot', ["minecraft:rabbit", "#forge:crops/potato", "#forge:crops/carrot", "#forge:crops/onion"], {}),
    ('dandelion_salad', 'craft', ["minecraft:bowl", "minecraft:dandelion", "minecraft:dandelion", "#forge:salad_ingredients"], {}),
    ('porridge', 'pot', ["#forge:crops/wheat", "#forge:crops/wheat", "#forge:milk"], {}),
    ('rice_gruel', 'pot', ["#forge:crops/rice", "#forge:crops/rice", "minecraft:dried_kelp"], {}),
    ('bunker_chili', 'pot', ["minecraft:beef", "fd:tomato_sauce", "minecraft:cocoa_beans", "#forge:crops/onion"], {}),
    ('scavenger_soup', 'pot', ["#forge:crops/potato", "#forge:crops/carrot", "#forge:crops/cabbage", "#forge:crops/onion"], {}),
    ('rice_crackers', 'craft', ["#forge:crops/rice", "#forge:crops/rice"], {"count": 2}),
    ('trail_mix', 'craft', ["minecraft:pumpkin_seeds", "minecraft:melon_seeds", "minecraft:sweet_berries", "minecraft:cocoa_beans", "minecraft:paper"], {"count": 2}),
    ('granola_bar', 'craft', ["#forge:crops/wheat", "minecraft:honey_bottle", "minecraft:sweet_berries", "minecraft:paper"], {"count": 2}),
    ('dried_fruit', 'smoke', "minecraft:apple", {"xp": 0.35}),
    ('fish_jerky', 'craft', ["#forge:cooked_fishes", "minecraft:sugar"], {"count": 2}),
    ('roasted_spider_eye', 'campfire', "minecraft:spider_eye", {"xp": 0.35}),
    ('roasted_spider_eye_from_smoker', 'smoke', "minecraft:spider_eye", {"xp": 0.35, "result": "ap:roasted_spider_eye"}),
    ('boiled_eggs', 'pot', ["#forge:eggs", "#forge:eggs"], {"count": 2}),
    ('pemmican', 'craft', ["minecraft:cooked_beef", "minecraft:sweet_berries", "minecraft:sweet_berries", "minecraft:paper"], {"count": 2}),
    ('hard_candy', 'craft', ["minecraft:sugar", "minecraft:sugar", "minecraft:sweet_berries"], {"count": 4}),
    ('pickled_eggs', 'pot', ["#forge:eggs", "#forge:eggs", "minecraft:sugar"], {}),
    ('sauerkraut', 'pot', ["#forge:crops/cabbage", "#forge:crops/cabbage", "minecraft:sugar"], {}),
    ('mystery_meat', 'craft', ["minecraft:rotten_flesh", "minecraft:cooked_mutton"], {"count": 2}),
    ('emergency_ration', 'craft', ["ap:hardtack", "minecraft:honey_bottle", "minecraft:paper"], {}),
    ('mushroom_skewer', 'craft', ["minecraft:stick", "minecraft:brown_mushroom", "minecraft:red_mushroom"], {}),
]
COOK = {'smelt': ('minecraft:smelting', 200), 'smoke': ('minecraft:smoking', 100), 'campfire': ('minecraft:campfire_cooking', 600)}

CROPS = ['potato', 'onion', 'carrot', 'wheat', 'rice', 'cabbage', 'tomato']
_FORGE_TAGS = ['#forge:milk', '#forge:dough', '#forge:salad_ingredients', '#forge:pasta', '#forge:eggs', '#forge:raw_fishes',
               '#forge:cooked_fishes'] + [f'#forge:crops/{c}' for c in CROPS]
TAGS = {
    'forge': {t: t for t in _FORGE_TAGS},
    'fab120': {**{f'#forge:crops/{c}': f'#c:crops/{c}' for c in CROPS},
               '#forge:milk': '#c:milks', '#forge:dough': '#c:foods/doughs', '#forge:salad_ingredients': '#c:salad_ingredients',
               '#forge:pasta': '#c:foods/pastas', '#forge:eggs': '#c:eggs', '#forge:raw_fishes': '#c:foods/raw_fishes',
               '#forge:cooked_fishes': '#c:foods/cooked_fishes'},
    'c': {**{f'#forge:crops/{c}': f'#c:crops/{c}' for c in CROPS},
          '#forge:milk': '#c:drinks/milk', '#forge:dough': '#c:foods/dough', '#forge:salad_ingredients': '#c:foods/leafy_green',
          '#forge:pasta': '#c:foods/pasta', '#forge:eggs': '#c:eggs', '#forge:raw_fishes': '#c:foods/safe_raw_fish',
          '#forge:cooked_fishes': '#c:foods/cooked_fish'},
}
FOODS_MILK = {'#forge:milk': '#c:foods/milk'}  # Farmer's Delight Refabricated 1.21.5 - 1.21.10
_TOOL_FORGE_OLD = {'tag': 'forge:tools/knives'}
_TOOL_FORGE = [{'type': 'farmersdelight:tool_action', 'action': 'knife_dig'}, {'tag': 'forge:tools/knives'}]
_TOOL_NEO = [{'type': 'farmersdelight:item_ability', 'action': 'knife_dig'}, {'tag': 'c:tools/knife'}]
_TOOL_FAB121 = {'fabric:type': 'fabric:any', 'ingredients': [{'fabric:type': 'farmersdelight:item_ability', 'action': 'knife_dig'},
                                                             {'tag': 'c:tools/knife'}]}
TARGETS = {
    '1.18.2-forge': dict(tags='forge', tool=_TOOL_FORGE_OLD, pack=(8, 9)),
    '1.19.2-forge': dict(tags='forge', tool=_TOOL_FORGE_OLD, pack=(9, 10)),
    '1.20.1-forge': dict(tags='forge', tool=_TOOL_FORGE, pack=(15, 15)),
    '1.20.1-fabric': dict(tags='fab120', tool={'tag': 'c:tools/knives'}),
    '1.21.1-neoforge': dict(tags='c', tool=_TOOL_NEO),
    '1.21.1-fabric': dict(tags='c', tool=_TOOL_FAB121),
    '1.21.5-fabric': dict(tags='c', extra=FOODS_MILK, tool='#c:tools/knife', tab_key='category'),
    '1.21.8-fabric': dict(tags='c', extra=FOODS_MILK, tool='#c:tools/knife'),
    '1.21.10-fabric': dict(tags='c', extra=FOODS_MILK, tool='#c:tools/knife'),
    '1.21.11-fabric': dict(tags='c', tool='#c:tools/knife'),
    '26.1-fabric': dict(tags='c', tool='#c:tools/knife'),
    '26.2-fabric': dict(tags='c', tool='#c:tools/knife'),
    '26.3-fabric': dict(tags='c', tool='#c:tools/knife'),
}


def ver(s):
    return tuple(int(x) for x in s.split('.'))


class Target:
    def __init__(self, name, spec):
        self.name = name
        mc = self.mc = ver(name.split('-')[0])
        self.tags = dict(TAGS[spec['tags']], **spec.get('extra', {}))
        self.tool = spec['tool']
        self.pack = spec.get('pack')
        self.tab_key = spec.get('tab_key', 'recipe_book_tab')
        self.plural = mc < (1, 21)
        self.result_key = 'item' if mc < (1, 20, 5) else 'id'
        self.string_ingredients = mc >= (1, 21, 2)
        self.holder_predicates = mc >= (1, 20, 5)
        self.unlock_key = 'recipes' if mc >= (26, 3) else 'recipe'
        self.item_models = mc >= (1, 21, 4)
        self.out = os.path.join(ROOT, 'versions', name, 'generated')

    def map(self, s):
        s = self.tags.get(s, s)
        return s.replace('ap:', AP).replace('fd:', 'farmersdelight:')

    def ingredient(self, s):
        s = self.map(s)
        if self.string_ingredients:
            return s
        return {'tag': s[1:]} if s.startswith('#') else {'item': s}

    def stack(self, item, count=1):
        res = {self.result_key: self.map(item)}
        if count > 1:
            res['count'] = count
        return res

    def cook_result(self, item):
        item = self.map(item)
        return item if self.mc < (1, 20, 5) else {'id': item}

    def predicate(self, s):
        s = self.map(s)
        if self.holder_predicates:
            return {'items': s}
        return {'tag': s[1:]} if s.startswith('#') else {'items': [s]}

    def dirs(self):
        return ('recipes', 'advancements', 'tags/items') if self.plural else ('recipe', 'advancement', 'tags/item')


def wjson(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')


def check():
    for name, kind, ings, opt in R:
        for x in (ings if isinstance(ings, list) else [ings]):
            if x.startswith('#') and any(x not in TAGS[k] for k in TAGS):
                raise SystemExit(f'{name}: tag {x} is not translated for every version (TAGS)')
        if kind == 'pot':
            assert len(ings) <= 6 and 'minecraft:bowl' not in ings, name
    made = {opt.get('result', 'ap:' + name).replace('ap:', '') for name, _, _, opt in R}
    missing = [i for i in ITEMS if i not in made]
    if missing:
        raise SystemExit(f'no recipe for {missing}')


def write_assets():
    a = os.path.join(RES, 'assets', MOD)
    for sub in ('models/item', 'textures/item'):
        shutil.rmtree(os.path.join(a, sub), ignore_errors=True)
    os.makedirs(os.path.join(a, 'textures', 'item'), exist_ok=True)
    for i in ITEMS:
        wjson(os.path.join(a, 'models', 'item', i + '.json'), {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'{MOD}:item/{i}'}})
        shutil.copyfile(os.path.join(ART, i + '.png'), os.path.join(a, 'textures', 'item', i + '.png'))
    for k, lang in ((0, 'en_us'), (1, 'ru_ru')):
        out = {f'item.{MOD}.{i}': v[k] for i, v in ITEMS.items()}
        out.update({f'effect.{MOD}.{i}': v[k] for i, v in EFFECTS.items()})
        out['itemGroup.' + MOD] = 'Apocalypse Pantry'
        wjson(os.path.join(a, 'lang', lang + '.json'), out)
    shutil.copyfile(os.path.join(ROOT, 'page', 'docs', 'icon-512.png'), os.path.join(RES, MOD + '_logo.png'))


def write_target(t):
    shutil.rmtree(t.out, ignore_errors=True)
    rec_dir, adv_dir, tag_dir = t.dirs()
    data = os.path.join(t.out, 'data')
    for name, kind, ings, opt in R:
        result = opt.get('result', 'ap:' + name)
        count = opt.get('count', 1)
        if kind == 'pot':
            obj = {'type': 'farmersdelight:cooking', t.tab_key: opt.get('tab', 'meals'),
                   'ingredients': [t.ingredient(x) for x in ings], 'result': t.stack(result, count),
                   'experience': 1.0, 'cookingtime': 200}
            sub, inputs = 'cooking', ings
        elif kind == 'cut':
            res = t.stack(result, count) if t.plural else {'item': t.stack(result, count)}
            obj = {'type': 'farmersdelight:cutting', 'ingredients': [t.ingredient(x) for x in ings], 'tool': t.tool, 'result': [res]}
            sub, inputs = 'cutting', ings
        elif kind == 'craft':
            obj = {'type': 'minecraft:crafting_shapeless', 'group': MOD,
                   'ingredients': [t.ingredient(x) for x in ings], 'result': t.stack(result, count)}
            sub, inputs = 'crafting', ings
        else:
            typ, time = COOK[kind]
            obj = {'type': typ, 'ingredient': t.ingredient(ings), 'result': t.cook_result(result),
                   'experience': opt.get('xp', 0.1), 'cookingtime': time}
            sub, inputs = 'smelting', [ings]
        wjson(os.path.join(data, MOD, rec_dir, sub, name + '.json'), obj)
        rec_id = f'{MOD}:{sub}/{name}'
        crit = {'has_the_recipe': {'trigger': 'minecraft:recipe_unlocked', 'conditions': {t.unlock_key: rec_id}}}
        uniq = []
        for x in inputs:
            if x not in uniq and x not in ('minecraft:paper', 'minecraft:sugar', 'minecraft:bowl'):
                uniq.append(x)
        for n, x in enumerate(uniq):
            crit[f'has_ingredient_{n}'] = {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [t.predicate(x)]}}
        wjson(os.path.join(data, MOD, adv_dir, 'recipes', sub, name + '.json'), {
            'parent': 'minecraft:recipes/root', 'criteria': crit, 'requirements': [list(crit.keys())],
            'rewards': {'recipes': [rec_id]}, 'sends_telemetry_event': False})
    cats = {'drinks': [], 'meals': [], 'sweets': [], 'snacks': []}
    for i, v in ITEMS.items():
        if v[2]:
            cats[v[2]].append(AP + i)
    for k, v in cats.items():
        wjson(os.path.join(data, 'farmersdelight', tag_dir, k + '.json'), {'replace': False, 'values': v})
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
    check()
    write_assets()
    for name, spec in TARGETS.items():
        write_target(Target(name, spec))
    print(f'OK: {len(ITEMS)} items, {len(R)} recipes, data for {len(TARGETS)} versions')


if __name__ == '__main__':
    main()
