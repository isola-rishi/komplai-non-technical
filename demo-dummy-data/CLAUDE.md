# Python Project Management with uv

## Overview
This project uses `uv` as the Python package manager and project runner. `uv` is a fast, Rust-based tool that replaces pip, pip-tools, virtualenv, and other Python tooling with a single, unified interface.

## Core Principles

1. **Always use uv**: Never use `pip`, `python -m venv`, or `virtualenv` directly
2. **Project-based workflow**: Work within the project context using `uv run` and `uv sync`
3. **Lockfile integrity**: The `uv.lock` file is the source of truth for exact dependencies

## Installation & Setup

If uv is not installed, install it with:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For project initialization:
```bash
# Initialize new project
uv init

# Or work with existing project (if pyproject.toml exists)
uv sync
```

## Common Commands

### Package Management

```bash
# Add a dependency
uv add <package>

# Add a development dependency
uv add --dev <package>

# Add specific version
uv add "package>=1.0.0,<2.0.0"

# Remove a dependency
uv remove <package>

# Update all dependencies
uv lock --upgrade

# Update specific package
uv lock --upgrade-package <package>

# Sync environment with lockfile
uv sync
```

### Running Code

```bash
# Run Python script
uv run python script.py

# Run Python module
uv run python -m module_name

# Run script with arguments
uv run python script.py --arg value

# Execute command in project environment
uv run <command>
```

### Environment Management

```bash
# Show project environment info
uv venv --help

# Manually create virtual environment (rarely needed)
uv venv

# Remove virtual environment
rm -rf .venv
```

### Inspecting Dependencies

```bash
# Show installed packages
uv pip list

# Show dependency tree
uv tree

# Show outdated packages
uv pip list --outdated
```

## Project Structure

Expected structure when using uv:
```
project/
├── pyproject.toml      # Project configuration and dependencies
├── uv.lock             # Locked dependency versions
├── .venv/              # Virtual environment (auto-created)
├── src/                # Source code
└── tests/              # Test files
```

## Workflow Guidelines

### Starting Work on Project

```bash
# 1. Ensure dependencies are synced
uv sync

# 2. Run your code
uv run python src/main.py
```

### Adding New Dependencies

```bash
# 1. Add the package
uv add package-name

# 2. Verify it's in pyproject.toml and uv.lock
cat pyproject.toml
```

### Updating Dependencies

```bash
# Update all packages
uv lock --upgrade
uv sync

# Update specific package
uv lock --upgrade-package requests
uv sync
```

### Running Tests

```bash
# Add pytest as dev dependency (if not present)
uv add --dev pytest

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src tests/
```

## Best Practices

1. **Always commit uv.lock**: This ensures reproducible builds
2. **Use `uv run` for all Python execution**: Ensures correct environment activation
3. **Sync before running**: Run `uv sync` after pulling changes or switching branches
4. **Group related additions**: Add multiple packages in one command when they're related
5. **Specify version constraints thoughtfully**: Use appropriate version specifiers (^, >=, ~=)

## Common Issues & Solutions

### "Command not found: uv"
```bash
# Install or reinstall uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH if needed
export PATH="$HOME/.cargo/bin:$PATH"
```

### "Lockfile is out of sync"
```bash
# Regenerate lockfile
uv lock
uv sync
```

### "Package not found in environment"
```bash
# Ensure package is in pyproject.toml
cat pyproject.toml

# Sync environment
uv sync
```

### Slow package installation
```bash
# uv is already fast, but you can clear cache if needed
rm -rf ~/.cache/uv
```

## Migration from pip/poetry

If migrating from existing tools:

**From pip + requirements.txt:**
```bash
# Convert requirements to pyproject.toml
uv init
uv add $(cat requirements.txt | grep -v "^#" | xargs)
```

**From poetry:**
```bash
# uv can read poetry's pyproject.toml directly
uv sync
```

## Python Version Management

```bash
# Specify Python version in pyproject.toml
# [project]
# requires-python = ">=3.11"

# uv will use the specified version or fail clearly
uv sync
```

