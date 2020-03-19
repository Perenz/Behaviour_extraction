import preprocessor as pp #https://pypi.org/project/tweet-preprocessor/

def text_cleaner(text):
    #Set the options to tokenize. URL -> $URL$, MENTION -> $MENTION$
    pp.set_options(pp.OPT.URL, pp.OPT.MENTION)
    return pp.tokenize(text)