from KasirGuiWindow import KasirGuiWindow
from KasirGuiLogic import KasirGuiLogic

if __name__ == "__main__":
    mainWindow = KasirGuiWindow()
    mainWindow.logic = KasirGuiLogic(mainWindow)
    mainWindow.window_initializer()
    mainWindow.draw_canvas()
    mainWindow.draw_widget()
    mainWindow.mainloop()