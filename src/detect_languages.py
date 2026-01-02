#!/usr/bin/env python3
# file: src/detect_languages.py
# version: 1.0.1
# guid: 6f7a8b9c-0d1e-2f3a-4b5c-6d7e8f9a0b1c

"""Detect project languages and technologies"""

import json
import os
from pathlib import Path


def write_output(name, value):
    """Write to GITHUB_OUTPUT."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"{name}={value}\n")


def write_summary(text):
    """Write to GITHUB_STEP_SUMMARY."""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write(text + "\n")


def normalize_override(value):
    value = str(value).lower()
    return value if value in ("true", "false") else "auto"


def main():
    skip_detection = os.environ.get("SKIP_DETECTION", "false").lower() == "true"

    overrides = {
        "go": normalize_override(os.environ.get("GO_ENABLED", "auto")),
        "python": normalize_override(os.environ.get("PYTHON_ENABLED", "auto")),
        "rust": normalize_override(os.environ.get("RUST_ENABLED", "auto")),
        "frontend": normalize_override(os.environ.get("FRONTEND_ENABLED", "auto")),
        "docker": normalize_override(os.environ.get("DOCKER_ENABLED", "auto")),
        "protobuf": normalize_override(os.environ.get("PROTOBUF_ENABLED", "auto")),
    }

    # Detect languages
    if skip_detection:
        has_go = overrides["go"] == "true"
        has_python = overrides["python"] == "true"
        has_rust = overrides["rust"] == "true"
        has_frontend = overrides["frontend"] == "true"
        has_docker = overrides["docker"] == "true"
        protobuf_needed = overrides["protobuf"] == "true"
    else:
        # File-based detection
        has_go = Path("go.mod").exists() or Path("main.go").exists() or Path("cmd").exists()
        has_python = any(
            Path(p).exists() for p in ["setup.py", "pyproject.toml", "requirements.txt"]
        )
        has_rust = Path("Cargo.toml").exists()
        has_frontend = Path("package.json").exists()
        has_docker = Path("Dockerfile").exists() or Path("docker-compose.yml").exists()
        protobuf_needed = any(Path(".").rglob("*.proto"))

        # Apply overrides
        if overrides["go"] != "auto":
            has_go = overrides["go"] == "true"
        if overrides["python"] != "auto":
            has_python = overrides["python"] == "true"
        if overrides["rust"] != "auto":
            has_rust = overrides["rust"] == "true"
        if overrides["frontend"] != "auto":
            has_frontend = overrides["frontend"] == "true"
        if overrides["docker"] != "auto":
            has_docker = overrides["docker"] == "true"
        if overrides["protobuf"] != "auto":
            protobuf_needed = overrides["protobuf"] == "true"

    # Determine primary language
    if has_go:
        primary = "go"
    elif has_python:
        primary = "python"
    elif has_rust:
        primary = "rust"
    elif has_frontend:
        primary = "frontend"
    elif has_docker:
        primary = "docker"
    else:
        primary = "unknown"

    # Generate basic matrices
    go_matrix = {"os": ["ubuntu-latest"], "go-version": ["1.23"]} if has_go else {}
    python_matrix = {"os": ["ubuntu-latest"], "python-version": ["3.12"]} if has_python else {}
    rust_matrix = {"os": ["ubuntu-latest"], "rust-version": ["1.75"]} if has_rust else {}
    frontend_matrix = {"os": ["ubuntu-latest"], "node-version": ["22"]} if has_frontend else {}
    docker_matrix = {"platform": ["linux/amd64"]} if has_docker else {}

    # Write outputs
    write_output("has-go", "true" if has_go else "false")
    write_output("has-python", "true" if has_python else "false")
    write_output("has-rust", "true" if has_rust else "false")
    write_output("has-frontend", "true" if has_frontend else "false")
    write_output("has-docker", "true" if has_docker else "false")
    write_output("protobuf-needed", "true" if protobuf_needed else "false")
    write_output("primary-language", primary)
    write_output("go-matrix", json.dumps(go_matrix, separators=(",", ":")))
    write_output("python-matrix", json.dumps(python_matrix, separators=(",", ":")))
    write_output("rust-matrix", json.dumps(rust_matrix, separators=(",", ":")))
    write_output("frontend-matrix", json.dumps(frontend_matrix, separators=(",", ":")))
    write_output("docker-matrix", json.dumps(docker_matrix, separators=(",", ":")))

    # Summary
    languages = [
        ("Go", has_go),
        ("Python", has_python),
        ("Rust", has_rust),
        ("Frontend", has_frontend),
        ("Docker", has_docker),
        ("Protobuf", protobuf_needed),
    ]
    write_summary("## 🔍 Detected Languages")
    for lang, detected in languages:
        icon = "✅" if detected else "❌"
        write_summary(f"- {icon} **{lang}**")
    write_summary(f"\n**Primary language:** `{primary}`")

    print("✅ Language detection complete")


if __name__ == "__main__":
    main()
