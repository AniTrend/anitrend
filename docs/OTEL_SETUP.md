# OpenTelemetry Setup for AniTrend

This document describes the OpenTelemetry (OTEL) observability setup for the AniTrend Django application.

## Overview

The application is configured with comprehensive OpenTelemetry instrumentation including:
- **Distributed Tracing**: Traces requests across Django views, database calls, and external HTTP requests
- **Metrics**: Application performance metrics and custom business metrics
- **Logs**: Structured logging with trace context correlation

## Configuration

### Environment Variables

Configure the following environment variables in your `.env` file:

```bash
# Service identification
OTEL_SERVICE_NAME="anitrend"
SERVICE_VERSION="1.0.0"  # Optional: service version

# OTLP endpoints (can use generic endpoint or specific ones)
OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4318"

# Or specific endpoints for each signal
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="http://otel-collector:4318/v1/traces"
OTEL_EXPORTER_OTLP_METRICS_ENDPOINT="http://otel-collector:4318/v1/metrics"  
OTEL_EXPORTER_OTLP_LOGS_ENDPOINT="http://otel-collector:4318/v1/logs"
```

### Automatic Instrumentation

The following components are automatically instrumented:

- **Django**: Request/response cycle, middleware, views
- **PostgreSQL**: Database queries via psycopg2
- **HTTP Requests**: Outgoing requests via the `requests` library
- **Logging**: Python logging with trace context injection
- **ASGI/WSGI**: Application server instrumentation

## Usage

### Custom Tracing

Use the `@trace_method` decorator for custom spans:

```python
from core.otel_utils import trace_method

class MyService:
    @trace_method("user_lookup", {"source": "database"})
    def get_user(self, user_id: int):
        # Your method implementation
        return user
```

### Custom Metrics  

Use the metrics helper for custom metrics:

```python
from core.otel_utils import metrics

# Increment a counter
metrics.increment_counter("api_requests_total", attributes={"endpoint": "/users"})

# Record a histogram value  
metrics.record_histogram("request_duration_seconds", 0.125, {"method": "GET"})
```

### Manual Tracing

For more control, use the tracer directly:

```python
from app.otel_config import get_tracer

tracer = get_tracer()

with tracer.start_as_current_span("custom_operation") as span:
    span.set_attribute("user_id", user_id)
    # Your code here
    result = do_work()
    span.set_attribute("result_count", len(result))
```

## Deployment Considerations

### Production Setup

1. **HTTPS Endpoints**: Set `insecure=False` in the OTLP exporters for production
2. **Resource Attributes**: Consider adding more resource attributes like:
   - `service.instance.id`
   - `deployment.environment` 
   - `service.namespace`

### Performance Impact

- **Sampling**: Consider implementing trace sampling for high-traffic applications
- **Batch Processing**: The setup uses batch processors to minimize performance impact
- **Resource Usage**: Monitor memory usage as telemetry data is buffered before export

## Troubleshooting

### Common Issues

1. **No traces appearing**: Check that `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` is set and accessible
2. **Missing database traces**: Ensure `opentelemetry-instrumentation-psycopg2` is installed  
3. **Import errors**: Run `poetry install` to install all OTEL dependencies

### Debug Mode

Add debug logging to see OTEL internal operations:

```python
import logging
logging.getLogger("opentelemetry").setLevel(logging.DEBUG)
```

## Architecture Integration

The OTEL setup follows the AniTrend clean architecture patterns:

- **Domain Layer**: Add custom tracing to use cases for business logic visibility
- **Data Layer**: Database calls are automatically traced via psycopg2 instrumentation  
- **Presentation Layer**: GraphQL resolvers benefit from automatic Django instrumentation

Example in a use case:

```python
from core.otel_utils import trace_method
from dependency_injector.wiring import inject, Provide

class MediaUseCase:
    @inject
    def __init__(self, repository: MediaRepository = Provide["media_container.repository"]):
        self.repository = repository
    
    @trace_method("fetch_media_list")
    async def get_media_list(self, filters: dict) -> List[Media]:
        # This will create a span "fetch_media_list" 
        # Database calls will be child spans automatically
        return await self.repository.get_filtered_media(filters)
```

This creates a complete observability story from GraphQL query → use case → repository → database.
