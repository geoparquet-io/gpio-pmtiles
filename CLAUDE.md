# GPIO-PMTiles Development Guide

> **Project**: PMTiles generation plugin for geoparquet-io
> **Purpose**: Convert GeoParquet files to PMTiles format using tippecanoe
> **Architecture**: CLI plugin with subprocess pipeline coordination

---

## Quick Start

```bash
# Setup
uv sync --all-extras

# Test workflow (run before ANY code changes)
uv run pytest -v

# Verify plugin registration
uv run python -c "import importlib.metadata; print(list(importlib.metadata.entry_points().select(group='gpio.plugins')))"

# Manual testing
uv run gpio pmtiles create test.parquet test.pmtiles --verbose
```

---

## Core Principles

### 1. Research First, Code Second

**ALWAYS start with research before writing code:**

```bash
# Understand before changing
rg "pattern" --type py
ls -R gpio_pmtiles/ tests/
git log --oneline -- <file>
```

**Ask questions first:**
- What does this code do?
- Why was it written this way?
- What are the edge cases?
- What tests cover this?

**Never assume. Always verify.**

### 2. Test-Driven Development (TDD)

**Red-Green-Refactor cycle is MANDATORY:**

```bash
# 1. RED - Write failing test first
uv run pytest tests/test_pmtiles.py::test_new_feature -v
# Should fail

# 2. GREEN - Write minimal code to pass
# Edit gpio_pmtiles/*.py

# 3. REFACTOR - Clean up while keeping tests green
uv run pytest -v
```

**Test markers:**
```python
@pytest.mark.slow  # For tests >1 second
```

**Run subsets:**
```bash
pytest -v -m "not slow"     # Fast tests only
pytest -v -k "test_create"  # Name matching
```

### 3. Git Workflow

**Branch naming:**
```bash
feature/add-zoom-validation
fix/path-injection-security
refactor/simplify-pipeline
docs/update-readme
```

**Commit message format:**
```
Add zoom level validation for tippecanoe commands

- Validate min_zoom <= max_zoom before subprocess call
- Add specific error messages for invalid ranges
- Prevent tippecanoe errors by catching issues early

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Rules:**
- Imperative mood (Add, Fix, Update, not Added, Fixed, Updated)
- Start with capital letter
- First line < 72 chars
- Body explains WHY, not WHAT (code shows what)
- Reference issues: `Fixes #123`

**Pre-commit hooks:**
```bash
# Install hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Manual run
pre-commit run --all-files
```

---

## Code Quality Standards

### Complexity Limits

**Cyclomatic complexity must stay low:**
```bash
# Check complexity (enforced in CI)
uv run xenon --max-absolute=E --max-modules=D --max-average=C gpio_pmtiles tests

# Find dead code
uv run vulture gpio_pmtiles tests
```

**If complexity increases:**
1. Stop and refactor immediately
2. Extract functions with single responsibilities
3. Simplify conditional logic
4. Add tests for extracted functions

**Target metrics:**
- Functions: < 10 complexity (E rating)
- Modules: < 25 complexity (D rating)
- Average: < 15 complexity (C rating)

### Code Style

**Formatting and linting:**
```bash
# Format (auto-fix)
uv run ruff format .

# Lint (auto-fix when possible)
uv run ruff check --fix .

# Check without fixing
uv run ruff check .
```

**Ruff configuration** (pyproject.toml):
- Line length: 100 characters
- Python 3.10+ syntax
- Import sorting with isort
- Selected rules: E, W, F, I, B, C4, UP

### Security

**Path validation is critical:**
```python
# ALWAYS validate paths before subprocess calls
_validate_path(input_path)
_validate_path(output_path)

# Prevent shell injection
# Use list form subprocess calls, NOT string commands
subprocess.Popen([cmd, arg1, arg2], ...)  # GOOD
subprocess.Popen(f"{cmd} {arg1} {arg2}", shell=True, ...)  # BAD
```

**Subprocess safety checklist:**
- [ ] Paths validated with `_validate_path()`
- [ ] Commands use list form, not strings
- [ ] No `shell=True` unless absolutely necessary
- [ ] User input sanitized before passing to subprocess

---

## Architecture

### Project Structure

```
gpio_pmtiles/
  ├── __init__.py         # Package exports
  ├── cli.py              # Click command definitions
  └── core.py             # Subprocess pipeline logic

tests/
  ├── conftest.py         # Pytest fixtures
  └── test_pmtiles.py     # Integration tests
```

### Pipeline Architecture

**gpio-pmtiles orchestrates a subprocess pipeline:**

```
GeoParquet → [gpio reproject] → [gpio extract] → [gpio convert geojson] → [tippecanoe] → PMTiles
              (optional)          (optional)       (streaming)            (subprocess)
```

