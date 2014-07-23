import sfml as sf

# fonts

font_8bit = sf.Font.from_file("content/fonts/8bit.ttf")

# images

textures = {}
textures["tree"] = sf.Texture.from_file("content/textures/tree.png")
textures["button"] = sf.Texture.from_file("content/gui/button.png")