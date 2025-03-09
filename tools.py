from langdetect import detect, detect_langs
import time
import re

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
    
    # Разделяем текст на предложения
    sentences = sentence_endings.split(text)
    
    result = []
    for sentence in sentences:
        # Если предложение больше 2000 символов
        if len(sentence) > 2000:
            parts = []
            start = 0
            while start < len(sentence):
                # Ищем позицию первого пробела после start
                space_pos = sentence.find(' ', start)
                if space_pos == -1:  # Если пробелов нет, берём оставшуюся часть
                    parts.append(sentence[start:])
                    break
                elif space_pos - start > 2000:  # Если часть снова больше 2000 символов
                    parts.append(sentence[start:space_pos])
                    start = space_pos + 1
                else:
                    parts.append(sentence[start:space_pos])
                    start = space_pos + 1
            result.extend(parts)
        
        # Если предложение больше 1500 символов
        elif len(sentence) > 1500:
            newline_pos = sentence.find('\n')
            if newline_pos != -1:
                result.append(sentence[:newline_pos])
                remainder = sentence[newline_pos+1:]
                if remainder:
                    result.append(remainder)
            else:
                result.append(sentence)
        
        else:
            result.append(sentence)
    
    return result
