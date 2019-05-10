import requests
from model.StringGenerator import StringGenerator
import math
from model.Paper import Paper
from model.StringAnalyser import StringAnalyser
import json
from model.xploreapi import XPLORE


class PaperSearcher:
    """Classe reponsável por procurar artigos nas bases"""

    # URL da Api Scopus Search
    __URL_SEARCH = "https://api.elsevier.com/content/search/scopus"
    #URL da Api Abstract Retriavel
    __URL_ABSTRACT = "https://api.elsevier.com/content/article/doi/"
    #URL da Api IEEE
    __URL_ABSTRACT = "https://ieeexploreapi.ieee.org/api/v1/search/articles"
    # Credenciais para acessar a scopus
    __API_KEY_Scopus = "64b1080620fa7f97908f4286ecb0dda3"
    # Credenciais para acessar a IEEE
    __API_KEY_IEEE = "9r2zvyxdw6pcefd4r7ypmqgf"

    def searchScopusPapers(self, query:str):
        """ Procura artigos na base Scopus e retorna uma lista com os resultados
        Parameters
        ----------
        query : str
            query que será usada para procurar os artigos

        Returns
        -------
        list
            lista com os artigos encontrados
        """
        papers = []
        response = PaperSearcher.searchPaperGroupScopus(self, query, 0)
        totalPages = int(response['search-results']['opensearch:totalResults'])
        pages = math.ceil(totalPages/25)

        papers.append(response)
        print("-------------------------------------------------------------")
        print("Artigos Encontrados = " + response['search-results']['opensearch:totalResults'])
        print("-------------------------------------------------------------")
        print("Número de páginas = " + str(pages))

        #Faz a procura de artigos por páginas, pois a Scopus tem um limite
        #de artigos que podem ser retornados por request
        for i in range(1, pages):
            print(i)
            start = (i * 25)
            i = i + 1
            find = PaperSearcher.searchPaperGroupScopus(self, query, start)
            papers.append(find)

        return self.organizePapersScopus(papers)


    def searchScopusPapers2(self, query:str, page):
        """ Procura artigos na base Scopus e retorna uma lista com os resultados
        Parameters
        ----------
        query : str
            query que será usada para procurar os artigos

        Returns
        -------
        list
            lista com os artigos encontrados
        """
        papers = []
        response = PaperSearcher.searchPaperGroupScopus(self, query, page)
        totalPages = int(response['search-results']['opensearch:totalResults'])
        pages = math.ceil(totalPages/25)

        papers.append(response)

        return response

    
    def returnPagesScopus(self,pappers):
        totalPages = int(pappers['search-results']['opensearch:totalResults'])
        pages = math.ceil(totalPages/25)
        return pages

    
    def searchPaperGroupScopus(self, query:str, page:int):
        """ Procura um grupo de artigos baseado na página que eles
            estão localizados.
        ----------
        query : str
            query que será usada para procurar os artigos
        page : int
            página para se procurar os artigos

        Returns
        -------
        list : JsonObject
            lista com os artigos encontrados
        """
        params = {'query': query, 'apiKey': self.__API_KEY_Scopus,
         'start': page, 'count': 25, 'view':'COMPLETE'}
        proxies = {
            'http':'http://121150130:Peu326598@200.132.146.39:3128',
            'https':'http://121150130:Peu326598@200.132.146.39:3128'
        }
        session = requests.sessions.Session()
        response = session.get(url=self.__URL_SEARCH, params=params, proxies=proxies)
        return response.json()


    def organizePapersScopus(self,papers:[]):
        """ Recebe uma lista de páginas contendo artigos
        encontrados na Scopos e os organiza.
        ----------
        papers : list
            lista de paginas com os artigos encontrados

        Returns
        -------
        list
            lista com os artigos organizados
        """
        newList = []
        cont = 0    

        for item in papers:
            entry = item['search-results']['entry']
            for paper in entry:
                cont += 1
                newList.append(self.createPaperScopus(paper))
        return newList


    def createPaperScopus(self, paper):
        """ Recebe um artigo retornado na pesquisa da Scopus e
        cria objetos Paper para serem utilizados na análise
        de eficácia da String.
        ----------
        papers : Json
            paper para se criar o objeto

        Returns
        -------
        Papper
            papper criado
        """
        newPaper = Paper()

        newPaper.title = self.getPaperValue(paper,'dc:title')
        newPaper.journal = self.getPaperValue(paper,'prism:publicationName')
        newPaper.abstract  = self.getPaperValue(paper,'dc:description')
        newPaper.authors  = self.getPaperValue(paper,'dc:creator')
        newPaper.keywords = self.getPaperValue(paper,'authkeywords')
       
        return newPaper

    
    def getPaperValue(self, paper, valueType):
        """ Pega um valor de um papper a partir do
        tipo de valor disponibilizado
        ----------
        paper : Json
            paper para se pegar o valor
        valueType : str
            tipo do valor que é para se pegar

        Returns
        -------
        str
            valor encontrado
        """
        try:
            return paper[valueType]
        except:
            return ''

    
    def createPaperScience(self, paper):
        newPaper = Paper()
        params = {'apiKey': self.__API_KEY_Scopus}
        newURL = self.__URL_ABSTRACT + paper['prism:doi']
        session = requests.sessions.Session()
        session.headers.update(
            {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
            }
        )
        response = session.get(url= newURL, params=params)
        article = response.json()
        keywords = []

        newPaper.title = article['dc:title']
        #newPaper.authors = paper['dc:author']
        newPaper.journal = ['prism:publicationName']

        try:
            newPaper.abstract = article['full-text-retrieval-response']['coredata']['dc:description']
        except:
            pass
        
        try:
            for item in article['full-text-retrieval-response']['coredata']['dcterms:subject']:
                keywords.append(item)
        except:
            pass

        newPaper.keywords = keywords

        return newPaper



    def searchIEEEPapers(self, query:str, fun):
        """ Procura artigos na base IEEE e retorna uma lista com os resultados
        Parameters
        ----------
        query : str
            query que será usada para procurar os artigos

        Returns
        -------
        list
            lista com os artigos encontrados
        """
        
        listPapers = []
        totalResults = 0
        pages = 0
        results = None

        api = XPLORE(self.__API_KEY_IEEE)
        api.booleanText(query)
        api.maximumResults(200)
        api.startingResult(0)
        data = api.callAPI()
        results = json.loads(data)
        totalResults = results['total_records']
        pages = math.ceil(totalResults/200)
        self.addToList(results, listPapers)

        print("-------------------------------------------------------------")
        print("Artigos encontrados = " + str(totalResults))
        print("-------------------------------------------------------------") 
        
        for i in range(1, pages):
            api.booleanText(query)
            api.startingResult((i*200) + 1)
            data = api.callAPI()
            results = json.loads(data)
            self.addToList(results, listPapers)
            i = i + 1

        return self.organizePapersIEEE(listPapers)

    
    def addToList(self, list1:list, list2:list):
        for item in list1['articles']:
            list2.append(item)


    def organizePapersIEEE(self,papers:[]):
        """ Recebe uma lista de páginas contendo artigos
        encontrados na Scopos e os organiza.
        ----------
        papers : list
            lista de paginas com os artigos encontrados

        Returns
        -------
        list
            lista com os artigos organizados
        """
        newList = []   

        if(papers != None and len(papers) != 0):
            for paper in papers:
                newList.append(self.createPaperIEEE(paper))

        return newList


    def createPaperIEEE(self, paper):
        """ Recebe um artigo retornado na pesquisa da IEEE e
        cria objetos Paper para serem utilizados na análise
        de eficácia da String.
        ----------
        papers : Json
            paper para se criar o objeto

        Returns
        -------
        Papper
            papper criado
        """
        newPaper = Paper()

        try:
            newPaper.title = self.getPaperValue(paper,'title')
        except:
            pass
        try:
            newPaper.journal = self.getPaperValue(paper,'publication_title')
        except:
            pass
        try:
            newPaper.abstract  = self.getPaperValue(paper,'abstract')
        except:
            pass
        try:
            newPaper.keywords = paper['index_terms']['author_terms']['terms']
        except:
            pass

        for author in paper['authors']['authors']:
            newPaper.authors = author['full_name']
            break
       
        return newPaper    

