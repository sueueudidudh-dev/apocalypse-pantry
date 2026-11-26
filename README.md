<p align="center"><img src="page/docs/banner.gif" alt="Apocalypse Pantry" width="100%"></p>

**Food for the end of the world.** 17 survival foods and five effects built around a zombie apocalypse.
The mod page text is in [`page/docs/description.md`](page/docs/description.md).

# Apocalypse Pantry — еда для зомби-апокалипсиса

* **Minecraft 1.18.2 – 26.3** на **Forge, NeoForge и Fabric** — те же версии, что у Stardew Delight (таблица ниже)
* Не требует других модов; на Fabric нужен **Fabric API**
* Нужен и на клиенте, и на сервере

## Версии
| Minecraft | Загрузчик | Файл |
|---|---|---|
| 26.3 | Fabric | `apocalypsepantry-fabric-26.3-1.0.0.jar` |
| 26.2 | Fabric | `apocalypsepantry-fabric-26.2-1.0.0.jar` |
| 26.1 – 26.1.2 | Fabric | `apocalypsepantry-fabric-26.1-1.0.0.jar` |
| 1.21.11 | Fabric | `apocalypsepantry-fabric-1.21.11-1.0.0.jar` |
| 1.21.9 – 1.21.10 | Fabric | `apocalypsepantry-fabric-1.21.10-1.0.0.jar` |
| 1.21.6 – 1.21.8 | Fabric | `apocalypsepantry-fabric-1.21.8-1.0.0.jar` |
| 1.21.5 | Fabric | `apocalypsepantry-fabric-1.21.5-1.0.0.jar` |
| 1.21.1 | NeoForge | `apocalypsepantry-neoforge-1.21.1-1.0.0.jar` |
| 1.21.1 | Fabric | `apocalypsepantry-fabric-1.21.1-1.0.0.jar` |
| 1.20.1 | Forge | `apocalypsepantry-forge-1.20.1-1.0.0.jar` |
| 1.20.1 | Fabric | `apocalypsepantry-fabric-1.20.1-1.0.0.jar` |
| 1.19.2 | Forge | `apocalypsepantry-forge-1.19.2-1.0.0.jar` |
| 1.18.2 | Forge | `apocalypsepantry-forge-1.18.2-1.0.0.jar` |

## Что в моде
* **17 блюд** (`Foods.java`) и 2 тары: пустая банка и пустая фляга. Консервы оставляют пустую банку, вода — стеклянную
  бутылку, похлёбка — миску, крыса — палку, чай — пустую флягу. Тара возвращается и при крафте из блюда.
* **5 эффектов** (`EffectLogic.java`, миксины в `mixin/`):
  * **Заражение** — удар зомби, кадавра, утопленника или зомби-жителя: 10 % на «Нормально», 25 % на «Сложно».
    Голод тратится в 1,5 раза быстрее, через 5 минут — Слабость, через 10 — Замедление. Длится час. Молоко и тотем
    его не снимают, лечит только фляга травяного чая. Если игрок умирает заражённым, на месте смерти появляется зомби
    с его именем.
  * **Мёртвый запах** — нежить не выбирает игрока целью, пока он сам её не ударит; удар снимает эффект.
  * **Адреналин** — Скорость II и Прыгучесть I; когда кончается — **Отходняк** (Замедление и Усталость, 0:30),
    его снимает вода.
  * **Запас сил** — голод тратится вдвое медленнее.
* Рецепты — `tools/gen.py` (верстак, коптильня и костёр, переплавка банки в самородок), открываются в книге рецептов,
  как только подобран ингредиент.
* Зомби, убитые игроком, с шансом 5 % роняют консервы, галеты, энергетик или воду.
* Подсказки: голод, насыщение, эффекты с длительностью, шансы, что снимает.

## Сборка
Один исходник на все версии — [Stonecutter](https://stonecutter.kikugie.dev/) 0.10, сборка устроена как у Stardew Delight.
```
py tools\gen.py                     # модели, текстуры, языки и данные для всех версий
py dev\build_all.py                 # все версии по очереди, логи в build/logs/
py dev\build_all.py 1.21.1-fabric   # одна версия
py dev\srv.py 1.21.1-fabric         # самопроверка на выделенном сервере (SELFTEST DONE в логе)
```
Готовые jar: `build/libs/1.0.0/apocalypsepantry-<загрузчик>-<версия MC>-1.0.0.jar`.
Текстуры — `art/make_textures.py`, значки эффектов — `art/make_effect_icons.py`, оформление страницы — `page/make_page.py`.

## Лицензия
MIT, см. [LICENSE](LICENSE).
