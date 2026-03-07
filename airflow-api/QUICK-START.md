# Airflow API Skill - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Set Environment Variables

**Option A: Username + Password (Recommended)**
```bash
export AIRFLOW_BASE_URL="http://tmp-airflow.momenta.works"
export AIRFLOW_USERNAME="admin"
export AIRFLOW_PASSWORD="your_password"
```

**Option B: Token**
```bash
export AIRFLOW_BASE_URL="http://tmp-airflow.momenta.works"
export AIRFLOW_TOKEN="your_token"
```

### Step 2: Run CLI Commands

```bash
# List all DAGs
python /Users/ppsteven/projects/skills/airflow-api/scripts/cli_tool.py dag list

# List connections
python /Users/ppsteven/projects/skills/airflow-api/scripts/cli_tool.py connection list

# List task instances
python /Users/ppsteven/projects/skills/airflow-api/scripts/cli_tool.py taskinstance list
```

## 📝 Available Commands

| Category | Commands |
|----------|----------|
| **Config** | `config list`, `config detail` |
| **Connection** | `connection list`, `connection detail` |
| **DAG** | `dag list`, `dag detail` |
| **DAGRun** | `dagrun list`, `dagrun detail` |
| **TaskInstance** | `taskinstance list`, `taskinstance detail` |
| **User** | `user list`, `user detail` |
| **Variable** | `variable list`, `variable detail` |
| **Pool** | `pool list`, `pool detail` |
| **Role** | `role list`, `role detail` |
| **And more...** | `dataset`, `eventlog`, `monitoring`, etc. |

## 🔑 Authentication Methods

### Method 1: Username + Password ✅ Recommended

```bash
export AIRFLOW_BASE_URL="http://tmp-airflow.momenta.works"
export AIRFLOW_USERNAME="admin"
export AIRFLOW_PASSWORD="securepassword"
```

Uses HTTP Basic Auth (standard, widely supported)

### Method 2: Bearer Token

```bash
export AIRFLOW_BASE_URL="http://tmp-airflow.momenta.works"
export AIRFLOW_TOKEN="ghp_xxxxxxxxxxxx"
```

Uses Bearer Token authentication

## 💾 Save Configuration

### Create `.airflow.env` file

```bash
cat > ~/.airflow.env << 'EOF'
export AIRFLOW_BASE_URL="http://tmp-airflow.momenta.works"
export AIRFLOW_USERNAME="admin"
export AIRFLOW_PASSWORD="your_password"
EOF

chmod 600 ~/.airflow.env
```

### Load configuration

```bash
source ~/.airflow.env

# Now run commands
python /Users/ppsteven/projects/skills/airflow-api/scripts/cli_tool.py dag list
```

## 🧪 Verify Setup

```bash
# Check environment variables are set
echo "Base URL: $AIRFLOW_BASE_URL"
echo "Username: $AIRFLOW_USERNAME"

# Test connection (should return DAG list)
python /Users/ppsteven/projects/skills/airflow-api/scripts/cli_tool.py dag list

# If successful, you'll see:
# ✅ Fetching DAG items (limit=10)...
```

## ❌ Troubleshooting

| Error | Solution |
|-------|----------|
| `401 Unauthorized` | Check username/password are correct |
| `Connection refused` | Verify AIRFLOW_BASE_URL is accessible |
| `ModuleNotFoundError: click` | Run `pip install click requests` |

## 📚 For More Details

- Full configuration: See `CONFIGURATION.md`
- API endpoints: See `references/api_endpoints.md`
- SKILL metadata: See `SKILL.md`

## 🔐 Security Tips

1. Never commit `.airflow.env` to git
2. Use `chmod 600` for env files
3. Change passwords regularly
4. Use environment-specific credentials

---

**Ready to use!** 🎉

Need help? Check `CONFIGURATION.md` for advanced setup.
