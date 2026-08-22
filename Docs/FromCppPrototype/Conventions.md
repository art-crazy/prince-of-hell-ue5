# Conventions — Prince of Hell

## Asset locations

| Location | Purpose | Git policy |
| --- | --- | --- |
| `SourceArt/` | Immutable sources: Tripo exports, Blender masters, texture masters | Git LFS |
| `Content/` | UE-imported assets and gameplay content | Git LFS for binary assets |
| `Docs/` | Specifications, contracts, manifests and decisions | Regular Git |
| `Scripts/` | Reproducible validation and editor automation | Regular Git |
| `Saved/`, `Intermediate/`, `DerivedDataCache/` | Machine-generated data | Never commit |

Do not overwrite a source export. A correction creates a new versioned source file and records the relationship in `Docs/AssetManifest.json`.

### Sandbox-to-production promotion

1. Import a new generated or external asset to `Content/_Sandbox/` and preserve its immutable source in `SourceArt/` through LFS.
2. Record provider, source file, licence URL/status, target skeleton, root-motion status and intended use in `Docs/AssetManifest.json`.
3. Run the relevant validator and inspect the asset in the test map. A character asset also needs UV0, normals, material-slot and scale checks.
4. Only then move it to its production folder and change `promotion_status` to `production_approved` in the same commit.

Unknown licence, unknown source, missing manifest record or a failed validator blocks promotion.

## UE asset names

Use English PascalCase names and one UE prefix. Names describe the asset's role, not the tool that produced it.

| Prefix | Use | Example |
| --- | --- | --- |
| `BP_` | Blueprint class | `BP_POHCharacter` |
| `GA_` | Gameplay Ability | `GA_HandDetach` |
| `GE_` | Gameplay Effect | `GE_HandRecallCost` |
| `GCN_` | Gameplay Cue Notify | `GCN_HellfireBurst` |
| `IA_` / `IMC_` | Enhanced Input action / mapping context | `IA_Dodge`, `IMC_Combat` |
| `SK_` | Skeletal mesh | `SK_POHPrince` |
| `SKEL_` | Skeleton | `SKEL_POHPrince` |
| `PHYS_` | Physics asset | `PHYS_POHPrince` |
| `ABP_` | Animation Blueprint | `ABP_POHPrince` |
| `AM_` / `AS_` | Anim Montage / Sequence | `AM_POH_LightCombo`, `AS_POH_Idle` |
| `IKR_` / `IK_` | IK Retargeter / IK Rig | `IKR_Manny_To_POH`, `IK_POHPrince` |
| `M_` / `MI_` / `T_` | Material / Material Instance / Texture | `M_BoneMaster`, `MI_POHArmor`, `T_POH_Body_BC` |
| `NS_` | Niagara System | `NS_Hellfire` |
| `MS_` | MetaSound Source | `MS_HandRecall` |
| `W_` | CommonUI / UMG widget | `W_PlayerHUD` |
| `L_` | Level map | `L_PrototypeArena` |
| `DA_` | Data Asset | `DA_POHCharacterDefinition` |

## Gameplay tags

Tags use dot-separated namespaces, start with a domain, and never encode a temporary implementation detail:

```text
Ability.Hand.Detach
Ability.Hand.Recall
State.HandLaunched
State.SoulTransferring
Event.Brazier.Ignited
```

The authoritative declarations are native tags in `POHGameplayTags`; do not
redeclare those names as ad-hoc strings or duplicate them in configuration.

## Change rules

1. A code or data change that alters an asset contract updates its document in the same commit.
2. Binary assets receive a short import/change note in the relevant manifest or feature specification.
3. Experimental plugins and systems live on `spike/<name>` until their acceptance criteria are met.
4. Assets first enter a `Content/_Sandbox/` area; only reviewed assets move into production folders.
