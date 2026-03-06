# Unsupported Airflow API Categories

The following API categories are available in the Airflow API but not yet implemented in this skill.

## Categories Not Implemented

- **DagStats** (1 endpoints)
- **DagWarning** (1 endpoints)
- **Dataset** (11 endpoints)
- **EventLog** (2 endpoints)
- **ImportError** (2 endpoints)
- **Monitoring** (2 endpoints)
- **Permission** (1 endpoints)
- **Plugin** (1 endpoints)
- **Pool** (5 endpoints)
- **Provider** (1 endpoints)
- **User** (5 endpoints)
- **XCom** (2 endpoints)

## Future Implementation

To add support for these categories:

1. Review the endpoint documentation
2. Add category group to `scripts/cli_tool.py`
3. Implement commands for each endpoint
4. Update `SKILL.md` with new commands
5. Test with running Airflow instance

## Category Descriptions

- **Dataset**: Airflow Dataset management and triggering
- **DagStats**: Statistical information about DAG runs
- **DagWarning**: Warning messages and issues for DAGs
- **EventLog**: Audit log of events in Airflow
- **ImportError**: Python module import errors
- **Monitoring**: System health and metrics monitoring
- **Permission**: Fine-grained permission management
- **Plugin**: Installed plugins and plugins information
- **Pool**: Resource pool management for parallelization
- **Provider**: Installed provider packages
- **User**: User account management
- **XCom**: Cross-communication between tasks
