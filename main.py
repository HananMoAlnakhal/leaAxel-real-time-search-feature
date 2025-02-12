import requests
from bs4 import BeautifulSoup
from duckduckgo_search  import DDGS
import threading
import queue
import re
from common.analyzer import TextAnalyzer
from common.large_lang_model import Summerier
from common.api import What_I_have

class Searcher():
    def __init__(self):
        self.result_queue = queue.Queue() 
        self.analysis_queue = queue.Queue()
        self.summarizer=Summerier()
    
    def search_the_web(self,user_query, num_results=20):
        google_thread = threading.Thread(target=self.search_google, args=(user_query,num_results))
        duckduckgo_thread = threading.Thread(target=self.search_duckduckgo, args=(user_query,num_results))

        google_thread.start()
        duckduckgo_thread.start()

        google_thread.join()
        duckduckgo_thread.join()

        results = {}
        for  result in self.result_queue.get().items():
            search_engine, data = result
            results[search_engine] = data
        print("got results from engines")
        analyzed_results = self.analyze_results(results, user_query)
        print("results that entered the LLM")
        final_ans=self.summarizer.getting_final_result(analyzed_results,user_query)# will ask Gemini for that :)
        return final_ans

    def search_duckduckgo(self, user_query, num_results=20):
        results = DDGS().text(user_query, max_results=num_results)
        Q=TextAnalyzer(user_query)
        
        search_results = [{"title": item["title"],
                            "link": item["href"],
                            "snippet": item["body"],
                            "rank":Q.KeywordPoints(item["body"])} for item in results]
        self.result_queue.put({"DuckDuckGo":search_results})
        return search_results

    def search_google(self,user_query, num_results=20):
        url = f"https://www.googleapis.com/customsearch/v1?q={user_query}&key={What_I_have('google API')}&cx={What_I_have('google cx')}"
        headers = {"User-Agent": "Mozilla/5.0"}  
        try:
            response = requests.get(url, headers=headers,timeout=30)
            response.raise_for_status() 
            Q=TextAnalyzer(user_query)
            results = response.json().get("items", [])
            search_results = [{"title": item["title"],
                                "link": item["link"],
                                "snippet": item["snippet"],
                                "rank":Q.KeywordPoints(item["snippet"])}for item in results[:num_results]]
            self.result_queue.put({"Google": search_results})
            return search_results
        
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []

    def analyze_results(self, search_results, user_query):
        threads = []
        self.user_query=user_query
        for eng_results in search_results.items():
            for result in eng_results[1]:
                if int(result["rank"]) > 0:
                    thread = threading.Thread(target=self.fetch_and_analyze, args=(result["link"],))
                    threads.append(thread)
                    thread.start()

        for thread in threads:
            thread.join()

        analyzed_results = []
        while not self.analysis_queue.empty():
            analyzed_results.append(self.analysis_queue.get())
        return analyzed_results
    
    def fetch_and_analyze(self, url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            article_title = soup.find('h1')
            main_content = []
            if article_title:
                for sibling in article_title.find_all_next():
                    if sibling.name == 'footer':
                        break  
                    main_content.append(sibling.get_text(strip=True))
            text_content = ' '.join(main_content)
            accuracy_score = self.calculate_accuracy(text_content,self.user_query)
            summ=self.summarizer.sum_webpages(text_content[:5000],self.user_query)
            self.analysis_queue.put({
                "content": summ,
                "url": url,
                "accuracy_score": accuracy_score})

        except requests.RequestException:
            pass 

    def calculate_accuracy(self, text, user_query):
        keywords = [kw.lower() for kw in TextAnalyzer(user_query).keywords]
        text_lower = text.lower()
        keyword_count = sum(len(re.findall(rf'\b{re.escape(kw)}\b', text_lower)) for kw in keywords)
        total_words = len(re.findall(r'\w+', text_lower))
        if total_words == 0 or keyword_count == 0:
            return 0.0 
        normalized_score = (keyword_count / total_words) * 100  
        return round(min(normalized_score, 100), 2)
    




