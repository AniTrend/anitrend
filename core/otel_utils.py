"""
OpenTelemetry utilities for AniTrend project.

This module provides convenient utilities for adding custom tracing and metrics
to your Django application.
"""

from typing import Any, Dict, Optional
from functools import wraps
import logging

from app.otel_config import get_tracer, get_meter


logger = logging.getLogger(__name__)


def trace_method(operation_name: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None):
    """
    Decorator to add tracing to methods.
    
    Args:
        operation_name: Name of the operation (defaults to method name)
        attributes: Additional attributes to add to the span
        
    Example:
        @trace_method("fetch_user_data", {"source": "database"})
        def get_user(self, user_id: int):
            # Your method implementation
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracer = get_tracer()
            span_name = operation_name or f"{func.__module__}.{func.__name__}"
            
            with tracer.start_as_current_span(span_name) as span:
                # Add attributes if provided
                if attributes:
                    for key, value in attributes.items():
                        span.set_attribute(key, value)
                
                # Add method arguments as attributes (be careful with sensitive data)
                if kwargs:
                    for key, value in kwargs.items():
                        if not key.startswith('_') and not callable(value):
                            span.set_attribute(f"method.arg.{key}", str(value))
                
                try:
                    result = func(*args, **kwargs)
                    span.set_attribute("success", True)
                    return result
                except Exception as e:
                    span.set_attribute("success", False)
                    span.set_attribute("error.type", type(e).__name__)
                    span.set_attribute("error.message", str(e))
                    raise
        
        return wrapper
    return decorator


class MetricsHelper:
    """Helper class for creating and managing custom metrics."""
    
    def __init__(self):
        self.meter = get_meter()
        self._counters = {}
        self._histograms = {}
        self._gauges = {}
    
    def get_counter(self, name: str, description: str = "", unit: str = ""):
        """Get or create a counter metric."""
        if name not in self._counters:
            self._counters[name] = self.meter.create_counter(
                name=name,
                description=description,
                unit=unit
            )
        return self._counters[name]
    
    def get_histogram(self, name: str, description: str = "", unit: str = ""):
        """Get or create a histogram metric."""
        if name not in self._histograms:
            self._histograms[name] = self.meter.create_histogram(
                name=name,
                description=description,
                unit=unit
            )
        return self._histograms[name]
    
    def increment_counter(self, name: str, value: int = 1, attributes: Optional[Dict[str, Any]] = None):
        """Increment a counter metric."""
        counter = self.get_counter(name)
        counter.add(value, attributes or {})
    
    def record_histogram(self, name: str, value: float, attributes: Optional[Dict[str, Any]] = None):
        """Record a value in a histogram metric."""
        histogram = self.get_histogram(name)
        histogram.record(value, attributes or {})


# Global instance for easy access
metrics = MetricsHelper()
