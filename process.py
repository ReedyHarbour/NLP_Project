import nltk
from sys import stdin
from nltk.tag.stanford import StanfordNERTagger
from nltk.tag import StanfordNERTagger
from stanford_utils import *
from nltk.stem.wordnet import WordNetLemmatizer

lemma = WordNetLemmatizer()

yesno_list = ['be','have', 'has', 'had', 'do','will','can','would','could','should','shall','may','might','did','does',"didn't","doesn't",'was','is','am','are','were']

def tokenizeDoc(cur_doc):
    return re.findall('\\w+', cur_doc)

def tokenizeSent(text):
    return nltk.sent_tokenize(text)

def tokenizeWord(sentence):
    return nltk.word_tokenize(sentence)

def tagSent(sentence):
    tokens = tokenizeWord(sentence)
    path_to_model = "stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz"
    path_to_jar = "stanford-ner/stanford-ner.jar"
    st = StanfordNERTagger(path_to_model, path_to_jar)
    return st.tag(tokens)

def get_best(candidates, question, tokens):
    mini = 10000
    index = -1
    for i,can in enumerate(candidates):
        pos1 = can[0]
        pos2 = can[-1]
        s = 0
        for w in question:
            indices = [i for i,x in enumerate(tokens) if x == w]
            if len(indices) > 0:
                s += min([min(abs(i-pos1),abs(i-pos2)) for i in indices])
        if s <= mini:
            mini = s
            index = i
    return index

def get_candidates(lst):
    ret = []
    cur = []
    prev = -1
    for id,num in enumerate(lst):
        if id > 0 and num != prev+1:
            ret.append(cur)
            cur = [num]
        else:
            cur.append(num)
        prev = num
    if len(cur) > 0:
        ret.append(cur)
    return ret

def who(question, sentence):
    tokens = tokenizeWord(sentence)
    tokens = [lemma.lemmatize(w) for w in tokens]
    tags = tagSent(sentence)
    answer = [i for i,tag in enumerate(tags) if tag[1] == 'PERSON']
    candidates = get_candidates(answer)
    result = []
    for ind_list in candidates:
        temp = []
        for i in ind_list:
            if tokens[i].lower() not in question:
                temp.append(i)
        if temp != []: 
            result.append(temp)
    candidates = result

    index = get_best(candidates, question, tokens)
    if index != -1:
        return ' '.join([tags[i][0] for i in candidates[index]])
    else:
        return sentence

def when(question, sentence):
    tokens = tokenizeWord(sentence)
    tokens = [lemma.lemmatize(w) for w in tokens]
    tags = tagSent(sentence)
    answer = [i for i,tag in enumerate(tags) if tag[1] == 'DATE' or tag[1] == 'TIME']
    candidates = get_candidates(answer)
    result = []
    for ind_list in candidates:
        temp = []
        for i in ind_list:
            if tokens[i].lower() not in question:
                temp.append(i)
        if temp != []: 
            result.append(temp)
    candidates = result
    index = get_best(candidates, question, tokens)
    if index != -1:
        return ' '.join([tags[i][0] for i in candidates[index]])
    else:
        return sentence

def where(question, sentence):
    tokens = tokenizeWord(sentence)
    tokens = [lemma.lemmatize(w) for w in tokens]
    tags = tagSent(sentence)
    answer = [i for i,tag in enumerate(tags) if tag[1] == 'LOCATION']
    candidates = get_candidates(answer)
    result = []
    for ind_list in candidates:
        temp = []
        for i in ind_list:
            if tokens[i].lower() not in question:
                temp.append(i)
        if temp != []: 
            result.append(temp)
    candidates = result
    index = get_best(candidates, question, tokens)
    if index != -1:
        return ' '.join([tags[i][0] for i in candidates[index]])
    else:
        return sentence

def what(question, sentence):
    tags = tagSent(sentence)
    return sentence

def which(question, sentence):
    tags = tagSent(sentence)
    return sentence

def how(question, sentence):
    tags = tagSent(sentence)
    return sentence

def howmany(question, sentence):
    tags = tagSent(sentence)
    return sentence

def howmuch(question, sentence):
    tokens = tokenizeWord(sentence)
    tokens = [lemma.lemmatize(w) for w in tokens]
    tags = tagSent(sentence)
    answer = [i for i,tag in enumerate(tags) if tag[1] == 'MONEY']
    candidates = get_candidates(answer)
    index = get_best(candidates, question, tokens)
    if index != -1:
        return ' '.join([tags[i][0] for i in candidates[index]])
    else:
        return sentence

def why(question, sentence):
    return sentence

def yesno(question, sentence):
    tags = tagSent(sentence)
    return sentence


def getTag(line):
    words = line.lower().split()
    if len(words) < 2:
        return "TOOSHORT"
    if words[0] == "who" or (words[0] == "to" and words[1] == "whom"):
        return "WHO"
    elif words[0] == "when":
        return "WHEN"
    elif words[0] == "where":
        return "WHERE"
    elif words[0] == "what":
        return "WHAT"
    elif words[0] == "which":
        return "WHICH"
    elif words[0] == "how" and words[1] == "many":
        return "HOW MANY"
    elif words[0] == "how" and words[1] == "much":
        return "HOW MUCH"
    elif words[0] == "how":
        return "HOW"
    elif words[0] == "why":
        return "WHY"
    elif lemma.lemmatize(words[0],'v') in yesno_list:
        return "YESNO"
    else:
        
        return "NONE"

