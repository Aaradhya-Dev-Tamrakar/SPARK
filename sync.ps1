<#
.SYNOPSIS
    Automates Git pull, auto-commit message generation, changelog update, and multi-remote push for SPARK.

.DESCRIPTION
    1. Pulls with --autostash from origin on the active branch.
    2. Auto-updates dev_logs/SPARK_TRACKER.md's "Last updated" timestamp if needed.
    3. Auto-generates a conventional commit message if none is provided.
    4. Stages and commits local changes.
    5. Automatically pushes to both primary (Aaradhya-Dev-Tamrakar/SPARK) and mirror (AaradhyaDT/SPARK) repositories.

.EXAMPLE
    .\sync.ps1                               # Fully automated: commit & push to all remotes
    .\sync.ps1 -m "feat(training): message"  # Uses custom conventional commit message
    .\sync.ps1 -SkipBuild                    # Sync but skip LaTeX PDF compilation
    .\sync.ps1 -PullOnly                     # Only pull without committing/pushing
#>

param (
    [Alias("m")]
    [string]$Message,

    [switch]$PullOnly,

    [Alias("Skip", "NoBuild", "SkipPdf")]
    [switch]$SkipBuild,

    [switch]$Build
)

$ErrorActionPreference = "Continue"

# Remotes to synchronize
$TargetRemotes = @(
    @{ Name = "origin"; Url = "https://github.com/Aaradhya-Dev-Tamrakar/SPARK.git" },
    @{ Name = "aaradhyadt"; Url = "https://github.com/AaradhyaDT/SPARK.git" }
)

function Initialize-RemotesConfigured {
    $existingRemotes = @(git remote)
    foreach ($target in $TargetRemotes) {
        if ($existingRemotes -notcontains $target.Name) {
            Write-Host "[Git Sync] Adding missing remote '$($target.Name)' ($($target.Url))..." -ForegroundColor DarkCyan
            git remote add $target.Name $target.Url
        } else {
            $currentUrl = (git remote get-url $target.Name 2>$null)
            if ($currentUrl) {
                $currentUrl = $currentUrl.Trim()
            }
            if ($currentUrl -and $currentUrl -ne $target.Url) {
                Write-Host "[Git Sync] Updating URL for remote '$($target.Name)' -> $($target.Url)..." -ForegroundColor DarkCyan
                git remote set-url $target.Name $target.Url
            }
        }
    }
}

# Provide alias for backward compatibility
Set-Alias -Name Ensure-RemotesConfigured -Value Initialize-RemotesConfigured -Scope Global -ErrorAction SilentlyContinue

function Get-AutoCommitMessage {
    $statusLines = @(git status --porcelain 2>$null)
    if (-not $statusLines -or $statusLines.Count -eq 0) {
        return $null
    }

    $modifiedFiles = @()
    $addedFiles = @()
    $deletedFiles = @()
    $allFiles = @()

    foreach ($line in $statusLines) {
        if ([string]::IsNullOrWhiteSpace($line) -or $line.Length -lt 3) {
            continue
        }

        $statusCode = $line.Substring(0, 2)
        $rawPath = $line.Substring(3).Trim()

        # Handle renamed files: "R  old -> new"
        if ($rawPath -match '->') {
            $rawPath = ($rawPath -split '->')[-1].Trim()
        }

        # Strip enclosing quotes if path contains spaces
        $cleanPath = $rawPath.Trim('"')
        $fileName = Split-Path $cleanPath -Leaf

        if ([string]::IsNullOrWhiteSpace($fileName)) {
            continue
        }

        $allFiles += @{ Name = $fileName; Path = $cleanPath; Status = $statusCode }

        if ($statusCode -match 'A|\?\?') {
            $addedFiles += $fileName
        } elseif ($statusCode -match 'D') {
            $deletedFiles += $fileName
        } else {
            $modifiedFiles += $fileName
        }
    }

    $allChangedNames = @($allFiles | ForEach-Object { $_.Name })
    if ($allChangedNames.Count -eq 0) {
        return $null
    }

    # Determine conventional commit prefix based on file types and locations
    $isAllDocs = $true
    $isAllTests = $true
    $hasSourceCode = $false
    $hasNewCode = $false

    foreach ($item in $allFiles) {
        $p = $item.Path
        $fn = $item.Name
        $isDoc = ($p -match '^(docs/|dev_logs/)') -or ($fn -match '\.(md|tex|bib|png|jpg|svg|drawio\.xml|pdf)$')
        $isTest = ($p -match '^(tests/|firmware/test/)') -or ($fn -match '^test_.*\.py$')
        $isCode = ($fn -match '\.(py|ino|cpp|c|h|hpp)$')

        if (-not $isDoc) { $isAllDocs = $false }
        if (-not $isTest) { $isAllTests = $false }
        if ($isCode) {
            $hasSourceCode = $true
            if ($item.Status -match 'A|\?\?') {
                $hasNewCode = $true
            }
        }
    }

    $prefix = "chore"
    if ($isAllDocs) {
        $prefix = "docs"
    } elseif ($isAllTests) {
        $prefix = "test"
    } elseif ($hasNewCode) {
        $prefix = "feat"
    } elseif ($hasSourceCode) {
        $prefix = "refactor"
    } elseif ($addedFiles.Count -gt 0) {
        $prefix = "feat"
    } elseif ($allFiles | Where-Object { $_.Path -match '^(pyproject\.toml|\.gitignore|sync\.ps1|CMakeLists\.txt)' }) {
        $prefix = "build"
    }

    # Action verb
    $action = "update"
    if ($addedFiles.Count -gt 0 -and $modifiedFiles.Count -eq 0 -and $deletedFiles.Count -eq 0) {
        $action = "add"
    } elseif ($deletedFiles.Count -gt 0 -and $modifiedFiles.Count -eq 0 -and $addedFiles.Count -eq 0) {
        $action = "remove"
    }

    # Summary list
    $summary = ""
    if ($allChangedNames.Count -le 3) {
        $summary = ($allChangedNames -join ", ")
    } else {
        $firstTwo = ($allChangedNames[0..1]) -join ", "
        $extraCount = $allChangedNames.Count - 2
        $summary = "$firstTwo +$extraCount more"
    }

    return "${prefix}: ${action} ${summary}"
}

