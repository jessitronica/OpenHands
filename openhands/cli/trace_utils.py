
from opentelemetry import trace

class TraceUtils:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.root_span = None
        return cls._instance

    def remember_root_span(self):
        self.root_span = trace.get_current_span()

    def set_attribute_on_root_span(self, key: str, value: str) -> None:
        if self.root_span:
            self.root_span.set_attribute(key, value)


trace_utils = TraceUtils()
