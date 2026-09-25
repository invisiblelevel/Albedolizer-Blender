# Albedolizer-Blender

Generate production-ready PBR maps from Albedo textures — right inside Blender.

Генерация готовых PBR-карт из Albedo-текстур — прямо внутри Blender.

**Free & open-source (GPL-3.0).**

**Бесплатно и с открытым исходным кодом (GPL-3.0).**

---

## 🇬🇧 English

### Features

- 🎨 **7 PBR maps** from a single Albedo texture:
  Height, Normal, AO, Roughness, Metallic, Edge, ORM
- ✨ **AI color correction** — Autolevels or LUTwithBGrid
- 🧮 **Math fallback** — CLAHE + soft-clip (no AI required)
- 🎯 **50 material presets** — metal, rust, wood, brick, concrete, fabric, fauna, and more
- 🤖 **Auto-detect preset from filename** — `brick_wall.png` → preset `brick`
- 🔲 **Seamless generation** — GIMP tile-seamless algorithm with optional hi-pass
- 🔗 **Auto-wired nodes** — maps connect to Principled BSDF automatically
- 🗂 **Batch mode** — generate for all selected objects at once
- 🎮 **Engine packing** — Unity HDRP, Unity URP, Unreal, Godot
- 💾 **Per-map bit depth** — 8-bit or 16-bit per map
- 🌐 **RU / EN interface**
- ⚡ **Works offline** — CLI is bundled inside the add-on

### Installation

1. Blender **4.2 LTS** or newer (tested on 5.2 LTS)
2. `Edit → Preferences → Add-ons → Install from Disk`
3. Pick `Albedolizer-Blender_v1.0.0_full.zip`
4. Enable **Albedolizer-Blender**
5. Done — the CLI is bundled and the path is set automatically.

### Usage

1. Open the **N-Panel** in the 3D Viewport (press `N`)
2. Go to the **Albedolizer** tab
3. Pick your **Albedo texture**
4. Choose:
   - **Material preset** — or let auto-detect guess from the filename
   - **Correction** — `AI` (recommended) / `Math` / `None`
   - **AI model** — Autolevels / LUTwithBGrid (if AI is selected)
   - **Seamless** — optional, for tiling textures
   - **Maps** — tick what you need
   - **Engine packing** — if you're exporting to a game engine
5. Hit **🎨 Generate PBR**

The maps are saved to a `_pbr` subfolder next to your texture, and wired into the active material.

### Batch mode

1. Select multiple mesh objects in the viewport
2. Pick an Albedo texture
3. Hit **🗂 Batch (all selected)**

One CLI run, all selected materials get their PBR nodes. Fast.

### Requirements

- Blender 4.2 LTS or newer
- Windows 10/11 (64-bit)
- No Python, no pip, no external dependencies — everything is bundled

### 💛 Support

This add-on is free. If it saves your time — drop some smokes:

- **BTC**: `bc1q2ka70s4vtmrskandqj8l4d6n3kdxyxa7kf3wf7`
- **USDT (TRC-20)**: `TUjY9p6oxKmeCQwNZwMfHqHdXuabaHpgT7`
- **GRAM**: `UQDWumGNNlnITx48WBzyI7Clb5wrpFRlJ3Se7xhfVKY5E2ad`

### About Albedolizer

This add-on is the Blender bridge for **Albedolizer** — a free desktop tool for 3D artists that checks Albedo textures, corrects color with AI, generates PBR maps and packs them for game engines.

**The full desktop app is free and open-source (MIT).** It adds a 3D preview, batch processing, texture compression, and a full GUI:

