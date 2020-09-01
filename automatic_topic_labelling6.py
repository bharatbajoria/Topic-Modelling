# -*- coding: utf-8 -*-
"""Automatic Topic labelling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RCwFQydCg_jvfYppylFD5gHRzAXEjUp2
"""

def automatic_labels(idealtopics,wikipedia,RegexpTokenizer,model1,stopwords,repetitions,word_limit=25):
  tokenizer = RegexpTokenizer(r'\w+')
  en_stop = set(stopwords.words('english'))
  en_stop.add('the')#The is not in stopwords
  
  dup_model=model1
  
  topic_count=1
  for reruns in range(repetitions):
    print("Repetition:-",reruns+1)
    Automatic_labels=[]
    for x in idealtopics:

      print("Finding label for Topic:",topic_count)
      topic_count+=1
      
      contents=[]
      title_vector=[]   
      index_topic=[]
      #ndex_topic[0][1] # index_topic[i] is a list of titles obtained for word-1
      ## index_topic[i][j] is a list of words in j-th title obtained for word-1
      word_limit=min(word_limit,len(x))
      x=x[:word_limit]
      count=0
      k=0
      for j in x:
        contents=[]
        index_word=[]
        file_title=wikipedia.search(j,results=15,suggestion= True)
        
      
        
        
        for l in range(len(file_title[0])):
          continue_var=0
          try:
            y = wikipedia.search(file_title[0][l])[2]
            y = wikipedia.page(y)
        # except wikipedia.DisambiguationError as e:
          #  s = e.options[0] 
          # y = wikipedia.page(s)
          except :             
            continue_var=1            

          if (continue_var==0 or type(y)=='str'):       
            token=tokenizer.tokenize(y.content)
            token=[i for i in token if(not(str(i).isdigit() or not(str(i).isalpha())) and len(str(i)) > 2 )]
            token=[i.lower() for i in token if( i not in en_stop)]
            contents.append(token)
          count+=1

        
          
        dup_model.build_vocab(contents,update= True)#content is a 2-d list
        dup_model.train(contents, total_examples=len(contents),epochs=2)
        for i in range(len(file_title[0])):
          
          
          y= file_title[0][i].lower()
          z=y.split()
          for m in range(len(z)):
            index=[]
            p=list(z[m])
            for k in range(len(p)):
              if (p[k]=="-" or p[k]==","):
                p[k]=" "

              if not(p[k].isalpha()):
                index.append(k)
            for k in range(len(index)):
              p.pop(index[len(index)-k-1])
            
            k=''
            for w in p:
              k+=w
            z[m]=k

          z=[k for k in z if not(k in en_stop or k== j or k=="" or k==",")]
          
          index_word.append(z)
          dup_model.build_vocab(index_word,update= True)
          dup_model.train(index_word, total_examples=len(contents),epochs=2)
        
          
        index_topic.append(index_word)

      max_score=0
      max_list=[]
      for i in range(len(index_topic)):
        o=0
        for j in range(len(index_topic[i])):
          o=0
          for k in range(len(index_topic[i][j])):
            for p in range(len(x)):
              o+=dup_model.similarity(index_topic[i][j][k],x[p])
          if len(index_topic[i][j])>0:
            o= o/len(index_topic[i][j])
          if o>max_score:
            max_score=o
            max_list=[i,j]

      file_title=wikipedia.search(x[max_list[0]],results=15,suggestion= False)
      Automatic_labels.append(file_title[max_list[1]])

  return Automatic_labels

def word_removal(lda_words,lda_words_to_remove):
  for i in range(len(lda_words)):
    index=[]
    if len(lda_words_to_remove[i])!=0:
      for j in range(len(lda_words[i])):
        if lda_words[i][j] in lda_words_to_remove[i]:
          index.append(j)
      index.reverse()

      for k in index:
        lda_words[i].pop(k)
  return lda_words