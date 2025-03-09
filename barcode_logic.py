import random
import string


from barcode import Code128
from barcode.writer import ImageWriter



def generate_barcode_image():
    data = generate_data()

    path = Code128(data, writer=ImageWriter())
    path.save(f"C:/Users/Admin/Documents/freshtopia/barcde_images/{data}", options=barcode_option()) ## <-------------------- ilisanan nga directory 
    return path


def generate_data():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def barcode_option():
    return dict(module_width=0.2, module_height=6, quiet_zone=3, font_size=6, text_distance=5,
                background='white', foreground='black', center_text=True, format='PNG')




