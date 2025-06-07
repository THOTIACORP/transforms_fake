import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QSpinBox,
    QVBoxLayout, QHBoxLayout, QTextEdit, QFileDialog,
    QLineEdit, QGroupBox, QProgressBar, QDoubleSpinBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from .core import ImageTransformer


class ProcessingThread(QThread):
    """Thread para processamento das imagens sem bloquear a interface."""
    
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(dict)
    
    def __init__(self, transformer, params):
        super().__init__()
        self.transformer = transformer
        self.params = params
    
    def run(self):
        """Executa o processamento em thread separada."""
        try:
            def log_callback(text):
                self.log_signal.emit(text)
            
            stats = self.transformer.process_images(
                image_dir=self.params['image_dir'],
                mask_dir=self.params['mask_dir'],
                output_dir=self.params['output_dir'],
                num_backgrounds=self.params['num_backgrounds'],
                num_variations_per_background=self.params['num_variations'],
                rotation_range=self.params['rotation_range'],
                mask_classes=self.params['mask_classes'],
                log_callback=log_callback
            )
            
            self.finished_signal.emit(stats)
            
        except Exception as e:
            self.log_signal.emit(f"❌ Erro durante processamento: {str(e)}")
            self.finished_signal.emit({'error': str(e)})


class MainWindow(QWidget):
    """Interface gráfica principal para o transforms_fake."""
    
    def __init__(self):
        super().__init__()
        self.transformer = ImageTransformer()
        self.processing_thread = None
        self.init_ui()
        
    def init_ui(self):
        """Inicializa a interface do usuário."""
        self.setWindowTitle("Transforms Fake - Gerador de Variações de Imagem")
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        
        # Grupo de configuração de diretórios
        dir_group = QGroupBox("Diretórios")
        dir_layout = QVBoxLayout()
        
        # Diretório de imagens
        img_layout = QHBoxLayout()
        img_layout.addWidget(QLabel("Imagens:"))
        self.img_dir_edit = QLineEdit()
        self.img_dir_edit.setPlaceholderText("Selecione o diretório das imagens...")
        img_layout.addWidget(self.img_dir_edit)
        btn_img_dir = QPushButton("Procurar")
        btn_img_dir.clicked.connect(self.select_image_dir)
        img_layout.addWidget(btn_img_dir)
        dir_layout.addLayout(img_layout)
        
        # Diretório de máscaras
        mask_layout = QHBoxLayout()
        mask_layout.addWidget(QLabel("Máscaras:"))
        self.mask_dir_edit = QLineEdit()
        self.mask_dir_edit.setPlaceholderText("Selecione o diretório das máscaras...")
        mask_layout.addWidget(self.mask_dir_edit)
        btn_mask_dir = QPushButton("Procurar")
        btn_mask_dir.clicked.connect(self.select_mask_dir)
        mask_layout.addWidget(btn_mask_dir)
        dir_layout.addLayout(mask_layout)
        
        # Diretório de saída
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Saída:"))
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setPlaceholderText("Selecione o diretório de saída...")
        output_layout.addWidget(self.output_dir_edit)
        btn_output_dir = QPushButton("Procurar")
        btn_output_dir.clicked.connect(self.select_output_dir)
        output_layout.addWidget(btn_output_dir)
        dir_layout.addLayout(output_layout)
        
        dir_group.setLayout(dir_layout)
        layout.addWidget(dir_group)
        
        # Grupo de parâmetros
        params_group = QGroupBox("Parâmetros de Processamento")
        params_layout = QVBoxLayout()
        
        # Primeira linha de parâmetros
        params_row1 = QHBoxLayout()
        params_row1.addWidget(QLabel("Número de fundos:"))
        self.spin_fundos = QSpinBox()
        self.spin_fundos.setMinimum(1)
        self.spin_fundos.setMaximum(1000)
        self.spin_fundos.setValue(5)
        params_row1.addWidget(self.spin_fundos)
        
        params_row1.addWidget(QLabel("Variações por fundo:"))
        self.spin_ratos = QSpinBox()
        self.spin_ratos.setMinimum(1)
        self.spin_ratos.setMaximum(1000)
        self.spin_ratos.setValue(10)
        params_row1.addWidget(self.spin_ratos)
        params_layout.addLayout(params_row1)
        
        # Segunda linha de parâmetros
        params_row2 = QHBoxLayout()
        params_row2.addWidget(QLabel("Rotação mín (°):"))
        self.spin_rot_min = QDoubleSpinBox()
        self.spin_rot_min.setMinimum(-360)
        self.spin_rot_min.setMaximum(360)
        self.spin_rot_min.setValue(-180)
        params_row2.addWidget(self.spin_rot_min)
        
        params_row2.addWidget(QLabel("Rotação máx (°):"))
        self.spin_rot_max = QDoubleSpinBox()
        self.spin_rot_max.setMinimum(-360)
        self.spin_rot_max.setMaximum(360)
        self.spin_rot_max.setValue(180)
        params_row2.addWidget(self.spin_rot_max)
        params_layout.addLayout(params_row2)
        
        # Terceira linha - classes da máscara
        params_row3 = QHBoxLayout()
        params_row3.addWidget(QLabel("Classes da máscara:"))
        self.mask_classes_edit = QLineEdit("1,2,3")
        self.mask_classes_edit.setPlaceholderText("Ex: 1,2,3")
        params_row3.addWidget(self.mask_classes_edit)
        params_layout.addLayout(params_row3)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Área de log
        log_group = QGroupBox("Log do Processamento")
        log_layout = QVBoxLayout()
        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.setMaximumHeight(200)
        log_layout.addWidget(self.log_widget)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # Botões de ação
        button_layout = QHBoxLayout()
        
        self.btn_processar = QPushButton("Processar Imagens")
        self.btn_processar.clicked.connect(self.start_processing)
        self.btn_processar.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
        button_layout.addWidget(self.btn_processar)
        
        self.btn_parar = QPushButton("Parar")
        self.btn_parar.clicked.connect(self.stop_processing)
        self.btn_parar.setEnabled(False)
        self.btn_parar.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; padding: 10px; }")
        button_layout.addWidget(self.btn_parar)
        
        btn_limpar_log = QPushButton("Limpar Log")
        btn_limpar_log.clicked.connect(self.clear_log)
        button_layout.addWidget(btn_limpar_log)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def select_image_dir(self):
        """Seleciona o diretório de imagens."""
        dir_path = QFileDialog.getExistingDirectory(self, "Selecionar Diretório de Imagens")
        if dir_path:
            self.img_dir_edit.setText(dir_path)
    
    def select_mask_dir(self):
        """Seleciona o diretório de máscaras."""
        dir_path = QFileDialog.getExistingDirectory(self, "Selecionar Diretório de Máscaras")
        if dir_path:
            self.mask_dir_edit.setText(dir_path)
    
    def select_output_dir(self):
        """Seleciona o diretório de saída."""
        dir_path = QFileDialog.getExistingDirectory(self, "Selecionar Diretório de Saída")
        if dir_path:
            self.output_dir_edit.setText(dir_path)
    
    def validate_inputs(self):
        """Valida as entradas do usuário."""
        errors = []
        
        if not self.img_dir_edit.text().strip():
            errors.append("Diretório de imagens não foi selecionado")
        elif not os.path.exists(self.img_dir_edit.text()):
            errors.append("Diretório de imagens não existe")
        
        if not self.mask_dir_edit.text().strip():
            errors.append("Diretório de máscaras não foi selecionado")
        elif not os.path.exists(self.mask_dir_edit.text()):
            errors.append("Diretório de máscaras não existe")
        
        if not self.output_dir_edit.text().strip():
            errors.append("Diretório de saída não foi selecionado")
        
        if self.spin_rot_min.value() >= self.spin_rot_max.value():
            errors.append("Rotação mínima deve ser menor que a máxima")
        
        # Validar classes da máscara
        try:
            mask_classes_text = self.mask_classes_edit.text().strip()
            if not mask_classes_text:
                errors.append("Classes da máscara não podem estar vazias")
            else:
                mask_classes = [int(x.strip()) for x in mask_classes_text.split(',')]
                if not mask_classes:
                    errors.append("Pelo menos uma classe da máscara deve ser especificada")
        except ValueError:
            errors.append("Classes da máscara devem ser números separados por vírgula")
        
        return errors
    
    def get_processing_params(self):
        """Obtém os parâmetros para processamento."""
        mask_classes_text = self.mask_classes_edit.text().strip()
        mask_classes = [int(x.strip()) for x in mask_classes_text.split(',')]
        
        return {
            'image_dir': self.img_dir_edit.text().strip(),
            'mask_dir': self.mask_dir_edit.text().strip(),
            'output_dir': self.output_dir_edit.text().strip(),
            'num_backgrounds': self.spin_fundos.value(),
            'num_variations': self.spin_ratos.value(),
            'rotation_range': (self.spin_rot_min.value(), self.spin_rot_max.value()),
            'mask_classes': mask_classes
        }
    
    def start_processing(self):
        """Inicia o processamento das imagens."""
        # Validar entradas
        errors = self.validate_inputs()
        if errors:
            self.log_widget.clear()
            self.log_widget.append("❌ Erros de validação:")
            for error in errors:
                self.log_widget.append(f"   - {error}")
            return
        
        # Preparar interface para processamento
        self.btn_processar.setEnabled(False)
        self.btn_parar.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminado
        self.log_widget.clear()
        
        # Iniciar thread de processamento
        params = self.get_processing_params()
        self.processing_thread = ProcessingThread(self.transformer, params)
        self.processing_thread.log_signal.connect(self.add_log)
        self.processing_thread.finished_signal.connect(self.processing_finished)
        self.processing_thread.start()
    
    def stop_processing(self):
        """Para o processamento das imagens."""
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.terminate()
            self.processing_thread.wait()
            self.add_log("⏹️ Processamento interrompido pelo usuário")
            self.processing_finished({'interrupted': True})
    
    def add_log(self, text):
        """Adiciona texto ao log."""
        self.log_widget.append(text)
        self.log_widget.verticalScrollBar().setValue(
            self.log_widget.verticalScrollBar().maximum()
        )
    
    def clear_log(self):
        """Limpa o log."""
        self.log_widget.clear()
    
    def processing_finished(self, stats):
        """Chamado quando o processamento termina."""
        # Restaurar interface
        self.btn_processar.setEnabled(True)
        self.btn_parar.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        # Mostrar estatísticas finais
        if 'error' not in stats and 'interrupted' not in stats:
            self.add_log("\n🎉 Processamento concluído com sucesso!")
            self.add_log(f"📊 Estatísticas finais:")
            self.add_log(f"   - Imagens processadas: {stats.get('images_processed', 0)}")
            self.add_log(f"   - Variações criadas: {stats.get('total_variations_created', 0)}")
            self.add_log(f"   - Erros: {stats.get('images_with_errors', 0)}")


def main():
    """Função principal para executar a GUI."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()