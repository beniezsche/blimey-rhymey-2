
from fastapi import FastAPI, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from pydantic_models import Headline, SearchResults, TextInput, UserCredentials
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import tensorflow as tf
import chromadb
import time
import secrets
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
from fastapi.middleware.cors import CORSMiddleware

from app_db import engine, SessionLocal
import database_models
from sqlalchemy import update

from rq import Queue
from redis import Redis


GENERATIVE_AI_MODEL_REPO = "TheBloke/Llama-2-7B-chat-GGUF"
GENERATIVE_AI_MODEL_FILE = "llama-2-7b-chat.Q6_K.gguf"

model_path = hf_hub_download(
    repo_id=GENERATIVE_AI_MODEL_REPO,
    filename=GENERATIVE_AI_MODEL_FILE
)

llama2_model = Llama(
    model_path=model_path,
    n_gpu_layers=64,
    n_ctx=2000
)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["Creator"] = "Bikraman"
    return response

queue = Queue(connection=Redis())

model = SentenceTransformer('all-mpnet-base-v2')

sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")

chroma_client = chromadb.PersistentClient(path="db")
current_collection = chroma_client.get_or_create_collection("test", embedding_function = sentence_transformer_ef)

# Example OAuth2PasswordBearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

database_models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Assume you have a function to verify the token
def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    # Your token validation logic here
    # Example: Decode the token, verify it, and return the user information
    # If the token is invalid, raise an HTTPException

    existing_token = db.query(database_models.Tokens).filter(database_models.Tokens.token == token).first()

    if existing_token is None:
        raise HTTPException(status_code=401, detail="User doesn't exist")
    

@app.get("/v1/user/gettoken")
def get_token(db = Depends(get_db)) -> str:
    try:    
        # Generate a random hex token (suitable for session tokens)
        random_token = secrets.token_hex(16)

        new_token = database_models.Tokens(token=random_token)
        db.add(new_token)
        db.commit()
        db.refresh(new_token)
        return random_token
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/headlines/all")
def get_all_headlines(user : UserCredentials = Depends(get_current_user), db: SessionLocal = Depends(get_db)) -> list[Headline]:

    list = db.query(database_models.Headlines).all()
    list.reverse()
    return list

@app.get("/v1/headlines/search")
def search(searchTerm: str, user: UserCredentials = Depends(get_current_user)) -> list[SearchResults]:

    something = current_collection.query(
        query_texts=searchTerm,
        n_results=100,
    )

    # Extract ids and distances
    ids = something['ids'][0]
    distances = something['distances'][0]
    documents = something['documents'][0]

    last_list = []

    for index, id in enumerate(ids):
        document = documents[index]
        distance = distances[index]

        if distance <= 1.6:
            last_list.append(SearchResults(id= id, headline = document, distance = distance))
    
    return last_list 


@app.get("/")
async def get():
    return { "response": "Server active!"}

def update_rhyme(headline, params):

    db = SessionLocal()

    new_rhyme = generate_rhyme_using_llama(create_prompt_from_headline(headline), params)
    # Update the email address for the user with id=1
    stmt = update(database_models.Headlines).where(database_models.Headlines.headline == headline).values(rhyme=new_rhyme)
    db.execute(stmt)
    db.commit()

    db.close()



@app.get("/v1/headlines/rhyme")
def get_new_rhyme(headline: str, token: str = Depends(get_current_user), db: SessionLocal = Depends(get_db)):

    params = {"temperature":0.95}

    job = queue.enqueue(update_rhyme, headline, params)

    while True:
        job_status = job.get_status()
        if job_status == "finished":
            break

    generated_rhyme = db.query(database_models.Headlines).filter(database_models.Headlines.headline == headline).first()

    new_rhyme = generated_rhyme.rhyme

    return new_rhyme


def create_prompt_from_headline(headline):

    prompt = f'''Please generate a two line rhyme based on this headline -> {headline}'''
    prompt_template=f'''SYSTEM: You are a helpful, respectful and honest assistant. Always answer as helpfully.

    USER: {prompt}

    ASSISTANT: Sure, here is a two line rhyme for you:
    '''

    return prompt_template


def generate_rhyme_using_llama(prompt_template, params):
    response = llama2_model(prompt=prompt_template, **params)
    model_out = response['choices'][0]['text']
    return model_out

def generate_rhyme(data, params):

    prompt_template = create_prompt_from_headline(data)

    db = SessionLocal()

    model_out = generate_rhyme_using_llama(prompt_template, params)

    new_headline = database_models.Headlines(headline = data, rhyme = model_out)

    db.add(new_headline)
    db.commit()
    db.refresh(new_headline)

    db.close()


@app.post("/v1/headlines/generate_rhyme/")
def generate_text(data: TextInput, user: UserCredentials = Depends(get_current_user), db : SessionLocal = Depends(get_db)) -> dict[str, str]:
    try:
        params = data.parameters or {}

        headline = data.inputs

        existing_rhyme = db.query(database_models.Headlines).filter(database_models.Headlines.headline == headline).first()

        if existing_rhyme is None:
            job = queue.enqueue(generate_rhyme, headline, params)

            while True:
                job_status = job.get_status()
                if job_status == "finished":
                    break

            generated_rhyme = db.query(database_models.Headlines).filter(database_models.Headlines.headline == headline).first()

            sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")

            client = chromadb.PersistentClient(path="db")
            collection = client.get_or_create_collection("test", embedding_function = sentence_transformer_ef)

            id = collection.add(
                    documents=[generated_rhyme.headline],
                    ids=[str(generated_rhyme.id)]
            )
            
            return {"generated_text": generated_rhyme.rhyme}
        else:
            return {"generated_text": existing_rhyme.rhyme}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))