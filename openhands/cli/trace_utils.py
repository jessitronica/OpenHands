from opentelemetry import trace


class TraceUtils:
    _instance = None
    occurrences: dict[str, int] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.root_span = None
        return cls._instance

    def remember_root_span(self):
        self.root_span = trace.get_current_span()

    # value can be string or number
    def set_attribute_on_root_span(self, key: str, value: str | int | float | bool) -> None:
        if self.root_span:
            self.root_span.set_attribute(key, value)

    def count_occurrence(self, key: str) -> None:
        occurrences = self.occurrences.get(key, 0)
        occurrences += 1
        self.occurrences[key] = occurrences
        self.set_attribute_on_root_span(f'app.count.{key}', occurrences)


trace_utils = TraceUtils()