- 🌐 **GitHub**: [github.com/invisiblelevel/Albedolizer](https://github.com/invisiblelevel/Albedolizer)
- 🎮 **itch.io**: [invlvl.itch.io/albedolizer](https://invlvl.itch.io/albedolizer)
- 🗡 **Nexus Mods** (Skyrim SE): [nexusmods.com/skyrimspecialedition/mods/192671](https://www.nexusmods.com/skyrimspecialedition/mods/192671)

The add-on uses the same core engine — identical results, just inside Blender.

### Support & Feedback

Found a bug? Have an idea? Open an issue:
[github.com/invisiblelevel/Albedolizer-Blender/issues](https://github.com/invisiblelevel/Albedolizer-Blender/issues)

### License

- Add-on code: **GPL-3.0-or-later**
- Bundled CLI binaries (`cli/`): proprietary, distributed as part of this product.

See [`LICENSE`](LICENSE) for details.

---

## 🇷🇺 Русский

### Возможности

- 🎨 **7 PBR-карт** из одной Albedo-текстуры:
  Height, Normal, AO, Roughness, Metallic, Edge, ORM
- ✨ **AI-коррекция цвета** — Autolevels или LUTwithBGrid
- 🧮 **Математический fallback** — CLAHE + soft-clip (без AI)
- 🎯 **50 пресетов материалов** — металл, ржавчина, дерево, кирпич, бетон, ткань, фауна и т.д.
- 🤖 **Автоопределение пресета из имени файла** — `brick_wall.png` → пресет `brick`
- 🔲 **Бесшовность** — алгоритм GIMP tile-seamless с опциональным hi-pass
- 🔗 **Автосборка нод** — карты подключаются к Principled BSDF автоматически
- 🗂 **Batch-режим** — генерация для всех выделенных объектов сразу
- 🎮 **Упаковка под движки** — Unity HDRP, Unity URP, Unreal, Godot
- 💾 **Битность на карту** — 8-бит или 16-бит для каждой отдельно
- 🌐 **Русский / English интерфейс**
- ⚡ **Работает офлайн** — CLI встроен в аддон

### Установка

1. Blender **4.2 LTS** или новее (тестировано на 5.2 LTS)
2. `Edit → Preferences → Add-ons → Install from Disk`
3. Выбери `Albedolizer-Blender_v1.0.0_full.zip`
4. Включи **Albedolizer-Blender**
5. Готово — CLI уже внутри, путь прописан автоматически.

### Как пользоваться

1. Открой **N-панель** в 3D Viewport (клавиша `N`)
2. Перейди на вкладку **Albedolizer**
3. Выбери **Albedo-текстуру**
4. Настрой:
   - **Пресет материала** — или оставь автоопределение из имени файла
   - **Коррекция** — `AI` (рекомендуется) / `Math` / `None`
   - **AI-модель** — Autolevels / LUTwithBGrid (если выбрана AI)
   - **Бесшовность** — опционально, для тайлящихся текстур
   - **Карты** — отметь нужные
   - **Упаковка под движок** — если экспортируешь в игровой движок
5. Жми **🎨 Сгенерировать PBR**

Карты сохраняются в подпапку `_pbr` рядом с текстурой и подключаются к активному материалу.

### Batch-режим

1. Выдели несколько mesh-объектов во вьюпорте
2. Выбери Albedo-текстуру
3. Жми **🗂 Batch (все выделенные)**

Один прогон CLI — все выделенные материалы получают PBR-ноды. Быстро.

### Требования

- Blender 4.2 LTS или новее
- Windows 10/11 (64-bit)
- Никакого Python, pip и внешних зависимостей — всё внутри

### 💛 Поддержать

Аддон бесплатный. Если экономит время — закинь на папиросы:

- **BTC**: `bc1q2ka70s4vtmrskandqj8l4d6n3kdxyxa7kf3wf7`
- **USDT (TRC-20)**: `TUjY9p6oxKmeCQwNZwMfHqHdXuabaHpgT7`
- **GRAM**: `UQDWumGNNlnITx48WBzyI7Clb5wrpFRlJ3Se7xhfVKY5E2ad`

### Про Albedolizer

Этот аддон — мост в Blender для **Albedolizer** — бесплатной десктопной утилиты для 3D-художников. Проверяет Albedo-текстуры, корректирует цвет через AI, генерирует PBR-карты и упаковывает их под игровые движки.

**Полная десктопная версия бесплатна и с открытым исходным кодом (MIT).** В ней есть 3D-превью, пакетная обработка, сжатие текстур и полноценный GUI:

- 🌐 **GitHub**: [github.com/invisiblelevel/Albedolizer](https://github.com/invisiblelevel/Albedolizer)
- 🎮 **itch.io**: [invlvl.itch.io/albedolizer](https://invlvl.itch.io/albedolizer)
- 🗡 **Nexus Mods** (Skyrim SE): [nexusmods.com/skyrimspecialedition/mods/192671](https://www.nexusmods.com/skyrimspecialedition/mods/192671)

Аддон использует то же ядро — результат идентичный, просто внутри Blender.

### Баги и идеи

Нашёл баг? Есть идея? Открой issue:
[github.com/invisiblelevel/Albedolizer-Blender/issues](https://github.com/invisiblelevel/Albedolizer-Blender/issues)

### Лицензия

- Код аддона: **GPL-3.0-or-later**
- Встроенные CLI-бинарники (`cli/`): проприетарные, распространяются как часть продукта.

Подробности в [`LICENSE`](LICENSE).

---

## License / Лицензия

- Add-on code: **GPL-3.0-or-later**
- Bundled CLI binaries (`cli/`): proprietary, distributed as part of this product.

- Код аддона: **GPL-3.0-or-later**
- Встроенные CLI-бинарники (`cli/`): проприетарные, часть продукта.

See [`LICENSE`](LICENSE) for details. / Подробности в [`LICENSE`](LICENSE).