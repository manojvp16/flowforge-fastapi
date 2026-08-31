# Testing Strategy

FlowForge will use a test pyramid:

- Unit tests for business logic
- Integration tests for database/API boundaries
- API regression tests for REST endpoints
- Locust for load/performance testing

The test suite will eventually run automatically in CI before deployment.
