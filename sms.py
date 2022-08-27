import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None
from collections import Counter
import nltk
import string

#path = 'C:/Users/User/Karachi ai/Class5/Assignment/SMS_data.csv'
#data = pd.read_csv(path,encoding="ISO-8859-1")
data = pd.read_csv('SMS_data.csv',encoding="ISO-8859-1")

####*******####
data["text_lower"] = data["Message_body"].str.lower()
####*******####

#data.drop(["text_lower"], axis=1, inplace=True)

PUNCT_TO_REMOVE = string.punctuation
def remove_punctuation(text):
    """custom function to remove the punctuation"""
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))
    
data['text_wo_punct'] = data['text_lower'].apply(lambda text: remove_punctuation(text))



####*******####
nltk.download('stopwords')
from nltk.corpus import stopwords
", ".join(stopwords.words('english'))

STOPWORDS = set(stopwords.words('english'))
def remove_stopwords(text):
    """custom function to remove the stopwords"""
    return " ".join([word for word in str(text).split() if word not in STOPWORDS])

data["text_wo_stop"] = data["text_wo_punct"].apply(lambda text: remove_stopwords(text))
####*******####


##***Message Count Received**##
msg_count = data.groupby('Date_Received')['Message_body'].count().sort_values(ascending=False)    

spam_data = data[data['Label'] == 'Spam']
no_spam_data = data[data['Label'] == 'Non-Spam']

##***SPAM**##
spam_cnt = Counter()
for text in data["Message_body"].values:
    for word in text.split():
        spam_cnt[word] += 1
spam_cnt.most_common(20)

common_word_spam = pd.DataFrame(spam_cnt.most_common(25), columns=['Common Words Spam', 'count'])
spm_msg_count    = spam_data.groupby('Date_Received')['text_wo_stop'].count().sort_values(ascending=False)    

##***NON-SPAM**##
from collections import Counter
no_spam_cnt = Counter()
for text in no_spam_data["Message_body"].values:
    for word in text.split():
        no_spam_cnt[word] += 1
no_spam_cnt.most_common(25)

common_word_no_spam = pd.DataFrame(no_spam_cnt.most_common(25), columns=['Common Words Non-Spam', 'count'])

no_spam_msg_count = no_spam_data.groupby('Date_Received')['text_wo_stop'].count().sort_values(ascending=False)    

def main():
    st.title('SMS Chat Analysis')
    filterby = st.selectbox('Filter By',data.Label.unique()) 
    button  = st.button('Show Results')
    
    if button:
      

        if filterby == 'Spam':
            st.subheader("Most Common Words (SPAM) uses in SMS Data")
            #subset  =  common_word_spam['Common Words Spam'] #common_word_spam

            #Bar Chart
            st.bar_chart(common_word_spam,x="count", y="Common Words Spam")
            
            st.subheader("Number of Messages Recieved over Dates")
            st.line_chart(spm_msg_count)
      
          
        elif filterby == 'Non-Spam':
            st.subheader("Most Common Words (NON-SPAM) uses in SMS Data")
            subset  =  common_word_no_spam['Common Words Non-Spam'] #common_word_no_spam
    
            st.bar_chart(subset)    
            st.subheader("Number of Messages Recieved over Dates")
            st.line_chart(no_spam_msg_count)

    
if __name__ == '__main__':
    main()
    
