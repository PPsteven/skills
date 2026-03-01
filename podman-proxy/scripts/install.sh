#!/bin/bash

# Installation script for podman-proxy skill
# This script installs the podman-proxy tools to /usr/local/bin

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${BIN_DIR:-/usr/local/bin}"

echo "Installing podman-proxy to $BIN_DIR..."

# Copy scripts
cp "$SKILL_DIR/podman-proxy-set" "$BIN_DIR/podman-proxy-set"
cp "$SKILL_DIR/podman-proxy-check" "$BIN_DIR/podman-proxy-check"

# Make executable
chmod +x "$BIN_DIR/podman-proxy-set"
chmod +x "$BIN_DIR/podman-proxy-check"

echo "✓ Installed podman-proxy-set"
echo "✓ Installed podman-proxy-check"
echo ""
echo "Quick start:"
echo "  podman-proxy-set 1088       # Set proxy to port 1088"
echo "  podman-proxy-check          # View current configuration"
echo ""
echo "Add to ~/.zshrc for convenience:"
echo "  alias pproxy='podman-proxy-set'"
