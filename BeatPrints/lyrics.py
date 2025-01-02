"""
Lyrics handling module
"""
import os
import requests
from typing import List
from .spotify import TrackMetadata
from .lrclib import LrcLibAPI


class Lyrics:
    def __init__(self):
        """初始化歌词处理器"""
        self.lyrics_dir = os.path.join(os.getcwd(), 'lyrics')
        os.makedirs(self.lyrics_dir, exist_ok=True)
        self.lrclib = LrcLibAPI(user_agent="BeatPrints/1.0")

    def get_lyrics(self, track: TrackMetadata) -> str:
        """获取歌词，如果找不到则让用户输入"""
        try:
            # 从 LRCLib 获取歌词
            lyrics = self.lrclib.get_lyrics(track.name, track.artist)
            
            # 如果找不到歌词，让用户输入
            if not lyrics:
                print(f"\n找不到歌词: {track.name} - {track.artist}")
                return self._input_default_lyrics(track)
                
            print(f"获取歌词成功: {track.name}")
            return lyrics

        except Exception as e:
            print(f"\n获取歌词出错: {str(e)}")
            return self._input_default_lyrics(track)

    def _input_default_lyrics(self, track: TrackMetadata) -> str:
        """让用户输入3句默认歌词"""
        lines = []
        print("\n请输入3句你喜欢的歌词片段:")
        print("请输入3句歌词 (每句回车确认):")
        
        for i in range(3):
            while True:
                line = input(f"第 {i+1} 句: ").strip()
                if line:  # 确保输入不为空
                    lines.append(line)
                    break
                print("歌词不能为空，请重新输入")
        
        lyrics = '\n'.join(lines)
        return lyrics

    def select_lines(self, lyrics: str, selection: str = "") -> List[str]:
        """选择歌词行"""
        lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
        
        if selection:
            selected = []
            for line in lines:
                if selection.lower() in line.lower():
                    selected.append(line)
            if selected:
                return selected

        return lines
