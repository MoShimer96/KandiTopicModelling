import os
import nltk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import processDocuments

# NLTK Setup
nltk.download('stopdwords')
nltk.download('punkt')
stopWords = set(stopwords.words('english'))


# Configurations for folder path name of files produced etc.
# The script runs the processDocuments script and returns
# the folder path where the cleaned documents are
FOLDERPATH = ".\\"+processDocuments.process_document()
TOP_N_WORDS = 12
REP_DOCS_FILE = 'repDocs_'
PLOT_FILE = 'faceted_topic_words_'
PROB_THRESHOLD = 0.3
MAX_REP_DOCS = 10
REP_DOCS_PER_N = 10
PLOT_DIR = "Plots"
os.makedirs(PLOT_DIR, exist_ok=True)
REP_TEXT_DIR = "RepDOCS"
os.makedirs(REP_TEXT_DIR, exist_ok=True)


def tokenization_function(text):
    words = word_tokenize(text.lower())
    return ' '.join(word for word in words if word.isalpha() and word not in stopWords)

def create_paragraphs(text):
    return[paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]

def load_documents(folderPath = FOLDERPATH):
    chunks = []
    for filename in os.listdir(folderPath):
        if filename.endswith(".txt"):
            with open(os.path.join(folderPath, filename), 'r', encoding='UTF-8') as openedFile:
                content = openedFile.read()
                paragraphs = create_paragraphs(content)
                paragraphsTokenized = [tokenization_function(paragraph) for paragraph in paragraphs if len(paragraph.strip()) > 20]
                chunks.extend(paragraphsTokenized)
    return chunks

# BERTopic pipeline

all_chunks = load_documents()
print(f"Total chunks to analyze: {len(all_chunks)}")

embeddingModel = SentenceTransformer("all-MiniLM-L6-v2")
topicModel = BERTopic(embedding_model = embeddingModel, nr_topics = 25)
topics, probabilities = topicModel.fit_transform(all_chunks)
topicInfo = topicModel.get_topic_info()
repDocsAll = topicModel.get_representative_docs()

# Filtering and sorting of results

topicToDocs = defaultdict(list)
for i, (topic_id, probability) in enumerate(zip(topics, probabilities)):
    if topic_id != -1 and probability is not None and probability >= PROB_THRESHOLD:
        topicToDocs[topic_id].append((i,probability))
for topic_id in topicToDocs:
    topicToDocs[topic_id].sort(key=lambda x: x[1], reverse=True)

# Visualisation of results

topicWords = []
for topic_id in topicInfo['Topic']:
    if topic_id == -1:
        continue
    words = topicModel.get_topic(topic_id)[:TOP_N_WORDS]
    for word, score in words:
        topicWords.append({'Topic': f"Topic {topic_id}", 'Word': word, 'Score': score})

dfWords = pd.DataFrame(topicWords)

g = sns.FacetGrid(dfWords, col="Topic", col_wrap=3, sharex=False, sharey=False, height=4)
g.map_dataframe(sns.barplot, y="Word", x="Score", palette="deep")
g.set_titles("{col_name}")
g.set_axis_labels("Score", "Word")
for ax in g.axes.flatten():
    for label in ax.get_xticklabels():
        label.set_rotation(45)
    ax.set_xlabel("Importance")
    ax.set_ylabel("")

plt.tight_layout()
resultNum = len(os.listdir(PLOT_DIR))
plt.savefig(os.path.join(PLOT_DIR, f"{PLOT_FILE}{resultNum}.png"), dpi=300)
plt.close()
print(f"Faceted word plot saved as '{PLOT_FILE}{resultNum}'")



# Write a doc that contains represntative documents for each topic
with open(os.path.join(REP_TEXT_DIR, f"{REP_DOCS_FILE}{len(os.listdir(REP_TEXT_DIR))}.txt"), 'w', encoding="UTF-8") as file:
    for _, row in topicInfo.iterrows():
        topic_id = row['Topic']
        if topic_id == -1 or topic_id not in topicToDocs:
            continue

        topWords = topicModel.get_topic(topic_id)[:TOP_N_WORDS]
        wordScores = ', '.join([f"{word} ({score:.4f})" for word, score in topWords])

        totalDocsInTopics = len(topicToDocs[topic_id])
        numReps = max(1, min(MAX_REP_DOCS, totalDocsInTopics // REP_DOCS_PER_N))

        file.write(f"Topic {topic_id}; {wordScores}; Representative chunks: {totalDocsInTopics}\n\n")

        for idx, _ in topicToDocs[topic_id][:numReps]:
            file.write(all_chunks[idx].strip() + "\n\n")

    print(f"Representative documents written to '{REP_DOCS_FILE}{len(os.listdir(REP_TEXT_DIR))}'")
