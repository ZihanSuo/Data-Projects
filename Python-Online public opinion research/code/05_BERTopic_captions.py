!pip install --quiet bertopic[all] sentence-transformers umap-learn hdbscan

# 导入所需的库
import pandas as pd
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from sentence_transformers import SentenceTransformer
from google.colab import files

# 额外导入 UMAP 和 HDBSCAN
from umap import UMAP
from hdbscan import HDBSCAN

# 上传文件
uploaded = files.upload()

# 读取文件内容
txt_filename = next(iter(uploaded.keys()))
with open(txt_filename, 'r') as file:
    text_data = file.read()

# 接将文本按行分割
docs = text_data.split("\n")

# 自定义停用词列表
custom_stops = ["oh", "yeah", "china", "music", "just", "also", "so"]
all_stops = list(ENGLISH_STOP_WORDS) + custom_stops  # 将集合转换为列表

# 加载 SentenceTransformer 句向量模型
emb_model = SentenceTransformer("all-MiniLM-L6-v2")

# 构造 UMAP 和 HDBSCAN 实例
umap_model    = UMAP(n_neighbors=15, n_components=5, metric='cosine')
hdbscan_model = HDBSCAN(min_cluster_size=5, min_samples=1, metric='euclidean')

# 初始化 BERTopic，传入自定义停用词和自定义 UMAP/HDBSCAN
vectorizer = CountVectorizer(stop_words=all_stops)
topic_model = BERTopic(
    embedding_model=emb_model,
    vectorizer_model=vectorizer,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model
)

# 训练主题模型
topics, probs = topic_model.fit_transform(docs)

# 查看主题概览
topics_overview = topic_model.get_topic_info()
print(topics_overview)

# 打印每个主题的关键词
for topic_id in topics_overview.Topic:
    print(f"\nTopic {topic_id}:")
    print(topic_model.get_topic(topic_id))
