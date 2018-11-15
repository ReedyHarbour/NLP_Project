import nltk
from nltk.tree import Tree
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import os
import re
import sys
import math

# nltk.download('punkt')
# nltk.download('stopwords')

class Answer(object):
    def __init__(self, sentences, question):
        self.sentences = sentences
        self.question = question
        self.length = 0
        for s in self.sentences:
            for word in self.question:
                self.length += s.count(word)

        self.sentences = self.preprocessSentence(self.sentences)
        self.questionDict = self.compQues(self.question)
        self.sentDict = self.calculToken(self.sentences, self.questionDict)
        self.vectorList = self.similarity(self.question)

    def preprocessSentence(self, sentList):
        for words in sentList:
            words = [w for w in words if w not in stopwords.words()]
        return sentList

    # take in a sentence of words
    def calculToken(self, sentList, questionDict):
        questionSet = questionDict.keys()
        vocabulary = set()
        sentDictList = []

        for words in sentList:
            d = dict()

            for word in words:
                if word in questionDict:
                    d[word] = d.get(word, 0) + 1
            for word in d:
                d[word] = d[word] / self.length
            sentDictList.append(d)
        return sentDictList

    def compQues(self, questionList):
        d = dict()
        for word in questionList:
            d[word] = d.get(word, 0) + 1
        return d

    def termFreq(self, sentDict, word):
        return sentDict.get(word, 0)

    def inverseFreq(self, word, sentDict):
        count = 0
        if word in sentDict:
            count += 1
        return math.log(len(self.sentences) / (count + 1))

    def similarity(self, question):
        vectorList = []
        for sent in self.sentDict:
            vector = []
            for word in question:
                tfidf = self.termFreq(sent, word) * self.inverseFreq(word, sent)
                vector.append(tfidf)
            vectorList.append(vector)
        return vectorList

    def getSentence(self):
        for vector in self.vectorList:
            pass

#with open ("data/set1/a2.txt", "r") as doc:
#text = doc.read()
text = "Early life and education\nDonovan was born on March 4, 1982, in Ontario, California, to Donna Kenney-Cash, a special education teacher, and Tim Donovan, a semi-professional ice hockey player originally from Canada, which makes Donovan a Canadian citizen by descent. His mother raised him and his siblings in Redlands, California.\nWhen Donovan was six, his mother allowed him to join an organized league, and he scored seven goals in his first game. Donovan was a member of Cal Heat – a club based in nearby Rancho Cucamonga under coach Clint Greenwood. In 1997, he was accepted into U.S. Youth Soccer's Olympic Development Program. He attended Redlands East Valley High School when not engaged in soccer activities elsewhere. In 1999, Donovan attended the IMG Academy in Bradenton, Florida, part of U.S. Soccer's training program."
sent_text = nltk.sent_tokenize(text)
token = []
for sentence in sent_text:
    tokenized_text = nltk.word_tokenize(sentence)
    token.append(tokenized_text)
question = "Who was born in California".split()
A = Answer(token, question)

        # tagged = nltk.pos_tag(tokenized_text) 