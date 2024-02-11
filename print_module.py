import matplotlib.pyplot as plt
import textwrap
import os
from escpos.printer import Usb
import time

# Настройки
BASE_WIDTH = 350
PRINTER_VENDOR_ID = 0x1fc9
PRINTER_PRODUCT_ID = 0x2016
ALIGN_MODE = 'left'  # Режим выравнивания: 'left', 'center', 'right'


def create_image_with_text(text, font_size, filename='text_image.png'):
    """Создает изображение с текстом жирным шрифтом."""
    char_per_line = BASE_WIDTH / (font_size * 0.65)
    lines = text.split('\n')
    wrapped_lines = [line for text_line in lines for line in textwrap.wrap(text_line, width=int(char_per_line))]

    line_height = font_size * 1.5
    image_height = int(line_height * len(wrapped_lines)) + 40

    plt.figure(figsize=(BASE_WIDTH / 100, image_height / 100), dpi=100)
    # Задаем стиль шрифта (жирный)
    font_properties = {'weight': 'normal', 'size': font_size}
    for i, line in enumerate(wrapped_lines):
        plt.text(0, 1 - (i * line_height) / image_height, line, ha='left', va='top', fontdict=font_properties, wrap=False)

    plt.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close()
    return filename


def print_text(text_to_print, font_size=18, end_blank_lines=3):
    """Печатает текст с использованием принтера."""
    try:
        printer = Usb(PRINTER_VENDOR_ID, PRINTER_PRODUCT_ID)
        printer.set(font='a', align=ALIGN_MODE, height=5)

        # Разделение текста на блоки
        blocks = text_to_print.split('\r\n\r\n')

        for block in blocks:
            if block.strip():  # Проверяем, не является ли блок пустым
                image_path = create_image_with_text(block, font_size)
                printer.image(image_path)
                os.remove(image_path)  # Удаление временного файла изображения  # Явное разделение между изображениями
                printer.text("\n")
            else:
                printer.text("\n")  # Дополнительная пустая строка  # Небольшая задержка для обработки принтером

                # Печать пустых строк в конце
        printer.text("\n" * end_blank_lines)

    except Exception as e:
        raise e
    finally:
        printer.close()


def print_image(image_path):
    """Печатает изображение."""
    try:
        printer = Usb(PRINTER_VENDOR_ID, PRINTER_PRODUCT_ID)
        printer.set(font='a', align=ALIGN_MODE, height=6)

        printer.image(image_path)

    except Exception as e:
        raise e
    finally:
        printer.close()
