# GitHub Copilot Instructions for AniTrend Project

These instructions will help GitHub Copilot understand the AniTrend project structure and conventions to provide better code suggestions.

## Project Architecture

```
The AniTrend project is a Django-based web application with multiple apps. It follows a clean architecture pattern:
- Domain layer: Contains business logic in usecase classes.
- Data layer: Contains repositories and data sources.
- Presentation layer: GraphQL API using Strawberry.

Key directories:
- app/: Django project settings and main configuration.
- core/: Common utilities, base classes, mixins, and core abstractions.
- config/, news/, episode/, media/: Domain-specific apps. The `media` app is a recent example of module structure and pattern application.
- di/: Project-wide dependency injection containers (though most DI is app-specific).
```

## Code Structure

```
Each app (e.g., `news/`, `episode/`, `media/`) is expected to follow this pattern. The `media` module serves as a good reference for new app development:

1.  `app_name/__init__.py`
2.  `app_name/apps.py`: Django application configuration.
3.  `app_name/domain/__init__.py`
4.  `app_name/domain/usecases.py`: Core business logic, orchestrating actions and data flow.
5.  `app_name/data/__init__.py`
6.  `app_name/data/repositories.py`: Repository pattern implementations, abstracting data access.
7. `app_name/data/sources.py`: Concrete data source interactions (e.g., API clients, complex database queries).
8. `app_name/graphql/__init__.py`
9. `app_name/graphql/types.py`: Strawberry type definitions for the GraphQL schema.
10. `app_name/graphql/queries.py`: GraphQL query definitions.
11. `app_name/graphql/mutations.py`: (Optional) GraphQL mutation definitions.
12. `app_name/graphql/resolvers.py`: Resolver functions that connect GraphQL operations to use cases or data layers.
13. `app_name/di/__init__.py`
14. `app_name/di/containers.py`: Dependency injection containers specific to the app, using `dependency_injector`.
15. `app_name/tests/`: Directory for unit and integration tests related to the app.
    - `app_name/tests/test_usecases.py`
    - `app_name/tests/test_repositories.py`
    - `app_name/tests/test_graphql.py`
    - etc.
```

## Patterns to Follow

```
These patterns are crucial for maintaining consistency and quality. They have been consistently applied in modules like `news/`, `episode/`, and the recently developed `media/` module.

1. Repository Pattern:
   - Use `RemoteSource` or similar classes for external API calls within the data layer.
   - `Repository` classes abstract data access logic (from DB, cache, or remote sources).
   - `UseCase` classes contain business logic and orchestrate repositories and other services.

2. Dependency Injection:
   - Utilize `dependency_injector` for managing dependencies. Define containers in `app_name/di/containers.py`.
   - Inject dependencies into classes (especially UseCases, Repositories, Sources) using constructor injection or the `@inject` decorator where appropriate.
   - Access container components via `Provide[Container.component]`.

3. GraphQL with Strawberry:
   - Define GraphQL types in `app_name/graphql/types.py` using `strawberry.type`.
   - Queries are defined in `app_name/graphql/queries.py`.
   - Mutations (if any) in `app_name/graphql/mutations.py`.
   - Resolvers in `app_name/graphql/resolvers.py` should primarily call use cases to fetch or manipulate data.
   - Pass necessary context (like HTTP headers) from the GraphQL context (e.g., `info.context`) down to use cases and data layers if needed for auth, feature flags, etc.

4. Feature Flags:
   - Use `GrowthBookMixin` (or a similar mechanism if evolved) for accessing feature flags.
   - Ensure feature flag evaluations are based on context (e.g., user attributes, request headers) passed appropriately.
```

## Naming, Typing, and Documentation Conventions

```
1. Naming:
   - Use snake_case for functions, methods, variables, and file names (e.g., `get_user_data.py`, `user_profile_service.py`).
   - Use PascalCase for class names (e.g., `UserProfile`, `MediaService`).
   - Module names (app names) should be snake_case (e.g., `user_profile`, `media_content`).

2. Typing and Docstrings:
   - Employ Python type hints for all function and method signatures, and for class attributes.
   - Write clear docstrings for all public classes, methods, and functions, explaining their purpose, arguments, and return values. Follow PEP 257.

3. Async Code:
   - Prefer `async/await` for I/O-bound operations (e.g., external API calls, database interactions when using an async ORM or driver).
   - Use `async def` for asynchronous functions and methods.
```

