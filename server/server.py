#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets
import json
from StringImprover import *
from PaperSearcher import *
from StringGenerator import *


async def time(websocket, path):
    while True:
        message = await websocket.recv()
        keywords = json.loads(message)
        stringBase = None
        stringGenerator = StringGenerator()

        if(message != None):
            query = stringGenerator.generateScopusString(keywords["keywords"])
            papers = await findArticles(websocket, keywords, query)
            analiser = StringAnalyser(keywords["bibTex"],keywords["keywords"])

            if(analiser.analysePapers(papers) or stringBase == None):
                stringBase = query

            result = sendResult(query, analiser.getSensibility(), analiser.getPrecision())
            await websocket.send(result)    
    

async def findArticles(websocket, keywords, query):
    searcher = PaperSearcher()
    print(query)
    group = searcher.searchScopusPapers2(query, 0)
    pages = searcher.returnPagesScopus(group)
    pappers = []

    pappers.append(group)
    await websocket.send(sendProgress(str(1), str(pages)))

    for i in range(1, pages):
        print(i)
        start = (i * 25)
        i = i + 1
        find = searcher.searchScopusPapers2(query, start)
        pappers.append(find)
        await websocket.send(sendProgress(str(i), str(pages)))
    
    return searcher.organizePapersScopus(pappers)


def getString(keywords):
    newKeywords = []

    for synonyms in keywords['keywords']:
        newSynonyms = []

        for synonym in synonyms:
            newSynonyms.append(synonym)

        newKeywords.append(newSynonyms)

    return newKeywords

def sendProgress(progress, pages):
    teste = {
        "typeMenssage":"progress",
        "progress":progress,
        "pages":pages
    }

    return json.dumps(teste)


def sendResult(query, sen, pre):
    teste = {
        "typeMenssage":"result",
        "query":query,
        "sensitivity":sen,
        "precision":pre
    }

    return json.dumps(teste)


start_server = websockets.serve(time, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
