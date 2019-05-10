from StringAnalyser import StringAnalyser
import unittest

class StringAnalyser_test(unittest.TestCase):

    def setUp(self):
        sinonimos1 = ["UI testing", "user interface testing",
          "graphical user interface testing", "GUI testing"]
        keywords = [sinonimos1]
        self.s = StringAnalyser('scopus.bib', keywords)

    #Quando houver ganho de sensibilidade e perda de precisão.
    def test_compareSenPre1(self):
        self.s.__sensibility = 70
        self.s.__sensibilityTemp = 75
        self.s.__precision = 10
        self.s.__precisionTemp = 12
        #Se o ganho de sensibilidade for maior que a perda de presisão.
        #Deverá retornar true, pois a nova string é melhor que a anterior
        self.assertEquals(True,self.s.compareSensibilityPrecision())
    
    
    #Quando houver ganho de sensibilidade e perda de precisão.
    def test_compareSenPre2(self):
        self.s.__sensibility = 70
        self.s.__sensibilityTemp = 75
        self.s.__precision = 10
        self.s.__precisionTemp = 18
        #Se o ganho de sensibilidade for menor que a perda de presisão.
        #Deverá retornar false, pois a nova string é pior que a anterior
        self.assertEquals(False,self.s.compareSensibilityPrecision())
    
    
    #Quando houver ganho de precisão e perda de sensibilidade.
    def test_compareSenPre3(self):
        self.s.__sensibility = 70
        self.s.__sensibilityTemp = 66
        self.s.__precision = 10
        self.s.__precisionTemp = 5
        #Se o ganho de precisão for maior que a perda de sensibilidade.
        #Deverá retornar true, pois a nova string é melhor que a anterior
        self.assertEquals(True,self.s.compareSensibilityPrecision())

    
    #Quando houver ganho de precisão e perda de sensibilidade.
    def test_compareSenPre4(self):
        self.s.__sensibility = 70
        self.s.__sensibilityTemp = 60
        self.s.__precision = 10
        self.s.__precisionTemp = 8
        #Se o ganho de precisão for menor que a perda de sensibilidade.
        #Deverá retornar false, pois a nova string é pior que a anterior
        self.assertEquals(False,self.s.compareSensibilityPrecision())


    #Quando houver ganho de precisão e ganho de sensibilidade.
    def test_compareSenPre5(self):
        self.s.__sensibility = 70
        self.s.__sensibilityTemp = 80
        self.s.__precision = 10
        self.s.__precisionTemp = 8
        #Deve retornar true, pois a string nova é melhor
        self.assertEquals(True,self.s.compareSensibilityPrecision())


    #Quando houver perda de precisão e perda de sensibilidade.
    def test_compareSenPre6(self):
        self.s.__sensibility = 70
        self.s.__sensibilityTemp = 60
        self.s.__precision = 10
        self.s.__precisionTemp = 12
        #Deve retornar false, pois a string antiga é melhor
        self.assertEquals(False,self.s.compareSensibilityPrecision())


    #Quando precisão não mudar e houver perda de sensibilidade.
    def test_compareSenPre7(self):
        self.s.__sensibility = 70
        self.s.__sensibilityTemp = 60
        self.s.__precision = 10
        self.s.__precisionTemp = 10
        
        self.assertEquals(False,self.s.compareSensibilityPrecision())

    
    #Quando precisão não mudar e hover ganho de sensibilidade.
    def test_compareSenPre8(self):
        self.s.__sensibility = 70
        self.s.__sensibilityTemp = 80
        self.s.__precision = 10
        self.s.__precisionTemp = 10
        
        self.assertEquals(True,self.s.compareSensibilityPrecision())

    
    #Quando sensibilidade não mudar e houver perda de precisão.
    def test_compareSenPre9(self):
        self.s.__sensibility = 70
        self.s.__sensibilityTemp = 70
        self.s.__precision = 10
        self.s.__precisionTemp = 12
        
        self.assertEquals(False,self.s.compareSensibilityPrecision())

    
    #Quando sensibilidade não mudar e houver ganho de precisão.
    def test_compareSenPre10(self):
        self.s.__sensibility = 70
        self.s.__sensibilityTemp = 70
        self.s.__precision = 10
        self.s.__precisionTemp = 8
        
        self.assertEquals(True,self.s.compareSensibilityPrecision())

if __name__ == '__main__':
    unittest.main()
