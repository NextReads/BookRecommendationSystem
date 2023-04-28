
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')

nltk.download('wordnet') 
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')
# Words Tokenization
import re
from nltk.tokenize import word_tokenize
nltk.download('punkt')
def TokenizeWords(text):
    review=[]
    for i in text:
        sent = re.sub(r'[^\'\w\s]', ' ', i)
        review.append(word_tokenize(sent.lower()))
        # texts=word_tokenize(text.lower())
    return review


stopwords_english = stopwords.words('english')
stopwords_english.append("<br />")
stopwords_english.append("br")
stopwords_english.append("<br /><br />")
stopwords_english.extend(["'ll","'re","'ve","'s","'m","n't","'d","'ll","'re","'ve","'s","'m","n't","'d"])
def removeSW(texts):
    texts=[w for w in texts if not w.lower() in stopwords_english]
    return texts


# split into sentences for negative phrase identification
def sentenceSplit(text):
    # print(text)
    # try:
    text=text.replace('<br /><br />','').replace('(', ' ').replace(')', ' ')
    # except:
        # print("Error: ",text)

    sentences = re.split(r'[.!?,]', text)
    # my_list_2 = re.split(r',|-|:|.', text)
    sentences = [s.strip() for s in sentences if len(s) > 0]
    return sentences
# spacy lemmatization

# import spacy
# # spacy.download('en')
# def spacyLemmatize(texts):
#     nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
#     review=[]
#     for sent in texts:
#         doc = nlp(sent)
#         # texts= " ".join([token.lemma_ for token in doc])
#         review.append(" ".join([token.lemma_ for token in doc]))
#     return review


from nltk.tokenize import word_tokenize, sent_tokenize
tags=["JJ","JJR","JJS","RB","RBR","RBS","VB","VBD","VBG","VBN","VBP","VBZ"]
def pos_tagging(review):
    pos_tag=[]
    for sent in review:
        tag=nltk.pos_tag(sent)
        pos_tag.append(tag)
    return pos_tag
def TagNounremoval(review):
    texts=[]
    for sent in review:
        text=[]
        # print(sent)
        for word in sent:
            if word[1] in tags:
                text.append(word)
                
        # print(text)
        if len(text)>0:
            texts.append(text) 
    return texts
# Negative Phrase Identification
# we can add negative words to hashtable and then check if the word is present in the hash table later for better performance
negative_words_english=["not","n't","no","never","none","nothing","nowhere","neither","nor","hardly","scarcely","barely","don't","doesn't","didn't","isn't","aren't","wasn't","weren't","haven't","hasn't","hadn't","won't","wouldn't","shan't","shouldn't","can't","couldn't","mustn't","mightn't","needn't","oughtn't","daren't","needn't","needn't've","oughtn't've","daren't've","aren't","aren't've","couldn't","couldn't've","didn't","didn't've","doesn't","doesn't've","don't","don't've","hadn't","hadn't've","hasn't","hasn't've","haven't","haven't've","isn't","isn't've","mightn't","mightn't've","mustn't","mustn't've","needn't","needn't've","oughtn't","oughtn't've","shan't","shan't've","shouldn't","shouldn't've","wasn't","wasn't've","weren't","weren't've","won't","won't've","wouldn't","wouldn't've","mayn't","might've","must've","needn't","oughtn't","sha'n't","shan't","shouldn't","wasn't","weren't","won't","wouldn't","mustn't","needn't","oughtn't","shan't","shouldn't","wasn't","weren't","won't","wouldn't","mustn't","needn't","oughtn't","shan't","shouldn't","wasn't","weren't","won't","wouldn't","mustn't","needn't","oughtn't","shan't","shouldn't","wasn't","weren't","won't","wouldn't","mustn't","needn't","oughtn't","shan't","shouldn't","wasn't","weren't","won't","wouldn't","mustn't","needn't","oughtn't","shan't","shouldn't","wasn't","weren't","won't","wouldn't","mustn't","needn't","oughtn't","shan"]
def negPhraseIdentification(texts):
    negPhrases=[]
    for sentence in texts:
        # print(sentence)
        for word in sentence:
            if word[0] in negative_words_english:
                print("Negative: ",sentence)
                break
                    
    return negPhrases
