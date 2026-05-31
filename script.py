from PIL import Image

ICON_PATH = "img/icon.jpg"

Image.open(ICON_PATH).save("icon.ico", format = "ICO")
