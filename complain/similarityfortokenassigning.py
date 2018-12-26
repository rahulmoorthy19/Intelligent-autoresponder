from rake_nltk import Rake
import sklearn
from sklearn.metrics import jaccard_similarity_score
import nltk 
import numpy as np
import pandas as pd
import textract
import string
import collections
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
stop_words=set(stopwords.words('english'))
keyword_extractor=Rake(stopwords=stop_words,punctuations=string.punctuation)
lemmatizer = WordNetLemmatizer()
feature_vector=sklearn.feature_extraction.text.TfidfVectorizer(min_df=0,max_df=50)


def file_processing(data):
    '''
    used for processing file
    Parameters:
    The text file path
    '''
    text=textract.process(data)
    text=text.decode("utf-8")
    text=text.lower()
    return text


def keyword_extractor_text(mail,refrencetoken):
    '''
    This Function is used for Extracting Keywords from two emails for similarity finding
    
    Parameters:
    The tokenised form of the text
    '''
    keyword_extractor.extract_keywords_from_text(mail)
    keywords_mail=keyword_extractor.ranked_phrases
    keywords_mail_tokens=''.join(c+" " for c in keywords_mail)
    keywords_mail_tokens=nltk.word_tokenize(keywords_mail_tokens)
    
    text_tokens_mail=nltk.word_tokenize(mail)
    text_tokens_mail = [s for s in text_tokens_mail if s]
    final_text_mail=[w for w in text_tokens_mail if w in keywords_mail_tokens]
    final_text_mail =[c for c in final_text_mail if c not in string.punctuation]
    final_text_mail=[w for w in final_text_mail if w.isalpha()]
    final_text_mail=[lemmatizer.lemmatize(s) for s in final_text_mail]
    
    keyword_extractor.extract_keywords_from_text(refrencetoken)
    keywords_ref=keyword_extractor.ranked_phrases
    keywords_tokens_ref=''.join(c+" " for c in keywords_ref)
    keywords_tokens_ref=nltk.word_tokenize(keywords_tokens_ref)
    
    text_tokens_ref=nltk.word_tokenize(refrencetoken)
    text_tokens2= [s for s in text_tokens_ref if s]
    final_text_ref=[w for w in text_tokens_ref if w in keywords_tokens_ref]
    final_text_ref =[c for c in final_text_ref if c not in string.punctuation]
    final_text_ref=[w for w in final_text_ref if w.isalpha()]
    final_text_ref=[lemmatizer.lemmatize(s) for s in final_text_ref]
    return final_text_mail,final_text_ref

def TFIDF(mail,refrencetokens):
    '''
    This function is used to calculate TFIDF vector
    Parameters:
    Job requirements keywords,cv keywords
    '''
    mail_lemmatization=[lemmatizer.lemmatize(s) for s in mail]
    ref_lemmatization=[lemmatizer.lemmatize(s) for s in refrencetokens]
    ref_feature=feature_vector.fit_transform(ref_lemmatization).toarray()
    mail_feature=feature_vector.transform(mail_lemmatization).toarray()
    return mail_feature,ref_feature

def jaccard_similarity(mail,query):
    '''
    CAN BE IMPLEMENTED ONLY WITH TFIDF OR SPARSE MATRIX!!!!!!
    This function is used to calculate jaccard_similarity
    Parameters:
    mail TFIDF matrix,query TFIDF matrix
    '''
    cnt=0
    for j in range(query.shape[1]):
        for i in range(query.shape[0]):
            if query[i][j]==1:
                cnt=cnt+1
                break
    similarity=(cnt/mail.shape[1])*100
    return similarity

def predict(mail,complain_1,service_1):
	'''
	Sample trial for two mails.The larger % similarity to a particular mail type so assign for the
	same
	'''
	complain=file_processing(complain_1)
	service=file_processing(service_1)
	keywords_complain,keywords_mail=keyword_extractor_text(complain,mail)
	keywords_service,keywords_mail1=keyword_extractor_text(service,mail)
	mail_tfidf,complain_tfidf=TFIDF(keywords_mail,keywords_complain)
	mail1_tfidf,service_tfidf=TFIDF(keywords_mail,keywords_service)
	complain=jaccard_similarity(complain_tfidf,mail_tfidf)
	service=jaccard_similarity(service_tfidf,mail1_tfidf)
	if complain>service:
		return 1
	elif complain<service:
		return 0
		


