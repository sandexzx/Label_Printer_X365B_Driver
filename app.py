from flask import Flask, render_template, request, jsonify
import print_module
import os
from urllib.parse import unquote_plus

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Папка для сохранения загруженных файлов
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Создать папку, если она не существует


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Запрос POST получен")
        text_to_print = request.form['text']
        print("Received text:", text_to_print)  # Вывод для отладки
        font_size = int(request.form.get('fontSize', 18))
        end_blank_lines = int(request.form.get('endBlankLines', 3))
        text_to_print = unquote_plus(text_to_print)

        image_file = request.files.get('image')  # Изменено на .get() для обработки случая отсутствия файла

        try:
            if image_file and image_file.filename != '':
                image_filename = image_file.filename
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image_file.save(image_path)
                print_module.print_image(image_path)  # Печать изображения

            if text_to_print:
                # передать декодированный текст в функцию печати
                print_module.print_text(text_to_print, font_size, end_blank_lines)

            return "Задание отправлено на печать"
        except Exception as e:
            return f"Произошла ошибка: {e}"

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='192.168.0.120')
