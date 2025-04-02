# AniTrend GraphQL API

A sophisticated GraphQL API that aggregates anime-related data from multiple sources with built-in caching capabilities. This API serves as a unified interface for accessing anime news, episodes, and configuration data with features like rate limiting, error handling, and connection pooling.

## Key Features

- **GraphQL Interface**: Built with Strawberry GraphQL for type-safe schema definitions and efficient queries
- **Data Aggregation**: Centralizes data from multiple sources into a unified API
- **Intelligent Caching**: Built-in caching mechanisms to optimize performance
- **Rate Limiting**: Protects upstream services with configurable rate limiting
- **Error Resilience**: Automatic retries with backoff strategies for API calls
- **WebSocket Support**: Real-time updates through GraphQL subscriptions
- **Type Safety**: Fully typed schemas using Python dataclasses and Strawberry types
- **Modular Architecture**: Clean separation of concerns with domain-driven design

## Core Components

### News Module
- Aggregates news from various sources
- Supports pagination through connection types
- Provides rich filtering and sorting capabilities
- Includes full text search for news content

### Configuration System
- Dynamic client configuration management
- Navigation structure configuration
- Media resource management
- Feature flag system
- Analytics integration options

### Episode Tracking
- Episode information aggregation
- Release schedule tracking
- Media metadata management

## Getting Started

### Prerequisites
- Python 3.8+
- Poetry for dependency management

### Setup

1. Clone the repository and set up environment variables:
```shell
cp .env.default .env
```

2. Install dependencies using Poetry:
```shell
poetry install
```

3. Set up the database:
```shell
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

4. Start the development server:
```shell
poetry run python manage.py runserver
```

The GraphQL playground will be available at `http://localhost:8000/playground`

The schema will be saved in `./tmp`

## Project Structure

- `app/`: Core application setup, including GraphQL schema configuration and ASGI/WSGI servers
- `core/`: Base utilities, middleware, and common functionality
  - Error handling
  - Rate limiting
  - Caching infrastructure
  - Common schemas and models
- `config/`: Configuration management and dependency injection
  - Client configuration
  - Feature flags
  - Resource management
- `news/`: News aggregation and management
  - News feed implementation
  - Source integration
  - Content caching
- `episode/`: Episode tracking and management
  - Episode data models
  - Release tracking
  - Media metadata
- `web/`: Web-specific implementations and views

## Development

The project uses a clean architecture pattern with:
- Domain-driven design
- Repository pattern for data access
- Use case pattern for business logic
- Dependency injection for flexible component coupling

## Testing

The project includes comprehensive unit tests for all major components. Run tests using:
```shell
poetry run pytest
```

## License

```
Copyright (C) 2021  AniTrend

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```