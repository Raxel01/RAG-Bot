Here is an RAG- Chat-Bot  this is a part of my learning process
For now this  projeet w'll just be a program wiht no [frontend - backend]
It will maybe added after  using Django-React ...
Key Technologies used Here are :
 * database : chromaDb
 * python : version-python:3.10-bullseye
 * docker and Docker-compose to avoid dependencies problems to be tested on any Device
 * Together ai and  model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
        you can get a free acces by visiting https://api.together.ai/signin and create a new account
Usage :
     Makefile : 
               Use [make ] to Create your chatbot container
               Use [make fclean] to cle an all : all = [images-volumes-container]
Implementation Guide for beginners like me :
<h1> RETREIVING PHASE : </h1>
   * get your together Ai api key  First </br>
   * get Togetherai=api=key fron your .env </br>
   * Load Your documents only .txt and store them on a dict </br>
     key,value articleId : articleContent </br>
   * use some model to create embedding from your own readed articles and store them :</br>
       either in new dictionary or the same dictionary that contain the text readed from articles so structur will be

```python
self.readed_articles = [
    {
        "id": "article-01",
        "text": ${Readed content from articles},  # Use quotes for strings
        "embeddings": model.build_embeddings()...   # Proper function call
    }
]
```

* upsert this array of articles data to chromaDb
* get user Question and create emebedding from it : 
  pay attention you should use the same model that you created your 
  article content Embeddings , this will prevent you to have conflicts
  - it's kind of you encrypt some data using an algorithme
  - and you try to decrypt it using some different algorithm
    
  <h1> AUGMENTATION PHASE : </h1>
      * costumise your own propmpt
```python
        constumised_prompt = (
            "You are an assistant for question-answering tasks. Use the following pieces of "
            "retrieved context to answer the question. If you don't know the answer, say that you "
            "don't know Use three sentences maximum and keep the answer concise."
            "If you don't know the answer just say I don't know with respecteful way "
            "\n\nContext:\n" + context + "\n\nQuestion:\n" + question
        )
```
  <h1> GENERATION PHASE : </h1>
    * make a request to the TogetherAi to create a chat pipe with him