**Key functions:**
- `_build_gpio_commands()`: Constructs pipeline stages based on options
- `_build_tippecanoe_command()`: Configures tippecanoe with quality settings
- `_run_pipeline()`: Manages subprocess communication and error handling

**Design principles:**
1. **Streaming**: GeoJSON flows through pipes, never materialized to disk
2. **Fail-fast**: Validate early, before spawning subprocesses
3. **Clean errors**: Surface helpful messages for common issues (tippecanoe missing, bad paths)

### Plugin System

**Entry point registration** (pyproject.toml):
```toml
[project.entry-points."gpio.plugins"]
pmtiles = "gpio_pmtiles.cli:pmtiles"
```

This makes `gpio pmtiles` available when both `geoparquet-io` and `gpio-pmtiles` are installed.

---

## Testing Strategy

### Test Categories

**1. Unit tests** - Test individual functions:
```python
def test_validate_path_rejects_shell_chars():
    with pytest.raises(ValueError):
        _validate_path("file; rm -rf /")
```

**2. Integration tests** - Test full pipeline:
```python
def test_create_pmtiles_basic(tmp_path, sample_parquet):
    output = tmp_path / "output.pmtiles"
    create_pmtiles_from_geoparquet(sample_parquet, str(output))
    assert output.exists()
```

**3. Error handling tests**:
```python
def test_tippecanoe_missing(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda x: None)
    with pytest.raises(TippecanoeNotFoundError):
        create_pmtiles_from_geoparquet("in.parquet", "out.pmtiles")
```

### Test Data

**Use fixtures** (tests/conftest.py):
```python
@pytest.fixture
def sample_parquet(tmp_path):
    # Create minimal test data
    return tmp_path / "test.parquet"
```

**Principles:**
- Fixtures for reusable test data
- `tmp_path` for temporary files (auto-cleaned)
- Small datasets (fast tests)
- Mark slow tests with `@pytest.mark.slow`

---

## Distill MCP Usage

**Use Distill to optimize token usage for large outputs:**

### When to use Distill

**✅ Use Distill for:**
- Reading long test output
- Analyzing verbose build logs
- Checking tippecanoe error messages
- Reviewing git diffs with large files

**❌ Don't use Distill for:**
- Source code reading (use Read tool)
- Short command outputs
- Interactive work requiring full context

### Distill Examples

```bash
# Compress verbose test output
distill auto_optimize "$(pytest -v 2>&1)"

# Read code structure without full content
distill smart_file_read --skeleton gpio_pmtiles/core.py

# Optimize git diff
distill auto_optimize "$(git diff)"
```

### Distill Session Stats

Check token savings:
```bash
distill session_stats
```

---

## Claude Hooks (Hookify)

**Use hooks to prevent anti-patterns:**

### Example Hooks

**1. Prevent skipping tests:**
```yaml
# .claude-hooks/no-skip-tests.yaml
trigger: "pytest.*-m.*not.*slow"
action: remind
message: "Are you skipping tests to save time? Run full suite before committing."
```

**2. Require path validation:**
```yaml
# .claude-hooks/validate-subprocess-paths.yaml
trigger: "subprocess\\.(Popen|run).*input_path"
action: block
message: "MUST call _validate_path() before subprocess with user input"
exception_pattern: "_validate_path\\(.*\\).*subprocess"
```

**3. Enforce TDD:**
```yaml
# .claude-hooks/test-first.yaml
trigger: "def (test_|[^_].*\\(.*\\):)"
action: remind
message: "TDD reminder: Write test first (RED), then implementation (GREEN), then refactor."
```

### Managing Hooks

```bash
# List hooks
claude hooks list

# Enable/disable
claude hooks enable no-skip-tests
claude hooks disable test-first

# Test a hook
claude hooks test validate-subprocess-paths "subprocess.Popen([cmd, input_path])"
```

---

## Common Tasks

### Adding a New CLI Option

**TDD workflow:**

1. **RED - Write test first:**
```python
def test_new_option(tmp_path, sample_parquet):
    output = tmp_path / "out.pmtiles"
    create_pmtiles_from_geoparquet(
        sample_parquet,
        str(output),
        new_option="value"
    )
    # Assert expected behavior
```

2. **GREEN - Add option to CLI:**
```python
# cli.py
@click.option("--new-option", help="Description")
def create(..., new_option):
    create_pmtiles_from_geoparquet(..., new_option=new_option)
```

3. **GREEN - Implement in core:**
```python
# core.py
def create_pmtiles_from_geoparquet(..., *, new_option=None):
    # Implement feature
```

4. **REFACTOR - Clean up, keep tests passing**

### Debugging Subprocess Issues

**Enable verbose mode:**
```bash
gpio pmtiles create input.parquet output.pmtiles --verbose
```

