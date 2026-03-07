# Airflow API Skill - Configuration Guide

## Quick Setup

### Prerequisites

- Python 3.7+
- Required packages: `click`, `requests`

```bash
pip install click requests
```

## Authentication Configuration

### Method 1: Username + Password (HTTP Basic Auth) ✅ **Recommended**

**Environment Variables:**

```bash
export AIRFLOW_BASE_URL="http://tmp-airflow.momenta.works"
export AIRFLOW_USERNAME="your_username"
export AIRFLOW_PASSWORD="your_password"
```

**Example:**

```bash
export AIRFLOW_BASE_URL="http://tmp-airflow.momenta.works"
export AIRFLOW_USERNAME="admin"
export AIRFLOW_PASSWORD="securepassword"

python scripts/cli_tool.py dag list
```

### Method 2: Bearer Token

**Environment Variables:**

```bash
export AIRFLOW_BASE_URL="http://tmp-airflow.momenta.works"
export AIRFLOW_TOKEN="your_api_token"
```

**Example:**

```bash
export AIRFLOW_BASE_URL="http://tmp-airflow.momenta.works"
export AIRFLOW_TOKEN="ghp_xxxxxxxxxxxx"

python scripts/cli_tool.py dag list
```

## Complete Configuration Examples

### Local Airflow (Development)

```bash
export AIRFLOW_BASE_URL="http://localhost:8080"
export AIRFLOW_USERNAME="airflow"
export AIRFLOW_PASSWORD="airflow"
```

### Production Airflow Server

```bash
export AIRFLOW_BASE_URL="http://tmp-airflow.momenta.works"
export AIRFLOW_USERNAME="prod_user"
export AIRFLOW_PASSWORD="$(cat ~/.airflow_password)"  # Read from secure file
```

### Secure Password Management

**Option A: Use a password file (chmod 600)**

```bash
export AIRFLOW_PASSWORD="$(cat ~/.airflow_password)"
```

**Option B: Use environment variable file (.airflow.env)**

Create `~/.airflow.env`:
```
AIRFLOW_BASE_URL=http://tmp-airflow.momenta.works
AIRFLOW_USERNAME=admin
AIRFLOW_PASSWORD=your_secure_password
```

Then load it:
```bash
source ~/.airflow.env
python scripts/cli_tool.py dag list
```

## Verification

Test your configuration:

```bash
# List all DAGs
python scripts/cli_tool.py dag list

# Get DAG details
python scripts/cli_tool.py dag detail my_dag_id

# List connections
python scripts/cli_tool.py connection list

# List tasks
python scripts/cli_tool.py taskinstance list
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `401 Unauthorized` | Check AIRFLOW_USERNAME and AIRFLOW_PASSWORD are correct |
| `Connection refused` | Verify AIRFLOW_BASE_URL is correct and server is running |
| `No module named 'click'` | Run `pip install click requests` |
| `SSL Certificate Error` | Add `--insecure` flag or configure SSL properly |

## Environment Variable Reference

| Variable | Required | Default | Example |
|----------|----------|---------|---------|
| `AIRFLOW_BASE_URL` | Yes | `http://localhost:8080` | `http://tmp-airflow.momenta.works` |
| `AIRFLOW_USERNAME` | Conditional* | Empty | `admin` |
| `AIRFLOW_PASSWORD` | Conditional* | Empty | `password` |
| `AIRFLOW_TOKEN` | Conditional* | Empty | `ghp_xxxx...` |

*\* Either (USERNAME + PASSWORD) OR TOKEN must be provided*

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** for sensitive data
3. **Restrict file permissions** on credential files (chmod 600)
4. **Rotate tokens** regularly
5. **Use HTTPS** for production endpoints
6. **Consider using** a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)

## Advanced Configuration

### Using Python Script

```python
from scripts.cli_tool import AirflowAPI

# Create client with explicit credentials
api = AirflowAPI(
    base_url="http://tmp-airflow.momenta.works",
    username="admin",
    password="password"
)

# Make API requests
result = api.request('GET', '/api/v1/dags')
print(result)
```

### Switching Between Environments

```bash
# Create environment-specific configs
cat > ~/.airflow-dev.env << EOF
export AIRFLOW_BASE_URL="http://localhost:8080"
export AIRFLOW_USERNAME="dev_user"
export AIRFLOW_PASSWORD="dev_pass"
EOF

cat > ~/.airflow-prod.env << EOF
export AIRFLOW_BASE_URL="http://prod-airflow.momenta.works"
export AIRFLOW_USERNAME="prod_user"
export AIRFLOW_PASSWORD="prod_pass"
EOF

# Use them:
source ~/.airflow-dev.env && python scripts/cli_tool.py dag list
source ~/.airflow-prod.env && python scripts/cli_tool.py dag list
```
