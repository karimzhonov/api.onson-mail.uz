import qrcode, io, base64
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw


def round_corners(img, radius):
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, img.size[0], img.size[1]), radius, fill=255)
    rounded_img = Image.new("RGBA", img.size)
    rounded_img.paste(img, (0, 0), mask=mask)
    return rounded_img


def _url(pk):
    return "https://onson-mail.uz/qrcode/?order_id={}".format(pk)


def generate_qrcode(pk):

    # Создание QR-кода
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(_url(pk))
    qr.make(fit=True)

    # Генерация QR-кода с закруглёнными модулями и глазами
    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),  # Закруглённые модули
        eye_drawer=RoundedModuleDrawer(radius_ratio=1),  # Закруглённые глаза
        color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(0, 0, 0))
    ).convert("RGBA")

    # Открываем логотип и добавляем белый фон
    logo = Image.open("contrib/assets/logo.png").convert("RGBA")
    logo_size = qr_img.size[0] // 4  # Размер логотипа (примерно 1/4 QR-кода)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # Создаём белый фон для логотипа
    white_bg = Image.new("RGB", logo.size, (255, 255, 255))
    white_bg.paste(logo, (0, 0), mask=logo)  # Вставляем логотип поверх белого фона

    # Закругляем углы логотипа
    logo_rounded = round_corners(white_bg, radius=15)

    # Закругляем углы самого QR-кода
    qr_img = round_corners(qr_img, radius=50)

    # Вставляем логотип в центр QR-кода
    qr_center = qr_img.size[0] // 2
    pos = (qr_center - logo_size // 2, qr_center - logo_size // 2)
    qr_img.paste(logo_rounded, pos, mask=logo_rounded)
    file = io.BytesIO()
    # Сохранение QR-кода
    qr_img.save(file, format="png")
    return base64.b64encode(file.getvalue()).decode()
