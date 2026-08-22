# Технический стек — UE5.8

## Решение

**Фиксируем Unreal Engine 5.8.** UE6 пока не является базой проекта. Все новые ассеты сохраняем только в UE5.8, чтобы не создавать несовместимость версий.

### Политика выбора технологий

Выбираем **новый, более функциональный и engine-native** вариант вместо старого «самого популярного по туториалам», если он имеет production-статус и даёт измеримое преимущество. Исключение одно: экспериментальные плагины сначала проходят отдельный spike-прототип и не становятся фундаментом vertical slice.

### Производительность — обязательное требование

Игра **не должна тормозить**: визуальная сложность, VFX, анимация, AI и новые инструменты принимаются только вместе с измеримым budget и проверкой на целевом ПК. Цель vertical slice — стабильные 60 FPS (16.67 ms на кадр) в репрезентативной боевой сцене, а не «в среднем в пустой комнате».

Если новая фича ухудшает frame-time, память или стабильность, приоритет такой: сначала измерить и устранить узкое место, затем упростить/LOD/cull/ограничить эффект, и только после этого расширять контент. Нельзя компенсировать неоптимизированный контент выключением диагностики, завышением Windows TDR или переносом проблемы «на потом».

| Зона | Выбор | Зачем |
| --- | --- | --- |
| Основа | C++ для систем + Blueprints для сборки контента | Агентам проще ревьюить и тестировать правила в C++, геймдизайнеру — собирать сцены в BP. |
| Ввод/UI | UE5.8 Unified Input: Enhanced Input + Common Input/UI | Современный объединённый ввод, контексты для боя/руки/UI, remapping и нормальная поддержка gamepad. |
| Бой/RPG | Gameplay Ability System + Gameplay Tags | Единая модель способностей, статусов, кулдаунов, урона и VFX-cues. Начинаем только с 4 способностей героя. |
| Анимация | IK Rig/Retargeter, Animation Montages, Motion Warping | Retarget готовых клипов на скелета; точный контакт во время атак, захватов и карабканья. |
| UI | UMG + CommonUI | Новый штатный стек для экранов, навигации и gamepad; не покупаем UI-kit до vertical slice. |
| VFX/звук | Niagara + MetaSounds | Одна переиспользуемая система адского огня для глаз, руки, смерти и жаровен; без FMOD/Wwise на старте. |
| AI | StateTree + AI Perception/EQS | Минимальный компаньон: выбрать цель, отвлечь, держать дистанцию. Не строим сложный squad AI. |
| Мир | PCG только как editor-time инструмент | Расстановка повторяемых руин, костей, декалей и огня; игра линейная, поэтому World Partition и Mass не нужны для vertical slice. |
| Контроль качества | UE Data Validation, Automation/Functional Tests, screenshot comparison | Раннее обнаружение сломанных импортов, механик и визуальных регрессий; сначала локально, затем в CI. |
| Профилирование | Unreal Insights, Memory Insights, Stat commands, RenderDoc | Измеряем CPU/GPU/память с первой арены; RenderDoc — только для целевой рендер-проблемы. |
| DCC | Blender; Houdini только после коммерческой лицензии | Blender — QA/LOD/rig cleanup. Houdini Apprentice не создаёт финальные коммерческие ассеты. |
| Editor automation | Встроенный **Unreal MCP** UE 5.8 + curated official toolsets | Codex/Claude управляют только локальным Editor: инспекция ассетов, сцены, GAS/tags и automation tests. |
| Версии | Git + Git LFS + GitHub | Текст/код ревьюятся обычным Git; `.uasset`, карты, FBX/GLB и текстуры — через LFS. |

## Языки и границы ответственности

| Технология | Используем для | Не используем для |
| --- | --- | --- |
| **C++ (версия, выбранная UE5.8)** | Runtime-ядро: GAS, боевые состояния, отсоединяемая рука, душа/сосуд, сохранения, интерфейсы AI и производительные подсистемы. | Быстрой сборки разового контента и крупных визуальных графов. |
| **Blueprints** | Сборки игровых сцен и контента: data-driven способности, интеракции, UI-flow, привязки VFX, Animation Montages/Notifies и квестовые события. | Монолитных графов с фундаментальной логикой или часто меняющихся алгоритмов. |
| **Python 3.11 (Editor only)** | Автоматизации: импорт и проверка ассетов, соглашения имён, отчёты QA, пакетные LOD/material-проверки. | Runtime-кода игры: Python работает в редакторе, а не в собранной игре. |

Не вводим C#, JavaScript/TypeScript, Lua или Verse в runtime UE-проекта без отдельного обоснованного решения. TypeScript допустим только для внешнего веб-инструмента; Verse относится к UEFN, не к обычному UE5-проекту.

**Правило для агентов:** правила и API сначала оформляются в C++ и открываются в Blueprint малыми, понятными точками расширения. Blueprint-ассеты считаются бинарным контентом и идут в LFS; не прячем в них сложную логику, которую нужно ревьюить, тестировать и часто сливать в Git.

## Новые технологии: что берём, а что не делаем фундаментом

