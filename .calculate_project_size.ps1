# Function to read .gitignore file and convert patterns
function Get-GitIgnorePatterns {
    param (
        [string]$Path
    )
    $patterns = Get-Content $Path | Where-Object { $_ -and $_ -notmatch '^\s*#' }
    return $patterns
}

# Function to check if a file or directory matches any pattern
function MatchesPattern {
    param (
        [string]$Item,
        [string[]]$Patterns
    )
    foreach ($pattern in $Patterns) {
        $wildcardPattern = $pattern.Replace('/', '\')
        if ($Item -like "*$wildcardPattern*") {
            return $true
        }
    }
    return $false
}

# Function to get the size of a directory excluding specified patterns
function Get-DirectorySize {
    param (
        [string]$Path,
        [string[]]$Exclusions
    )
    $totalSize = 0
    $items = Get-ChildItem -Recurse -Force -Path $Path
    foreach ($item in $items) {
        $relativePath = $item.FullName.Substring($Path.Length).TrimStart('\')
        if (-not (MatchesPattern -Item $relativePath -Patterns $Exclusions)) {
            if ($item -is [System.IO.FileInfo]) {
                $totalSize += $item.Length
            }
        }
    }
    return $totalSize
}

# Read .gitignore file
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$gitignorePath = Join-Path -Path $scriptDir -ChildPath ".gitignore"
$excludePatterns = @()
if (Test-Path $gitignorePath) {
    $excludePatterns = Get-GitIgnorePatterns -Path $gitignorePath
}

# Get the size of the current directory
$currentDir = Get-Location
$sizeInBytes = Get-DirectorySize -Path $currentDir -Exclusions $excludePatterns

# Convert size to a human-readable format
$sizeInMB = [math]::round($sizeInBytes / 1MB, 2)

Write-Output "Total project size (excluding specified patterns): $sizeInMB MB"


























<# # Get the total size of the project, excluding the specified patterns
$excludePatterns = @(
    ".vscode",
    "app/media",
    "*.sqlite3",
    "*.log",
    "*.pyc",
    "*.pyo",
    "__pycache__",
    "venvpy_3.9",
    "blender-3.2.2",
    "ffmpeg-6.0-full_build",
    "rembg/test",
    "rembg/tests/fixtures",
    "rembg/tests/results",
    "rembg/.dockerignore",
    "rembg/Dockerfile",
    "unsused scripts",
    "dump.rdb",
    "Ivan.code-workspace",
    "Three-Structure.ps1",
    "Tree_Structure.txt",
    "C:\B-Star\billboardstar_2\app\templates_BBS\footage"
)

# Function to get the size of a directory excluding specified patterns
function Get-DirectorySize {
    param (
        [string]$Path,
        [string[]]$Exclusions
    )
    $totalSize = 0
    $items = Get-ChildItem -Recurse -Force -Path $Path -Exclude $Exclusions
    foreach ($item in $items) {
        if ($item -is [System.IO.FileInfo]) {
            $totalSize += $item.Length
        }
    }
    return $totalSize
}

# Get the size of the current directory
$currentDir = Get-Location
$sizeInBytes = Get-DirectorySize -Path $currentDir -Exclusions $excludePatterns

# Convert size to a human-readable format
$sizeInMB = [math]::round($sizeInBytes / 1MB, 2)

Write-Output "Total project size (excluding specified patterns): $sizeInMB MB" #>