# Workflow Engine

The workflow engine will interpret workflow definitions stored in MongoDB.

Example:

Trigger -> Condition -> Approval -> Notification -> Webhook

The goal is to execute configurable workflows without requiring a new backend implementation for every customer workflow.

Planned capabilities:

- Node registry
- Condition evaluation
- Approval steps
- Notifications
- Webhooks
- Retry handling
- Execution state
- Workflow versioning
