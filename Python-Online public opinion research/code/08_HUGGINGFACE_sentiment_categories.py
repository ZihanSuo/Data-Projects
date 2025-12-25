# ✅ 导入所需库
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from tqdm import tqdm

# ✅ 加载情绪分类模型
model_name = "j-hartmann/emotion-english-distilroberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# ✅ 情绪标签列表
labels = ['admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
          'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval', 'disgust',
          'embarrassment', 'excitement', 'fear', 'gratitude', 'grief', 'joy', 'love',
          'nervousness', 'optimism', 'pride', 'realization', 'relief', 'remorse',
          'sadness', 'surprise', 'neutral']

# ✅ 上传 CSV 文件
from google.colab import files
uploaded = files.upload()  # 运行后上传你本地的 CSV 文件（例如 top_youtube_comments.csv）

# ✅ 读取文件（会自动取第一个上传的文件名）
file_name = next(iter(uploaded))
df = pd.read_csv(file_name)
print("列名如下：", df.columns.tolist())
comment_column = 'comment'

# ✅ 情绪识别函数
def classify_emotion(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
    top_prob, top_idx = torch.topk(probs, 1)
    return labels[top_idx.item()], round(top_prob.item(), 4)

# ✅ 应用情绪识别并保存结果
tqdm.pandas()
df['predicted_emotion'], df['emotion_prob'] = zip(*df[comment_column].progress_apply(classify_emotion))

# ✅ 保存为 CSV 文件
output_file = "emotion_results.csv"
df.to_csv(output_file, index=False)
print(f"\n✅ 结果已保存为：{output_file}")
