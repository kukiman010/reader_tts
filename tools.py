from langdetect import detect, detect_langs
import time
import re, os
import stat

def get_time_string():
    current_time = time.time()
    time_struct = time.localtime(current_time)
    milliseconds = int((current_time - int(current_time)) * 1000)
    return time.strftime("%Y%m%d_%H%M%S", time_struct) + f"_{milliseconds:03d}"


def split_text(text):
    max_message_length = 2500
    hard_break_point = 2200
    soft_break_point = 1800
    results = []

    while len(text) > max_message_length:
        offset = text[soft_break_point:hard_break_point].rfind('\n')
        if offset == -1:
            offset = text[soft_break_point:max_message_length].rfind(' ')
        if offset == -1:
            results.append(text[:max_message_length])
            text = text[max_message_length:]
        else:
            original_index = offset + soft_break_point
            results.append(text[:original_index])
            text = text[original_index:]

    if text:
        results.append(text)

    return results


# Определяем наиболее вероятный язык текста
def detect_language(text):
    try:
        language = detect(text)
        return language
    except Exception as e:
        print(str(e))
        return None


# Определяем вероятности для всех возможных языков текста
def detect_multiple_languages(text):
    try:
        languages = detect_langs(text)
        return languages
    except Exception as e:
        print(str(e))
        return None
        

def split_text_sentences(text):
    sentence_endings = re.compile(r'(?<=[.!?])\s')

    max_message_length = 980
    hard_break_point = 650
    
    sentences = sentence_endings.split(text)
    
    result = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) == 0:
            continue

        # Если предложение длинное, разбиваем его на части
        if len(sentence) > max_message_length:
            parts = []
            start = 0
            while start < len(sentence):
                # Последний возможный пробел, до предела
                end = min(start + max_message_length, len(sentence))
                space_pos = sentence.rfind(' ', start, end)
                if space_pos == -1:
                    space_pos = end
                parts.append(sentence[start:space_pos])
                start = space_pos + 1
            result.extend(parts)
        
        elif len(sentence) > hard_break_point:
            newline_pos = sentence.find('\n')
            if newline_pos != -1 and newline_pos < hard_break_point:
                result.append(sentence[:newline_pos])
                remainder = sentence[newline_pos+1:]
                if remainder:
                    result.append(remainder)
            else:
                result.append(sentence)
        
        else:
            result.append(sentence)
    
    return result


def remove_file(path):
    try:
        # Удаление файла
        os.chmod(path, stat.S_IWUSR | stat.S_IRUSR)
        os.remove(path)
        print(f"Файл {path} успешно удалён.")
    except FileNotFoundError:
        print(f"Файл {path} не найден.")
    except PermissionError:
        print(f"Нет разрешения на удаление файла {path}.")
    except Exception as e:
        print(f"Ошибка: {e}")