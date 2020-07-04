# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 20:55:01 2020

Created for testing the application of Google Translation and Google NLP APIs

@author: Levitannin

"""
import os

#apikey = r"C:\Users\Levitannin\Desktop\googlelang\amblykey.json"
#   Key for language service client -- nlp through google

apikey = r"C:/Users/Levitannin/Desktop/googlelang/amblytranskey.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = apikey

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import translate_v2 as translate

def google_translation(text):
    #   
    translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.detect_language(text)
    print(result)

    #print('Text: {}'.format(text))
    #print('Confidence: {}'.format(result['confidence']))
    #   Confidence is a range of 0 to 1, where 1 is equvilant to 100%
    #print('Language: {}'.format(result['language']))
    
    if result['confidence'] >= 0.80 and result['language'] == 'en':
        return True
    return False

def google_lang_analysis(text, verbose = True):
    client = language.LanguageServiceClient()
    document = types.Document(
        content = text,
        type = enums.Document.Type.PLAIN_TEXT
        )
    response = client.classify_text(document)
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence
    print(result)
    print()

    if verbose:
        print(text)
        for category in categories:
            print(u'=' * 20)
            print(u'{:<16}: {}'.format('category', category.name))
            print(u'{:<16}: {}'.format('confidence', category.confidence))
    
    sentiment = client.analyze_sentiment(document = document).document_sentiment
    #   inspects given text and identifies the prevailing emotional opinion
    #   within the text.  Attiude as positive, negative, oir neutral.
    
    print(sentiment)
    #   inspects given text for known entities (nouns like public figures, etc)
    #   Returns information about entities.
    
    return sentiment, result

if __name__ == '__main__':
    test_en = "This is a sentence in English.  The sentence is meant to help verify if Watson is able to identify this string of text as English.  It should be noted that the samples we will be dealing with will be quite longer than this."
    test_du = "Dies ist ein Satz auf Deutsch.  Der Satz soll helfen zu überprüfen, ob Watson in der Lage ist, diese Textfolge als deutsch zu identifizieren.  Es sei angemerkt, dass die Proben, mit denen wir uns befassen werden, wesentlich länger sein werden."
    test_ru = "Это предложение на русском.  Предложение призвано помочь проверить, может ли Ватсон идентифицировать эту строку текста как русскую.  Следует отметить, что примеры, с которыми мы будем иметь дело, будут гораздо длиннее."
    
    sen, result = google_lang_analysis(test_en)
    #   Not currently used -- for future testing.
    
    lang = google_translation(test_en)
    if lang: print("Great! This is in English")
    print()
        
    lang = google_translation(test_du)
    if lang: print("Great! This is in English")
    else: print("Uh oh, this is not English")
    print()
    
    lang = google_translation(test_ru)
    if lang: print("Great! This is in English")
    else: print("Uh oh, this is not English")