def contractions(s):
 s = re.sub(r"won't", "will not",s)
 s = re.sub(r"would't", "would not",s)
 s = re.sub(r"could't", "could not",s)
 s = re.sub(r"\'d", " would",s)
 s = re.sub(r"can\'t", "can not",s)
 s = re.sub(r"n\'t", " not", s)
 s = re.sub(r"\'re", " are", s)
 s = re.sub(r"\'s", " is", s)
 s = re.sub(r"\'ll", " will", s)
 s = re.sub(r"\'t", " not", s)
 s = re.sub(r"\'ve", " have", s)
 s = re.sub(r"\'m", " am", s)
 return s
# def preprocessingWord(review):
#     # review=contractions(review)
#     review = spacyLemmatize(review)
#     # print(review)
#     review=TokenizeWords(review)
#     review=removeSW(review)

    
#     # review=lemmatize(review)
#     return review

import re
# text="One of the other reviewers has mentioned that after watching just 1 Oz episode you'll be hooked. They are right, as this is exactly what happened with me.<br /><br />The first thing that struck me about Oz was its brutality and unflinching scenes of violence, which set in right from the word GO. Trust me, this is not a show for the faint hearted or timid. This show pulls no punches with regards to drugs, sex or violence. Its is hardcore, in the classic use of the word.<br /><br />It is called OZ as that is the nickname given to the Oswald Maximum Security State Penitentary. It focuses mainly on Emerald City, an experimental section of the prison where all the cells have glass fronts and face inwards, so privacy is not high on the agenda. Em City is home to many..Aryans, Muslims, gangstas, Latinos, Christians, Italians, Irish and more....so scuffles, death stares, dodgy dealings and shady agreements are never far away.<br /><br />I would say the main appeal of the show is due to the fact that it goes where other shows wouldn't dare. Forget pretty pictures painted for mainstream audiences, forget charm, forget romance...OZ doesn't mess around. The first episode I ever saw struck me as so nasty it was surreal, I couldn't say I was ready for it, but as I watched more, I developed a taste for Oz, and got accustomed to the high levels of graphic violence. Not just violence, but injustice (crooked guards who'll be sold out for a nickel, inmates who'll kill on order and get away with it, well mannered, middle class inmates being turned into prison bitches due to their lack of street skills or prison experience) Watching Oz, you may become comfortable with what is uncomfortable viewing....thats if you can get in touch with your darker side."
# print(text)
# print('--------------------------------')
# print(preprocessingWord(text))
# text=sentenceSplit(text)

# text=pos_tagging(text)
# negPhraseIdentification(text)
from itertools import chain

def sentMerge(review):
    unzippedReview= list(chain(*review))
    return unzippedReview
       
def removePosTag(review):
    texts=[]
    for sent in review:
        text=[]
        for word in sent:
            text.append(word[0])
        texts.append(text)
    return texts
