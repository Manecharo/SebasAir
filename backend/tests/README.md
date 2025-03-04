# Testing Documentation for Air Ambulance Fleet Tracking Dashboard

This directory contains tests for the backend components of the Air Ambulance Fleet Tracking Dashboard application.

## Testing Approach

We use pytest as our testing framework, with the following approach:

1. **Unit Tests**: Testing individual functions and classes in isolation
2. **Mock-based Testing**: Using mocks to avoid dependencies on external systems like databases
3. **Async Testing**: Using pytest-asyncio for testing asynchronous code like WebSockets

## Test Files

- `test_simple.py`: Basic tests that don't depend on any external systems
- `test_flight_service_simple.py`: Tests for the flight service functions
- `test_websocket_simple.py`: Tests for WebSocket functionality
- `conftest.py`: Common fixtures and configuration for tests
- `test_db.py`: Database mocking utilities for tests

## Running Tests

To run all tests:

```bash
python -m pytest
```

To run specific test files:

```bash
python -m pytest tests/test_simple.py
python -m pytest tests/test_flight_service_simple.py
python -m pytest tests/test_websocket_simple.py
```

To run tests with verbose output:

```bash
python -m pytest -v
```

## Test Coverage

The tests cover the following components:

1. **Flight Service**:
   - Getting active flights
   - Getting flights by ID
   - Getting flights by date
   - Creating flights
   - Updating flights
   - Deleting flights

2. **WebSocket Functionality**:
   - Connecting to WebSockets
   - Disconnecting from WebSockets
   - Broadcasting messages
   - Receiving messages

## Mocking Strategy

We use the following mocking strategies:

1. **Database Mocking**: We mock the SQLAlchemy session to avoid actual database connections
2. **WebSocket Mocking**: We create mock WebSocket classes to test WebSocket functionality
3. **Function Patching**: We use `unittest.mock.patch` to replace functions with mocks

## Future Improvements

1. Add integration tests that test the API endpoints
2. Add end-to-end tests that test the full application flow
3. Implement test coverage reporting
4. Add performance tests for critical components 