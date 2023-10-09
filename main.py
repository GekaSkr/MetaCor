
import os
from PIL import Image

folder_path = input("Input Folder Path: ")

# Указываем путь к новой папке
input_new_folder = input("Input New Folder Name for copies with new metadata (or skip and press Enter and files will be rewrited): ")
new_folder_path = folder_path + input_new_folder+"\\"

# Проверяем, существует ли папка, и если нет, то создаем её
if not os.path.exists(new_folder_path):
    os.makedirs(new_folder_path)
else:
    pass


# Получите список файлов в папке
file_list = os.listdir(folder_path)
print(file_list)

#Функция проверки, является ли файл изображением или папкой
def is_image(file_path):
    try:
        # Попытка открыть файл как изображение
        image = Image.open(file_path)
        image.close()  # Закрываем изображение после проверки
        return True
    except Exception:
        return False


# проходим по каждому файлу, открывам, вносим изменения и закрываем
for file in file_list:

    full_path = folder_path + file

    #Проверяем является ли файл изображением при помощи функци выше, если нет то ничего не делаем
    if is_image(full_path):
        image = Image.open(full_path)
        EXIF = image.getexif()
        INFO = image.info
        dpi = INFO.get("title")
        print(dpi)

        # открываем, декодируем, делаем изменения, кодируем, переназначаем новый параметр в словаре exif
        title = EXIF.get(40091)
        print("EXIF", EXIF)
        if title:
            title_decoded = title.decode('utf-16')
            title_decoded = title_decoded.title()
            title_decoded = title_decoded.replace("\x00","")
            title_encoded = title_decoded.encode('UTF-16le') #использовать кодировку 16le

            EXIF[40091] = title_encoded
            print("EXIF", EXIF[40091])

        # открываем, делаем изменения, переназначаем новый параметр в словаре exif
        description = EXIF.get(270)
        description = description.title() #все слова начинаются с заглавных букв
        print('DES', description)


        description_generative = description + ", Slow Motion"
        description_generative = description_generative.replace("\x00", "") #нужно обязательно очистить от непечатаемых символов, она не сработает
        description_generative_encoded = description_generative.encode('UTF-16le') #использовать кодировку 16le


        # Если в исходном у нас строка, то выполняем, иначе ошибка
        if type(description) is str :
            EXIF[40095] = description_generative_encoded
            EXIF[270] = description_generative

        else:
            print("Descriptoin non str in file:", file)

        # открываем, декодируем, делаем изменения, кодируем, переназначаем новый параметр в словаре exif
        keywords = EXIF.get(40094)
        if keywords:
            keywords_decoded = keywords.decode('utf-16')
            keywords_decoded = keywords_decoded.replace("\x00", "") #нужно обязательно очистить от непечатаемых символов, она не сработает
            add_ai_words = ""
            keyword_AI = keywords_decoded + add_ai_words

            print("keyword_AI", keyword_AI)
            keyword_AI_encoded = keyword_AI.encode('utf-16le')
            EXIF[40094] = keyword_AI_encoded




        # Устанавливаем параметры сохранения
        save_options = {
            'format': 'JPEG',            # Формат файла (например, JPEG, PNG, GIF)
            'quality': 100,              # Качество JPEG (от 0 до 100)
            "subsampling": 0,            # Параметр пересчета в JPEG, 0 для сохранения без пересчета
            'dpi': (300, 300),           # DPI (dots per inch)
            'compress_level': 100,       # Уровень сжатия (для форматов, поддерживающих сжатие, таких как JPEG)
            'optimize': False,           # Оптимизация (только для форматов, поддерживающих оптимизацию, таких как PNG)
            'exif': EXIF,  # EXIF-данные (если они есть)
        }


        # Сохраняем изображение с параметрами
        new_file_path = (new_folder_path +

                         file)
        image.save(new_file_path, **save_options)

        # Закрываем изображение (необязательно, но рекомендуется)
        image.close()
