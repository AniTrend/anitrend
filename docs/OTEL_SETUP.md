# OpenTelemetry Setup for AniTrend

This document describes the OpenTelemetry (OTEL) observability setup for the AniTrend Django application. It has been updated to align with the current OpenTelemetry Python packages and environment variable conventions (traces, metrics, logs, exporters and instrumentation).

## Overview

The application is configured with comprehensive OpenTelemetry instrumentation including:
- **Distributed Tracing**: Traces requests across Django views, database calls, and external HTTP requests
- **Metrics**: Application performance metrics and custom business metrics
- **Logs**: Structured logging with trace context correlation

## Configuration

### Environment variables

Use environment variables to configure the SDK and exporters without code changes. Put these in your `.env` (or your container environment). A few current conventions and examples:

```bash
# Service identification (recommended)
# Either set the single service name env var or use OTEL_RESOURCE_ATTRIBUTES for multiple attributes
OTEL_SERVICE_NAME=anitrend
SERVICE_VERSION=1.0.0  # optional app-level variable (useful for deployment tooling)

# Alternative: set multiple resource attributes in a single variable
# Note: values containing commas or equal signs may need quoting depending on your environment
OTEL_RESOURCE_ATTRIBUTES="service.name=anitrend,service.version=1.0.0,service.instance.id=instance-1,deployment.environment=production"

# OTLP endpoints. Default ports: gRPC 4317, HTTP 4318
# Use the signal-specific variables when you need different endpoints for traces/metrics/logs
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317          # generic OTLP endpoint (often gRPC)
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://otel-collector:4317  # gRPC:4317 (or http://collector:4318/v1/traces for HTTP/protobuf over HTTP)
OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://otel-collector:4317
OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://otel-collector:4317

# Protocol and insecure settings (for Python exporters you may also configure in code):
# For HTTP/protobuf export (default HTTP port 4318) set OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf

# Sampling (example: 10% sampling)
OTEL_TRACES_SAMPLER=traceidratio
OTEL_TRACES_SAMPLER_ARG=0.1

# Enable/disable instrumentation (used by opentelemetry-instrument and some instrumentors)
# Example: comma-separated list of instrumentations to disable
OTEL_PYTHON_DISABLED_INSTRUMENTATIONS=django-templates
```

### Automatic instrumentation

AniTrend can use OpenTelemetry auto-instrumentation or explicit instrumentation. Common instrumentations and packages:

- Django: `opentelemetry-instrumentation-django` (web request lifecycle, view spans)
- PostgreSQL (psycopg2): `opentelemetry-instrumentation-psycopg2` or the DBAPI instrumentation
- HTTP client: `opentelemetry-instrumentation-requests` (outgoing requests)
- ASGI/WSGI servers: covered by Django instrumentation when using WSGI/ASGI


You can enable auto-instrumentation on startup with the opentelemetry-instrument CLI. Because this project uses Poetry, prefer adding runtime dependencies to `pyproject.toml` and using `poetry run` for developer commands.

```bash
# add packages with poetry (example)
poetry add --group runtime opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp \
    opentelemetry-instrumentation-django opentelemetry-instrumentation-psycopg2 opentelemetry-instrumentation-requests

# run django with instrumentation enabled (use --noreload to avoid double-initialization in dev)
poetry run opentelemetry-instrument python manage.py runserver --noreload
```

Programmatic initialization (recommended for production for more control): set a TracerProvider, Resource attributes and processors in a bootstrapping module (example below).

## Usage

### Custom tracing

Use helpers like `@trace_method` to create named spans in the application code. If your repo already includes `core.otel_utils.trace_method` (as this project does), prefer that for consistency. Example (existing helper):

```python
from core.otel_utils import trace_method

class MyService:
    @trace_method("user_lookup", {"source": "database"})
    def get_user(self, user_id: int):
        # implementation
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
from opentelemetry import trace
from app.otel_config import get_tracer  # or use trace.get_tracer(__name__)

tracer = get_tracer()

with tracer.start_as_current_span("custom_operation") as span:
    span.set_attribute("user_id", user_id)
    # work
    result = do_work()
    span.set_attribute("result_count", len(result))
```

## Deployment Considerations

### Production Setup