# Lemmatization wordnet
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
# review=[[('one', 'CD'), ('of', 'IN'), ('the', 'DT'), ('other', 'JJ'), ('reviewers', 'NNS'), ('has', 'VBZ'), ('mentioned', 'VBN'), ('that', 'IN'), ('after', 'IN'), ('watching', 'VBG'), ('just', 'RB'), ('1', 'CD'), ('oz', 'JJ'), ('episode', 'NN'), ('you', 'PRP'), ("'ll", 'MD'), ('be', 'VB'), ('hooked', 'VBN')], [('they', 'PRP'), ('are', 'VBP'), ('right', 'JJ')], [('as', 'IN'), ('this', 'DT'), ('is', 'VBZ'), ('exactly', 'RB'), ('what', 'WP'), ('happened', 'VBD'), ('with', 'IN'), ('me', 'PRP')], [('the', 'DT'), ('first', 'JJ'), ('thing', 'NN'), ('that', 'WDT'), ('struck', 'VBD'), ('me', 'PRP'), ('about', 'IN'), ('oz', 'NN'), ('was', 'VBD'), ('its', 'PRP$'), ('brutality', 'NN'), ('and', 'CC'), ('unflinching', 'JJ'), ('scenes', 'NNS'), ('of', 'IN'), ('violence', 'NN')], [('which', 'WDT'), ('set', 'VBP'), ('in', 'IN'), ('right', 'NN'), ('from', 'IN'), ('the', 'DT'), ('word', 'NN'), ('go', 'VB')], [('trust', 'NN'), ('me', 'PRP')], [('this', 'DT'), ('is', 'VBZ'), ('not', 'RB'), ('a', 'DT'), ('show', 'NN'), ('for', 'IN'), ('the', 'DT'), ('faint', 'NN'), ('hearted', 'VBD'), ('or', 'CC'), ('timid', 'VB')], [('this', 'DT'), ('show', 'NN'), ('pulls', 'VBZ'), ('no', 'DT'), ('punches', 'NNS'), ('with', 'IN'), ('regards', 'NNS'), ('to', 'TO'), ('drugs', 'NNS')], [('sex', 'NN'), ('or', 'CC'), ('violence', 'NN')], [('its', 'PRP$'), ('is', 'VBZ'), ('hardcore', 'NN')], [('in', 'IN'), ('the', 'DT'), ('classic', 'JJ'), ('use', 'NN'), ('of', 'IN'), ('the', 'DT'), ('word', 'NN')], [('it', 'PRP'), ('is', 'VBZ'), ('called', 'VBN'), ('oz', 'RB'), ('as', 'IN'), ('that', 'DT'), ('is', 'VBZ'), ('the', 'DT'), ('nickname', 'JJ'), ('given', 'VBN'), ('to', 'TO'), ('the', 'DT'), ('oswald', 'JJ'), ('maximum', 'JJ'), ('security', 'NN'), ('state', 'NN'), ('penitentary', 'NN')], [('it', 'PRP'), ('focuses', 'VBZ'), ('mainly', 'RB'), ('on', 'IN'), ('emerald', 'NNS'), ('city', 'NN')], [('an', 'DT'), ('experimental', 'JJ'), ('section', 'NN'), ('of', 'IN'), ('the', 'DT'), ('prison', 'NN'), ('where', 'WRB'), ('all', 'PDT'), ('the', 'DT'), ('cells', 'NNS'), ('have', 'VBP'), ('glass', 'NN'), ('fronts', 'NNS'), ('and', 'CC'), ('face', 'NN'), ('inwards', 'NNS')], [('so', 'RB'), ('privacy', 'NN'), ('is', 'VBZ'), ('not', 'RB'), ('high', 'JJ'), ('on', 'IN'), ('the', 'DT'), ('agenda', 'NN')], [('em', 'JJ'), ('city', 'NN'), ('is', 'VBZ'), ('home', 'VBN'), ('to', 'TO'), ('many', 'JJ')], [('aryans', 'NNS')], [('muslims', 'NNS')], [('gangstas', 'NNS')], [('latinos', 'NNS')], [('christians', 'NNS')], [('italians', 'NNS')], [('irish', 'JJ'), ('and', 'CC'), ('more', 'JJR')], [('so', 'RB'), ('scuffles', 'NNS'), ('death', 'NN'), ('stares', 'NNS'), ('dodgy', 'JJ'), ('dealings', 'NNS'), ('and', 'CC'), ('shady', 'JJ'), ('agreements', 'NNS'), ('are', 'VBP'), ('never', 'RB'), ('far', 'RB'), ('away', 'RB')], [('i', 'NN'), ('would', 'MD'), ('say', 'VB'), ('the', 'DT'), ('main', 'JJ'), ('appeal', 'NN'), ('of', 'IN'), ('the', 'DT'), ('show', 'NN'), ('is', 'VBZ'), ('due', 'JJ'), ('to', 'TO'), ('the', 'DT'), ('fact', 'NN'), ('that', 'IN'), ('it', 'PRP'), ('goes', 'VBZ'), ('where', 'WRB'), ('other', 'JJ'), ('shows', 'NNS'), ('would', 'MD'), ("n't", 'RB'), ('dare', 'VB')], [('forget', 'VB'), ('pretty', 'RB'), ('pictures', 'NNS'), ('painted', 'VBN'), ('for', 'IN'), ('mainstream', 'JJ'), ('audiences', 'NNS')], [('forget', 'VB'), ('charm', 'NN')], [('forget', 'VB'), ('romance', 'NN')], [('oz', 'NN'), ("does", 'VBZ'), ("n't", 'RB'), ('mess', 'VB'), ('around', 'RB')], [('the', 'DT'), ('first', 'JJ'), ('episode', 'NN'), ('i', 'NN'), ('ever', 'RB'), ('saw', 'VBD'), ('struck', 'VBN'), ('me', 'PRP'), ('as', 'IN'), ('so', 'RB'), ('nasty', 'JJ'), ('it', 'PRP'), ('was', 'VBD'), ('surreal', 'JJ'), ('i', 'NN'), ('could', 'MD')]]
def get_wordnet_pos(tag):
    """Map POS tag to first character lemmatize() accepts"""
    tag = tag[0].lower()
    tag_dict = {"j": wordnet.ADJ,
                "n": wordnet.NOUN,
                "v": wordnet.VERB,
                "r": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)
