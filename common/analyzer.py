import spacy
import yake

class TextAnalyzer():
    def __init__(self,Text=""):
        self.nlp = spacy.load("en_core_web_sm")
        self.text=Text
        self.keywords=TextAnalyzer.extract_keywords(self.text)

    def extract_keywords(text, max_keywords=5,details=False):
        kw_extractor = yake.KeywordExtractor(n=1, top=max_keywords)
        keywords = kw_extractor.extract_keywords(text)
        if details:
            return [(i[0],i[1]) for i in keywords]
        return [i[0] for i in keywords]
    
    def KeywordPoints(self, explore):
        bodyKeyWords = explore.lower()
        Rank = 0
        for word in self.keywords:
            word_lower = word.lower()
            Rank += bodyKeyWords.count(word_lower) 

        return Rank

