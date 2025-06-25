import os
import yaml
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QMessageBox, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect,
    QFrame
)
from PyQt5.QtGui import QPixmap, QFont, QLinearGradient, QPalette, QColor, QPainter, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QRect
from .quiz import QuizWindow

CONFIG_PATH = os.path.join("config", "config.yaml")

def get_version():
    try:
        with open(CONFIG_PATH, "r") as f:
            cfg = yaml.safe_load(f)
        return str(cfg.get("version", "1.0.0"))
    except Exception:
        return "Error Fetching Version"

class AnimatedButton(QPushButton):
    """Custom button with hover animations and modern styling"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMouseTracking(True)
        
        # Apply shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(0, 4)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)
    
    def enterEvent(self, event):
        # Just trigger the CSS hover state, no geometry changes
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        # Just trigger the CSS hover state, no geometry changes
        super().leaveEvent(event)

class GradientFrame(QFrame):
    """Custom frame with gradient background"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(245, 247, 250))
        gradient.setColorAt(1, QColor(255, 255, 255))
        painter.fillRect(self.rect(), gradient)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EigenPrep - Quantitative Interview Preparation")
        self.setMinimumSize(1000, 750)
        self.version = get_version()
        
        # Set window icon
        icon_path = os.path.join("assets", "eigenprep-nav.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.quiz_window = None
        self.init_ui()
        self.apply_modern_styling()
    
    def init_ui(self):
        # Main container with gradient background
        main_container = GradientFrame()
        container_layout = QVBoxLayout(main_container)
        container_layout.setContentsMargins(50, 50, 50, 50)
        container_layout.setSpacing(40)
        
        # Header section with improved layout
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 25, 30, 25)
        
        # Logo section
        logo_section = QVBoxLayout()
        logo_path = os.path.join("assets", "eigenprep.png")
        
        if os.path.exists(logo_path):
            #pixmap = QPixmap(logo_path).scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pixmap = QPixmap(logo_path).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo = QLabel()
            logo.setPixmap(pixmap)
            logo.setFixedSize(250, 250)
            
            # Add shadow to logo
            logo_shadow = QGraphicsDropShadowEffect()
            logo_shadow.setOffset(0, 2)
            logo_shadow.setBlurRadius(10)
            logo_shadow.setColor(QColor(0, 0, 0, 30))
            logo.setGraphicsEffect(logo_shadow)
        else:
            logo = QLabel("EigenPrep")
            logo.setFont(QFont("Segoe UI", 32, QFont.Bold))
            logo.setStyleSheet("color: #215bbb; margin: 10px;")
        
        logo_section.addWidget(logo, alignment=Qt.AlignCenter)
        header_layout.addLayout(logo_section)
        
        # Info section
        info_section = QVBoxLayout()
        info_section.setSpacing(15)
        
        title = QLabel("Quantitative Interview Preparation")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        
        subtitle = QLabel("Master brain teasers, mathematical concepts, and finance questions")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: #7f8c8d; line-height: 1.4;")
        subtitle.setWordWrap(True)
        
        features = QLabel("• Interactive quizzes with detailed explanations\n• Timed assessments to simulate real interviews\n• Track your progress and identify weak areas")
        features.setFont(QFont("Segoe UI", 12))
        features.setStyleSheet("color: #34495e; margin-top: 10px; line-height: 1.6;")
        
        info_section.addWidget(title)
        info_section.addWidget(subtitle)
        info_section.addWidget(features)
        info_section.addStretch()
        
        header_layout.addLayout(info_section, 2)
        container_layout.addWidget(header_frame)
        
        # Buttons section
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 15px;
            }
        """)
        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(40, 30, 40, 30)
        buttons_layout.setSpacing(20)
        
        # Button configurations
        button_configs = [
            ("Start Quiz", "Begin your quantitative practice session", True, self.start_quiz),
            ("Online Assessment", "Take a timed mock interview assessment", True, self.start_oa),
            ("View Statistics", "Track your progress and performance", False, None),
            ("Settings", "Customize your learning experience", False, None),
            ("Exit Application", "Close EigenPrep", True, self.close)
        ]
        
        for text, description, enabled, callback in button_configs:
            btn_container = QVBoxLayout()
            btn_container.setSpacing(8)
            
            btn = AnimatedButton(text)
            btn.setFixedHeight(65)
            btn.setFont(QFont("Segoe UI", 14, QFont.Medium))
            btn.setEnabled(enabled)
            
            if callback:
                btn.clicked.connect(callback)
            
            # Description label
            desc_label = QLabel(description)
            desc_label.setFont(QFont("Segoe UI", 11))
            desc_label.setStyleSheet("color: #7f8c8d; margin-left: 5px; margin-bottom: 5px;")
            
            btn_container.addWidget(btn)
            btn_container.addWidget(desc_label)
            
            buttons_layout.addLayout(btn_container)
        
        container_layout.addWidget(buttons_frame)
        container_layout.addStretch()
        
        # Footer
        footer_frame = QFrame()
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(20, 15, 20, 15)
        
        built_by = QLabel("Built by CU Quants")
        built_by.setFont(QFont("Segoe UI", 11))
        built_by.setStyleSheet("color: #7f8c8d;")
        
        version_label = QLabel(f"Version {self.version}")
        version_label.setFont(QFont("Segoe UI", 11))
        version_label.setStyleSheet("color: #7f8c8d;")
        
        footer_layout.addWidget(built_by)
        footer_layout.addStretch()
        footer_layout.addWidget(version_label)
        
        container_layout.addWidget(footer_frame)
        
        # Set main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(main_container)
    
    def apply_modern_styling(self):
        """Apply modern styling to the entire application"""
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            AnimatedButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px 25px;
                font-weight: 500;
                text-align: left;
            }
            
            AnimatedButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
            
            AnimatedButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #1f618d);
            }
            
            AnimatedButton:disabled {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #bdc3c7, stop:1 #95a5a6);
                color: #7f8c8d;
            }
            
            QLabel {
                background: transparent;
            }
        """)
    
    def start_quiz(self):
        try:
            self.quiz_window = QuizWindow(main_window=self)
            self.quiz_window.setAttribute(Qt.WA_DeleteOnClose)
            self.hide()
            self.quiz_window.show()
        except Exception as e:
            print("Error launching QuizWindow:", e)
    
    def start_oa(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Online Assessment")
        msg.setText("Assessment mode is being prepared!")
        msg.setInformativeText("This feature will simulate real interview conditions with timed questions and comprehensive scoring.")
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                font-family: 'Segoe UI';
            }
            QMessageBox QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: 500;
            }
            QMessageBox QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        msg.exec_()