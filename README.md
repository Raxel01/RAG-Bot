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
   * get your together Ai api key  First
   * get Togetherai=api=key fron your .env
   * Load Your documents only .txt and store them on a dict
     key,value articleId : articleContent 
               