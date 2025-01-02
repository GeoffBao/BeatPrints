"""
LrcLib API 处理模块
"""
import requests
from typing import Dict, Any


class LrcLibAPI:
    def __init__(self, user_agent: str = "BeatPrints/1.0"):
        """初始化 LrcLib API
        
        Args:
            user_agent: 请求头中的 User-Agent
        """
        self.base_url = "https://lrclib.net/api"
        self.headers = {
            "User-Agent": user_agent
        }

    def search_lyrics(self, track_name: str, artist_name: str) -> Dict[str, Any]:
        """搜索歌词"""
        endpoint = f"{self.base_url}/search"
        params = {
            "track_name": track_name,
            "artist_name": artist_name
        }
        
        response = requests.get(endpoint, params=params, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"搜索歌词失败: {response.status_code}")
            
        return response.json()

    def get_lyrics(self, track_name: str, artist_name: str) -> str:
        """获取歌词"""
        try:
            results = self.search_lyrics(track_name, artist_name)
            print(f"\n调试 - API 返回结果: {results}")  # 保留调试信息
            
            if not results:
                raise Exception(f"找不到歌词: {track_name} - {artist_name}")
            
            lyrics = results[0].get('plainLyrics', '')
            
            if not lyrics:
                raise Exception(f"歌词内容为空: {track_name} - {artist_name}")
            
            return lyrics
        except Exception as e:
            print(f"\n调试 - 错误详情: {str(e)}")
            raise


# 导出类
__all__ = ['LrcLibAPI'] 