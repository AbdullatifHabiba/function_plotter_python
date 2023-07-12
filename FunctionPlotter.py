import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, \
    QMessageBox, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sympy import symbols, sympify


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setCentralWidget(FunctionPlotWidget())


class FunctionPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        # Create a widget for the left side (input fields and buttons)
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkGray)

        self.setPalette(p)

        # Create input fields and labels
        self.function_label = QLabel("Enter a function of x:")
        self.function_input = QLineEdit()

        # reduce the margin of the input field
        self.x_min_label = QLabel("Enter the minimum value of x:")
        self.x_min_input = QLineEdit()
        self.x_max_label = QLabel("Enter the maximum value of x:")

        self.x_max_input = QLineEdit()

        # Create the plot button
        self.plot_button = QPushButton("Plot")
        self.plot_button.setStyleSheet("background-color:green ; color: #ffffff;")
        self.plot_button.clicked.connect(self.plot)

        # Add widgets to the left layout
        left_layout.addWidget(self.function_label)
        left_layout.addWidget(self.function_input)
        left_layout.addWidget(self.x_min_label)
        left_layout.addWidget(self.x_min_input)
        left_layout.addWidget(self.x_max_label)
        left_layout.addWidget(self.x_max_input)
        left_layout.addWidget(self.plot_button)
        # Add a stretch to the left layout to push the widgets to the center
        left_layout.addStretch()
        # Set the margins of the left layout to 10 pixels
        left_layout.setContentsMargins(0, 10, 10, 10)
        # Set the spacing between widgets to 10 pixels
        left_layout.setSpacing(15)
        # Set the width of the left widget to 200 pixels
        left_widget.setFixedWidth(220)

        # Create a widget for the right side (figure canvas)
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)

        # Create a figure and a canvas for Matplotlib
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        right_layout.addWidget(self.canvas)

        # Set the layout for the main widget
        layout.addWidget(left_widget)
        layout.addWidget(right_widget)

        # Set the layout for the FunctionPlotWidget
        self.setLayout(layout)

    def plot(self):
        # Retrieve user inputs
        function = self.function_input.text()
        x_min = self.x_min_input.text()
        x_max = self.x_max_input.text()

        # Validate inputs and display an error message if any of the inputs are invalid
        message = check_inputs(function, x_min, x_max)
        if message != "True":
            QMessageBox.critical(self, "Error", message)
            return
        x_min = float(x_min)
        x_max = float(x_max)
        # Create an array of x values
        x = []
        step = 0.1
        while x_min <= x_max:
            x.append(x_min)
            x_min += step

        # Evaluate the function for each x value
        y = []
        for val in x:
            # Evaluate the function for each x value and append the result to the y array if the evaluation succeeds
            try:
                v = evaluate_function(function, val)
                y.append(v)
            except (TypeError, ValueError):
                QMessageBox.critical(self, "Error", invalid_function_message)
                return

        # Clear the previous plot and create a new one
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y, color="red", linewidth=2)

        # Draw the canvas to update the plot
        self.canvas.draw()


invalid_function_message = "Invalid function!! \n function should be in the form of x  and with those  operations   " \
                           "*/+-^ sin cos tan log exp  \n Example: 2*x^2+3*x-4  or 2*sin(x)+3*cos(x)  or 2*log(" \
                           "x)+3*exp(x)"


def check_inputs(function, x_min, x_max):
    errors = []
    x1 = 0
    x2 = 0
    if not function:
        errors.append("Function cannot be empty")
    if not x_min:
        errors.append("x_min cannot be empty")
    else:
        try:
            x1 = float(x_min)
        except ValueError:
            errors.append("x_min should be a number")
    if not x_max:
        errors.append("x_max cannot be empty")
    else:
        try:
            x2 = float(x_max)
        except ValueError:
            errors.append("x_max should be a number")

    if x1 and x2:
        if float(x_min) >= float(x_max):
            errors.append("x_min should be less than x_max")
    if function:
        try:
            evaluate_function(function, 1)
        except:
            errors.append(invalid_function_message)

    if not errors:
        return "True"
    else:
        return "\n".join(errors)


def evaluate_function(function, x_value):
    function = function.replace("X", "x")
    x = symbols('x')
    expr = sympify(function)
    # Substitute the value of 'x'
    expr_with_x = expr.subs(x, x_value)
    # Evaluate the expression
    # check result is a number
    try:
        result = expr_with_x.evalf()
        return float(result)
    except (ZeroDivisionError, ValueError):
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
