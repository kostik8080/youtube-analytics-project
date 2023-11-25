import datetime
from datetime import timedelta
import os

import isodate
from googleapiclient.discovery import build
import pprint


class APIMixin:
    __API_KEY: str = os.getenv('YT_API_KEY')

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.__API_KEY)


class PlayList(APIMixin):
    def __init__(self, playlist_id):
        super().__init__()
        self.playlist_id = playlist_id

        self.service = self.get_service()
        self.get_playlist = self.get_playlist_item_data()
        self.join = self.get_playlist['snippet']['title'].split()[:4]
        self.title = " ".join(self.join).strip(".")
        self.url = "https://www.youtube.com/playlist?list=PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw"
        self.videos = []


    def get_playlist_item_data(self):
        """
        Выводит информацию о плейлисте
        """
        playlist_info_response = self.service.playlistItems().list(
            part='snippet, contentDetails',
            playlistId=self.playlist_id,
            maxResults=1
        ).execute()

        playlist_info = playlist_info_response.get('items')[0]
        return playlist_info

    @property
    def total_duration(self):
        """
        Выводит продолжительность всех видео по времени
        """
        global result
        total = timedelta()
        playlist_id = self.playlist_id
        playlist_videos = self.service.playlistItems().list(playlistId=playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.service.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        # print(video_response)
        list_of_duration = []
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            durations = isodate.parse_duration(iso_8601_duration)
            list_of_duration.append(durations)
            result = sum(list_of_duration, datetime.timedelta())
        return result


    def show_best_video(self):
        """
        Выводит лучшее видедо по лайкам из плейлиста
        """
        playlist_id = self.playlist_id
        playlist_videos = self.service.playlistItems().list(playlistId=playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.service.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        max_like = 0
        max_video_id = 0
        for videos in video_response["items"]:
            like_count = videos["statistics"]["likeCount"]
            video_id = videos["id"]
            if int(like_count) > int(max_like):
                max_like = like_count
                max_video_id = video_id
        return f"https://youtu.be/{max_video_id}"




