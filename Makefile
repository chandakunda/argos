# -------------------------
# Argos – Makefile
# -------------------------

VENV = venv/bin/activate

# -------------------------
# Setup
# -------------------------

install:
	python3 -m venv venv
	. $(VENV) && pip install -r requirements.txt

# -------------------------
# Run API
# -------------------------

run:
	bash scripts/run_api.sh

# -------------------------
# Database Operations
# -------------------------

reset-db:
	bash scripts/reset_db.sh

demo-data:
	bash scripts/run_demo_data.sh

# -------------------------
# Tests
# -------------------------

test:
	pytest -q

test-full:
	pytest -vv

# -------------------------
# Cleanup
# -------------------------

clean:
	bash scripts/clean_project.sh

# -------------------------
# Lint (optional)
# -------------------------

lint:
	. $(VENV) && pylint common services api || true

# -------------------------
# Packaging
# -------------------------

install:
	pip install .

reinstall:
	pip uninstall -y argos-academic-system || true
	pip install .
