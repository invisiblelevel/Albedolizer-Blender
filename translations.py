"""
translations.py — RU/EN strings для аддона.
"""

T = {
    "ru": {
        "panel_title": "Albedolizer PBR",
        "cli_section": "CLI",
        "cli_status_ok": "✅ CLI OK",
        "cli_status_missing": "❌ CLI не найден",
        "cli_status_unknown": "⚠ CLI не проверен",
        "cli_check": "Проверить",
        "cli_copy": "Копировать путь",
        "cli_open_folder": "Открыть папку CLI",
        "cli_copied": "Путь скопирован в буфер",

        "albedo_section": "Albedo текстура",
        "albedo_pick": "Выбрать файл",
        "albedo_clear": "Очистить",

        "preset_section": "Пресет материала",
        "autodetect_preset": "Автоопределение из имени файла",
        "autodetect_hint": "Например, brick_wall.png → пресет brick",

        "correction_section": "Коррекция",
        "correction_none": "Без коррекции",
        "correction_ai": "AI",
        "correction_math": "Математика",
        "ai_model": "AI модель",

        "seamless_section": "Бесшовность",
        "seamless_enable": "Сделать бесшовной",
        "seamless_hipass": "Hi-pass (выровнять яркость)",

        "maps_section": "Карты",
        "maps_all": "Все",
        "maps_none": "Ничего",
        "maps_height": "Height",
        "maps_normal": "Normal",
        "maps_ao": "AO",
        "maps_roughness": "Roughness",
        "maps_metallic": "Metallic",
        "maps_edge": "Edge",
        "maps_orm": "ORM",

        "engine_section": "Упаковка под движок",
        "engine_none": "Без упаковки",

        "generate_btn": "🎨 Сгенерировать PBR",
        "generate_batch_btn": "🗂 Batch (все выделенные)",
        "open_folder_btn": "📁 Открыть папку с PBR",
        "cancel_btn": "Отмена",

        "progress_generating": "Генерация PBR...",
        "progress_cancelled": "Отменено пользователем",
        "progress_seamless": "Бесшовность...",

        "msg_no_albedo": "Сначала выбери Albedo-текстуру",
        "msg_no_material": "У объекта нет материала — создаю новый",
        "msg_material_created": "Создан материал",
        "msg_no_object": "Выдели объект",
        "msg_cli_missing": "CLI не найден. Проверь путь в настройках аддона",
        "msg_generating": "Генерация PBR для",
        "msg_generated": "PBR готов",
        "msg_failed": "Ошибка генерации",
        "msg_no_maps": "Не выбрано ни одной карты",
        "msg_batch_no_objects": "Выдели объекты с материалами",
        "msg_batch_done": "Batch готов",
        "msg_folder_missing": "Папка не найдена — сгенерируй PBR сначала",

        "batch_progress": "Batch: объект",
        "batch_of": "из",

        "support_section": "Поддержать проект",
        "support_btn": "💛 Поддержать",
        "support_title": "Поддержать Albedolizer",
        "support_text": (
            "Аддон бесплатный. Если он экономит тебе время —\n"
            "можешь закинуть на папиросы. Спасибо!"
        ),
        "support_copied": "✅ Адрес скопирован",
        "support_close": "Закрыть",
        "github_btn": "GitHub проекта",
        "itch_btn": "Скачать полную прогу",
    },

    "en": {
        "panel_title": "Albedolizer PBR",
        "cli_section": "CLI",
        "cli_status_ok": "✅ CLI OK",
        "cli_status_missing": "❌ CLI not found",
        "cli_status_unknown": "⚠ CLI not checked",
        "cli_check": "Check",
        "cli_copy": "Copy path",
        "cli_open_folder": "Open CLI folder",
        "cli_copied": "Path copied to clipboard",

        "albedo_section": "Albedo Texture",
        "albedo_pick": "Pick file",
        "albedo_clear": "Clear",

        "preset_section": "Material Preset",
        "autodetect_preset": "Auto-detect from filename",
        "autodetect_hint": "e.g. brick_wall.png → brick preset",

        "correction_section": "Correction",
        "correction_none": "None",
        "correction_ai": "AI",
        "correction_math": "Math",
        "ai_model": "AI model",

        "seamless_section": "Seamless",
        "seamless_enable": "Make seamless",
        "seamless_hipass": "Hi-pass (even brightness)",

        "maps_section": "Maps",
        "maps_all": "All",
        "maps_none": "None",
        "maps_height": "Height",
        "maps_normal": "Normal",
        "maps_ao": "AO",
        "maps_roughness": "Roughness",
        "maps_metallic": "Metallic",
        "maps_edge": "Edge",
        "maps_orm": "ORM",

        "engine_section": "Engine Packing",
        "engine_none": "None",

        "generate_btn": "🎨 Generate PBR",
        "generate_batch_btn": "🗂 Batch (all selected)",
        "open_folder_btn": "📁 Open PBR folder",
        "cancel_btn": "Cancel",

        "progress_generating": "Generating PBR...",
        "progress_cancelled": "Cancelled by user",
        "progress_seamless": "Seamless...",

        "msg_no_albedo": "Pick an Albedo texture first",
        "msg_no_material": "Object has no material — creating a new one",
        "msg_material_created": "Material created",
        "msg_no_object": "Select an object",
        "msg_cli_missing": "CLI not found. Check path in add-on preferences",
        "msg_generating": "Generating PBR for",
        "msg_generated": "PBR done",
        "msg_failed": "Generation failed",
        "msg_no_maps": "No maps selected",
        "msg_batch_no_objects": "Select objects with materials",
        "msg_batch_done": "Batch done",
        "msg_folder_missing": "Folder not found — generate PBR first",

        "batch_progress": "Batch: object",
        "batch_of": "of",

        "support_section": "Support the project",
        "support_btn": "💛 Support",
        "support_title": "Support Albedolizer",
        "support_text": (
            "This add-on is free. If it saves your time —\n"
            "drop some smokes for uncle. Thank you!"
        ),
        "support_copied": "✅ Address copied",
        "support_close": "Close",
        "github_btn": "Project on GitHub",
        "itch_btn": "Get the full app",
    },
}


def get_lang(prefs):
    """Возвращает строку языка: 'ru' или 'en'."""
    return prefs.language if hasattr(prefs, "language") else "en"


def tr(prefs, key):
    """Возвращает перевод по ключу."""
    lang = get_lang(prefs)
    return T.get(lang, T["en"]).get(key, key)