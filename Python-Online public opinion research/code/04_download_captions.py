import os
import re

def clean_vtt_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}', line):  # 跳过时间戳行
            continue
        if '-->' in line or line.strip().isdigit() or line.strip() == '':
            continue
        cleaned_lines.append(line.strip())
    return cleaned_lines

# 找出所有 .vtt 文件
all_subtitles = []
for filename in os.listdir('.'):
    if filename.endswith('.vtt'):
        all_subtitles.extend(clean_vtt_content(filename))

# 保存到一个文件
with open('all_subtitles.txt', 'w', encoding='utf-8') as f:
    for line in all_subtitles:
        f.write(line + '\n')
