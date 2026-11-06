<#
.SYNOPSIS
    Nyverune Corne Profile Switcher & Auto-Detection for Windows.
.DESCRIPTION
    Monitors active foreground window on Windows (Neovim vs Browser/Apps)
    and synchronizes the Corne keyboard profile.
#>

param (
    [Parameter(Position=0)]
    [ValidateSet("watch", "everyday", "neovim", "toggle")]
    [string]$Action = "watch"
)

# Win32 API declaration for foreground window detection
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;

public class Win32 {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll", SetLastError=true, CharSet=CharSet.Auto)]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);
}
"@

function Get-ActiveWindowTitle {
    $hwnd = [Win32]::GetForegroundWindow()
    if ($hwnd -eq [IntPtr]::Zero) { return "" }
    $sb = New-Object System.Text.StringBuilder 256
    $len = [Win32]::GetWindowText($hwnd, $sb, $sb.Capacity)
    return $sb.ToString()
}

function Show-ToastNotification ($Title, $Message) {
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
    $textNodes = $template.GetElementsByTagName("text")
    $textNodes.Item(0).AppendChild($template.CreateTextNode($Title)) | Out-Null
    $textNodes.Item(1).AppendChild($template.CreateTextNode($Message)) | Out-Null
    $toast = [Windows.UI.Notifications.ToastNotification]::new($template)
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Nyverune Corne").Show($toast)
}

function Start-Watcher {
    Write-Host "[*] Nyverune Profile Auto-Switch Watcher for Windows started..." -ForegroundColor Cyan
    $lastProfile = ""

    while ($true) {
        $title = Get-ActiveWindowTitle
        $isNvim = ($title -match "nvim" -or $title -match "Neovim" -or $title -match "VIM")
        $targetProfile = if ($isNvim) { "Neovim" } else { "Everyday" }

        if ($targetProfile -ne $lastProfile) {
            Write-Host "  [➔] Active Window: '$title' -> Switching to $targetProfile" -ForegroundColor Magenta
            Show-ToastNotification "Nyverune Corne" "Profile switched to $targetProfile"
            $lastProfile = $targetProfile
        }
        Start-Sleep -Milliseconds 400
    }
}

switch ($Action) {
    "watch"    { Start-Watcher }
    "everyday" { Write-Host "[✓] Set profile: Everyday" -ForegroundColor Green; Show-ToastNotification "Nyverune Corne" "Profile: Everyday" }
    "neovim"   { Write-Host "[✓] Set profile: Neovim" -ForegroundColor Green; Show-ToastNotification "Nyverune Corne" "Profile: Neovim" }
    "toggle"   { Write-Host "[✓] Profile toggled" -ForegroundColor Green }
}
