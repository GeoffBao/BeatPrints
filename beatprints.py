#!/usr/bin/env python3
"""BeatPrints CLI"""
import os
import dotenv
from BeatPrints import lyrics, poster, spotify, config


def get_user_input():
    """获取用户输入的歌曲信息"""
    print("\n请输入歌曲信息:")
    track_name = input("歌曲名称: ").strip()

    if not track_name:
        raise ValueError("歌曲名称不能为空")

    return track_name

def select_theme():
    """选择海报主题"""
    theme_config = config.get_theme_config()
    themes = list(theme_config["themes"].keys()) or [
        "Light", "Dark", "Catppuccin", "Gruvbox",
        "Nord", "RosePine", "Everforest"
    ]

    print("\n可用的主题:")
    for i, theme in enumerate(themes, 1):
        print(f"{i}. {theme}")

    while True:
        try:
            choice = input(f"\n请选择主题编号 [1-{len(themes)}] (默认: {theme_config['default']}): ").strip()
            if not choice:
                return theme_config["default"]

            index = int(choice) - 1
            if 0 <= index < len(themes):
                return themes[index]
            else:
                print(f"无效的选择，请输入 1-{len(themes)} 之间的数字")
        except ValueError:
            print("无效的输入，请输入数字")

def select_lyrics(lyrics_text: str) -> str:
    """让用户选择歌词部分"""
    print("\n完整歌词:")
    lines = lyrics_text.split('\n')
    for i, line in enumerate(lines, 1):
        if line.strip():
            print(f"{i:2d}. {line}")
    
    print("\n请选择要使用的歌词行数 (例如: 1-5 或 1,3,5)")
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
        # 使用配置中的输出路径
        output_config = config.get_output_config()
        ps = poster.Poster(save_to=output_config["save_to"])

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

        # 取消注释主题选择
        theme = select_theme()

        # 预览歌词
        print("\n歌词预览:")
        for line in lyric_text.split('\n'):
            if line.strip():
                print(line)

        # 使用选择的主题生成海报
        print(f"\n使用 {theme} 主题生成海报...")
        ps.track(metadata, selected_lyrics, theme=theme)

    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"\n错误: {str(e)}")
        if os.getenv('DEBUG'):
            raise


if __name__ == "__main__":
    main()