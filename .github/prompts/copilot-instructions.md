# GitHub Copilot Instructions for AniTrend Project

These instructions will help GitHub Copilot understand the AniTrend project structure and conventions to provide better code suggestions.

## Project Architecture

```
The AniTrend project is a Django-based web application with multiple apps. It follows a clean architecture pattern:
- Domain layer: Contains business logic in usecase classes
- Data layer: Contains repositories and data sources
- Presentation layer: GraphQL API using strawberry

Key directories:
- app/: Django project settings
- core/: Common utilities and mixins
- config/, news/, episode/: Domain-specific apps
- di/: Dependency injection containers
```

## Code Structure

```
Each app follows the same pattern:
1. models.py: Django models
2. schemas.py: Data schemas using marshmallow
3. domain/usecases.py: Business logic
4. data/repositories.py: Repository pattern implementations
5. data/sources.py: Data sources (API clients)
6. graphql/: GraphQL types and resolvers
7. di/containers.py: Dependency injection containers
```

## Patterns to Follow

```
1. Repository Pattern:
   - Use RemoteSource for API calls
   - Use Repository classes to handle data access
   - Use UseCase classes for business logic

2. Dependency Injection:
   - Use dependency_injector containers and providers
   - Inject dependencies using @inject decorator
   - Access containers through Provide[Container.component]

3. GraphQL:
   - Define strawberry types with descriptive fields
   - Use resolvers to fetch data through use cases
   - Pass headers from GraphQL context to APIs

4. Feature Flags:
   - Use GrowthBookMixin for feature flag access
   - Set attributes based on context headers
```

## Testing Conventions

```
1. Unit Tests:
   - Mock repositories in use case tests
   - Use unittest.TestCase as base class
   - Use pytest fixtures when needed
   - Use @pytest.mark.integration for integration tests

2. Test Structure:
   - setUp: Initialize mocks and test data
   - Test success scenarios
   - Test error handling
```

## Common Utilities

```
1. Headers:
   - Use get_forwarded_headers() to extract headers from context
   - Use UserAgentInfo for parsing user agent strings
   - Use ContextHeader for storing request context

2. Error Handling:
   - Use raise_api_error decorator for consistent API error handling
   - Log errors using LoggerMixin
```

## Environment Setup

```
1. Use poetry for dependency management
2. Copy .env.default to .env for local development
3. Run migrations before starting server
4. Use start.sh script with -d flag for debug mode
```
