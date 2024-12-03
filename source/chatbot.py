
import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
from together import Together
import sys

load_dotenv()

Together_API_KEY = os.getenv('TOGETHER_API_KEY')

class GlobalData:
    # This Variables are shared between all instance
    readed_articles = list()
    articles_dir    = '../news_articles' 
    chormaDbClient  =  chromadb.PersistentClient(path="../chroma_storage")
    collection_name = 'ragCollection'
    collection = chormaDbClient.get_or_create_collection(name=collection_name)
    TogetherClient = Together(api_key=Together_API_KEY)
    # Methodes
    def __init__(self) -> None:
        self.Conversation = list()
        self.read_All_docs()
        self.create_embeddings()
        self.upsertToChromaDb()
        
    def read_All_docs(self):
        i = 0
        for filename in os.listdir(self.articles_dir):
            with open (os.path.join(self.articles_dir, filename)) as file:
                print(filename)
                if not filename.endswith('.txt'):
                    raise AssertionError('Error on File extension only .txt accepted')
                self.readed_articles.append({'id': f'article-{i}', 'text' : file.read()})
                i+=1
    
    def queryToEmbedding(self, Query):
        return self.TogetherClient.embeddings.create(
                    model = "togethercomputer/m2-bert-80M-8k-retrieval",
                    input = Query
            ).data[0].embedding
        
    def create_embeddings(self):
        for article_data in self.readed_articles:
            article_data['embedding'] =  self.queryToEmbedding(article_data['text'])
    def upsertToChromaDb(self):
        for singleArticle in self.readed_articles:
            self.collection.upsert(
                ids=[singleArticle.get('id')],
                documents=[singleArticle.get("text")], embeddings=[singleArticle.get('embedding')]
            ) 
    def query_context(self, Query, n_results):
        EmbeddingQuery = self.queryToEmbedding(Query)
        context = self.collection.query(query_embeddings=EmbeddingQuery, n_results=n_results)
        return context.get('documents')[0]

    def insert_to_history(self, single_message):
        self.Conversation.append(single_message)
        
    def generate_response(self, question, related_articles):
        context = "\n".join(related_articles)
        constumised_prompt = (
            "You are an assistant for question-answering tasks. Use the following pieces of "
            "retrieved context to answer the question. If you don't know the answer, say that you "
            "don't know Use three sentences maximum and keep the answer concise."
            "If you don't know the answer just say I don't know with respecteful way "
            "\n\nContext:\n" + context + "\n\nQuestion:\n" + question
        )
        # print('Context [', context, ']')
        
        self.insert_to_history({ "role": "system", "content": constumised_prompt })                
        self.insert_to_history({ "role": "user", "content": question, })
        
        chat_phase = self.TogetherClient.chat.completions.create(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
            messages=self.Conversation  
        )
        response = chat_phase.choices[0].message.content
        self.Conversation.append({"role" : "system", "content" : response})
        return response

def main():
    if len(sys.argv) != 3:
        raise AssertionError('provide us only one query please!')
    Query = sys.argv[1]
    n_results = sys.argv[2]
    globalDataHolder = GlobalData()
    related_articles = globalDataHolder.query_context(Query, int(n_results))
    query_response = globalDataHolder.generate_response(Query, related_articles)
    print(query_response)
    
# semantic similarity by keyword matching
# poor integration and generation
if __name__=='__main__':
    try:
        main()
    except Exception as e:
        print(f'Error Reason: {e}')
    pass