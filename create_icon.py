from PIL import Image, ImageDraw

def create_feather_icon():
    """Создать иконку пера в разных размерах для .ico"""
    sizes = [16, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Масштабируем координаты
        scale = size / 64

        # Перо (стилизованное)
        points = [
            (int(48 * scale), int(8 * scale)),
            (int(52 * scale), int(16 * scale)),
            (int(20 * scale), int(52 * scale)),
            (int(12 * scale), int(56 * scale)),
            (int(8 * scale), int(52 * scale)),
            (int(44 * scale), int(12 * scale)),
        ]
        draw.polygon(points, fill=(70, 130, 180, 255), outline=(50, 100, 150, 255))

        # Стержень пера
        draw.line([
            (int(12 * scale), int(56 * scale)),
            (int(6 * scale), int(62 * scale))
        ], fill=(139, 69, 19, 255), width=max(1, int(3 * scale / 2)))

        # Блик на пере
        draw.line([
            (int(42 * scale), int(18 * scale)),
            (int(24 * scale), int(42 * scale))
        ], fill=(135, 180, 220, 255), width=max(1, int(2 * scale / 2)))

        images.append(image)

    # Сохраняем как .ico
    images[0].save('icon.ico', format='ICO', sizes=[(s, s) for s in sizes], append_images=images[1:])
    print("icon.ico создан!")

if __name__ == '__main__':
    create_feather_icon()
