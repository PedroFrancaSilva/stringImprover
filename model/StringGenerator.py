import random

class StringGenerator:
    """Classe responsável por gerar strings de busca"""

    def generateScopusString(self, keywords: []):
        """ Gera uma String para Scopus baseados nas keywords diponibilizadas
        Parameters
        ----------
        keywords : []
            keywords para se gerar uma string de busca

        Returns
        -------
        string
            String de busca gerada
        """
        newKeywords = StringGenerator.selectKeywords(StringGenerator,keywords)
        stringGerada = 'TITLE-ABS-KEY('
        contKeywords = 1

        for synonyms in newKeywords:
            localString = '("'
            contSynonyms = 1

            for word in synonyms:
                localString = localString + word
                if(contSynonyms != len(synonyms)):
                    localString = localString + '" OR "'
                else:
                    localString = localString + '"'
                contSynonyms = contSynonyms + 1

            stringGerada = stringGerada + localString

            if(contKeywords != len(keywords)):
                stringGerada = stringGerada + ') AND '
            else:
                stringGerada = stringGerada + ')'
            contKeywords = contKeywords + 1

        stringGerada = stringGerada + ')'
        return stringGerada


    def generateIEEEString(self, keywords: []):
        """ Gera uma String para Science Direct baseados nas keywords diponibilizadas
        Parameters
        ----------
        keywords : []
            keywords para se gerar uma string de busca

        Returns
        -------
        string
            String de busca gerada
        """
        newKeywords = StringGenerator.selectKeywords(StringGenerator,keywords)
        stringGerada = ''
        contKeywords = 1

        for synonyms in newKeywords:
            localString = '("'
            contSynonyms = 1

            for word in synonyms:
                localString = localString + word
                if(contSynonyms != len(synonyms)):
                    localString = localString + '" OR "'
                else:
                    localString = localString + '"'
                contSynonyms = contSynonyms + 1

            stringGerada = stringGerada + localString

            if(contKeywords != len(keywords)):
                stringGerada = stringGerada + ') AND '
            else:
                stringGerada = stringGerada + ')'
            contKeywords = contKeywords + 1

        stringGerada = stringGerada
        return stringGerada
    
    
    def selectKeywords(self, keywords: []):
        """ Seleciona keywords de uma lista e retorna uma nova lista
            com as keywords selecionadas.
        Parameters
        ----------
        keywords : []
            keywords para se selecionar uma nova lista

        Returns
        -------
        list
            nova lista com as keywords selecionadas
        """
        newKeywords = []

        for synonyms in keywords:
            newSynonym = []
            synonymsNumber = random.randint(1, len(synonyms))
            newSynonym = random.sample(synonyms, synonymsNumber)
            random.shuffle(newSynonym)
            newKeywords.append(newSynonym)

        return newKeywords