def lemmatize(review):
    lemmatizer = WordNetLemmatizer()

    for sent in review:
        # print(sent)
        for i in range(len(sent)):
            sent[i]=(lemmatizer.lemmatize(sent[i][0],pos=get_wordnet_pos(sent[i][1])),sent[i][1])
        # print(sent)
    return review
# lemmatize(review)
def reviewMerge(review):
    return ' '.join(review)

def convertToString(review):
    review = str(review)
    return review

def preprocessing(data):
   
    # # print(data.iloc[:1])
    # data['review_text']=data['review_text'].apply(convertToString)
    # data['review_text']=data['review_text'].apply(sentenceSplit)
    # # print("sentence split is complete")
    # data['review_text']=data['review_text'].apply(TokenizeWords)
    # # print("tokenization is complete")
    # data['review_text']=data['review_text'].apply(pos_tagging)
    # # print(data['review_text'][0])
    # # print("pos tagging is complete")
    # data['review_text']=data['review_text'].apply(TagNounremoval)
    # # print("noun removal is complete")
    # data['review_text']=data['review_text'].apply(lemmatize)
    # # print("lemmatization is complete")
    # data['review_text']=data['review_text'].apply(removePosTag)
    # # print("pos tag removal is complete")
    # # print(data['review_text'][0])
    # data['review_text']=data['review_text'].apply(sentMerge)
    # # print("merging is complete")
    # # print(data['review_text'][0])
    # data['review_text']=data['review_text'].apply(removeSW)
    # # print("stopword removal is complete")
    # data['review_text']=data['review_text'].apply(reviewMerge)
    # # print("review Merging is complete")
    # # print(data['review'][0])
    # return data
    data.loc[:, 'review_text']=data['review_text'].apply(convertToString)
    data.loc[:, 'review_text']=data['review_text'].apply(sentenceSplit)
    data.loc[:, 'review_text']=data['review_text'].apply(TokenizeWords)
    data.loc[:, 'review_text']=data['review_text'].apply(pos_tagging)
    data.loc[:, 'review_text']=data['review_text'].apply(TagNounremoval)
    data.loc[:, 'review_text']=data['review_text'].apply(lemmatize)
    data.loc[:, 'review_text']=data['review_text'].apply(removePosTag)
    data.loc[:, 'review_text']=data['review_text'].apply(sentMerge)
    data.loc[:, 'review_text']=data['review_text'].apply(removeSW)
    data.loc[:, 'review_text']=data['review_text'].apply(reviewMerge)
    return data
# print(df.iloc[:])
def preprocessReview(review):
   
    # print(data.iloc[:1])
    review=convertToString(review)
    review=sentenceSplit(review)
    # print("sentence split is complete")
    review=TokenizeWords(review)
    # print("tokenization is complete")
    review=pos_tagging(review)
    # print(review[0])
    # print("pos tagging is complete")
    review=TagNounremoval(review)
    # print("noun removal is complete")
    review=lemmatize(review)
    # print("lemmatization is complete")
    review=removePosTag(review)
    # print("pos tag removal is complete")
    # print(review[0])
    review=sentMerge(review)
    # print("merging is complete")
    # print(review[0])
    review=removeSW(review)
    # print("stopword removal is complete")
    review=reviewMerge(review)
    # print("review Merging is complete")
    # print(data['review'][0])
    return review