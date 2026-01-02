# Detect Languages Action

Automatically detect which languages and technologies are used in your
repository with intelligent overrides and fallback handling.

## Usage

```yaml
- name: Detect languages
  id: detect
  uses: jdfalk/detect-languages-action@v1
  with:
    skip-detection: false
    build-target: all

- name: Log detected languages
  run: |
    echo "Go: ${{ steps.detect.outputs.has-go }}"
    echo "Python: ${{ steps.detect.outputs.has-python }}"
    echo "Rust: ${{ steps.detect.outputs.has-rust }}"
    echo "Primary: ${{ steps.detect.outputs.primary-language }}"
```

## Inputs

| Input              | Description                                 | Default |
| ------------------ | ------------------------------------------- | ------- |
| `skip-detection`   | Skip file-based detection                   | `false` |
| `build-target`     | Build targets to validate (comma-separated) | `all`   |
| `go-enabled`       | Override Go detection (true/false/auto)     | `auto`  |
| `python-enabled`   | Override Python detection                   | `auto`  |
| `rust-enabled`     | Override Rust detection                     | `auto`  |
| `frontend-enabled` | Override Frontend detection                 | `auto`  |
| `docker-enabled`   | Override Docker detection                   | `auto`  |
| `protobuf-enabled` | Override Protobuf detection                 | `auto`  |

## Outputs

| Output             | Description                           |
| ------------------ | ------------------------------------- |
| `has-go`           | Whether Go is detected                |
| `has-python`       | Whether Python is detected            |
| `has-rust`         | Whether Rust is detected              |
| `has-frontend`     | Whether Frontend/Node.js is detected  |
| `has-docker`       | Whether Docker is detected            |
| `protobuf-needed`  | Whether Protobuf processing is needed |
| `primary-language` | Primary language of project           |
| `go-matrix`        | Basic Go CI matrix                    |
| `python-matrix`    | Basic Python CI matrix                |
| `rust-matrix`      | Basic Rust CI matrix                  |
| `frontend-matrix`  | Basic Frontend CI matrix              |
| `docker-matrix`    | Basic Docker CI matrix                |

## Detection Logic

### Automatic Detection

- **Go**: `go.mod`, `main.go`, `cmd/` directory
- **Python**: `setup.py`, `pyproject.toml`, `requirements.txt`
- **Rust**: `Cargo.toml`
- **Frontend**: `package.json`
- **Docker**: `Dockerfile`, `docker-compose.yml`
- **Protobuf**: Any `.proto` files

### Overrides

Use override inputs to force specific languages:

```yaml
with:
  go-enabled: 'true' # Force Go detected
  python-enabled: 'false' # Force Python not detected
  rust-enabled: 'auto' # Auto-detect Rust
```

## Features

✅ **File-Based Detection** - Inspects actual project files ✅ **Smart
Overrides** - Force languages on/off as needed ✅ **Primary Language** -
Identifies main project language ✅ **Matrix Generation** - Basic CI matrices
for each language ✅ **Protobuf Support** - Detects proto files for code
generation

## Related Actions

- [load-config-action](https://github.com/jdfalk/load-config-action) - Load
  repository config
- [ci-generate-matrices-action](https://github.com/jdfalk/ci-generate-matrices-action) -
  Generate test matrices
- [release-strategy-action](https://github.com/jdfalk/release-strategy-action) -
  Determine release strategy
