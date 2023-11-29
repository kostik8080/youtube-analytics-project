import json
import os
from src import playlist
# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

import isodate

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video(playlist.APIMixin):

    def __init__(self, id_video):
        self.__id_video = id_video
        self.service = self.get_service()
        self.channel_data = self.get_channel_data()
        self.title = self.channel_data[0]
        self.url = f"https://youtu.be/{self.id_video}"
        self.view_count = self.channel_data[1]
        self.like_count = self.channel_data[2]




    @property
    def id_video(self):
        return self.__id_video

    # @classmethod
    # def get_service(cls):
    #     api_service_name = "youtube"
    #     api_version = "v3"
    #     DEVELOPER_KEY = api_key
    #     return build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    def get_channel_data(self):
        list_value = []
        video_id = self.id_video
        try:
            request = self.service.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                 id=video_id
                                                 ).execute()
            title_video: str = request['items'][0]['snippet']['title']
            list_value.append(title_video)
            view_count: int = request['items'][0]['statistics']['viewCount']
            list_value.append(view_count)
            like_count: int = request['items'][0]['statistics']['likeCount']
            list_value.append(like_count)
        except IndexError:
            list_value.append(None)
            list_value.append(None)
            list_value.append(None)
        return list_value

    def __str__(self):
        return f"{self.title}"


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
        return f"{self.title}"


broken_video = Video('broken_video_id')
assert broken_video.title is None
assert broken_video.like_count is None

