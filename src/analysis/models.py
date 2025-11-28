import os
from sentence_transformers import SentenceTransformer
from transformers import pipeline

class ModelManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
            cls._instance.models = {}
            cls._instance.models_dir = os.path.join(os.getcwd(), "models")
        return cls._instance
    
    def get_embedding_model(self):
        if "embedding" not in self.models:
            print("Loading embedding model...")
            self.models["embedding"] = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=self.models_dir)
        return self.models["embedding"]
    
    def get_sentiment_pipeline(self):
        if "sentiment" not in self.models:
            print("Loading sentiment pipeline...")
            model_name = "distilbert-base-uncased-finetuned-sst-2-english"
            self.models["sentiment"] = pipeline("sentiment-analysis", model=model_name, tokenizer=model_name)
        return self.models["sentiment"]
    
    def get_zeroshot_pipeline(self):
        if "zeroshot" not in self.models:
            print("Loading zero-shot pipeline...")
            model_name = "facebook/bart-large-mnli"
            self.models["zeroshot"] = pipeline("zero-shot-classification", model=model_name, tokenizer=model_name)
        return self.models["zeroshot"]

model_manager = ModelManager()
