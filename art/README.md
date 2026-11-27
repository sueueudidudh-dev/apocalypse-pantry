# Apocalypse Delight: текстуры и значки эффектов

48 блюд и пустая банка (16×16) и 5 значков эффектов (18×18) нарисованы в Aseprite, в духе Farmer's Delight: обводка — тёмный оттенок своего цвета, свет сверху слева.

- Исходники: `aseprite/<id>.aseprite`.
- Готовые текстуры предметов: `textures/<id>.png`. Значки эффектов экспортируются сразу в `src/main/resources/assets/apocalypsedelight/textures/mob_effect/`.
- Превью всех предметов и эффектов: `preview_sheet.png` (собран в Aseprite, исходник `aseprite/preview_sheet.aseprite`).
- `aseprite/specs_part1.json`, `specs_part2.json`: пиксельные схемы, по которым спрайты рисовались через Aseprite MCP.

Чтобы поправить текстуру: открой `aseprite/<id>.aseprite` в Aseprite, сохрани, экспортируй PNG поверх `textures/<id>.png` и запусти `py tools\gen.py`.

Как эффекты и блюда работают в моде на самом деле — см. README.md в корне проекта и `src/main/java/com/apocalypsedelight/Foods.java`.
