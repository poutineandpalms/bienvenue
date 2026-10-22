$ErrorActionPreference = 'Stop'
$env:PATH = "C:\Users\maple\tools\node-v24.21.0-win-x64;" + $env:PATH
Set-Location C:\Users\maple\tizen-homebrew\bienvenue-stg
# Clean stale packages BEFORE building: tizenjs packs the whole staging dir,
# so a leftover bienvenue.wgt gets nested inside the next build and the push
# to the TV times out (bit us Oct 5 2026 at ~54 MB, and again Oct 20 at ~50 MB).
Remove-Item *.wgt -ErrorAction SilentlyContinue
$pw = (Get-Content C:\Users\maple\.tizen-certs\author.pw -Raw).Trim()
& ..\node_modules\.bin\tizenjs.cmd build --type wgt -o bienvenue.wgt --author C:\Users\maple\.tizen-certs\author.p12 --distributor C:\Users\maple\.tizen-certs\distributor.p12 --authorPwd $pw --distributorPwd $pw .
if ($LASTEXITCODE -ne 0) { throw "build failed: $LASTEXITCODE" }
Set-Location C:\Users\maple\tizen-homebrew
node install-bienvenue.js
if ($LASTEXITCODE -ne 0) { throw "install failed: $LASTEXITCODE" }
Write-Output "DEPLOY_DONE"
