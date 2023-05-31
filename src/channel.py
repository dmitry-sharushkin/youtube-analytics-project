import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._channel_id = channel_id
        self.title = None
        self.description = None
        self.url = None
        self.subscribers_count = None
        self.video_count = None
        self.view_count = None
        self._get_channel_info()

    @property
    def channel_id(self):
        return self._channel_id

    def _get_channel_info(self) -> None:
        """Заполняет атрибуты экземпляра данными о канале."""
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()
        channel_info = channel['items'][0]
        self.title = channel_info['snippet']['title']
        self.description = channel_info['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self._channel_id}"
        self.subscribers_count = int(channel_info['statistics']['subscriberCount'])
        self.video_count = int(channel_info['statistics']['videoCount'])
        self.view_count = int(channel_info['statistics']['viewCount'])

    @classmethod
    def get_service(cls, api_key: str = os.getenv('YOUTUBE_API_KEY')):
        """Возвращает объект для работы с YouTube API."""
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file_path: str) -> None:
        """Сохраняет в файл значения атрибутов экземпляра Channel."""
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(self.__dict__, f, indent=2, ensure_ascii=False)

        print(f"Данные канала {self.title} сохранены в файл {file_path}")

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))
