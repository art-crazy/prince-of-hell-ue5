# MCP Automation Bridge — what works, what doesn't

Notes from vibecoding the lock-on feature (2026-08-23). Read before authoring
Blueprint logic through `mcp__unreal-engine__unreal`.

## Reliable — use freely

- `create_node` for plain nodes: `K2Node_CallFunction`, `K2Node_VariableGet/Set`,
  `K2Node_IfThenElse`, `K2Node_EnhancedInputAction` (structurally — see below).
- `connect_pins`, `set_pin_default_value`, `delete_node` (needs `consent`), `compile`.
- `add_variable` / `remove_variable`.
- `manage_networking`: `create_input_action`, `map_input_action`, `set_input_trigger`.
- `manage_asset.search_assets`, `control_actor.spawn_blueprint` / `find_by_class` / `get_transform`.
- `blueprint.get_pin_details`, `get_graph_details` — good for reading wiring.

## Broken or unreliable — avoid / verify independently

- **`K2Node_SetFieldsInStruct` / `K2Node_MacroInstance` (ForEachLoop etc.) via
  `create_node`**: node is created but comes back with **zero pins** — no struct
  type or macro graph bound. Unusable through this API. Need loops/struct-field
  editing → do it by hand in the editor, or write C++.
- **`K2Node_EnhancedInputAction` runtime binding**: the node *looks* correct
  (all pins present, `InputAction` default set, compiles clean) but the
  Blueprint's `Triggered` exec never actually fires — confirmed with
  `showdebug enhancedinput`, which shows the action reaching `Completed` at the
  engine level while the graph stays silent. Recreating the node doesn't fix it.
  **Don't trust a bridge-created Enhanced Input event node until you've proven
  it fires** (see debugging recipe below). If it doesn't, that logic needs to
  move to C++ or be wired by hand in the editor.
- **Exec output pins only hold one link.** `connect_pins` on an already-connected
  exec output **silently replaces** the old link instead of erroring. Before
  rewiring an existing node's exec pin, `get_pin_details` it first and preserve
  the downstream chain (insert your new node *between*, don't just redirect).
- **`get_blueprint`, `get_node_details`, `inspect_object`, `list_struct_members`**:
  return errors or empty payloads even on success — don't rely on them for
  reading values.
- **`control_editor.save_all` under-reports.** Often says "Saved 0 packages"
  even when there are real unsaved changes (seen on both Input assets and
  Blueprints). Don't trust the message — verify with `git status`/mtime, or
  save via Python directly (see below), which has actually worked every time.
- **`system_control.console_command` blocks `py ...` commands** by policy. Use
  `system_control.execute_python` instead — separate action, not blocked.

## Debugging recipe that actually works

1. **Python + file round-trip.** `execute_python` doesn't return stdout, so make
   every script write results to a scratch file (e.g. `Saved/mcp_debug.txt`)
   and `Read` it back. Wrap risky calls in `try/except` — one unguarded
   exception kills the whole script silently.
2. **`unreal.EditorLevelLibrary.get_game_world()`** returns `None` when PIE
   isn't running — cheap liveness check before debugging "nothing happens" reports.
3. **`showdebug enhancedinput`** (via `SystemLibrary.execute_console_command`,
   then ask the user for a screenshot) — shows every active mapping context,
   priority, key conflicts (`OVERRIDDEN BY ...`), and each action's live
   trigger state. The single most useful diagnostic for input bugs.
4. Many Actor properties are **protected from Python** (`Pawn`, `Controller`,
   `Player`, `InputComponent`, `GameInstance.LocalPlayers`) — no workaround
   found. Getting the `EnhancedInputLocalPlayerSubsystem` from Python failed
   entirely; don't burn time on it. Custom BlueprintReadWrite variables (e.g.
   our own `LockedTarget`) read fine via `get_editor_property`.
5. To read/edit `InputMappingContext` mappings in UE 5.8, the top-level
   `mappings` property is empty — go through
   `imc.get_editor_property('default_key_mappings').get_editor_property('mappings')`,
   each entry has `action`/`key`, and `key.get_editor_property('key_name')` for
   the string. Build `unreal.Key()` empty then
   `.set_editor_property('key_name', 'F')` — passing `key_name` to the
   constructor throws.
6. Reliable save from Python:
   `unreal.EditorLoadingAndSavingUtils.save_packages([obj.get_outermost()], False)`.
