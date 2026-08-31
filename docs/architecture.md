# FlowForge Architecture

## High-level design

React frontend
        |
        v
FastAPI backend
        |
  +-----+------+
  |            |
  v            v
PostgreSQL   MongoDB
  |            |
Identity     Workflows
RBAC         Executions
             Audit events

## Database responsibility

PostgreSQL is intended for strongly relational platform data such as organizations, users, roles, and permissions.

MongoDB is intended for flexible workflow definitions, workflow versions, execution documents, and event/audit-style data.

## Engineering goals

- API-first architecture
- Configuration-driven workflows
- Organization-level isolation
- Role-based access control
- Automated testing
- Observable and debuggable services
- CI/CD quality gates
