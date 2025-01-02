"""
歌词处理模块
"""
import os
import re
from typing import List
from .spotify import TrackMetadata
from .lrclib import LrcLibAPI  # 修改这里，使用相对导入


class Lyrics:
    def __init__(self):
        self.lrclib = LrcLibAPI(user_agent="BeatPrints/1.0")

    def get_lyrics(self, track: TrackMetadata) -> str:
        """获取歌词"""
        try:
            return self.lrclib.get_lyrics(track.name, track.artist)
        except Exception as e:
            raise Exception(f"获取歌词失败: {str(e)}")

    def select_lines(self, lyrics: str, selection: str) -> List[str]:
        """选择歌词行"""
        lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
        
        if selection:
            selected = []
            for line in lines:
                if selection.lower() in line.lower():
                    selected.append(line)
            if selected:
                return selected

        return [line for line in lines if line]
