import preprocessor as pp #https://pypi.org/project/tweet-preprocessor/

def text_cleaner(text):
    #Set the options to tokenize. URL -> $URL$, MENTION -> $MENTION$
    pp.set_options(pp.OPT.URL)
    toRtn = pp.tokenize(text)
    return toRtn.replace("$URL$", "")