from StringGenerator import *
from Paper import *
from StringAnalyser import StringAnalyser
from PaperSearcher import PaperSearcher

class StringImprover:

    def improveStringScopus(self,keywords:[], bib):
        """ Gera uma string e a melhora.
        ----------
        keywords: list
            Lista de keywords e seus sinônimos que serão utilizados
            na geração das Strings.
        bib: str
            Caminho do arquivo bib que será utilizado como base para
            analisar a string
        """
        analyser = StringAnalyser(bib, keywords)
        stringBase = None
        paperSearcher = PaperSearcher()
       
        string = StringGenerator.generateScopusString(StringGenerator,keywords)
        print(string)
        papers = paperSearcher.searchScopusPapers(string)
            
        if(analyser.analysePapers(papers) or stringBase == None):
            stringBase = string
            
        print("Precisão da melhor String = " + str(analyser.getPrecision()))
        print("Sensibilidade da melhor String = " + str(analyser.getSensibility()))

        print("Precisão Atual = " + str(analyser.getPrecisionTemp()))
        print("Sensibilidade Atual = " + str(analyser.getSensibilityTemp()) + "\n\n")
        
        print("\n\nString Final = " +  stringBase)
        return stringBase
        
        
    def improveStringIEEE(self,keywords:[], bib, fun):
        """ Gera uma string e a melhora.
        ----------
        keywords: list
            Lista de keywords e seus sinônimos que serão utilizados
            na geração das Strings.
        bib: str
            Caminho do arquivo bib que será utilizado como base para
            analisar a string
        """
        analyser = StringAnalyser(bib, keywords)
        stringBase = None
        paperSearcher = PaperSearcher()

        
        string = StringGenerator.generateIEEEString(StringGenerator,keywords)
        print(string)
        papers = paperSearcher.searchIEEEPapers(string, fun)
            
        if(analyser.analysePapers(papers) or stringBase == None):
            stringBase = string
            
        print("Precisão da melhor String = " + str(analyser.getPrecision()))
        print("Sensibilidade da melhor String = " + str(analyser.getSensibility()))

        print("Precisão Atual = " + str(analyser.getPrecisionTemp()))
        print("Sensibilidade Atual = " + str(analyser.getSensibilityTemp()) + "\n\n")
        
        print("\n\nString Final = " +  stringBase)
        return stringBase



    def teste(self, baseName, fun):
        seacher = StringImprover()
        #sinonimos1 = ["Scope", "Scoping"]
        sinonimos1 = ["user inteface testing", "UI testing", "graphical user interface testing", "GUI testing"]
        #sinonimos2 = ["Software product line", "software family", "software reuse", "spl"]
        #sinonimos3 = ["approach", "method", "methodology", "technique"]
        keywords = [sinonimos1]

        if(baseName == "Scopus"):            
            return seacher.improveStringScopus(keywords,'scopus.bib')
        elif (baseName == "IEEE"):
            return seacher.improveStringIEEE(keywords,'scopus.bib', fun)


