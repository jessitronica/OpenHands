# Summary of Changes: Mark Spans with Error Status for ErrorObservation

## Overview
Implemented functionality to automatically mark OpenTelemetry spans with error status whenever an `ErrorObservation` is received. This improves observability and error tracking in the system.

## Changes Made

### 1. `/workspaces/openhands/openhands/events/stream.py`
- **Added import**: `ErrorObservation` from `openhands.events.observation.error`
- **Modified method**: `add_event()`
  - Added check to detect when an `ErrorObservation` is added to the event stream
  - Automatically marks the current span with error status using `trace.get_current_span().set_status(trace.StatusCode.ERROR)`
  - This ensures all ErrorObservations are caught at the stream level, regardless of where they originate

### 2. `/workspaces/openhands/openhands/controller/agent_controller.py`
- **Modified method**: `_handle_observation()`
  - Added check to detect when an `ErrorObservation` is being handled
  - Automatically marks the current span with error status using `trace.get_current_span().set_status(trace.StatusCode.ERROR)`
  - This provides an additional layer of error tracking at the controller level

## Implementation Details

### Code Pattern Used
```python
# Mark span as error if ErrorObservation is received/added
if isinstance(observation/event, ErrorObservation):
    trace.get_current_span().set_status(trace.StatusCode.ERROR)
```

### Why Two Locations?
1. **EventStream.add_event()**: Catches all ErrorObservations as they're added to the event stream, providing comprehensive coverage
2. **AgentController._handle_observation()**: Provides specific error marking when the controller processes observations, ensuring the controller's span context is properly marked

## Testing

### Verification
- Created and ran manual tests to verify span marking functionality
- All existing unit tests pass:
  - `tests/unit/test_agent_controller.py`: 28/28 tests passed
  - `tests/unit/test_event_stream.py`: 18/18 tests passed
- Pre-commit hooks (ruff, ruff-format, trailing whitespace) all pass

### Test Results
```
✓ ErrorObservation marks span with error status in EventStream
✓ ErrorObservation marks span with error status in AgentController
✓ All existing tests continue to pass
```

## Benefits
1. **Improved Observability**: Error spans are now automatically marked in OpenTelemetry traces
2. **Better Debugging**: Easier to identify and track errors in distributed tracing systems
3. **Consistent Error Tracking**: All ErrorObservations are consistently marked regardless of origin
4. **No Breaking Changes**: Implementation is additive and doesn't modify existing behavior

## Dependencies
- Uses existing `opentelemetry` package (already imported in both files)
- Uses `trace.StatusCode.ERROR` (standard OpenTelemetry status code)
- No new dependencies required
