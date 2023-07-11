import pytest
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton

from FunctionPlotter import FunctionPlotWidget, check_inputs, evaluate_function, invalid_function_message


@pytest.fixture
def q_app(qtbot):
    app = FunctionPlotWidget()
    qtbot.addWidget(app)
    return app


def test_function_plot_widget1(q_app, qtbot):
    widget = FunctionPlotWidget()

    # Test initial state
    assert isinstance(widget.function_label, QLabel)
    assert isinstance(widget.function_input, QLineEdit)
    assert isinstance(widget.x_min_label, QLabel)
    assert isinstance(widget.x_min_input, QLineEdit)
    assert isinstance(widget.x_max_label, QLabel)
    assert isinstance(widget.x_max_input, QLineEdit)
    assert isinstance(widget.plot_button, QPushButton)

    assert widget.function_input.text() == ""
    assert widget.x_min_input.text() == ""
    assert widget.x_max_input.text() == ""

    # Simulate user input
    qtbot.keyClicks(widget.function_input, "5^x")
    qtbot.keyClicks(widget.x_min_input, "1")
    qtbot.keyClicks(widget.x_max_input, "2")

    # Click the plot button
    qtbot.mouseClick(widget.plot_button, Qt.LeftButton)

    # Verify the plot
    assert widget.figure.axes
    assert len(widget.figure.axes[0].lines) == 1


def test_check_inputs():
    assert check_inputs("", "1", "2") == "Function cannot be empty"
    assert check_inputs("5*x^3 + 2*x", "a", "2") == "x_min should be a number"
    assert check_inputs("5*x^3 + 2*x", "1", "b") == "x_max should be a number"
    assert check_inputs("5*x^3 + 2*x", "2", "1") == "x_min should be less than x_max"
    assert check_inputs("5*x^3 + 2*x", "1", "2") == "True"
    assert check_inputs("", "", "") == "Function cannot be empty\nx_min cannot be empty\nx_max cannot be empty"
    assert check_inputs("5*x^3 + 2*x", "a", "b") == "x_min should be a number\nx_max should be a number"
    assert check_inputs("x+y", "2", "1") == "x_min should be less than x_max\n" + invalid_function_message


def test_evaluate_function():
    assert evaluate_function("5*x^3 + 2*x", 2) == 44.0
    assert evaluate_function("sin(x)", 0) == 0.0
    assert evaluate_function("1/x", 1) == 1.0


def test_function_plot_widget2(q_app, qtbot):
    # Create the FunctionPlotWidget
    widget = FunctionPlotWidget()

    # Simulate user input
    qtbot.keyClicks(widget.function_input, "5*x^3 + 2*x")
    qtbot.keyClicks(widget.x_min_input, "1")
    qtbot.keyClicks(widget.x_max_input, "10")

    # Click the plot button
    qtbot.mouseClick(widget.plot_button, Qt.LeftButton)

    # Assert the plot is displayed correctly
    assert len(widget.figure.axes) == 1
    assert len(widget.figure.axes[0].lines) == 1

    # Assert the evaluated function values are correct
    expected_x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    expected_y = [7.0, 44.0, 141.0, 328.0, 635.0, 1092.0, 1729.0, 2576.0, 3663.0, 5020.0]

    for x, y in zip(expected_x, expected_y):
        assert evaluate_function("5*x^3 + 2*x", x) == y
