import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

import isodate

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:

    def __init__(self, id_video):
        self.__id_video = id_video
        self.service = self.get_service()
        self.channel_data = self.get_channel_data()
        self.title_video = self.channel_data['snippet']['title']
        self.url = f"https://youtu.be/{self.id_video}"
        self.count_views = self.channel_data['statistics']['viewCount']
        self.count_likes = self.channel_data['statistics']['likeCount']

    @property
    def id_video(self):
        return self.__id_video

    @classmethod
    def get_service(cls):
        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = api_key
        return build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    def get_channel_data(self):
        request = self.service.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                             id=self.id_video
                                             ).execute()
        return request['items'][0]

    def __str__(self):
        return f"{self.title_video}"


class PLVideo(Video):

    def __init__(self, id_video, pl_id):
        super().__init__(id_video)
        self.__pl_id = pl_id


    @property
    def pl_id(self):
        return self.__pl_id

    def get_playlist_item_data(self):
        playlist_info_response = self.service.playlistItems().list(
            part='snippet',
            playlistId=self.pl_id,
            maxResults=1
        ).execute()

        playlist_info = playlist_info_response.get('items')[0]
        return playlist_info

    def __str__(self):
        return f"{self.title_video}"




