import os
from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM

def download_models():
    print("Downloading models... This may take a while.")
    
    # Create models directory if it doesn't exist
    models_dir = os.path.join(os.getcwd(), "models")
    os.makedirs(models_dir, exist_ok=True)
    
    # 1. Embeddings Model: sentence-transformers/all-MiniLM-L6-v2
    print("Downloading embedding model: all-MiniLM-L6-v2...")
    SentenceTransformer('all-MiniLM-L6-v2', cache_folder=models_dir)
    
    # 2. Sentiment Analysis Model: distilbert-base-uncased-finetuned-sst-2-english
    print("Downloading sentiment model: distilbert-base-uncased-finetuned-sst-2-english...")
    sentiment_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    pipeline("sentiment-analysis", model=sentiment_model_name, tokenizer=sentiment_model_name)
    # Note: Transformers pipeline caches to ~/.cache/huggingface by default. 
    # To force local project cache, we'd need to set HF_HOME or similar, 
    # but standard cache is usually fine. For strict project containment:
    # AutoModelForSequenceClassification.from_pretrained(sentiment_model_name, cache_dir=models_dir)
    # AutoTokenizer.from_pretrained(sentiment_model_name, cache_dir=models_dir)

    # 3. Topic Classification (Zero-Shot): facebook/bart-large-mnli
    print("Downloading zero-shot model: facebook/bart-large-mnli...")
    zeroshot_model_name = "facebook/bart-large-mnli"
    pipeline("zero-shot-classification", model=zeroshot_model_name, tokenizer=zeroshot_model_name)
    
    print("All models downloaded successfully!")

if __name__ == "__main__":
    download_models()
