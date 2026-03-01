---
name: podman-proxy
description: Flexible SOCKS5 proxy management for Podman on macOS. Quickly switch proxy ports without manual configuration. Perfect for pulling images through different proxy services.
allowed-tools: Bash(podman-proxy-set), Bash(podman-proxy-check), Bash(podman machine ssh)
---

# Podman Proxy Management

Easily manage SOCKS5 proxy settings for Podman on macOS. Switch between different proxy ports with a single command.

## Quick Start

```bash
# Set proxy to port 1088
podman-proxy-set 1088

# Set proxy from environment variable
export PROXY_PORT=8080
podman-proxy-set

# Check current proxy configuration
podman-proxy-check
```

## Installation

To install the scripts from this skill:

```bash
bash scripts/install.sh
```

The scripts will be installed at:
- `/usr/local/bin/podman-proxy-set` - Set/change proxy port
- `/usr/local/bin/podman-proxy-check` - View current configuration

Add to your shell profile (`~/.zshrc` or `~/.bashrc`) for convenience:

```bash
alias pproxy='podman-proxy-set'
```

Then reload:
```bash
source ~/.zshrc
```

## Essential Commands

### Set Proxy Port

```bash
# Explicit port
podman-proxy-set 1088       # SOCKS5 at port 1088
podman-proxy-set 8080       # SOCKS5 at port 8080
podman-proxy-set 1086       # SOCKS5 at port 1086

# From environment variable (useful for scripts)
export PROXY_PORT=1090
podman-proxy-set            # Uses $PROXY_PORT
```

### Check Configuration

```bash
# View current proxy settings
podman-proxy-check

# Example output:
# [engine]
# http_proxy = "socks5h://host.containers.internal:1088"
# https_proxy = "socks5h://host.containers.internal:1088"
```

### With Alias

```bash
# After adding 'pproxy' alias to ~/.zshrc
pproxy 1088                 # Set to 1088
pproxy 8080                 # Set to 8080
pproxy                      # Use $PROXY_PORT
```

## How It Works

### The Problem

Podman on macOS runs inside a virtual machine. Local proxy configurations don't automatically transfer to the VM, causing Docker registry access to fail.

### The Solution

This skill:
1. Configures proxy inside the Podman VM via `podman machine ssh`
2. Uses `host.containers.internal` to reach the host machine's proxy
3. Restarts the Podman daemon to apply changes
4. Supports environment variables for flexible scripting

### Architecture

```
Your Computer (macOS)
    ↓
SOCKS5 Proxy (localhost:1088)
    ↓
Podman VM
    ├─ ~/.config/containers/containers.conf
    └─ Podman daemon (restarted after config change)
```

## Common Workflows

### Quick Image Pulls with Different Proxies

```bash
# Switch to fast proxy, pull large image
podman-proxy-set 1088
podman pull myregistry/large-image:v1

# Switch to backup proxy for another pull
podman-proxy-set 1090
podman pull another-registry/image:latest
```

### CI/CD with Environment Variables

```bash
#!/bin/bash
# script.sh - automatically use different proxy for different environments

export PROXY_PORT=${CI_PROXY_PORT:-1088}
podman-proxy-set

podman pull myimage:latest
podman run myimage:latest
```

### Batch Operations

```bash
# Pull multiple images with a specific proxy
export PROXY_PORT=1088
podman-proxy-set

podman pull alpine:latest
podman pull nginx:latest
podman pull postgres:latest
```

## Troubleshooting

### Check if Proxy is Accessible

```bash
# From macOS host
nc -zv localhost 1088           # Should succeed
all_proxy=socks5h://localhost:1088 curl -I https://google.com
```

### Verify Configuration in VM

```bash
# SSH into the VM to debug
podman machine ssh
cat ~/.config/containers/containers.conf
sudo systemctl status podman
```

### Manual Reset

```bash
# Manually configure if script fails
podman machine ssh
mkdir -p ~/.config/containers
cat > ~/.config/containers/containers.conf << 'EOF'
[engine]
http_proxy = "socks5h://host.containers.internal:1088"
https_proxy = "socks5h://host.containers.internal:1088"
EOF
sudo systemctl restart podman
exit
```

## Key Technical Details

### SOCKS5h Protocol

- `socks5h://` - The 'h' means hostname resolution happens on the SOCKS5 server
- Better for Docker registry access than regular `socks5://`

### host.containers.internal

- Special DNS name that resolves to the host machine from inside the VM
- Used instead of `localhost:1088` (which would point inside the VM)

### Configuration Persistence

- Configuration lives in `/root/.config/containers/containers.conf` inside the VM
- Survives VM restarts
- Can be manually edited if needed

### Daemon Restart

- Script automatically restarts `podman` daemon after config changes
- Takes ~2-3 seconds
- Required for new proxy settings to take effect

## Limitations

- Only works on macOS with Podman running in a virtual machine
- Requires the SOCKS5 proxy to be running on localhost
- Linux/WSL users can use environment variables directly: `export http_proxy=socks5h://localhost:1088`

## Integration with Other Tools

### With Podman Compose

```bash
podman-proxy-set 1088
podman compose pull
podman compose up
```

### With Kubernetes (via Podman)

```bash
export PROXY_PORT=1088
podman-proxy-set
# k8s operations will now use the configured proxy
```

## Advanced: Creating Custom Port Profiles

Create your own wrapper script for quick switching:

```bash
# ~/.local/bin/pproxy-main
#!/bin/bash
podman-proxy-set 1088

# ~/.local/bin/pproxy-backup
#!/bin/bash
podman-proxy-set 1090

# Now use:
# pproxy-main    # Quick switch to main proxy
# pproxy-backup  # Quick switch to backup proxy
```
