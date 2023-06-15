from ast import literal_eval
from llama_index import StorageContext, load_index_from_storage
import os
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
import numpy as np
import boto3

from deepavatar.settings import OPENAI_API_KEY, AWS_ACCESS_KEY, AWS_SECRET_KEY

# This needs to be the object names for the AWS S3 Videos and must match the order
# of the scripts in Scripts.xlsx.
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


def chat(input_text):
    # index_dir = os.path.join(os.getcwd())
    # print(index_dir)
    #storage_context = StorageContext.from_defaults(persist_dir=".\storage")
    storage_context = StorageContext.from_defaults(persist_dir="/mnt/avatar_storage")
    index = load_index_from_storage(storage_context)
    
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)

    return response.response

def avatar_gen(video_path):
    return

def generate_presigned_url(object_key, expiry=300):
    client = boto3.client("s3",region_name="us-east-2",
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY)
    
    # client = boto3.client("s3")
    
    response = client.generate_presigned_url('get_object',
                                                Params={'Bucket': "avatar-digital-twin-bucket",'Key': object_key},
                                                ExpiresIn=expiry)
    
    return response


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

        #self.embedding_filename = 'Scripts_embedding.csv'
        self.embedding_filename = "/mnt/avatar_storage/Scripts_embedding.csv"
        df.to_csv(self.embedding_filename)

        self.df = df

        return self.embedding_filename
    
    def pre_process_embeddings(self):
        self.df["embedding"] = self.df["embedding"].apply(eval).apply(np.array)
    
    def find_similar_text(self, input_response, n=1, print_results=False):
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