1. **Secure endpoints / TLS**: Use TLS in production. When constructing exporters programmatically, prefer passing `insecure=False` (or using an HTTPS endpoint) and ensure the collector or backend has the proper certificates.
2. **Resource Attributes**: Consider adding more resource attributes like:
   - `service.instance.id`
   - `deployment.environment` 
   - `service.namespace`

### Performance impact and tuning

- Sampling: Configure `OTEL_TRACES_SAMPLER` + `OTEL_TRACES_SAMPLER_ARG` (e.g. `traceidratio` + `0.1`) to reduce trace volume in high-traffic services.
- BatchSpanProcessor: Use batch processors (the SDK default for performance) when exporting spans. When running in pre-fork servers (uWSGI), initialize the processor after fork (see note below).
- Metrics: Prometheus exporter is pull-based (use `opentelemetry-exporter-prometheus` with PrometheusMetricReader). Push-based metric exporters are also available but may require a collector.
- Resource usage: telemetry is buffered—monitor memory and use appropriate exporters and batch sizes.

uWSGI / pre-fork servers:

- If using uWSGI or other pre-fork models, initialize the exporter/span processor in a post-fork hook (e.g., `uwsgidecorators.postfork`) so the BatchSpanProcessor doesn't attempt to run across the fork boundary.

## Troubleshooting

### Common Issues

1. **No traces appearing**: Check that OTLP endpoints are reachable from the application and that the exporter packages were installed (e.g., `opentelemetry-exporter-otlp` or `opentelemetry-exporter-otlp-proto-grpc`). Confirm collector is listening on the expected port (gRPC 4317 or HTTP 4318).
2. **Missing database traces**: Ensure the DB instrumentation package is installed and enabled (for psycopg2 use `opentelemetry-instrumentation-psycopg2`). If you use an async DB driver, use the matching instrumentation.
3. **Logs missing trace context**: Inject trace identifiers into your log formatter (example below) or use a logging instrumentor if available. Verify that the logs exporter is configured if you expect logs to appear in the collector/back end.
4. **Import / dependency errors**: Run `poetry install` to install project dependencies (this repository uses Poetry). If you need to reproduce quickly in an isolated environment you can use `pip` in a virtualenv, but prefer Poetry for consistency.

### Debug Mode

Add debug logging to see OTEL internal operations:

```python
import logging
logging.getLogger("opentelemetry").setLevel(logging.DEBUG)

You can also enable debug for exporters / collector networking when diagnosing connectivity issues.

### Helpful installation notes

Add these packages to your project's dependencies (poetry):

```
opentelemetry-api
opentelemetry-sdk
opentelemetry-exporter-otlp          # convenience package that includes OTLP exporters
opentelemetry-exporter-otlp-proto-grpc
opentelemetry-exporter-otlp-proto-http
opentelemetry-instrumentation-django
opentelemetry-instrumentation-requests
opentelemetry-instrumentation-psycopg2
opentelemetry-exporter-prometheus    # if using Prometheus for metrics
opentelemetry-semantic-conventions
```

Install with poetry (example):

```bash
poetry add --group runtime opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp \
    opentelemetry-instrumentation-django opentelemetry-instrumentation-requests opentelemetry-instrumentation-psycopg2
```
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

### Example: programmatic tracer + OTLP exporter (recommended for production)

```python
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry import trace

resource = Resource.create({"service.name": "anitrend", "service.version": "1.0.0"})

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("startup"):
    pass
```

Notes:
- Use `insecure=False` and proper TLS in production, or point to an HTTPS endpoint.
- For HTTP/protobuf export you can instead use the `opentelemetry-exporter-otlp-proto-http` exporter and point to `http://collector:4318/v1/traces`.

### Inject trace context into logs (simple formatter example)

```python
import logging
from opentelemetry import trace

class TraceIdLogFilter(logging.Filter):
    def filter(self, record):
        span = trace.get_current_span()
        ctx = span.get_span_context()
        record.otel_trace_id = format(ctx.trace_id, '032x') if ctx.trace_id else None
        record.otel_span_id = format(ctx.span_id, '016x') if ctx.span_id else None
        return True

# then add the filter to your handlers and include %(otel_trace_id)s in the formatter
```

This approach keeps logs and traces correlated without relying on a logging-specific exporter.
