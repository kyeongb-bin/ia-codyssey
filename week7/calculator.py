import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QGridLayout, QWidget, QLineEdit
from PyQt5.QtCore import Qt

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("아이폰 계산기")
        self.setGeometry(100, 100, 400, 600)  # 아이폰 계산기와 유사한 크기로 조정

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 전체 배경색 검정으로 설정
        central_widget.setStyleSheet("background-color: black;")

        # 입력 및 결과를 표시할 디스플레이
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

        # 버튼 레이아웃
        layout = QVBoxLayout()
        layout.addWidget(self.display)

        # 버튼 생성 및 배치
        grid_layout = QGridLayout()
        buttons = [
            ['AC', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        # 버튼 스타일 설정
        button_styles = {
            "default": """
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
            "orange": """
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
            "gray": """
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
                    button.setStyleSheet(button_styles["orange"])
                elif button_text in ['AC', '±', '%']:
                    button.setStyleSheet(button_styles["gray"])
                else:
                    button.setStyleSheet(button_styles["default"])
                
                button.clicked.connect(lambda checked, text=button_text: self.on_button_click(text))
                
                if button_text == '0':  # '0' 버튼은 가로로 길게 설정
                    grid_layout.addWidget(button, row_idx, col_idx, 1, 2)
                    col_idx += 1
                else:
                    grid_layout.addWidget(button, row_idx, col_idx)
                
                col_idx += 1

        layout.addLayout(grid_layout)
        central_widget.setLayout(layout)

    def on_button_click(self, text):
        if text == 'AC':
            self.display.setText('')
        elif text == '=':
            self.calculate(self.display.text())
        elif text == '±':
            current_text = self.display.text().replace(',', '')
            if current_text and current_text[0] == '-':
                self.display.setText(self.format_number(current_text[1:]))
            else:
                self.display.setText(self.format_number('-' + current_text))
        else:
            current_text = self.display.text()
            
            # 숫자 입력 시 쉼표 추가
            if text.isdigit() or text == '.':
                current_text += text
                formatted_text = self.format_number(current_text.replace(',', ''))
                self.display.setText(formatted_text)
            else:
                self.display.setText(current_text + text)


    def calculate(self, expression):
        try:
            expression = expression.replace('÷', '/').replace('×', '*').replace(',', '')
            result = eval(expression)
            
            # 결과 값에 쉼표 추가
            formatted_result = self.format_number(str(result))
            self.display.setText(formatted_result)
        except Exception:
            self.display.setText('오류')

    def format_number(self, num_str):
        """3자리마다 쉼표를 추가하는 함수"""
        try:
            if '.' in num_str:
                integer_part, decimal_part = num_str.split('.')
                integer_part = f"{int(integer_part):,}"
                return f"{integer_part}.{decimal_part}"
            else:
                return f"{int(num_str):,}"
        except ValueError:
            return num_str

def main():
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
