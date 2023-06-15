import datetime
import isodate
import os

from googleapiclient.discovery import build


class PlayList:

    def __init__(self, playlist_id: str) -> None:
        self.playlist = self.get_service().playlists().list(part="snippet,contentDetails", id=playlist_id).execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
        self.playlist_videos = self.get_service().playlistItems().list(
            playlistId=playlist_id,
            part='contentDetails',
            maxResults=50,
        ).execute()
        self.video_id: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=','.join(self.video_id)
                                                               ).execute()

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YOUTUBE_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def total_duration(self):
        """Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""
        total_time_videos = datetime.timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time_videos += duration
        return total_time_videos

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        like_count = 0
        for video in self.video_response['items']:
            video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                              id=video['id']).execute()
            if int(video_response['items'][0]['statistics']['likeCount']) > like_count:
                like_count = int(video_response['items'][0]['statistics']['likeCount'])
                self.video_url = video_response['items'][0]['id']

        return f'https://youtu.be/{self.video_url}'
