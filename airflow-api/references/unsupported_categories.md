# Unsupported API Categories

The following Airflow API categories are available but not currently wrapped in the CLI tool:

- Config
- DagStats
- DagWarning
- EventLog
- ImportError
- Monitoring
- Permission
- Plugin
- Pool
- Provider
- Role
- User
- XCom

## Rationale

These categories were not included to keep the initial skill focused on core operational needs (DAGs, tasks, variables, connections, datasets). 

## Future Expansion

To add support for these categories in a future version:

1. Edit `scripts/cli_tool.py` to add new Click command groups
2. Implement endpoint wrappers for each unsupported category
3. Update this documentation

## See Also

For complete Airflow API documentation, visit:
https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html
