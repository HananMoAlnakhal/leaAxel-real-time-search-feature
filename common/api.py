def What_I_have(name):
    """This is a Function That has all of the APIs I have got !\n
    use :\n
    What_I_have('API name') #to get the API!\n
    Output:\n
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    """
    APIs={
        'google API':"xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",#<---this is for the programable search API 
        'google cx' :"xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",#<---this is for the programable search engine CX
        'Gemini':'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'#<--this si for LLM Gemini :)
    }
    if not(name in APIs):
        raise TypeError("*"*50+"\nthe thing your looking for is not here \nGo Get an API!")
    result=APIs.get(name)
    return result