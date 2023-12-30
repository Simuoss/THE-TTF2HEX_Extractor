from PySide6.QtWidgets import QApplication
from extractor import FontExtractorApp


if __name__ == "__main__":
    app = QApplication([])
    window = FontExtractorApp()
    window.show()
    app.exec()