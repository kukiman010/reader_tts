import json
# import os
# import re
from pathlib import Path
from typing import Dict, Optional

from tools import split_text_sentences

class Sentence:
    def __init__(self, book_id: str, chapter_id: str, position: int, text: str, 
                 audio_path: Optional[str] = None, audio_format: str = 'mp3',
                 audio_duration: float = 0.0):
        self.book_id = book_id
        self.chapter_id = chapter_id
        self.position = position
        self.text = text.strip()
        self.audio_path = audio_path
        self.audio_format = audio_format
        self.audio_duration = audio_duration

    def to_dict(self) -> Dict:
        return {
            'position': self.position,
            'text': self.text,
            'audio_path': self.audio_path,
            'audio_format': self.audio_format,
            'audio_duration': self.audio_duration
        }

    @classmethod
    def from_dict(cls, data: Dict, book_id: str, chapter_id: str):
        return cls(
            book_id=book_id,
            chapter_id=chapter_id,
            position=data['position'],
            text=data['text'],
            audio_path=data.get('audio_path'),
            audio_format=data.get('audio_format', 'mp3'),
            audio_duration=data.get('audio_duration', 0.0)
        )


class Chapter:
    def __init__(self, chapter_id: str, title: Optional[str] = None):
        self.chapter_id = chapter_id
        self.title = title
        self.sentences = []

    def add_sentence(self, sentence: Sentence):
        expected_position = len(self.sentences) + 1
        if sentence.position != expected_position:
            raise ValueError(f"Invalid sentence position: expected {expected_position}, got {sentence.position}")
        self.sentences.append(sentence)

    def __iter__(self):
        return iter(self.sentences)

    def __len__(self):
        return len(self.sentences)

    def to_dict(self) -> Dict:
        return {
            'chapter_id': self.chapter_id,
            'title': self.title,
            'sentences': [s.to_dict() for s in self.sentences]
        }

    @classmethod
    def from_dict(cls, data: Dict):
        chapter = cls(data['chapter_id'], data['title'])
        chapter.sentences = data['sentences'] 
        return chapter


class Book:
    def __init__(self, book_id: str, title: str, author: str, **metadata):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.metadata = metadata
        self.chapters: Dict[str, Chapter] = {}
        self.storage_path = f"books/{self.book_id}"

    def add_metadata(self, key, value):
        self.metadata[key] = value


    def save_to_disk(self, base_path: str = "books"):
        book_dir = Path(base_path) / self.book_id
        book_dir.mkdir(parents=True, exist_ok=True)
        
        meta = {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'metadata': self.metadata,
            'chapters': [ch.to_dict() for ch in self.chapters.values()]
        }

        with (book_dir / "meta.json").open('w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)


    @classmethod
    def load_from_disk(cls, book_id: str, base_path: str = "books"):
        book_dir = Path(base_path) / book_id
        meta_file = book_dir / "meta.json"

        with meta_file.open('r', encoding='utf-8') as f:
            meta = json.load(f)

        book = cls(
            book_id=meta['book_id'],
            title=meta['title'],
            author=meta['author'],
            **meta['metadata']
        )

        for ch_data in meta['chapters']:
            chapter = Chapter.from_dict(ch_data)
            book.chapters[chapter.chapter_id] = chapter

            # Восстанавливаем предложения как объекты Sentence
            chapter.sentences = [
                Sentence.from_dict(s_data, book_id=book.book_id, chapter_id=chapter.chapter_id)
                for s_data in ch_data['sentences']
            ]

        return book


    def add_chapter(self, chapter_id: str, title: Optional[str] = None) -> Chapter:
        if chapter_id in self.chapters:
            raise ValueError(f"Chapter {chapter_id} already exists")
        chapter = Chapter(chapter_id, title)
        self.chapters[chapter_id] = chapter
        return chapter

    def add_sentence(self, chapter_id: str, text: str) -> Sentence:
        chapter = self.chapters.get(chapter_id)
        # if not chapter:
            # chapter = self.add_chapter(chapter_id)
        
        # Исправленный расчет позиции
        position = len(chapter) + 1  # Теперь используем __len__ из Chapter
        sentence = Sentence(
            book_id=self.book_id,
            chapter_id=chapter_id,
            position=position,
            text=text
        )
        chapter.add_sentence(sentence)
        return sentence

    # def load_text(self, text: str, 
    #              chapter_pattern: str = r"^\s*## Chapter (\S+)(:.*?)?\s*$", 
    #              sentence_delimiters: str = r'(?<=[.!?])\s+'):
    #     current_chapter = None
        
    #     for line in text.split('\n'):
    #         line = line.strip()
    #         if not line:
    #             continue

    #         # Проверяем, является ли строка заголовком главы
    #         chapter_match = re.match(chapter_pattern, line, re.IGNORECASE)
    #         if chapter_match:
    #             chapter_id = chapter_match.group(1).strip()
    #             chapter_title = chapter_match.group(2).strip()[1:].strip() if chapter_match.group(2) else None
    #             current_chapter = self.add_chapter(chapter_id, chapter_title)
    #             continue

    #         if not current_chapter:
    #             raise ValueError(f"Текст вне главы: '{line}'")

    #         # Разделяем строку на предложения
    #         sentences = re.split(sentence_delimiters, line)
    #         for sentence in sentences:
    #             if sentence.strip():
    #                 self.add_sentence(current_chapter.chapter_id, sentence.strip())

    #     return self

    def iter_sentences(self):
        for chapter in self.chapters.values():
            yield from chapter
           

    def load_text(self, text: str):

        sentences = split_text_sentences(text)
        self.add_chapter(1,"1")
        for i, sentence in enumerate(sentences):
            if sentence:
                self.add_sentence(1, sentence)





# class Book:
#     def __init__(self):
#         self.name = ''
#         self.autor = ''
#         self.publication = ''
#         self.dataRelease = 0
#         self.fileText = ''



# text = """
# ## Chapter 1
# First sentence. Second sentence!
# ## Chapter 2: My Chapter
# Third sentence? Fourth sentence.
# """

# book = Book("test", "Test Book", "Author")
# book.load_text(text)

# for chapter in book.chapters.values():
#     title = f" {chapter.title}" if chapter.title else ""
#     print(f"Глава {chapter.chapter_id}{title}:")
#     for sentence in chapter.sentences:
#         print(f"- {sentence.text}")

# book.save_to_disk()


# book = Book.load_from_disk('80e91dbb-9bb8-429f-a8cf-8352e64f03d5')

# print()