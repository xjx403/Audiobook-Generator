import os
import asyncio
import io
from pydub import AudioSegment
from pydub.utils import which
import re
import edge_tts  # Import edge_tts library

# 手动指定FFmpeg可执行文件的路径
AudioSegment.converter = which("E:\\study\\tools\\pytools\\ffmpeg-7.0.1-full_build\\bin\\ffmpeg.exe")

def read_novel(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        novel_text = file.read()
    
    # 使用正则表达式来匹配章节标题，并分割文本
    chapters = re.split(r'(第.*?章.*)', novel_text)
    
    # 将章节标题和内容合并在一起
    merged_chapters = []
    for i in range(1, len(chapters), 2):
        title = chapters[i].strip()
        content = chapters[i+1].strip() if i+1 < len(chapters) else ''
        merged_chapters.append((title, content))
    print(merged_chapters)
    return merged_chapters

async def text_to_speech(title, content, voice="zh-CN-YunyangNeural", rate=0, volume=0):
    # 格式化rate和volume参数
    rate_str = f"{rate:+d}%"  # 转换为带正负号的字符串，末尾加上百分号
    volume_str = f"{volume:+d}%"  # 转换为带正负号的字符串，末尾加上百分号
    
    # 合并章节标题和内容
    
    
    communicate = edge_tts.Communicate(content, voice, rate=rate_str, volume=volume_str)
    segment_audio = b''
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            segment_audio += chunk["data"]
    return segment_audio

def split_text(text, max_length=500):
    text = text.replace('\n', ' ')
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(' '.join(current_chunk)) + len(word) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

async def generate_audio_book(novel_file_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    chapters = read_novel(novel_file_path)

    for title, content in chapters:
        text_chunks = split_text(f"{title}\n{content}")
        combined_audio = AudioSegment.empty()  # 用于合并音频段

        for j, chunk in enumerate(text_chunks):
            print(f"Text chunk {j+1} for {title}:")
            print(chunk)  # 打印文本内容
            segment_audio_bytes = await text_to_speech(title, chunk)
            
            # 将字节数据转换为AudioSegment对象，并指定格式为"mp3"
            with io.BytesIO(segment_audio_bytes) as audio_io:
                segment_audio = AudioSegment.from_file(audio_io, format="mp3")
            
            combined_audio += segment_audio
            print(f"Generated audio part {j+1} for {title}")

        chapter_audio_file = os.path.join(output_dir, f"{title}.mp3")
        combined_audio.export(chapter_audio_file, format="mp3")
        print(f"Generated audio file for {title}: {chapter_audio_file}")

# 使用示例
novel_file_path = 'data/test.txt'  # 小说文本文件路径
output_dir = 'data/audiobook'                 # 输出目录

# 运行异步函数
asyncio.run(generate_audio_book(novel_file_path, output_dir))
