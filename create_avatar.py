from ast import literal_eval
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, VectorStoreIndex, ServiceContext, LLMPredictor, PromptHelper, StorageContext, load_index_from_storage
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
import gradio as gr
import os
import environ
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import numpy as np
from elevenlabs import generate, play, clone
from llama_index import Document
from llama_index.node_parser import SimpleNodeParser
import logging

env = environ.Env()
environ.Env.read_env()

logging.basicConfig(filename="chat_response_log.txt", filemode='w')
logger=logging.getLogger() 
logger.setLevel(logging.ERROR) 

video_paths = [
    "1.mp4",
    "2.mp4",
    "3.mp4",
    "4.mp4",
    "5.mp4",
    "6.mp4",
    "7.mp4",
    "8.mp4",
    "9.mp4",
    "10.mp4",
    "11.mp4",
    "12.mp4",
    "13.mp4",
    "14.mp4",
    "15.mp4",
    "16.mp4",
    "17.mp4",
    "18.mp4",
    "19.mp4",
    "20.mp4",
    "21.mp4",
    "22.mp4",
    "23.mp4",
    "24.mp4",
    "25.mp4",
    "26.mp4",
    "27.mp4",
    "28.mp4"
]


def create_index(directory_path):
    parser = SimpleNodeParser()

    documents = SimpleDirectoryReader(directory_path).load_data()

    nodes = parser.get_nodes_from_documents(documents)
    index = VectorStoreIndex(nodes)
    
    index.storage_context.persist(persist_dir=".")
    print("Index saved to disk as vector_store.json")

def chat(input_text, log_it=False):
    storage_context = StorageContext.from_defaults(persist_dir=".")
    index = load_index_from_storage(storage_context)
    
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)

    if log_it == True:
        logger.error("---- USER PROMPT ----")
        logger.error(input_text)
        logger.error("---- MODEL RESPONSE ----")
        logger.error(response.response)

    return response.response

# To be called from Python in Command Prompt
def test_chat():
    interface = gr.Interface(fn=chat,
                        inputs=gr.components.Textbox(lines=5, label="Enter your text"),
                        outputs="text",
                        title="Custom-trained AI Chatbot")

    index = create_index("docs")
    interface.launch(share=True)


class ScriptFinder:

    def __init__(self, input_scripts):
        self.input_scripts = input_scripts # "Scripts.xlsx"
        self.df = pd.read_csv(input_scripts)
        self.df['embedding'] = self.df['embedding'].apply(literal_eval)

    def generate_embeddings_from_scripts(self):
        df = pd.read_excel(self.input_scripts)

        embedding_model = "text-embedding-ada-002"
        df['embedding'] = df['Scripts'].apply(lambda x: get_embedding(x, engine = embedding_model))
        
        df['video_path'] = video_paths

        self.embedding_filename = 'Scripts_embedding.csv'
        df.to_csv(self.embedding_filename)

        self.df = df

        return self.embedding_filename
    
    def pre_process_embeddings(self):
        self.df["embedding"] = self.df["embedding"].apply(eval).apply(np.array)
    
    def find_similar_text(self, input_response, n=3, print_results=True):
        script_embeddings = get_embedding(input_response, engine="text-embedding-ada-002")
        similar_embeddings_df = self.df

        similar_embeddings_df["similarity"] = similar_embeddings_df["embedding"].apply(
            lambda x: cosine_similarity(x, script_embeddings)
        )

        # Sort the notes by similarity in descending order and select the top `n` notes.
        results = similar_embeddings_df.sort_values("similarity", ascending=False).head(n)
        
        if print_results == True:
            for index, row in results.iterrows():
                print(row["similarity"], row["Scripts"])

        return results


class AudioGenerator:

    def __init__(self, input_scripts):
        self.input_scripts = input_scripts # "Scripts.xlsx"

    def generate_audio_file_from_script(self, autoplay=True):
        self.voice = clone(
            name="JP",
            description="TBD", # Optional
            files=["./sample_0.mp3", "./sample_1.mp3", "./sample_2.mp3"],
        )

        audio = generate(text="Hi! I'm a cloned voice!", voice=self.voice)

        if autoplay == True:
            play(audio)

        return audio
    
    