**Check intermediate output:**
```bash
# Test gpio pipeline stage
gpio convert geojson test.parquet | head -20

# Test with filters
gpio extract test.parquet --bbox "-122,37,-121,38" | gpio convert geojson - | head
```

**Inspect tippecanoe directly:**
```bash
# See what tippecanoe receives
gpio convert geojson test.parquet > test.geojson
tippecanoe -P -o test.pmtiles test.geojson --progress-interval=1
```

### Adding Error Handling

**Pattern:**
```python
# Validate early
if invalid_condition:
    raise ValueError("Specific error message with solution")

# Catch subprocess errors and add context
try:
    proc.communicate()
except subprocess.CalledProcessError as e:
    raise RuntimeError(
        f"Command failed: {' '.join(cmd)}\n"
        f"Exit code: {e.returncode}\n"
        f"Error: {e.stderr}"
    ) from e
```

---

## CI/CD

### GitHub Actions Workflows

**.github/workflows/tests.yml** - On push/PR:
- Matrix test: Python 3.10, 3.11, 3.12
- Install tippecanoe (system dependency)
- Verify plugin registration
- Run pytest
- Check formatting (ruff format)
- Lint (ruff check)

**.github/workflows/publish.yml** - On release:
- Run tests
- Check formatting/linting
- Check complexity (xenon) - informational only
- Check dead code (vulture) - informational only
- Build package (uv build)
- Publish to PyPI (trusted publishing with OIDC)

### Dependabot

**.github/dependabot.yml**:
- GitHub Actions: weekly updates
- Python (pip): weekly updates
- Groups minor/patch together to reduce PR noise

---

## Troubleshooting

### Test failures

**"tippecanoe not found"**
```bash
# Ubuntu/Debian
sudo apt-get install tippecanoe

# macOS
brew install tippecanoe

# CI: already installed in workflow
```

**"Plugin not registered"**
```bash
# Reinstall in editable mode
uv pip install -e .

# Verify
uv run python -c "import importlib.metadata; print(list(importlib.metadata.entry_points().select(group='gpio.plugins')))"
```

**"Subprocess pipeline failed"**
```bash
# Run with verbose to see commands
gpio pmtiles create input.parquet output.pmtiles --verbose

# Test each stage
gpio convert geojson input.parquet | head  # Should output GeoJSON
```

### Performance

**Large files taking too long?**
- Use `--bbox` to filter spatially
- Use `--where` to filter by attributes
- Use `--include-cols` to reduce property size
- Consider `--max-zoom` to limit tile generation

**Memory issues?**
- Pipeline streams data (shouldn't buffer)
- Check if tippecanoe is the bottleneck
- Use `--drop-densest-as-needed` (already default)

---

## Release Checklist

**Before releasing:**

1. **Tests pass**
   ```bash
   uv run pytest -v
   ```

2. **Linting clean**
   ```bash
   uv run ruff format --check .
   uv run ruff check .
   ```

3. **Complexity acceptable**
   ```bash
   uv run xenon --max-absolute=E --max-modules=D --max-average=C gpio_pmtiles tests
   ```

4. **Update CHANGELOG.md**
   - Document new features
   - Document breaking changes
   - Document bug fixes

5. **Version bump** (pyproject.toml)
   - Follow semver: MAJOR.MINOR.PATCH
   - Breaking change = MAJOR
   - New feature = MINOR
   - Bug fix = PATCH

6. **Tag and release**
   ```bash
   git tag -a v0.1.1 -m "Release v0.1.1"
   git push origin v0.1.1
   ```

7. **Create GitHub release**
   - GitHub Actions will auto-publish to PyPI
   - Release notes from CHANGELOG.md

---

## Resources

**Project links:**
- Repository: https://github.com/geoparquet/gpio-pmtiles
- Parent project: https://github.com/geoparquet/geoparquet-io
- Documentation: https://geoparquet.io/

**Dependencies:**
- geoparquet-io: https://github.com/geoparquet/geoparquet-io
- tippecanoe: https://github.com/felt/tippecanoe
- PMTiles spec: https://github.com/protomaps/PMTiles

**Tools:**
- uv: https://docs.astral.sh/uv/
- ruff: https://docs.astral.sh/ruff/
- pytest: https://docs.pytest.org/

---

## Philosophy

**1. Simplicity over cleverness**
- Readable code beats clever code
- Extract functions for clarity
- Name things clearly

**2. Fail fast with helpful errors**
- Validate early
- Surface specific errors
- Include solutions in error messages

**3. Test everything**
- Tests are documentation
- Tests enable refactoring
- Tests catch regressions

**4. Research before coding**
- Understand existing patterns
- Check git history for context
- Ask questions before changing

**5. Keep complexity low**
- Monitor with xenon
- Refactor when complexity creeps up
- Extract, don't expand

