# OpenAPI Schema Reference

This document explains the OpenAPI 3.0 and Swagger 2.0 specification structure relevant to the swagger2skill generator.

## OpenAPI 3.0 Structure

### Root Object

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "API Title",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://api.example.com"
    }
  ],
  "paths": { /* ... */ },
  "components": { /* ... */ }
}
```

### Paths Object

The `paths` object contains all API endpoints:

```json
{
  "paths": {
    "/users": {
      "get": {
        "tags": ["Users"],
        "summary": "List all users",
        "description": "Retrieve a list of all users",
        "operationId": "listUsers",
        "parameters": [
          {
            "name": "limit",
            "in": "query",
            "required": false,
            "schema": { "type": "integer" }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful response"
          }
        }
      }
    }
  }
}
```

### Key Fields

| Field | Purpose |
|-------|---------|
| `tags` | Category grouping (used for skill category organization) |
| `summary` | Brief endpoint description |
| `description` | Detailed endpoint documentation |
| `operationId` | Unique operation identifier |
| `parameters` | Request parameters (query, path, header, body) |
| `requestBody` | Request payload schema |
| `responses` | Possible response schemas |

## Tags (Categories)

Tags organize endpoints into logical groups. The swagger2skill generator uses tags as skill categories:

```json
{
  "paths": {
    "/dags": {
      "get": {
        "tags": ["DAG"],  // This becomes a category option
        "summary": "List DAGs"
      }
    },
    "/dags/{dag_id}": {
      "get": {
        "tags": ["DAG"],  // Same category
        "summary": "Get DAG details"
      }
    }
  }
}
```

## Parameter Types

### Query Parameters
```json
{
  "name": "limit",
  "in": "query",
  "schema": { "type": "integer", "default": 10 }
}
```

### Path Parameters
```json
{
  "name": "user_id",
  "in": "path",
  "required": true,
  "schema": { "type": "string" }
}
```

### Header Parameters
```json
{
  "name": "X-API-Key",
  "in": "header",
  "schema": { "type": "string" }
}
```

## Request Body

```json
{
  "requestBody": {
    "required": true,
    "content": {
      "application/json": {
        "schema": {
          "$ref": "#/components/schemas/User"
        }
      }
    }
  }
}
```

## Response Schemas

```json
{
  "responses": {
    "200": {
      "description": "Success",
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "id": { "type": "integer" },
              "name": { "type": "string" }
            }
          }
        }
      }
    },
    "404": {
      "description": "Not found"
    }
  }
}
```

## Swagger 2.0 Structure

Similar to OpenAPI 3.0 but with slight syntax differences:

```json
{
  "swagger": "2.0",
  "info": { "title": "...", "version": "1.0.0" },
  "basePath": "/api/v1",
  "paths": { /* ... */ },
  "definitions": { /* schemas */ }
}
```

Key differences:
- Uses `swagger` instead of `openapi`
- Uses `basePath` instead of `servers`
- Uses `definitions` instead of `components/schemas`
- Parameters are defined directly in paths

## Authentication

### Bearer Token (OpenAPI 3.0)
```json
{
  "components": {
    "securitySchemes": {
      "BearerAuth": {
        "type": "http",
        "scheme": "bearer"
      }
    }
  },
  "security": [
    { "BearerAuth": [] }
  ]
}
```

### API Key (OpenAPI 3.0)
```json
{
  "components": {
    "securitySchemes": {
      "ApiKeyAuth": {
        "type": "apiKey",
        "name": "X-API-Key",
        "in": "header"
      }
    }
  },
  "security": [
    { "ApiKeyAuth": [] }
  ]
}
```

## Example: Complete Simple API

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Task API",
    "version": "1.0.0"
  },
  "servers": [
    { "url": "https://api.example.com" }
  ],
  "paths": {
    "/tasks": {
      "get": {
        "tags": ["Task"],
        "summary": "List tasks",
        "operationId": "listTasks",
        "parameters": [
          {
            "name": "status",
            "in": "query",
            "schema": { "type": "string", "enum": ["pending", "completed"] }
          }
        ],
        "responses": {
          "200": {
            "description": "List of tasks"
          }
        }
      },
      "post": {
        "tags": ["Task"],
        "summary": "Create task",
        "operationId": "createTask",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "title": { "type": "string" },
                  "description": { "type": "string" }
                },
                "required": ["title"]
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Task created"
          }
        }
      }
    },
    "/tasks/{task_id}": {
      "get": {
        "tags": ["Task"],
        "summary": "Get task details",
        "operationId": "getTask",
        "parameters": [
          {
            "name": "task_id",
            "in": "path",
            "required": true,
            "schema": { "type": "string" }
          }
        ],
        "responses": {
          "200": {
            "description": "Task details"
          },
          "404": {
            "description": "Task not found"
          }
        }
      }
    }
  }
}
```

## Best Practices for API Documentation

1. **Always use tags** to organize endpoints into logical categories
2. **Provide clear summaries** - Use concise, action-oriented descriptions
3. **Document parameters** - Include type, format, and required status for each parameter
4. **Define response schemas** - Make response structures explicit
5. **Include examples** - Provide sample requests and responses
6. **Use consistent naming** - Follow RESTful conventions for endpoint names

## Resources

- [OpenAPI 3.0 Specification](https://spec.openapis.org/oas/v3.0.3)
- [Swagger 2.0 (OpenAPI 2.0) Specification](https://swagger.io/specification/v2/)
- [OpenAPI Best Practices](https://swagger.io/resources/webinars/best-practices-in-api-documentation/)