7. Compare a **known-working pre-existing node** against a new one when a bound
   event seems dead (e.g. we diffed our `IA_LockOn` against the template's
   `IA_Strafe`) — isolates "my new node is broken" from "input isn't reaching
   the pawn at all" fast.

## Two real bugs found this way (not bridge issues)

- **Key collision, no error:** mapping a new Input Action to an already-used
  key in the same context just makes the *older* action win silently — no
  warning anywhere. Check `showdebug enhancedinput` for `OVERRIDDEN BY` before
  assuming a key is free.
- **`.gitignore` had excluded the entire active Sandbox Input Action set**
  (`IMC_Sandbox` + ~18 `IA_*` assets) under a stale "not yet decided" block —
  they're load-bearing (this is the character's real input context), not
  scaffolding. Removed from `.gitignore`.

## Bottom line

For plain data/logic nodes, the bridge is fast and reliable — keep using it.
For struct-field edits, loops, and (until proven otherwise per-case) Enhanced
Input event bindings, don't trust bridge-authored nodes blind — verify with
the debugging recipe above, or do that specific piece by hand / in C++.

## C++ pivot (2026-08-23): lock-on solved by moving input binding to C++

Root cause of the original bug was confirmed: `K2Node_EnhancedInputAction`
nodes created by the bridge are structurally fine, the engine just never
calls their delegate — this is a bridge/graph-authoring limitation, not an
Enhanced Input config problem. Native `EnhancedInputComponent::BindAction` in
C++ is unaffected and fixed it immediately.

Project had no `Source/` yet. Added a minimal game module (`Source/test/`,
`test.Target.cs`, `testEditor.Target.cs`) — **remember to add a `"Modules"`
array to `test.uproject`** (Blueprint-only projects have none); without it
the editor loads the compiled DLL but the module's classes never register,
and Python calls like `unreal.LockOnComponent` silently return
`AttributeError`. Build with:
`Build.bat testEditor Win64 Development -Project="<abs path to .uproject>"`.
No engine restart tool exists through the bridge — close/relaunch
`UnrealEditor.exe` via Bash/PowerShell around each rebuild.

Lock-on logic now lives in `Source/test/LockOnComponent.h/.cpp`, a plain
`UActorComponent` added to the character's SCS, using
`UKismetSystemLibrary::SphereOverlapActors` for target search (reuse over
hand-rolled queries) and `EnhancedInputComponent::BindAction` for input.

**New bridge gaps found while wiring the component into the Blueprint:**
- `blueprint.add_scs_component` throws `OUTPUT_SCHEMA_VIOLATION` ("Missing
  required parameter 'componentName'") even though the component **is**
  actually added — always verify with `blueprint.get_scs` rather than
  trusting the error.
- `blueprint.set_scs_property` / `modify_scs` cannot set object-reference
  properties (e.g. binding a `UInputAction*`) — both reject every value
  format tried (`"Property value is invalid"`, or `modify_scs` demands an
  undocumented `operations` array that its own schema then rejects). Set
  object references from Python instead: the SCS template is reachable at
  `unreal.load_object(blueprint.generated_class(), "<ComponentName>_GEN_VARIABLE")`
  (not `"<ComponentName>"` — that returns `None`), then
  `template.set_editor_property(...)` works normally, followed by
  `unreal.BlueprintEditorLibrary.compile_blueprint(bp)` and the Python save.

**Pawn possession timing gotcha (project-specific, not a bridge bug):** this
character's Blueprint convention binds input in the `Possessed` event, not
`BeginPlay` — because `PlayerController->Possess()` happens *after* the
pawn's `BeginPlay`. A C++ component's `BeginPlay` will see
`GetController() == nullptr` and silently no-op. Fix: don't bind once in
`BeginPlay`; retry every `TickComponent` (guarded by a bound-flag) until a
valid locally-controlled `PlayerController` with a live `InputComponent`
exists. Cheap and self-healing regardless of spawn/possession order.

Debug UPROPERTYs (`bInputBound`, `TriggerCount`, `OverlapCount` on
`ULockOnComponent`) were left in — they're the fastest way to tell, via
Python readback in PIE, whether a fresh symptom is "input never bound",
"input fires but nothing overlaps", or "found a target but camera logic is
wrong", without adding new debug infra each time.
