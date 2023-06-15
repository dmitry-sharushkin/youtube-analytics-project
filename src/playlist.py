import os
import datetime

import isodate
from googleapiclient.discovery import build


class PlayList:
    """Класс, который инициализируется по id плейлиста"""

    def __init__(self, playlist_id: str):
        """Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API."""
        self.playlist_id = playlist_id
        playlist_videos = self._get_playlist_info()
        video_response = self._get_videos()
        self.title = playlist_videos['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.like_count_video = video_response['items'][0]['statistics']['likeCount']

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def _get_playlist_info(self):
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails,snippet',
                                                                  maxResults=50, ).execute()
        return playlist_videos

    def _get_videos(self):
        """Заполняет список видео в плейлисте."""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)
                                                          ).execute()
        return video_response

    @property
    def total_duration(self):
        """Возвращает суммарную длительность плейлиста."""
        total_duration = datetime.timedelta()
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            time = str(duration).split(":")
            duration = datetime.timedelta(hours=int(time[0]), minutes=int(time[1]), seconds=int(time[2]))
            total_duration += duration
            return total_duration

    def __str__(self):
        """Метод возвращает общую продолжительность play-листа"""
        return self.total_duration

    def show_best_video(self) -> str:
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)."""
        self.like_count_video = video_response['items'][0]['statistics']['likeCount'].sort(reverse=True)
        max_like_video = self.like_count_video[0]
        return max_like_video