function Update-TrackerLog {
    param ([string]$CommitMsg)

    $trackerPath = "dev_logs/SPARK_TRACKER.md"
    if (-not (Test-Path $trackerPath)) {
        $found = Get-ChildItem -Path . -Recurse -Filter "SPARK_TRACKER.md" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) {
            $trackerPath = $found.FullName
        } else {
            return
        }
    }

    $todayIso = Get-Date -Format "yyyy-MM-dd"
    $todayReadable = Get-Date -Format "MMMM d, yyyy"

    try {
        $fullTrackerPath = (Resolve-Path $trackerPath).Path
        $content = [System.IO.File]::ReadAllText($fullTrackerPath, [System.Text.Encoding]::UTF8)

        # Match bare date without parenthetical notes (e.g. "**Last updated:** 2026-08-22 ·" or "**Last updated:** August 22, 2026 ·")
        if ($content -match '\*\*Last updated:\*\*\s*(?:[A-Za-z]+\s+\d{1,2},\s+\d{4}|\d{4}-\d{2}-\d{2})\s*·') {
            $content = [System.Text.RegularExpressions.Regex]::Replace(
                $content,
                '\*\*Last updated:\*\*\s*(?:[A-Za-z]+\s+\d{1,2},\s+\d{4}|\d{4}-\d{2}-\d{2})\s*·',
                "**Last updated:** $todayReadable ·"
            )
            [System.IO.File]::WriteAllText($fullTrackerPath, $content, (New-Object System.Text.UTF8Encoding($false)))
            Write-Host "[Git Sync] Updated $(Split-Path $trackerPath -Leaf) timestamp to $todayReadable." -ForegroundColor Cyan
        } elseif ($content -match '\*\*Last updated:\*\*.*?\(.*?\).*?·') {
            Write-Host "[Git Sync] $(Split-Path $trackerPath -Leaf) has detailed 'Last updated' note, keeping intact." -ForegroundColor DarkGray
        }
    } catch {
        Write-Host "[Git Sync] Warning: Could not update tracker timestamp: $_" -ForegroundColor Yellow
    }
}

