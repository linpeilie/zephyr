$dirs = @("connectivity", "contribute", "develop", "hardware", "kernel", "project", "releases", "services", "security", "safety")
foreach ($dir in $dirs) {
    $fullTrans = 0
    $partialTrans = 0
    Get-ChildItem "d:\Development\Workspace\zephyr\doc-zh\$dir" -Recurse -Filter "*.rst" -File -ErrorAction SilentlyContinue | ForEach-Object {
        $content = Get-Content $_ -Raw -ErrorAction SilentlyContinue
        $chCount = 0
        foreach ($char in $content.ToCharArray()) {
            $code = [int]$char
            if ($code -ge 0x4e00 -and $code -le 0x9fff) {
                $chCount++
            }
        }
        if ($chCount -gt 100) {
            $fullTrans++
        } elseif ($chCount -gt 0) {
            $partialTrans++
        }
    }
    $total = $fullTrans + $partialTrans
    if ($total -gt 0) {
        Write-Host "$dir : 完整=$fullTrans 部分=$partialTrans 总计=$total"
    }
}
