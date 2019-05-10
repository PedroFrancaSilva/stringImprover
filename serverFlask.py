from flask import Flask
from flask_sockets import Sockets
import json
from model.StringAnalyser import StringAnalyser
from model.StringGenerator import StringGenerator
from model.PaperSearcher import PaperSearcher


app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/scopus')
def scopus_socket(ws):
    print("Conectou")
    while not ws.closed:
        message = ws.receive()
        
        try:
            handleMessage(ws,message)
        except :
            ws.send("Wrong Format!!! JSON expected.")

def handleMessage(ws, message):
    keywords = json.loads(message)
    stringBase = None
    stringGenerator = StringGenerator()

    if(message != None):
        query = stringGenerator.generateScopusString(keywords["keywords"])
        papers = findArticles(ws, keywords, query)
        analiser = StringAnalyser(keywords["bibTex"],keywords["keywords"])
        print("Analisou")

        if(analiser.analysePapers(papers) or stringBase == None):
            stringBase = query
        
        print("Analisou 2")

        result = sendResult(query, analiser.getSensibility(), analiser.getPrecision())

        print("Tem resultado = " + result)
        ws.send(result)
        
        print("enviou")

def findArticles(websocket, keywords, query):
    searcher = PaperSearcher()
    print(query)
    group = searcher.searchScopusPapers2(query, 0)
    pages = searcher.returnPagesScopus(group)
    pappers = []

    pappers.append(group)
    websocket.send(sendProgress(str(1), str(pages)))

    for i in range(1, pages):
        print(i)
        start = (i * 25)
        i = i + 1
        find = searcher.searchScopusPapers2(query, start)
        pappers.append(find)
        websocket.send(sendProgress(str(i), str(pages)))
    
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



@app.route('/')
def hello():
    return 'You are in the String Improver'


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()