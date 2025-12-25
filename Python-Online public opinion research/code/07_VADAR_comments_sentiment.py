import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

# 指定 nltk 本地数据路径
nltk_data_path = "/Users/yunimashu/nltk_data/vader_lexicon"
nltk.data.path.append(nltk_data_path)

# 加载 CSV 文件
df = pd.read_csv("top_youtube_comments.csv")

# 显示前几行检查格式
print(df.head())

comment_col = 'comment'
if comment_col not in df.columns:
    raise ValueError(f"列名 '{comment_col}' 不存在，请检查 CSV 文件！")

# 初始化情感分析器
sia = SentimentIntensityAnalyzer()

# 对每条评论进行情感打分
df['sentiment_score'] = df[comment_col].astype(str).apply(lambda x: sia.polarity_scores(x)['compound'])

# 添加情感标签
df['sentiment_label'] = df['sentiment_score'].apply(
    lambda score: 'positive' if score >= 0.05 else ('negative' if score <= -0.05 else 'neutral')
)

# 保存结果
output_path = "comments_with_sentiment.csv"
df.to_csv(output_path, index=False)
print(f"✅ 情感分析完成，结果已保存至：{output_path}")
