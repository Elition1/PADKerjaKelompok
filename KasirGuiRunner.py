import KasirGuiWindow

if __name__ == "__main__":
    mainWindow = KasirGuiWindow.KasirGuiWindow()
    mainWindow.window_initializer()
    mainWindow.draw_canvas()
    mainWindow.draw_widget()
    mainWindow.mainloop()