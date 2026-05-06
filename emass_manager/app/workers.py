from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool

class WorkerSignals(QObject):
    finished=pyqtSignal(object)

class ApiWorker(QRunnable):
    def __init__(self, fn):
        super().__init__(); self.fn=fn; self.signals=WorkerSignals()
    def run(self): self.signals.finished.emit(self.fn())

POOL=QThreadPool.globalInstance()