## Advanced Usage

### Running Scripts with Inline Dependencies

```bash
# Create script with dependencies declared inline
uv run --with requests python script.py
```

### Working with Multiple Projects

```bash
# Each project maintains its own .venv and uv.lock
cd project1 && uv sync && uv run python main.py
cd project2 && uv sync && uv run python main.py
```

### CI/CD Integration

```yaml
# Example GitHub Actions workflow
steps:
  - uses: actions/checkout@v4
  - name: Set up uv
    run: curl -LsSf https://astral.sh/uv/install.sh | sh
  - name: Install dependencies
    run: uv sync
  - name: Run tests
    run: uv run pytest
```

## Quick Reference

| Task | Command |
|------|---------|
| Install package | `uv add package` |
| Install dev package | `uv add --dev package` |
| Remove package | `uv remove package` |
| Update all | `uv lock --upgrade && uv sync` |
| Run script | `uv run python script.py` |
| Run tests | `uv run pytest` |
| Sync environment | `uv sync` |
| List packages | `uv pip list` |
| Show tree | `uv tree` |

## When to Use What

- **`uv add`**: Adding new dependencies to project
- **`uv sync`**: Installing/updating dependencies from lockfile
- **`uv run`**: Executing any command in project environment
- **`uv lock`**: Regenerating lockfile (usually with --upgrade)
- **`uv pip`**: Low-level pip operations (rarely needed)

## Running the Komplai Demo Pipeline

This project includes a main data generation pipeline that creates invoices, bills, bank transactions, and PDFs.

### Quick Start

```bash
# Run the pipeline (recommended)
./run_pipeline.sh
```

The helper script automatically sets up the correct environment for PDF generation on macOS.

### Alternative Methods

```bash
# Run with uv directly (requires environment setup on macOS)
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
uv run python main_pipeline.py

# Or run the main pipeline file directly
uv run python main_pipeline.py
```

### What the Pipeline Does

1. Loads existing data from Excel and Google Sheets
2. Generates 2 new invoices per week
3. Generates 4 new bills per week
4. Generates corresponding bank transactions
5. Saves all data to Excel and syncs to Google Sheets
6. Creates PDF documents for invoices and bills

### Requirements

- **GTK Libraries** (for PDF generation on macOS): Installed via Homebrew
  - pango, cairo, gdk-pixbuf, glib, harfbuzz, gobject-introspection
  - Already configured if using `./run_pipeline.sh`

- **Google Sheets Access**: Requires service account credentials
  - File: `dummy-data-483609-2b5f128b43ad.json`
  - Configured in `config.yaml`

- **Excel File**: `Komplai_Demo_Master (Claude).xlsx`

### Pipeline Output

- **Excel**: Updates local Excel file with new data
- **Google Sheets**: Syncs data to cloud spreadsheet
- **PDFs**: Generated in `./output/pdfs/` directory
  - Invoice PDFs: `INV-YYYYMM-NNNN.pdf`
  - Bill PDFs: `BILL-YYYYMM-NNNN.pdf`

### Troubleshooting

**PDF Generation Fails on macOS:**
```bash
# Ensure GTK libraries are installed
brew install pango cairo gdk-pixbuf glib harfbuzz gobject-introspection

# Use the helper script which sets DYLD_LIBRARY_PATH
./run_pipeline.sh
```

**Google Sheets Sync Fails:**
- Check that credentials file exists
- Verify Sheet ID in `config.yaml`
- Ensure service account has access to the spreadsheet

**Missing Dependencies:**
```bash
# Sync all project dependencies
uv sync
```

## Resources

- Official docs: https://docs.astral.sh/uv/
- GitHub: https://github.com/astral-sh/uv
- Migration guide: https://docs.astral.sh/uv/guides/migration/

---

**Remember**: uv replaces pip, virtualenv, poetry, and related tools. When in doubt, use `uv run` to execute commands and `uv sync` to ensure your environment matches the lockfile.
