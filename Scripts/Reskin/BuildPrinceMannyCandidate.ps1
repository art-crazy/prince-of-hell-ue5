param(
    [string]$SourceFbx = 'C:\Users\artcr\Downloads\skeleton+warrior+3d+model (2)\tripo_convert_64b875e2-394a-4cba-9050-fdd54b8c44c1.fbx'
)

$ErrorActionPreference = 'Stop'
$Project = 'C:\Users\artcr\Documents\Unreal Projects\test'
$Blender = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
$Layout = Join-Path $Project 'Saved\ReskinPipeline\MannySkeletonLayout.json'
$Output = Join-Path $Project 'Saved\ReskinPipeline\POH_Prince_MannyCandidate.fbx'
$Script = Join-Path $Project 'Scripts\Reskin\ReskinPrinceToManny.py'
$Validator = Join-Path $Project 'Scripts\Reskin\ValidateReskinnedFbx.py'
$Log = Join-Path $Project 'Saved\Logs\PrinceMannyReskin.log'

New-Item -ItemType Directory -Force (Split-Path $Log) | Out-Null
"[$(Get-Date -Format o)] POH_RESKIN_BUILD start" | Set-Content -Encoding utf8 $Log
$BuildOutput = Join-Path $Project 'Saved\Logs\PrinceMannyReskin-build.tmp.log'
$BuildError = Join-Path $Project 'Saved\Logs\PrinceMannyReskin-build-error.tmp.log'
$ValidationOutput = Join-Path $Project 'Saved\Logs\PrinceMannyReskin-validate.tmp.log'
$ValidationError = Join-Path $Project 'Saved\Logs\PrinceMannyReskin-validate-error.tmp.log'
$BuildArguments = '--factory-startup --background --python "{0}" -- "{1}" "{2}" "{3}"' -f $Script, $SourceFbx, $Layout, $Output
$BuildProcess = Start-Process -FilePath $Blender -ArgumentList $BuildArguments -Wait -PassThru -NoNewWindow -RedirectStandardOutput $BuildOutput -RedirectStandardError $BuildError
$BuildText = (Get-Content -Raw $BuildOutput) + (Get-Content -Raw $BuildError)
$BuildText | Tee-Object -FilePath $Log -Append
$BuildExitCode = $BuildProcess.ExitCode
if ($BuildExitCode -ne 0 -or $BuildText -notmatch 'POH_RESKIN SUCCESS') { throw "Reskin build failed (exit $BuildExitCode); see $Log" }
$ValidationArguments = '--factory-startup --background --python "{0}" -- "{1}" "{2}"' -f $Validator, $Output, $Layout
$ValidationProcess = Start-Process -FilePath $Blender -ArgumentList $ValidationArguments -Wait -PassThru -NoNewWindow -RedirectStandardOutput $ValidationOutput -RedirectStandardError $ValidationError
$ValidationText = (Get-Content -Raw $ValidationOutput) + (Get-Content -Raw $ValidationError)
$ValidationText | Tee-Object -FilePath $Log -Append
$ValidationExitCode = $ValidationProcess.ExitCode
if ($ValidationExitCode -ne 0 -or $ValidationText -notmatch 'POH_RESKIN_VALIDATE PASS') { throw "Candidate validation failed (exit $ValidationExitCode); see $Log" }
Remove-Item -LiteralPath $BuildOutput, $BuildError, $ValidationOutput, $ValidationError -Force -ErrorAction SilentlyContinue
"[$(Get-Date -Format o)] POH_RESKIN_BUILD success" | Add-Content -Encoding utf8 $Log
Write-Host "Candidate: $Output"
Write-Host "Log: $Log"
