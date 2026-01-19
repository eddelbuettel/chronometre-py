#!/usr/bin/env python3

import pytest
import time
from datetime import timedelta
import chronometre


class TestStopwatchBasicFunctionality:
    """Test basic stopwatch operations."""

    def test_stopwatch_creation(self):
        """Test that a stopwatch can be created."""
        sw = chronometre.Stopwatch()
        assert sw is not None

    def test_elapsed_returns_timedelta(self):
        """Test that elapsed() returns a timedelta object."""
        sw = chronometre.Stopwatch()
        elapsed = sw.elapsed()
        assert isinstance(elapsed, timedelta)

    def test_elapsed_is_positive(self):
        """Test that elapsed time is positive."""
        sw = chronometre.Stopwatch()
        time.sleep(0.01)  # Sleep for 10ms
        elapsed = sw.elapsed()
        assert elapsed.total_seconds() > 0

    def test_elapsed_increases_over_time(self):
        """Test that elapsed time increases."""
        sw = chronometre.Stopwatch()
        time.sleep(0.01)
        first_elapsed = sw.elapsed()
        time.sleep(0.01)
        second_elapsed = sw.elapsed()
        assert second_elapsed > first_elapsed

    def test_reset_functionality(self):
        """Test that reset() resets the stopwatch."""
        sw = chronometre.Stopwatch()
        time.sleep(0.05)  # Sleep for 50ms
        elapsed_before = sw.elapsed()

        sw.reset()
        elapsed_after = sw.elapsed()

        # After reset, elapsed time should be much smaller
        assert elapsed_after < elapsed_before
        assert elapsed_after.total_seconds() < 0.01  # Should be very small


class TestStopwatchTimingAccuracy:
    """Test timing accuracy of the stopwatch."""

    def test_elapsed_time_approximately_correct(self):
        """Test that elapsed time is approximately correct."""
        sw = chronometre.Stopwatch()
        sleep_duration = 0.1  # 100ms
        time.sleep(sleep_duration)
        elapsed = sw.elapsed().total_seconds()

        # Allow 20ms tolerance for timing variations
        assert abs(elapsed - sleep_duration) < 0.02

    def test_multiple_elapsed_calls_increase(self):
        """Test that multiple calls to elapsed() return increasing values."""
        sw = chronometre.Stopwatch()
        measurements = []

        for _ in range(5):
            time.sleep(0.01)
            measurements.append(sw.elapsed().total_seconds())

        # Each measurement should be larger than the previous
        for i in range(1, len(measurements)):
            assert measurements[i] > measurements[i-1]

    def test_reset_resets_timer_correctly(self):
        """Test that reset() properly resets the timer."""
        sw = chronometre.Stopwatch()
        time.sleep(0.05)

        sw.reset()
        time.sleep(0.05)
        elapsed = sw.elapsed().total_seconds()

        # Should be approximately 50ms, not 100ms
        assert abs(elapsed - 0.05) < 0.02


class TestStopwatchEdgeCases:
    """Test edge cases and special scenarios."""

    def test_rapid_successive_calls(self):
        """Test rapid successive calls to elapsed()."""
        sw = chronometre.Stopwatch()

        # Make many rapid calls - should not crash
        for _ in range(100):
            elapsed = sw.elapsed()
            assert isinstance(elapsed, timedelta)

    def test_immediate_elapsed_after_creation(self):
        """Test calling elapsed() immediately after creation."""
        sw = chronometre.Stopwatch()
        elapsed = sw.elapsed()

        # Should be very small but non-negative
        assert elapsed.total_seconds() >= 0
        assert elapsed.total_seconds() < 0.01  # Should be less than 10ms

    def test_multiple_independent_stopwatches(self):
        """Test that multiple stopwatch instances are independent."""
        sw1 = chronometre.Stopwatch()
        time.sleep(0.05)
        sw2 = chronometre.Stopwatch()
        time.sleep(0.05)

        elapsed1 = sw1.elapsed().total_seconds()
        elapsed2 = sw2.elapsed().total_seconds()

        # sw1 should have approximately twice the elapsed time of sw2
        assert elapsed1 > elapsed2
        assert abs(elapsed1 - 0.1) < 0.02
        assert abs(elapsed2 - 0.05) < 0.02

    def test_reset_multiple_times(self):
        """Test resetting the stopwatch multiple times."""
        sw = chronometre.Stopwatch()

        for _ in range(5):
            time.sleep(0.02)
            sw.reset()
            elapsed = sw.elapsed().total_seconds()
            assert elapsed < 0.01  # Should be very small after each reset

    def test_long_running_stopwatch(self):
        """Test stopwatch after a longer delay."""
        sw = chronometre.Stopwatch()
        time.sleep(0.5)  # 500ms
        elapsed = sw.elapsed().total_seconds()

        assert abs(elapsed - 0.5) < 0.05  # 50ms tolerance


class TestStopwatchStringConstructor:
    """Test the string-based copy constructor."""

    def test_copy_constructor_basic(self):
        """Test creating a stopwatch from another's address."""
        sw1 = chronometre.Stopwatch()
        time.sleep(0.05)

        # Get the memory address of sw1
        address = hex(id(sw1))

        # Create sw2 from sw1
        sw2 = chronometre.bake(sw1)

        # Both should have similar elapsed times
        elapsed1 = sw1.elapsed().total_seconds()
        elapsed2 = sw2.elapsed().total_seconds()

        # Should be very close (within 1ms)
        assert abs(elapsed1 - elapsed2) < 0.001

    def test_copy_constructor_preserves_start_time(self):
        """Test that copy constructor preserves the start time."""
        sw1 = chronometre.Stopwatch()
        time.sleep(0.1)

        sw2 = chronometre.bake(sw1)

        # Wait a bit more
        time.sleep(0.05)

        # Both should show approximately the same elapsed time
        elapsed1 = sw1.elapsed().total_seconds()
        elapsed2 = sw2.elapsed().total_seconds()

        assert abs(elapsed1 - elapsed2) < 0.001


class TestStopwatchInterface:
    """Test the stopwatch interface and types."""

    def test_module_has_stopwatch_class(self):
        """Test that the module exports the Stopwatch class."""
        assert hasattr(chronometre, 'Stopwatch')

    def test_stopwatch_has_elapsed_method(self):
        """Test that Stopwatch has an elapsed method."""
        sw = chronometre.Stopwatch()
        assert hasattr(sw, 'elapsed')
        assert callable(sw.elapsed)

    def test_stopwatch_has_reset_method(self):
        """Test that Stopwatch has a reset method."""
        sw = chronometre.Stopwatch()
        assert hasattr(sw, 'reset')
        assert callable(sw.reset)

    def test_elapsed_return_type(self):
        """Test that elapsed() returns the correct type."""
        sw = chronometre.Stopwatch()
        elapsed = sw.elapsed()
        assert isinstance(elapsed, timedelta)

    def test_reset_return_value(self):
        """Test that reset() returns None."""
        sw = chronometre.Stopwatch()
        result = sw.reset()
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
