import logging
import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Add imports for log exporter
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

# Add imports for metrics exporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter


def setup_otel(app_name: str):
    """Configure OpenTelemetry for the Django application."""
    # Service name is required for most backends
    resource = Resource(
        attributes={
            "service.name": app_name,
        }
    )

    # --- trace provider setup ---
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # Configure the OTLP trace exporter
    # Choose trace endpoint (use specific or fallback)
    trace_endpoint = os.environ.get(
        "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
    )
    if trace_endpoint:
        otlp_exporter = OTLPSpanExporter(endpoint=trace_endpoint, insecure=True)
        processor = BatchSpanProcessor(otlp_exporter)
        provider.add_span_processor(processor)
    else:
        logging.error(
            "Tracing endpoint not set (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT or OTEL_EXPORTER_OTLP_ENDPOINT)."
        )

    # --- log provider setup ---
    # Setup log exporter (specific or fallback)
    log_provider = LoggerProvider(resource=resource)
    set_logger_provider(log_provider)
    logs_endpoint = os.environ.get(
        "OTEL_EXPORTER_OTLP_LOGS_ENDPOINT",
    )
    if logs_endpoint:
        log_exporter = OTLPLogExporter(endpoint=logs_endpoint, insecure=True)
        log_processor = BatchLogRecordProcessor(log_exporter)
        log_provider.add_log_record_processor(log_processor)
    else:
        logging.error(
            "Logs endpoint not set (OTEL_EXPORTER_OTLP_LOGS_ENDPOINT or OTEL_EXPORTER_OTLP_ENDPOINT)."
        )

    # --- metrics provider setup ---
    metrics_endpoint = os.environ.get(
        "OTEL_EXPORTER_OTLP_METRICS_ENDPOINT",
    )
    if metrics_endpoint:
        metric_exporter = OTLPMetricExporter(
            endpoint=metrics_endpoint,
            insecure=True,
        )
        metric_reader = PeriodicExportingMetricReader(metric_exporter)
        meter_provider = MeterProvider(
            resource=resource,
            metric_readers=[metric_reader],
        )
        # Set global meter provider
        from opentelemetry import metrics

        metrics.set_meter_provider(meter_provider)
    else:
        logging.error(
            "OTEL_EXPORTER_OTLP_METRICS_ENDPOINT not set. Metrics will not be exported."
        )

    # Instrument Django framework
    DjangoInstrumentor().instrument()

    # Instrument HTTP calls (requests)
    RequestsInstrumentor().instrument()

    # Instrument Python logging to inject trace context
    LoggingInstrumentor().instrument(set_logging_format=True)

    logging.info(f"OpenTelemetry configured for {app_name}")