function Invoke-ThesisPdfBuild {
    $thesisDir = "docs/SPARK_Proposal/ThesisReports"
    $thesisTex = "thesis_report.tex"
    $thesisTexPath = Join-Path $thesisDir $thesisTex

    if (Test-Path $thesisTexPath) {
        $hasPdflatex = [bool](Get-Command pdflatex -ErrorAction SilentlyContinue)
        if ($hasPdflatex) {
            Write-Host "[Git Sync] Compiling thesis PDF ($thesisTex)..." -ForegroundColor Cyan
            Push-Location $thesisDir
            try {
                # Two passes to resolve cross-references, TOC, and list of figures/tables
                $null = & pdflatex -interaction=nonstopmode $thesisTex 2>&1
                $null = & pdflatex -interaction=nonstopmode $thesisTex 2>&1

                # Brief pause so Windows releases file handles on .aux/.log/.toc etc.
                Start-Sleep -Seconds 2

                if (Test-Path "thesis_report.pdf") {
                    Write-Host "[Git Sync] Thesis PDF compiled successfully." -ForegroundColor Green
                } else {
                    Write-Host "[Git Sync] Warning: thesis_report.pdf was not produced by pdflatex." -ForegroundColor Yellow
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

# Provide alias for backward compatibility
Set-Alias -Name Build-ThesisPdf -Value Invoke-ThesisPdfBuild -Scope Global -ErrorAction SilentlyContinue

function Clear-IgnoredArtifacts {
    $cleanupPaths = @(
        "docs/SPARK_Proposal/ThesisReports"
    )
    # LaTeX auxiliary extensions to remove (thesis_report.pdf is kept)
    $auxExtensions = @("*.aux","*.bbl","*.blg","*.fdb_latexmk","*.fls","*.idx",
                       "*.ilg","*.ind","*.lof","*.log","*.lot","*.out",
                       "*.synctex.gz","*.synctex(busy)","*.toc")

    foreach ($path in $cleanupPaths) {
        if (Test-Path $path) {
            Write-Host "[Git Sync] Cleaning LaTeX build artifacts in $path..." -ForegroundColor DarkCyan
            $removed = 0
            foreach ($ext in $auxExtensions) {
                $files = Get-ChildItem -Path $path -Filter $ext -File -ErrorAction SilentlyContinue
                foreach ($f in $files) {
                    # Retry up to 3 times in case Windows still holds a file lock
                    for ($attempt = 1; $attempt -le 3; $attempt++) {
                        try {
                            Remove-Item -Path $f.FullName -Force -ErrorAction Stop
                            $removed++
                            break
                        } catch {
                            if ($attempt -lt 3) {
                                Start-Sleep -Milliseconds 500
                            }
                            # Silently skip on final attempt — file is gitignored anyway
                        }
                    }
                }
            }
            if ($removed -gt 0) {
                Write-Host "[Git Sync] Removed $removed build artifact(s)." -ForegroundColor DarkCyan
            }
        }
    }
}

# Provide alias for backward compatibility
Set-Alias -Name Clean-IgnoredArtifacts -Value Clear-IgnoredArtifacts -Scope Global -ErrorAction SilentlyContinue

# -------------------------------------------------------------
# Execution Routine
# -------------------------------------------------------------

Initialize-RemotesConfigured

# Detect current branch
$currentBranch = (git branch --show-current 2>$null)
if ($currentBranch) {
    $currentBranch = $currentBranch.Trim()
}
if (-not $currentBranch) {
    $currentBranch = "main"
}

# Determine whether to build PDF
$shouldBuild = -not $SkipBuild
if ($PSBoundParameters.ContainsKey('Build') -and -not $Build) {
    $shouldBuild = $false
}

if ($shouldBuild) {
    Invoke-ThesisPdfBuild
    $pdfPath = "docs/SPARK_Proposal/ThesisReports/thesis_report.pdf"
    if (-not (Test-Path $pdfPath)) {
        Write-Host "[Git Sync] Error: Thesis PDF build failed or thesis_report.pdf is missing. Aborting sync." -ForegroundColor Red
        exit 1
    }
    Clear-IgnoredArtifacts
} else {
    Write-Host "[Git Sync] Skipping thesis PDF build." -ForegroundColor DarkGray
}

Write-Host "[Git Sync] Pulling latest changes from origin $currentBranch..." -ForegroundColor Cyan
git pull --autostash origin $currentBranch

if ($PullOnly) {
    Write-Host "[Git Sync] Pull complete (PullOnly flag set)." -ForegroundColor Green
    exit 0
}

# Determine commit message if not explicitly supplied (or supplied as empty/whitespace string)
$autoGenerated = $false
if ([string]::IsNullOrWhiteSpace($Message)) {
    $Message = Get-AutoCommitMessage
    if ($Message) {
        $autoGenerated = $true
        Write-Host "[Git Sync] Auto-generated commit message: '$Message'" -ForegroundColor Yellow
    }
}

# Check if there are local uncommitted changes
$hasLocalChanges = [bool](git status --porcelain 2>$null)

if ($hasLocalChanges -and -not [string]::IsNullOrWhiteSpace($Message)) {
    Update-TrackerLog -CommitMsg $Message

    Write-Host "[Git Sync] Staging changes..." -ForegroundColor Cyan
    git add .

    Write-Host "[Git Sync] Committing: '$Message'..." -ForegroundColor Cyan
    git commit -m "$Message"
} elseif ($hasLocalChanges -and [string]::IsNullOrWhiteSpace($Message)) {
    Write-Host "[Git Sync] Local changes present but no commit message could be determined." -ForegroundColor Yellow
} else {
    Write-Host "[Git Sync] No local uncommitted changes." -ForegroundColor Gray
}

# Synchronize all configured remotes
foreach ($target in $TargetRemotes) {
    Write-Host "[Git Sync] Pushing to $($target.Name) ($($target.Url)) on branch $currentBranch..." -ForegroundColor Cyan
    git push $target.Name $currentBranch
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[Git Sync] Push to $($target.Name) rejected. Re-pulling and retrying push..." -ForegroundColor Yellow
        git pull --rebase --autostash $target.Name $currentBranch
        git push $target.Name $currentBranch
    }
}

# Post-sync verification
$remaining = @(git status --porcelain 2>$null | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
if ($remaining.Count -gt 0) {
    Write-Host "[Git Sync] Warning: $($remaining.Count) file(s) still have uncommitted changes:" -ForegroundColor Yellow
    foreach ($r in $remaining) {
        Write-Host "           $r" -ForegroundColor Yellow
    }
} else {
    Write-Host "[Git Sync] All repositories are clean and fully synchronized!" -ForegroundColor Green
}
