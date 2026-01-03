<!-- file: CHANGELOG.md -->
<!-- version: 1.0.0 -->
<!-- guid: 74cde51a-856c-4019-b712-98c31ca2340f -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Dockerized execution path controlled by `use-docker`/`docker-image`
- Automated GHCR publish workflow with digest pinning and tag bump

### Changed

- Updated composite action outputs to work across host and docker paths

### Fixed

- Prevented future additions of build artifacts from docker publishing

### Security

- Container base pinned by digest for reproducible builds

## [1.0.0] - 2026-01-02

### Added

- Initial implementation of action functionality
- Core workflow integration
- Documentation and usage examples

---

_Format: [version] - YYYY-MM-DD_
