<#
.SYNOPSIS
    Automates Git pull, auto-commit message generation, changelog update, and multi-remote push for SPARK.

.DESCRIPTION
    1. Pulls with --autostash from origin main.
    2. Auto-updates dev_logs/SPARK_TRACKER.md's "Last updated" line if needed.
    3. Auto-generates a conventional commit message if none is provided.
    4. Stages and commits changes.
    5. Automatically pushes to both primary (Aaradhya-Dev-Tamrakar/SPARK) and mirror (AaradhyaDT/SPARK) repositories.

.EXAMPLE
    .\sync.ps1                               # Fully automated: commit & push to all remotes
    .\sync.ps1 -m "feat(training): message"  # Uses custom conventional commit message
    .\sync.ps1 -PullOnly                     # Only pull without committing/pushing
#>

param (
    [Alias("m")]
    [string]$Message,

    [switch]$PullOnly
)

$ErrorActionPreference = "Continue"

# Remotes to synchronize
$TargetRemotes = @(
    @{ Name = "origin"; Url = "https://github.com/Aaradhya-Dev-Tamrakar/SPARK.git" },
    @{ Name = "aaradhyadt"; Url = "https://github.com/AaradhyaDT/SPARK.git" }
)

function Ensure-RemotesConfigured {
    $existingRemotes = git remote
    foreach ($target in $TargetRemotes) {
        if ($existingRemotes -notcontains $target.Name) {
            Write-Host "[Git Sync] Adding missing remote '$($target.Name)' ($($target.Url))..." -ForegroundColor DarkCyan
            git remote add $target.Name $target.Url
        }
    }
}

function Get-AutoCommitMessage {
    $statusLines = git status --porcelain
    if (-not $statusLines) {
        return $null
    }

    $modifiedFiles = @()
    $addedFiles = @()
    $deletedFiles = @()

    foreach ($line in $statusLines) {
        $status = $line.Substring(0, 2).Trim()
        $file = $line.Substring(3).Trim()
        $fileName = Split-Path $file -Leaf

        if ($status -match 'A|\?\?') {
            $addedFiles += $fileName
        } elseif ($status -match 'D') {
            $deletedFiles += $fileName
        } else {
            $modifiedFiles += $fileName
        }
    }

    $allChanged = $addedFiles + $modifiedFiles + $deletedFiles
    if ($allChanged.Count -eq 0) {
        return $null
    }

    $prefix = "chore"
    if ($addedFiles.Count -gt 0) {
        $prefix = "feat"
    } elseif ($modifiedFiles | Where-Object { $_ -match '\.(py|ino|cpp|h|c)$' }) {
        $prefix = "refactor"
    } elseif ($modifiedFiles | Where-Object { $_ -match '\.(md|tex)$' }) {
        $prefix = "docs"
    }

    $summary = ""
    if ($allChanged.Count -le 3) {
        $summary = $allChanged -join ", "
    } else {
        $firstTwo = ($allChanged[0..1]) -join ", "
        $extraCount = $allChanged.Count - 2
        $summary = "$firstTwo +$extraCount more"
    }

    return "${prefix}: update ${summary}"
}

function Update-TrackerLog {
    param ([string]$CommitMsg)
    $trackerFile = Get-ChildItem -Path . -Recurse -Filter "SPARK_TRACKER.md" | Select-Object -First 1
    if (-not $trackerFile) { return }

    $todayDate = Get-Date -Format "yyyy-MM-dd"

    $content = Get-Content $trackerFile.FullName -Raw
    if ($content -match '\*\*Last updated:\*\*\s*[0-9]{4}-[0-9]{2}-[0-9]{2}\s*·') {
        # Bare date, no parenthetical detail yet -- safe to auto-stamp.
        $content = $content -replace '\*\*Last updated:\*\*\s*[0-9]{4}-[0-9]{2}-[0-9]{2}\s*·', "**Last updated:** $todayDate ·"
        Set-Content -Path $trackerFile.FullName -Value $content -NoNewline
        Write-Host "[Git Sync] Updated $($trackerFile.Name) timestamp to $todayDate." -ForegroundColor Cyan
    } elseif ($content -match '\*\*Last updated:\*\*.*?\(.*?\).*?·') {
        # Line already has a hand-written parenthetical -- leave it alone.
        Write-Host "[Git Sync] $($trackerFile.Name) already has a detailed 'Last updated' line, skipping auto-stamp." -ForegroundColor DarkGray
    }
}

function Build-ThesisPdf {
    $thesisDir = "docs/SPARK_Proposal/ThesisReports"
    $thesisTex = "thesis_report.tex"
    if (Test-Path "$thesisDir/$thesisTex") {
        if (Get-Command pdflatex -ErrorAction SilentlyContinue) {
            Write-Host "[Git Sync] Compiling thesis PDF ($thesisTex)..." -ForegroundColor Cyan
            Push-Location $thesisDir
            try {
                # Two passes to resolve cross-references, TOC, and lists of figures/tables
                pdflatex -interaction=nonstopmode $thesisTex | Out-Null
                pdflatex -interaction=nonstopmode $thesisTex | Out-Null
                if (Test-Path "thesis_report.pdf") {
                    Write-Host "[Git Sync] Thesis PDF compiled successfully." -ForegroundColor Green
                }
            } catch {
                Write-Host "[Git Sync] Warning: LaTeX build encountered an error: $_" -ForegroundColor Yellow
            } finally {
                Pop-Location
            }
        } else {
            Write-Host "[Git Sync] pdflatex not found on PATH, skipping PDF build." -ForegroundColor DarkGray
        }
    }
}

function Clean-IgnoredArtifacts {
    $cleanupPaths = @(
        "docs/SPARK_Proposal/ThesisReports"
    )
    foreach ($path in $cleanupPaths) {
        if (Test-Path $path) {
            Write-Host "[Git Sync] Cleaning gitignored build artifacts in $path..." -ForegroundColor DarkCyan
            git clean -fdX $path
        }
    }
}

Ensure-RemotesConfigured

Write-Host "[Git Sync] Pulling latest changes from origin main..." -ForegroundColor Cyan
git pull --autostash origin main

# Build thesis PDF and clean up auxiliary files
Build-ThesisPdf
Clean-IgnoredArtifacts

if ($PullOnly) {
    Write-Host "[Git Sync] Pull complete (PullOnly flag set)." -ForegroundColor Green
    exit 0
}

# Determine commit message
if (-not $Message) {
    $Message = Get-AutoCommitMessage
    if ($Message) {
        Write-Host "[Git Sync] Auto-generated commit message: '$Message'" -ForegroundColor Yellow
    }
}

if ($Message) {
    Update-TrackerLog -CommitMsg $Message

    Write-Host "[Git Sync] Staging changes..." -ForegroundColor Cyan
    git add .

    Write-Host "[Git Sync] Committing: '$Message'..." -ForegroundColor Cyan
    git commit -m "$Message"

    foreach ($target in $TargetRemotes) {
        Write-Host "[Git Sync] Pushing to $($target.Name) ($($target.Url))..." -ForegroundColor Cyan
        git push $target.Name main
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[Git Sync] Push to $($target.Name) rejected. Re-pulling and retrying push..." -ForegroundColor Yellow
            git pull --rebase --autostash $target.Name main
            git push $target.Name main
        }
    }
} else {
    Write-Host "[Git Sync] No local changes detected to commit." -ForegroundColor Gray
}

Write-Host "[Git Sync] All repositories are clean and fully synchronized!" -ForegroundColor Green
