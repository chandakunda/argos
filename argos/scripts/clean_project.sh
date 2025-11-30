#!/bin/bash
set -e

echo "🧹 Cleaning Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + || true
find . -type f -name "*.pyc" -delete || true

echo "🧹 Cleaning test SQLite databases..."
find . -maxdepth 1 -type f -name "test_*.db" -delete || true

echo "✅ Project cleanup complete."
