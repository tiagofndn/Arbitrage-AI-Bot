#!/bin/bash
# Generate sample data for development and CI
set -e
cd "$(dirname "$0")/.."
ai-arb-lab generate-data --output data/sample --days 1 --seed 42
echo "Sample data generated in data/sample/"
