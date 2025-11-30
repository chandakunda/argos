#!/usr/bin/env bash
set -e

echo "==========================================="
echo "   ARGOS — FULL PHASE 5 REBUILD SCRIPT"
echo "==========================================="

# 1. Fix Python path
echo "[1] Ensuring project root is in PYTHONPATH..."
export PYTHONPATH="$PWD:$PYTHONPATH"

# 2. Recreate proper namespace package layout
echo "[2] Recreating argos/argos_pkg directory structure..."

rm -rf argos/argos_pkg
mkdir -p argos/argos_pkg

# Move ONLY the actual package folders, not tests/docs/data/etc.
for pkg in api common services scripts ml verification; do
    if [ -d "$pkg" ]; then
        echo " - Moving $pkg → argos/argos_pkg/"
        mv "$pkg" argos/argos_pkg/
    fi
done

# Recreate __init__.py
find argos/argos_pkg -type d -exec touch "{}"/__init__.py \;

echo "Namespace layout:"
tree argos/argos_pkg || ls -R argos/argos_pkg

# 3. Rewrite pyproject.toml cleanly
echo "[3] Rewriting pyproject.toml..."

cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "argos_academic_system"
version = "1.0.0"
description = "Argos Academic Management System"
readme = "README.md"
requires-python = ">=3.10"

authors = [
    { name = "Francis Munganga", email = "francis@example.com" }
]

license = { text = "MIT" }

dependencies = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "httpx",
    "sqlite-utils"
]

[project.optional-dependencies]
dev = ["pytest", "faker"]

[tool.setuptools.packages.find]
where = ["argos"]
EOF

echo "[OK] pyproject.toml regenerated."

# 4. Clean old builds
echo "[4] Cleaning dist/ build/"
rm -rf dist build *.egg-info

# 5. Generate required README.md if missing
if [ ! -f README.md ]; then
    echo "[5] Creating README.md..."
    echo "# Argos Academic System" > README.md
fi

# 6. Build wheel + sdist
echo "[6] Building wheel..."
python -m build

echo "Build complete. Files in dist/:"
ls -l dist

# 7. Force reinstall package
echo "[7] Installing wheel..."
pip install dist/*.whl --force-reinstall

# 8. Verify import
echo "[8] Testing import..."

python3 - << 'EOF'
import argos_academic_system
print("✔ Top-level package OK")

from argos_pkg.api.app import create_app
print("✔ API import OK")

print(">>> All imports pass.")
EOF

# 9. Test API creation
echo "[9] Creating and testing FastAPI app instantiation..."

python3 - << 'EOF'
from argos_pkg.api.app import create_app
app = create_app()
print("✔ FastAPI app instantiated successfully")
EOF

# 10. Run optional demo-data test
echo "[10] Running demo loader check..."

python3 - << 'EOF'
try:
    from argos_pkg.scripts.load_demo_data import load
    print("✔ Demo data loader exists")
except Exception as e:
    print("⚠ Demo loader import failed:", e)
EOF

echo "==============================================="
echo "   ALL PHASE 5 TASKS COMPLETED SUCCESSFULLY"
echo "==============================================="
echo "You may now proceed to PHASE 6."
