import google.generativeai as genai
from common.api import What_I_have

genai.configure(api_key=What_I_have("Gemini"))

class Summerier():
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro') 
        pass
    def sum_webpages(self,scrapedText,Query):
        self.prompt=f"""You are an AI assistant that summarizes text based on the provided content. Your task is to analyze the text, reason over the context, and extract the most relevant information to answer the user's question. If the information is not explicitly stated but can be reasonably inferred from the context, provide the inferred answer. However, do not add any information that cannot be supported by the text.

Guidelines:
1. The summary must be factual, objective, and non-conversational.
2. If the text does not contain relevant information to answer the question, state that clearly instead of making assumptions.
3. Present the summary in clear, direct sentences without introductory phrases like "the text states" or "the article discusses."
4. If the answer can be inferred from the context, provide the inferred answer with a clear indication that it is based on contextual reasoning.
5. Structure the response using bullet points or short factual statements.

User Question: {Query}
Text to summarize: {scrapedText}

Output Format:
- Directly answer the question using information from the text.
- If the answer is based on contextual reasoning, indicate this by starting with "Based on the context, ..."
- If the answer is unclear or not present in the text, explicitly state: 'The provided text does not contain information to answer this question.'"""
        response = self.model.generate_content(self.prompt)
        return response.text
    
    def getting_final_result(self,result,Query):
        self.prompt=f""""Based strictly on the provided extracted content, generate a user-friendly and factual response to the question.

Guidelines:
Treat URLs as plain text and extract meaningful information from them.
Ignore any entries where the content states, ‘The provided text does not contain information to answer this question.’
Ignore the accuracy score in all entries.
Extract useful information from the remaining entries, including any meaningful details within URLs.
Generate a friendly and informative response based only on the provided valid content.
Include two URLs from the sources where the useful information was found, formatted as:
‘For more details, visit: [URL1], [URL2]’
Do not add any external knowledge beyond the provided text.
User Question:
{Query}

Extracted Relevant Content:
{result}

Output Format:
A clear and friendly response that answers the user’s question.
Two URLs as clickable references for more details."""
        response = self.model.generate_content(self.prompt)
        return response.text

