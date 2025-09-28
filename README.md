Topic Modelling Pipeline for Text Documents. This was the code I used for my bachelors thesis.
This project provides an automated pipeline for cleaning raw text documents and performing topic modelling using BERTopic. It is designed to ingest .txt files, clean and tokenize the content, generate interpretable topic clusters, and output:
Faceted bar plots of top topic words
Representative document excerpts for each topic
Cleaned text files for reproducibility

🚀 Features
Document Cleaning (processDocuments.py):
Removes citations, headers, footers, line breaks, duplicate lines, page numbers, and unwanted institution references.
Outputs clean, whitespace-normalized text files.
Topic Modelling (topicModelling.py):
Loads cleaned text and splits it into meaningful paragraphs.
Tokenizes and removes stopwords using NLTK.
Applies BERTopic with SentenceTransformer embeddings.
Filters topic assignments based on probability threshold.

Generates:
📊 Faceted bar plots of top topic words (stored in /Plots)
📝 Representative topic chunks per topic (stored in /RepDOCS)
📁 Project Structure
.
\n├── Documents/                # (Input) Raw .txt files
\n├── DocumentsCleaned/         # (Output) Cleaned documents from processDocuments.py
├── Plots/                    # Generated topic word plots
├── RepDOCS/                  # Text files containing representative topic chunks
├── processDocuments.py       # Cleans and sanitizes raw text files
├── topicModelling.py         # Runs topic modelling with BERTopic
└── README.md

⚙️ Installation & Requirements
pip install nltk pandas seaborn matplotlib bertopic sentence-transformers
You'll also need to download NLTK resources (handled automatically on first run).

▶️ How to Run
Place your raw .txt files inside the Documents/ folder.
Run the topic modelling script:
python topicModelling.py


This will:
✅ Clean all documents
✅ Train a BERTopic model
✅ Save visualizations and representative text results

🧪 Configuration
Inside topicModelling.py, you can tweak:
Variable	Purpose	Default
TOP_N_WORDS	Number of top words per topic	12
PROB_THRESHOLD	Minimum probability to assign a chunk to a topic	0.3
nr_topics (in BERTopic)	Number of topics to extract	25
MAX_REP_DOCS	Max number of representative samples per topic	10

✅ Output Examples
Plot Example: Plots/faceted_topic_words_0.png
Representative Text Example: RepDOCS/repDocs_0.txt

📌 Notes
The cleaning script avoids overwriting already cleaned files.
Ensure your text files have meaningful paragraph separation (\n\n) for best chunking.
The pipeline currently expects English-language content due to stopword filtering.

📄 License
MIT License — feel free to use and modify!
