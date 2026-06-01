import tkinter as tk
from tkinter import ttk
from KasirGuiWindow import KasirGuiWindow

class KasirGuiLogic:
    def __init__(self, windowKasir):
        self.windowKasir = windowKasir

    def non_background_effects(self, event = None):
        self.windowKasir.comboBoxCanvasLeft.selection_clear()
