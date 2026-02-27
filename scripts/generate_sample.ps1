# Generate sample data for development and CI
Set-Location $PSScriptRoot\..
ai-arb-lab generate-data --output data/sample --days 1 --seed 42
Write-Host "Sample data generated in data/sample/"
