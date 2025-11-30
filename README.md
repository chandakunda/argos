# Argos

Argos is a lightweight command-line toolkit starter that provides a simple, extensible foundation for future automation.

## Features
- Clean Python package layout using `src/` style imports.
- A friendly CLI (`argos`) with helpful `hello` and `info` commands.
- Ready-to-run Pytest suite to validate basic behavior.

## Quick start
1. Create and activate a Python 3.9+ virtual environment.
2. Install the package in editable mode:
   ```bash
   pip install -e .
   ```
3. Explore the CLI:
   ```bash
   argos hello
   argos hello --name "Ada"
   argos info
   ```
4. Run the tests:
   ```bash
   pytest
   ```

## CLI overview
- `argos hello` prints a friendly greeting, optionally addressing a provided name.
- `argos info` reports basic metadata about the Argos toolkit.

## Contributing
Feel free to open issues or submit pull requests as Argos evolves.