## Error Handling and Logging

```
1. Consistent Error Handling:
   - Use custom exception classes derived from a base project exception where appropriate.
   - The `raise_api_error` decorator (or similar centralized mechanism) should be used in the presentation layer (e.g., GraphQL resolvers) to ensure consistent error responses to the client.
2. Logging:
   - Utilize `LoggerMixin` (or standard Python logging configured for the project) for logging.
   - Log errors with tracebacks, important business events, and relevant context for debugging.
   - Avoid logging sensitive information.
```

## Code Formatting and Linting

```
1. Code Formatter: Use `black` for consistent code formatting.
2. Import Sorter: Use `isort` for organizing imports.
3. Linter: Use `flake8` (or a pre-configured linter like Ruff) to enforce code style and catch potential errors.
4. Pre-commit Hooks: Ensure these tools are run via pre-commit hooks to maintain code quality before changes are committed.
```

## Testing Conventions

```
1. Unit Tests:
   - Focus on testing individual units (classes, methods, functions) in isolation.
   - Mock external dependencies (repositories in use case tests, sources in repository tests, external APIs in source tests).
   - Use `unittest.TestCase` or `pytest` style tests. Pytest is generally preferred for its conciseness and fixture model.
2. Integration Tests:
   - Test interactions between components (e.g., use case with a real repository but mocked external source, or GraphQL resolver with real use case).
   - Mark integration tests appropriately (e.g., `@pytest.mark.integration`).
3. Test Structure (within each `app_name/tests/` directory):
   - `setUp` methods (for `unittest`) or `pytest` fixtures for common test setup.
   - Test success scenarios (happy paths).
   - Test failure scenarios and error handling (sad paths).
   - Test edge cases.
```

## Testing Methodologies and Preferred Approaches

```
1. Test Pyramid:
   - Prioritize a large base of unit tests.
   - Have a moderate number of integration tests.
   - Implement a few end-to-end tests for critical user flows (if applicable, managed separately).

2. Mocking and Isolation:
   - Use `unittest.mock` or `pytest-mock` for mocking.
   - Ensure mocks are specific and verify interactions correctly.
   - Leverage dependency injection to easily replace real implementations with mocks during tests.

3. Parametrization and Coverage:
   - Use `pytest.mark.parametrize` to test functions with multiple input scenarios efficiently.
   - Aim for high test coverage, particularly for business logic (domain layer) and data manipulation (data layer). Use coverage tools to track this.

4. Assertions and Fixtures:
   - Use expressive assertions provided by `pytest` or `unittest`.
   - Utilize `pytest` fixtures for reusable test data, mocked objects, and setup/teardown logic.

5. Test Naming and Organization:
   - Test function names should be descriptive: `test_<method_or_feature>_<condition_or_scenario>_<expected_outcome>`.
   - Group related tests in classes (if using `unittest`) or by file (e.g., `test_user_usecases.py`).

6. Continuous Integration (CI):
   - All tests (unit and integration) must pass in the CI pipeline before code is merged.
   - CI pipeline should also run linters and formatters.
```

## Common Utilities

```
(Located in the `core/` app)
1. Headers & Context:
   - `get_forwarded_headers()`: Utility to extract relevant headers from the request context (e.g., `info.context` in GraphQL).
   - `UserAgentInfo`: Class for parsing user-agent strings.
   - `ContextHeader`: Dataclass or Pydantic model for storing and passing request-specific context.

2. Error Handling Utilities:
   - `raise_api_error` decorator: As mentioned, for consistent API error responses.
   - Base exception classes in `core/errors.py`.

3. Mixins:
   - `LoggerMixin`: For easy access to a logger instance.
   - `GrowthBookMixin`: For feature flag evaluations.
```

## Environment Setup

```
1. Dependency Management: Use `poetry`. Key files: `pyproject.toml`, `poetry.lock`.
2. Environment Variables: Copy `.env.default` to `.env` for local development and customize as needed.
3. Database Migrations: Run `poetry run python manage.py migrate` after pulling changes or setting up.
4. Development Server: Use `start.sh` script. The `-d` flag enables debug mode (`poetry run python manage.py runserver`).
5. Poetry Scripts: Check `pyproject.toml` for `[tool.poetry.scripts]` for common tasks (e.g., `lint`, `test`).
```