- **Берём сейчас:** Unified Input UE5.8, StateTree, GAS, Motion Warping, PCG editor-time, Niagara, MetaSounds, Control Rig, FullBodyIK, Data Validation и UE Automation/Functional Testing.
- **Берём как reference only:** Lyra и Game Animation Sample. Их не копируем в production-проект целиком; извлекаем только документированные паттерны после проверки лицензии и версии UE.
- **Добавляем только после гейта:** self-hosted GitHub Actions — когда локальная проверка работает без диалогов; Substance 3D Painter — когда герой прошёл mesh/UV/material QA; коммерческий Houdini — когда есть повторяемая задача для окружения или VFX.
- **Проверяем отдельным spike:** Gameplay Camera System — он очень удобен для data-driven камер, но Epic всё ещё помечает его как Experimental.
- **Проверяем отдельным spike:** Pose Search/Motion Matching. Он может повысить качество locomotion, но требует достаточного набора root-motion клипов и сравнения с baseline по отзывчивости, памяти и frame-time.
- **Не берём в production сейчас:** Mover/ChaosMover. Это перспективная замена Character Movement, но всё ещё Experimental; для shipping vertical slice используем проверенный Character Movement Component + Motion Warping.

## Модульность без переусложнения

### GAS foundation

Native C++ owns the `AbilitySystemComponent`, resource attributes and gameplay-effect resolution. Blueprints may configure future abilities, costs, cues and presentation, but do not directly mutate Health, Stamina, Soul or HandIntegrity.

### Граница Blueprint для prototype HUD и способностей

Текущие четыре hero-ability и debug HUD создаются в C++ и безопасны без финальных Blueprint-ассетов. Blueprint может заменить визуальный HUD, подключить montage, Niagara, MetaSound и data-driven values, но не должен обходить GAS или напрямую изменять core attributes/state tags. Prototype HUD обновляет только текстовый readout с частотой 10 Hz и удаляется вместе с pawn; финальный UI заменит его без изменения боевых контрактов.

Vertical slice строится через C++ components/interfaces, Data Assets, Gameplay Tags и небольшие подсистемы. Game Features/Modular Gameplay и полная архитектура Lyra не являются базой: они станут оправданными только когда появятся две независимо включаемые игровые experience/feature-зоны. Это сохраняет маленький проект понятным для Git и агентов.

## Агенты

Codex/Claude работают с текстом, C++, Blueprint-спецификациями, Data Assets, тестами и CI. Они не должны:

- коммитить кэш UE (`Saved`, `Intermediate`, `DerivedDataCache`);
- добавлять сторонние плагины или новые уникальные механики без записи решения в Git;
- менять версию UE5.8 без отдельной миграционной ветки;
- выдавать AI-анимацию или Tripo-сетку за готовый production-asset без QA.

### Unreal MCP — редакторский контур

Используем официальный экспериментальный **Unreal MCP** из UE 5.8, а не
сторонний сервер. Он включён только для target `Editor`; packaged/development
build игры не должен запускать MCP. Сервер автоматически поднимается только на
`http://127.0.0.1:8000/mcp`; у него нет аутентификации, поэтому запрещены
удалённый bind, port-forwarding и публикация этого адреса.

В проекте хранится endpoint для Codex в `.codex/config.toml`, а общие
editor-настройки — в `Config/DefaultEditorPerProjectUserSettings.ini`. После
перезапуска Codex и Unreal Editor агент открывает проект из его корня и
проверяет MCP через discovery toolsets. Включён Tool Search: контекст не
загружается сотнями схем сразу. Подключены только Editor, Automation Test,
GAS и Gameplay Tags toolsets; агрегатор All Toolsets намеренно не используется,
пока его экспериментальные модули не проходят clean smoke. Все изменения,
выполненные через MCP, проходят
обычные Git diff, Data Validation и automation/smoke-test до коммита.

MCP ускоряет editor-операции, но не заменяет C++/Python scripts, ревью и
performance QA; поскольку функция экспериментальная, любой сбой оставляет
воспроизводимый CLI/Python fallback.

## Не добавляем до vertical slice

- мультиплеер, Epic Online Services, Mass, сложную экономику;
- сторонние UI/audio/framework-плагины;
- runtime LLM и генерируемый в реальном времени сюжетный текст.

## Первые проверяемые результаты

1. Игрок: перемещение, камера, lock-on, один удар, dodge.
2. GAS: здоровье, урон, `Hand.Detach`, `Hand.Recall`, `Soul.Transfer`.
3. Niagara: огонь глаз и огонь руки.
4. Один враг и один AI-компаньон с одной задачей.
5. Одна маленькая арена; только затем — гигантский босс.

## Quality gates

1. Любой source animation или AI-ассет живёт в `_Sandbox`, пока не записаны источник, лицензия, skeleton target, root-motion status и назначение.
2. Baseline-анимация на Animation Blueprint + Montages никогда не удаляется ради experimental spike.
3. У каждой новой системы есть budget: допустимое влияние на CPU/GPU frame-time, память, число активных actor/component/VFX и fallback при превышении.
4. Каждый vertical-slice gate имеет Unreal Insights/Memory Insights capture на целевом ПК и результат относительно 60 FPS (16.67 ms) target; проверяется репрезентативный бой, а не пустая карта.
5. CI появляется только после успешного unattended local verification; не добавляем облачный сервис или remote UBA cache «на вырост».

## Официальные опоры

- [UE 5.8 release notes](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes)
- [Gameplay Ability System](https://dev.epicgames.com/documentation/unreal-engine/gameplay-ability-system-for-unreal-engine)
- [Enhanced Input](https://dev.epicgames.com/documentation/unreal-engine/enhanced-input-in-unreal-engine)
- [Motion Warping](https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-warping-in-unreal-engine)
- [PCG Framework](https://dev.epicgames.com/documentation/unreal-engine/pcg-development-guides)
- [Unreal MCP (UE 5.8)](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor)
