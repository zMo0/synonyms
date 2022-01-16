import math
import time
def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    sum1_sq = norm(vec1)
    sum2_sq = norm(vec2)

    numerator = 0
    for key in vec1:
        if key in vec2:
            numerator += vec1[key] * vec2[key]
    
    return numerator/(sum1_sq * sum2_sq)


def build_semantic_descriptors(sentences):
    dictionary = {}
    for s in range (0, len(sentences)):
        dif_words = []
        for d in range (0, len(sentences[s])):
            if sentences[s][d] not in dif_words:
                dif_words.append(sentences[s][d]) 

        for w in range (0, len(dif_words)):
            if dif_words[w] in dictionary:
                for o_w in range (0, len(dif_words)):
                    if dif_words[o_w] in dictionary[dif_words[w]] and dif_words[o_w] != dif_words[w]:
                        dictionary[dif_words[w]][dif_words[o_w]] +=1
                    elif dif_words[o_w] == dif_words[w]:
                        pass
                    else:
                        dictionary[dif_words[w]][dif_words[o_w]] = 1
            
            else: #word not in dictionary yet
                dictionary[dif_words[w]] ={}
                for o_w in range (0, len(dif_words)):
                    if dif_words[o_w] in dictionary[dif_words[w]] and dif_words[o_w] != dif_words[w]:
                        dictionary[dif_words[w]][dif_words[o_w]] +=1
                    elif dif_words[o_w] == dif_words[w]:
                        pass
                    else:
                        dictionary[dif_words[w]][dif_words[o_w]] = 1
    return dictionary
                    
def build_semantic_descriptors_from_files(filenames):
    split_sentences =[]
    for file in filenames:
        f = open(file, 'r', encoding ='latin1') 
        text = f.read()
        for punct in ['-','--','\n']:
            text = text.replace(punct, ' ')
        for punct in [',',':',';']:
            text = text.replace(punct,'')
        
        text = text.lower().replace('?','.').replace('!','.').replace('...','.')
        sentences = text.split('.')
        all_sentences = [x for x in sentences if x != '']
        for s in range (0,len(all_sentences)):
            all_sentences[s] = all_sentences[s].replace('.','').strip().split()
        split_sentences += all_sentences
    return build_semantic_descriptors(split_sentences)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_sim = -1
    choice = -1
    for c in range (0,len(choices)):
        if (word in semantic_descriptors) and (choices[c] in semantic_descriptors) and choices[c] != '':
            s = similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[c]])
            if s > max_sim:
                max_sim = s
                choice = c
    if choice != -1:
        return choices[choice] 
    else: 
        if choices != []:
            return choices[0]
        else:
            pass
    
def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    f = open(filename, 'r', encoding ='latin1') 
    text = f.read()
    text = text.split('\n')
    correct_count = 0
    for q in range (0, len(text)):
        text[q] = text[q].split(' ')
        answer = most_similar_word(text[q][0], text[q][2:], semantic_descriptors, similarity_fn)
        if text[q] != ['']:
            print(answer, text[q][1])
            if answer == text[q][1]:
                correct_count += 1
    if text[q] != ['']:
        ratio = correct_count/len(text)
    else: 
        ratio = correct_count/(len(text)-1)
        
    return ratio*100

if __name__ == '__main__':
    sem_descriptors = build_semantic_descriptors_from_files(['swannsway.txt','War&Peace.txt'])
    res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")
