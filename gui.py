import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QSpinBox, QVBoxLayout, QHBoxLayout, QTextEdit
)
from .core import process_images

class MainWindow(QWidget):
    def __main__(self):
        super().__init__()
        self.setWindowTitle("Gerador de Ratos c/ Fundo Aleatório")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        # número de fundos
        h1 = QHBoxLayout()
        h1.addWidget(QLabel("Qtd de fundos:"))
        self.spin_bgs = QSpinBox(); self.spin_bgs.setRange(1,100); self.spin_bgs.setValue(5)
        h1.addWidget(self.spin_bgs)
        layout.addLayout(h1)
        # número de ratos
        h2 = QHBoxLayout()
        h2.addWidget(QLabel("Qtd de ratos/fundo:"))
        self.spin_rats = QSpinBox(); self.spin_rats.setRange(1,100); self.spin_rats.setValue(10)
        h2.addWidget(self.spin_rats)
        layout.addLayout(h2)
        # log
        self.log = QTextEdit(); self.log.setReadOnly(True)
        layout.addWidget(self.log)
        # botão
        btn = QPushButton("Processar")
        btn.clicked.connect(self.on_click)
        layout.addWidget(btn)
        self.setLayout(layout)

    def on_click(self):
        self.log.clear()
        process_images(self.spin_bgs.value(), self.spin_rats.value(), self.log)

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
