import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QGridLayout, QWidget, QLineEdit
from PyQt5.QtCore import Qt

class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_input = '0'
        self.pending_operation = None
        self.previous_value = None
        self.decimal_present = False

    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다.")
        return x / y

    def negative_positive(self):
        if self.current_input == '0':
            return self.current_input
        if self.current_input.startswith('-'):
            self.current_input = self.current_input[1:]
        else:
            self.current_input = '-' + self.current_input
        return self.current_input

    def percent(self):
        try:
            value = float(self.current_input)
            self.current_input = str(value / 100)
            return self.current_input
        except ValueError:
            return '오류'

    def append_number(self, number):
        if self.current_input == '0' and number != '.':
            self.current_input = number
        else:
            self.current_input += number

    def append_decimal(self):
        if not self.decimal_present:
            self.current_input += '.'
            self.decimal_present = True

    def equal(self):
        try:
            current_value = float(self.current_input)
            if self.pending_operation:
                if self.pending_operation == '+':
                    result = self.add(self.previous_value, current_value)
                elif self.pending_operation == '-':
                    result = self.subtract(self.previous_value, current_value)
                elif self.pending_operation == '*':
                    result = self.multiply(self.previous_value, current_value)
                elif self.pending_operation == '/':
                    result = self.divide(self.previous_value, current_value)
                else:
                    return '오류'

                if isinstance(result, float):
                    result = round(result, 6)

                self.reset()
                self.current_input = str(result)
                return str(result)
            else:
                return self.current_input
        except ZeroDivisionError:
            self.reset()
            return '오류: 0으로 나눔'
        except Exception:
            self.reset()
            return '오류'


class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()
        self.setWindowTitle('아이폰 계산기')
        self.setGeometry(100, 100, 400, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet('background-color: black;')

        # 수식 디스플레이 추가
        self.formula_display = QLineEdit()
        self.formula_display.setAlignment(Qt.AlignRight)
        self.formula_display.setReadOnly(True)
        self.formula_display.setStyleSheet("""
            QLineEdit {
                background-color: black;
                color: gray;
                font-size: 20px;
                border: none;
                padding: 5px;
            }
        """)

        # 메인 디스플레이
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: black;
                color: white;
                font-size: 40px;
                border: none;
                padding: 10px;
            }
        """)
        self.display.setText('0')

        layout = QVBoxLayout()
        layout.addWidget(self.formula_display)  # 수식 디스플레이 추가
        layout.addWidget(self.display)

        grid_layout = QGridLayout()
        buttons = [
            ['AC', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        button_styles = {
            'default': """
                QPushButton {
                    background-color: #333333;
                    color: white;
                    font-size: 20px;
                    border-radius: 40px;
                    height: 80px;
                }
                QPushButton:pressed {
                    background-color: #666666;
                }
            """,
            'orange': """
                QPushButton {
                    background-color: orange;
                    color: white;
                    font-size: 20px;
                    border-radius: 40px;
                    height: 80px;
                }
                QPushButton:pressed {
                    background-color: #ff9500;
                }
            """,
            'gray': """
                QPushButton {
                    background-color: #a6a6a6;
                    color: black;
                    font-size: 20px;
                    border-radius: 40px;
                    height: 80px;
                }
                QPushButton:pressed {
                    background-color: #d4d4d2;
                }
            """
        }

        for row_idx, row in enumerate(buttons):
            col_idx = 0
            for button_text in row:
                button = QPushButton(button_text)

                if button_text in ['÷', '×', '-', '+', '=']:
                    button.setStyleSheet(button_styles['orange'])
                elif button_text in ['AC', '±', '%']:
                    button.setStyleSheet(button_styles['gray'])
                else:
                    button.setStyleSheet(button_styles['default'])

                button.clicked.connect(lambda checked, text=button_text: self.on_button_click(text))

                if button_text == '0':
                    grid_layout.addWidget(button, row_idx, col_idx, 1, 2)
                    col_idx += 1
                else:
                    grid_layout.addWidget(button, row_idx, col_idx)

                col_idx += 1

        layout.addLayout(grid_layout)
        central_widget.setLayout(layout)

    def on_button_click(self, text):
        if text == 'AC':
            self.calculator.reset()
            self.display.setText('0')
            self.formula_display.setText('')
        elif text.isdigit():
            self.calculator.append_number(text)
            self.display.setText(self.calculator.current_input)
            self.adjust_font_size(self.calculator.current_input)
        elif text == '.':
            self.calculator.append_decimal()
            self.display.setText(self.calculator.current_input)
            self.adjust_font_size(self.calculator.current_input)
        elif text in ['+', '-', '×', '÷']:
            self.calculator.previous_value = float(self.calculator.current_input)
            self.calculator.pending_operation = text.replace('×', '*').replace('÷', '/')
            self.formula_display.setText(f"{self.calculator.current_input} {text}")
            self.calculator.current_input = '0'
            self.calculator.decimal_present = False
            self.display.setText('0')
            self.adjust_font_size('0')
        elif text == '=':
            result = self.calculator.equal()
            self.display.setText(result)
            self.adjust_font_size(result)
            self.formula_display.setText('')  # 수식 창 초기화
        elif text == '±':
            self.calculator.negative_positive()
            self.display.setText(self.calculator.current_input)
            self.adjust_font_size(self.calculator.current_input)
        elif text == '%':
            self.calculator.percent()
            self.display.setText(self.calculator.current_input)
            self.adjust_font_size(self.calculator.current_input)

    def adjust_font_size(self, text):
        text_length = len(text)
        if text_length > 10:
            font_size = 20
        elif text_length > 8:
            font_size = 25
        elif text_length > 6:
            font_size = 30
        else:
            font_size = 40

        self.display.setStyleSheet(f"""
            QLineEdit {{
                background-color: black;
                color: white;
                font-size: {font_size}px;
                border: none;
                padding: 10px;
            }}
        """)

def main():
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
