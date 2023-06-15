import os

from googleapiclient.discovery import build


class Video:
    """ Класс для видео"""

    def __init__(self, video_id):
        """Экземпляр инициализируется реальными данными."""
        self.video_id = video_id
        video_response = self._get_video_info()
        self.title = video_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/videos/{self.video_id}'
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """Выводит название канала"""
        return self.title

    def _get_video_info(self):
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=self.video_id
                                                          ).execute()
        return video_response

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class PLVideo(Video):
    """Второй класс для видео (плейлисты)"""

    def __init__(self, video_id, playlist_id):

        super().__init__(video_id)
        self.playlist_id = playlist_id
