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
        except Exception as e:
            if(str(e) == "Expecting value: line 1 column 1 (char 0)"): 
                if(message == "open"):
                    ws.send("Connection open.")
                elif(message != "mantain"):
                    ws.send("Wrong Format!!! JSON expected.")
            else:
                print(e)
                ws.send("Error on server.")
            

def handleMessage(ws, message):
    keywords = json.loads(message)
    stringBase = None
    stringGenerator = StringGenerator()

    if(message != None):
        query = stringGenerator.generateScopusString(keywords["keywords"])
        papers = findArticles(ws, keywords, query)
        analiser = StringAnalyser(keywords["bibTex"],keywords["keywords"])

        if(analysePapers(analiser, papers, ws) or stringBase == None):
            stringBase = query

        result = sendResult(
            query,
            analiser.getSensibility(),
            analiser.getPrecision(),
            analiser.getRelevant(),
            analiser.getNRelevant()
            )
            
        ws.send(result)


def analysePapers(analiser:StringAnalyser, papers, ws):
    relevant = []
    notRelevant = []
    cont = 0

    for papper in papers:        
        analiser.analysePaper(papper, relevant, notRelevant)
        cont += 1

        if((cont/50).is_integer()):
            ws.send(sendProgressAnalysis(cont))
    
    return analiser.calSenPre(relevant, notRelevant)

def findArticles(websocket, keywords, query):
    searcher = PaperSearcher()
    print(query)
    group = searcher.searchScopusPapers2(query, 0)
    pages = searcher.returnPagesScopus(group)
    pappers = []

    pappers.append(group)
    websocket.send(sendProgress(str(1), str(pages), getTotalArticles(pappers)))

    for i in range(1, pages):
        print(i)
        start = (i * 25)
        i = i + 1
        find = searcher.searchScopusPapers2(query, start)
        pappers.append(find)
        websocket.send(sendProgress(str(i), str(pages), getTotalArticles(pappers)))
    
    return searcher.organizePapersScopus(pappers)


def getTotalArticles(papers):
    for item in papers:
            return item['search-results']['opensearch:totalResults']

            

def getString(keywords):
    newKeywords = []

    for synonyms in keywords['keywords']:
        newSynonyms = []

        for synonym in synonyms:
            newSynonyms.append(synonym)

        newKeywords.append(newSynonyms)

    return newKeywords


def sendProgress(progress, pages, totalArticles):
    response = {
        "typeMenssage":"progress",
        "progress":progress,
        "pages":pages,
        "totalArticles":totalArticles
    }

    return json.dumps(response)

def sendProgressAnalysis(progress):
    response = {
        "typeMenssage":"progressAnalysis",
        "progress":progress
    }

    return json.dumps(response)



def sendResult(query, sen, pre, rel, nRel):
    response = {
        "typeMenssage":"result",
        "query":query,
        "sensitivity":sen,
        "precision":pre,
        "relevant":rel,
        "notRelevant":nRel
    }

    return json.dumps(response)



@app.route('/')
def hello():
    return 'You are in the String Improver'


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()