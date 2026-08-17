#include "PrinceAnimationGraphLibrary.h"

#if WITH_EDITOR
#include "AnimGraphNode_Base.h"
#include "Animation/AnimBlueprint.h"
#include "Animation/AnimationAsset.h"
#include "EdGraph/EdGraph.h"
#include "EdGraph/EdGraphNode.h"
#include "Kismet2/KismetEditorUtilities.h"
#include "Misc/PackageName.h"
#include "UObject/SavePackage.h"
#endif

namespace PrinceAccuRigGraphPaths
{
    constexpr TCHAR Blueprint[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/ABP_POH_AccuRig_UE58.ABP_POH_AccuRig_UE58");
    constexpr TCHAR RetargetedFolder[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP");
}

bool UPrinceAnimationGraphLibrary::RebindAccuRigUE58Graph()
{
#if !WITH_EDITOR
    return false;
#else
    UAnimBlueprint* Blueprint = LoadObject<UAnimBlueprint>(nullptr, PrinceAccuRigGraphPaths::Blueprint);
    if (!Blueprint)
    {
        UE_LOG(LogTemp, Error, TEXT("POH_ANIMGRAPH_BUILD missing isolated UE58 graph"));
        return false;
    }

    TArray<UEdGraph*> Graphs;
    Blueprint->GetAllGraphs(Graphs);

    TArray<UAnimGraphNode_Base*> Nodes;
    for (UEdGraph* Graph : Graphs)
    {
        if (Graph)
        {
            for (UEdGraphNode* Node : Graph->Nodes)
            {
                if (UAnimGraphNode_Base* AnimNode = Cast<UAnimGraphNode_Base>(Node))
                {
                    Nodes.Add(AnimNode);
                }
            }
        }
    }

    TArray<UAnimationAsset*> ReferencedAnimations;
    for (UAnimGraphNode_Base* Node : Nodes)
    {
        Node->GetAllAnimationSequencesReferred(ReferencedAnimations);
    }

    TMap<UAnimationAsset*, UAnimationAsset*> Replacements;
    for (UAnimationAsset* Source : ReferencedAnimations)
    {
        if (!Source || Source->GetPathName().StartsWith(PrinceAccuRigGraphPaths::RetargetedFolder))
        {
            continue;
        }

        const FString TargetName = FString::Printf(TEXT("UE58_%s"), *Source->GetName());
        const FString TargetPath = FString::Printf(TEXT("%s/%s.%s"), PrinceAccuRigGraphPaths::RetargetedFolder, *TargetName, *TargetName);
        UAnimationAsset* Target = LoadObject<UAnimationAsset>(nullptr, *TargetPath);
        if (!Target)
        {
            UE_LOG(LogTemp, Error, TEXT("POH_ANIMGRAPH_BUILD missing target clip %s"), *TargetPath);
            return false;
        }
        Replacements.Add(Source, Target);
    }

    for (UAnimGraphNode_Base* Node : Nodes)
    {
        Node->Modify();
        Node->ReplaceReferredAnimations(Replacements);
    }

    FKismetEditorUtilities::CompileBlueprint(Blueprint);
    UPackage* Package = Blueprint->GetOutermost();
    FSavePackageArgs SaveArgs;
    SaveArgs.TopLevelFlags = RF_Public | RF_Standalone;
    SaveArgs.Error = GError;
    const FString Filename = FPackageName::LongPackageNameToFilename(Package->GetName(), FPackageName::GetAssetPackageExtension());
    if (!UPackage::SavePackage(Package, Blueprint, *Filename, SaveArgs))
    {
        UE_LOG(LogTemp, Error, TEXT("POH_ANIMGRAPH_BUILD unable to save %s"), *Filename);
        return false;
    }

    UE_LOG(LogTemp, Log, TEXT("POH_ANIMGRAPH_BUILD complete nodes=%d replaced_assets=%d asset=%s"), Nodes.Num(), Replacements.Num(), *Blueprint->GetPathName());
    return true;
#endif
}
