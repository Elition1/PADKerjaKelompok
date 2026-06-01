from KasirGuiWindow import KasirGuiWindow
from KasirGuiLogic import KasirGuiLogic

if __name__ == "__main__":
    mainWindow = KasirGuiWindow()
    mainWindow.window_initializer()
    mainWindow.logic = KasirGuiLogic(mainWindow)
    mainWindow.draw_canvas()
    mainWindow.draw_widget()
    mainWindow.logic.footer_data()
    mainWindow.mainloop()