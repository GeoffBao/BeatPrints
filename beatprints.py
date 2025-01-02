#!/usr/bin/env python3
"""BeatPrints CLI"""
import os
import dotenv
from BeatPrints import lyrics, poster, spotify


def get_user_input():
    """获取用户输入的歌曲信息"""
    print("\n请输入歌曲信息:")
    track_name = input("歌曲名称: ").strip()
    
    if not track_name:
        raise ValueError("歌曲名称不能为空")
        
    return track_name


def select_lyrics(lyrics_text: str) -> str:
    """让用户选择歌词部分"""
    print("\n完整歌词:")
    lines = lyrics_text.split('\n')
    for i, line in enumerate(lines, 1):
        if line.strip():
            print(f"{i:2d}. {line}")
    
    print("\n请选择要使用的歌词行数（例如：1-5 或 1,3,5）")
    selection = input("选择（直接回车使用全部）: ").strip()
    
    if not selection:
        return lyrics_text
        
    try:
        selected_lines = []
        for part in selection.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                selected_lines.extend(lines[start-1:end])
            else:
                selected_lines.append(lines[int(part)-1])
        return '\n'.join(line for line in selected_lines if line.strip())
    except (ValueError, IndexError):
        print("输入格式错误，将使用全部歌词")
        return lyrics_text


def main():
    # 加载环境变量
    dotenv.load_dotenv()
    
    # 获取 Spotify 认证信息
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("请在环境变量中设置 SPOTIFY_CLIENT_ID 和 SPOTIFY_CLIENT_SECRET")

    try:
        # 初始化组件
        sp = spotify.Spotify(CLIENT_ID, CLIENT_SECRET)
        ly = lyrics.Lyrics()
        ps = poster.Poster(save_to='posters')
        
        # 获取用户输入
        track_name = get_user_input()
        print(f"\n搜索歌曲: {track_name}")
        # Search for a track
        search = sp.get_track(track_name, limit=1)
        #track = search
        #print(f"找到歌曲: {track.name} - {track.artist}")
        # Get the track's metadata and lyrics
        metadata = search[0]

        print("\n获取歌词...")
        lyric_text = ly.get_lyrics(metadata)
        #highlighted_lyrics = ly.select_lines(lyric_text, "5-9")
        # 选择歌词部分
        selected_lyrics = select_lyrics(lyric_text)
        
        # 预览歌词
        print("\n歌词预览:")
        for line in lyric_text.split('\n'):
            if line.strip():
                print(line)

        # Generate the track poster
        ps.track(metadata, selected_lyrics)

    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"\n错误: {str(e)}")
        if os.getenv('DEBUG'):
            raise


if __name__ == "__main__":
    main()