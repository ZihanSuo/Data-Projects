import os
import re

subtitle_dir = "/Users/marsf/Desktop/test"
output_file = os.path.join(subtitle_dir, "merged_subtitles.txt")

def clean_subtitle_lines(lines):
    cleaned = []
    # 由于重复出现，每3行为一组，我们只保留每组的最后一行（最终字幕行）
    for i in range(2, len(lines), 3):
        line = lines[i].strip()
        # 删除所有尖括号内的时间标签，如 <00:00:01.560>
        line = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', line)
        # 删除所有 <c> </c> 标签
        line = re.sub(r'</?c>', '', line)
        if line:
            cleaned.append(line)
    return cleaned

def process_vtt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()

    # 过滤掉无用行：WEBVTT、空行、时间戳行、序号行
    content_lines = []
    for line in raw_lines:
        line_strip = line.strip()
        if not line_strip:
            continue
        if line_strip.startswith("WEBVTT"):
            continue
        if re.match(r'^\d+$', line_strip):  # 纯数字序号
            continue
        if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3} -->', line_strip):  # 标准时间戳行
            continue
        content_lines.append(line_strip)

    # 清理重复和标签，得到纯净字幕行
    cleaned_lines = clean_subtitle_lines(content_lines)
    return cleaned_lines

def main():
    vtt_files = sorted([f for f in os.listdir(subtitle_dir) if f.endswith('.vtt')])
    all_text = []

    for filename in vtt_files:
        video_id = os.path.splitext(filename)[0]
        all_text.append(f"\n--- {video_id} ---\n")
        path = os.path.join(subtitle_dir, filename)
        subs = process_vtt_file(path)
        all_text.extend(subs)

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_text:
            f.write(line + '\n')

    print(f"合并完成，输出路径：{output_file}")

if __name__ == "__main__":
    main()
