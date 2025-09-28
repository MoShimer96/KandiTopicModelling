# KandiTopicModelling

Topic Modelling Pipeline for Text Documents  
This was the code I used for my bachelor’s thesis. This project provides an automated pipeline for cleaning raw text documents and performing topic modelling using BERTopic. It is designed to ingest `.txt` files, clean and tokenize the content, generate interpretable topic clusters, and output:

- Faceted bar plots of top topic words  
- Representative document excerpts for each topic  
- Cleaned text files for reproducibility  

---

## 🚀 Features

**Document Cleaning (processDocuments.py):**  
- Removes citations, headers, footers, line breaks, duplicate lines, page numbers, and unwanted institution references.  
- Outputs clean, normalized text files.

**Topic Modelling (topicModelling.py):**  
- Loads cleaned text and splits it into meaningful paragraphs.  
- Tokenizes and removes stopwords using NLTK.  
- Applies **BERTopic** with **SentenceTransformer embeddings**.  
- Filters topic assignments based on probability threshold.  
- Generates:  
  - 📊 Faceted bar plots of top topic words (exported to /Plots)  
  - 📝 Representative topic chunks per topic (exported to /RepDOCS)  

---

## 📁 Project Structure

 
.
- ├── Documents/                # Input: raw .txt files
- ├── DocumentsCleaned/         # Output: cleaned documents
- ├── Plots/                    # Generated topic word visualizations
- ├── RepDOCS/                  # Representative text excerpts per topic
- ├── processDocuments.py       # Cleaning pipeline
- ├── topicModelling.py         # Topic modelling + visualizations
- └── README.md                 # This file
 

---

## ⚙️ Installation & Requirements

Install dependencies using pip:

```bash
pip install nltk pandas seaborn matplotlib bertopic sentence-transformers
```
The project also uses NLTK's resources (e.g. stopwords); these are usually downloaded during the first run.

---

## ▶️ How to Run

1. Put your raw .txt files into the Documents/ directory.  
2. Run the topic modelling script:
   ```bash
   python topicModelling.py
   ```
   

That will:

- Clean your documents (into DocumentsCleaned/)  
- Train a BERTopic model  
- Save visualizations to Plots/  
- Save representative text chunks into RepDOCS/

---

## 🔧 Configuration

In \topicModelling.py\ you can adjust the following settings:

| Variable        | Description                                  | Default |
|------------------|----------------------------------------------|---------|
| \TOP_N_WORDS\     | Number of top words per topic                | 12    |
| \PROB_THRESHOLD\  | Minimum probability to assign a chunk to a topic | 0.3   |
| \nr_topics\       | Number of topics to extract                  | 25    |
| \MAX_REP_DOCS\    | Max number of representative samples per topic | 10    |

---

## ✅ Output Examples

- **Plot Example**: Plots/faceted_topic_words_0.png 
- **Representative Text**: RepDOCS/repDocs_0.txt

---

## 📝 Notes & Tips

- The cleaning script avoids overwriting already cleaned files.  
- Ensure your .txt files use **double newlines (\`\\n\\n\`)** to mark paragraphs for best chunking.  
- Currently the pipeline uses English stopwords, so it’s optimized for English-language documents.

---

## 📄 License

This project uses the **MIT License** — free to use, modify, and distribute.
