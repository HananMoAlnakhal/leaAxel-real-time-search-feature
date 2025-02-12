# Search Engine

## about the feature

This project is an AI-powered search engine designed to analyze the users' questions, searching the web based on the Keywords found in the user's question, and provides structured responses based on provided text.
The system integrates **LLMs (Large Language Models), keyword extraction, web scrapping, summarization, multithreading, and entity recognition** to enhance the accuracy and usefulness of processed text.

## how to use it?

1. **Clone the Repository**

   ```bash
   git clone https://github.com/HananMoAlnakhal/leaAxel-real-time-search-feature
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **add your APIs in `common/api.py`**

   ```python
   APIs={
       'google API':"xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",#<---this is for the programable search API
       'google cx' :"xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",#<---this is for the programable search engine CX
       'Gemini':'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'#<--this si for LLM Gemini :)
   }
   ```

4. **You can now import the module `Searcher()` !**

### example usage

```python
searcher=Searcher()
user_query = "who is the current president of the usa?"
search_Results=searcher.search_the_web(user_query)
print("answer:")
print(search_Results)
```

#### output

```plaintext
answer:
The current president of the United States is Donald John Trump. He is the 47th and current president of the United States.

For more details, visit:
https://www.whitehouse.gov/administration/donald-j-trump/
https://www.usa.gov/presidents

```

## Project structure

```plaintext
axel_search/
├── README.md                # Project overview and setup instructions
├── main.py                  # Runs the application and manages the workflow
├── requirements.txt         # Python dependencies
└── common/
    ├── api.py               # has the API configs
    ├── analyzer.py          # keyword extraction and nlp entities
    └── large_lang_model.py  # Handles interactions with external LLM services
```

## special requirements

- Requires Python 3.8+ for compatibility.
- Needs an active API keys.

## Limitation

- The processing speed depends on the text length and the model being used.
- If using SpaCy features, ensure `en_core_web_sm` is downloaded.
- specific info e.g.(weather, stock market..etc.) must be looked up using an API directly without searching the web

## Future Improvements

- Support for additional LLMs and APIs.
- More advanced entity recognition.
- Optimization for faster query processing.
