import bibtexparser
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from model.Paper import Paper

class StringAnalyser:
    __meanKeywords = 0
    __bibText = ""
    __keywords = []
    __goals = []
    __precisionTemp = 0
    __sensibilityTemp = 0
    __precision = -1
    __sensibility = -1
    __relevantes = []
    __nRelevantes = []

    def __init__(self, bibText, keywords:[]):
        """ Cria um objeto StringAnalyser.
        ----------
        bibText : str
            caminho do bibTex que será utilizado como
            base para a análise.
        keywords : list
            Lista de keywords e seus sinônimos que serão utilizados
            na geração das Strings.

        Returns
        -------
        StringAnalyser : StringAnalyser
            Um objeto StringAnalyser
        """
        self.__bibText = bibText
        self.__keywords = self.prepareKeywords(keywords)
        self.analyseGoal()
        return None

    def analyseGoal(self):
        """ Analisa os artigos disponibilizados no bibtex para
        determinar qual será meta a ser atingida.
        ----------
        """
        result = bibtexparser.loads(self.__bibText)
            

        self.__goals = self.createPapers(result)
        self.analyseAbstract(result)

    
    def createPapers(self,bibTexObject):
        """ Cria um objeto StringAnalyser.
        ----------
        bibText : str
            caminho do bibTex que será utilizado como
            base para a análise.
        keywords : list
            Lista de keywords e seus sinônimos que serão utilizados
            na geração das Strings.

        Returns
        -------
        StringAnalyser : StringAnalyser
            Um objeto StringAnalyser
        """
        papers = []

        for item in bibTexObject.entries_dict.items():
            paper = Paper()
            
            try:
                paper.title = item[1]['title']
            except Exception as e: print(e)

            try:
                paper.abstract = item[1]['abstract']
            except Exception as e: print(e)
            
            try:
                paper.journal = item[1]['journal']
            except Exception as e: print(e)

            try:
                paper.authors = item[1]['author']
            except Exception as e: print(e)
        
            papers.append(paper)
        return papers


    
    def analyseAbstract(self,bibtexObject):
        """ Analisa um conjunto de abstracts para determinar
        a média de keywords encontradas.
        ----------
        bibtexObject : Json
            Objeto pra se buscar o abstract
        """
        contObject = 0
        totalcont = 0
        
        for item in bibtexObject.entries_dict.items():
            try:
                tokens = nltk.word_tokenize(item[1]['abstract'])
                totalcont += self.compareAbstract(tokens)
                contObject += 1
            except Exception as e: print(e)

        self.__meanKeywords = totalcont/contObject


    def compareAbstract(self, tokens):
        """ Compara os valores dentro de um abstract com as keywords
        estabelecidas.
        ----------
        bibText : str
            tokens para ser comparados

        Returns
        -------
        cont : int
            Número de keywords enontrados dentro do abstract
        """
        tokens = self.prepareWords(tokens)
        cont = 0
        
        for word in tokens:
            for keyword in self.__keywords:
                if (word == keyword):
                    cont += 1

        return cont

    def prepareKeywords(self, keywords:[]):
        """ Prepara Keywords para serem comparadas.
        ----------
        keywords : list
            Lista de keywords e seus sinônimos que serão utilizados
            na geração das Strings.

        Returns
        -------
        newList : list
            Nova lista com as keywords preparadas para serem
            comparadas
        """
        preparedWords = []
        newList = []

        for item in keywords:
            preparedWords.append(self.prepareWords(item))

        for listWord in preparedWords:
            for word in listWord:
                newList.append(word)
        
        return newList
    
    def prepareWords(self, listWords):
        """ Prepara palavras para serem comparadas.
        ----------
        listWords : list
            Lista de palavras que serão utilizados

        Returns
        -------
        newList : list
            Nova lista com as palavras preparadas para serem
            comparadas
        """
        newWords = []
        stemmer = PorterStemmer()
        stop_words = set(stopwords.words("english"))

        #Para comparar melhor as palavras, é necessário retirar
        #as palavras desnecessárias e retirar sufixos
        for item in listWords:
            newList = nltk.word_tokenize(item)
            for word in newList:
                if word not in stop_words:
                    newWord = stemmer.stem(word)
                    newWords.append(newWord)
        
        newWords = list(set(newWords))
        
        return newWords
    
    
    def analysePapers(self, papers:Paper):
        """ Analisa um conjunto de papers a partir da meta
        estabelecida anteriormente.
        ----------
        papers : Paper
            Conjunto de papers para se analisar

        Returns
        -------
        resultado : bool
            Retorna True se o resultado atual for melhor
            que o resultado anterior ou se não houver
            resultado anterior.
        """
        relevantes = []
        nRelevantes = []

        for paper in papers:
            total = 0
            total += self.analysePaperAbstract(paper)
            total += self.analyseJournalAuthor(paper)
            
            if(total >= 0.5):
                relevantes.append(paper)
            else:
                nRelevantes.append(paper)
        
        #Fórmula da sensibilidade
        self.__sensibilityTemp = (len(relevantes) /
         (len(relevantes) + len(self.__goals))) * 100

        #Fórmula da precisão
        self.__precisionTemp = (len(relevantes) /
         (len(relevantes) + len(nRelevantes))) * 100

        if(self.__precision != -1 and self.__sensibility != -1):
            #Se a nova sensibilidade não estiver respeitando os limites
            if(self.__sensibilityTemp < 80 and self.__sensibility >= 80):
                return False

            #Se a nova precisão não estiver respeitando os limites    
            if(self.__precisionTemp >= 60 and self.__precision < 60):
                return False
        
        self.__relevantes = len(relevantes)
        self.__nRelevantes = len(nRelevantes)

        return self.compareSensibilityPrecision()

    
    def analysePaper(self, paper, relevantes, nRelevantes):
        total = 0
        total += self.analysePaperAbstract(paper)
        total += self.analyseJournalAuthor(paper)
            
        if(total >= 0.5):
            relevantes.append(paper)
        else:
            nRelevantes.append(paper)

    
    def calSenPre(self, relevantes, nRelevantes):
        #Fórmula da sensibilidade
        self.__sensibilityTemp = (len(relevantes) /
         (len(relevantes) + len(self.__goals))) * 100

        #Fórmula da precisão
        self.__precisionTemp = (len(relevantes) /
         (len(relevantes) + len(nRelevantes))) * 100

        if(self.__precision != -1 and self.__sensibility != -1):
            #Se a nova sensibilidade não estiver respeitando os limites
            if(self.__sensibilityTemp < 80 and self.__sensibility >= 80):
                return False

            #Se a nova precisão não estiver respeitando os limites    
            if(self.__precisionTemp >= 60 and self.__precision < 60):
                return False
        
        self.__relevantes = len(relevantes)
        self.__nRelevantes = len(nRelevantes)

        return self.compareSensibilityPrecision()

    
    def compareSensibilityPrecision(self):
        """ Compara a precisão e a sensibilidade da análise
        anterior com a análise atual.
        ----------

        Returns
        -------
        resultado : bool
            Retorna True se o resultado atual for melhor
            que o resultado anterior ou se não houver
            resultado anterior.
        """
        precisionDiference = 0
        sensibilityDiference = 0

        if(self.__precision == -1):
            self.__precision = self.__precisionTemp
            self.__sensibility = self.__sensibilityTemp
        else:
            precisionDiference = self.__precisionTemp - self.__precision
            sensibilityDiference = self.__sensibilityTemp - self.__sensibility

        return self.substitutePS(precisionDiference, sensibilityDiference)   
            

    def substitutePS(self, precisionDiference:int, sensibilityDiference:int):
        """ Substitui os valores anteriores da sensibilidade e precisão,
        se a análise atual for melhor que a análise anterior .
        ----------
        precisionDiference : int
            Diferença entre a precisão atual e a precisão anterior
        sensibilityDiference : int
            Diferença entre a sensibilidade atual e a
            sensibilidade anterior

        Returns
        -------
        resultado : bool
            Retorna True se o resultado atual for melhor
            que o resultado anterior ou se não houver
            resultado anterior.
        """
        sensibilityBetter = False
        precisionBetter = False

        if(precisionDiference < 0):
            precisionBetter = True
        else:
            precisionBetter = False

        if(sensibilityDiference > 0):
            sensibilityBetter = True
        else:
            sensibilityBetter = False

        if (sensibilityBetter and precisionBetter):
            self.__precision = self.__precisionTemp
            self.__sensibility = self.__sensibilityTemp
            return True         
        elif(sensibilityBetter):
            if(sensibilityDiference > precisionDiference):
                self.__precision = self.__precisionTemp
                self.__sensibility = self.__sensibilityTemp
                return True
        elif(precisionBetter):
            if(abs(precisionDiference) > abs(sensibilityDiference)):
                self.__precision = self.__precisionTemp
                self.__sensibility = self.__sensibilityTemp
                return True
    
        return False
    
    def analysePaperAbstract(self, paper:Paper):
        """ Compara os valores dentro de um abstract com as keywords
        estabelecidas.
        ----------
        paper : Paper
            paper para se retirar o abstract

        Returns
        -------
        total : int
            Número de keywords encontrados dentro do abstract
        """
        total = 0
        contTotal = 0
        tokens = nltk.word_tokenize(paper.abstract)
        tokens = self.prepareWords(tokens)

        for token in tokens:
            if token in self.__keywords:
                contTotal += 1
            
        if(contTotal >= self.__meanKeywords):
            total += 0.5

        return total

    
    def analyseJournalAuthor(self, paper:Paper):
        """ Analisa se os autores e jornais no paper disponibilizados
        atendem as metas.
        ----------
        paper : Paper
            paper para se analisar

        Returns
        -------
        total : int
            Número de artigos que atigiram as metas
        """
        total = 0
        
        for goal in self.__goals:
            if (goal.authors == paper.authors):
                total += 0.25
            if(goal.journal == paper.journal):
                total += 0.25
        
        return total

    
    def getPrecision(self):
        return self.__precision

    def getPrecisionTemp(self):
        return self.__precisionTemp

    def getSensibility(self):
        return self.__sensibility

    def getSensibilityTemp(self):
        return self.__sensibilityTemp

    def getRelevant(self):
        return self.__relevantes

    def getNRelevant(self):
        return self.__nRelevantes