import streamlit as st
import pandas as pd
pd.options.mode.chained_assignment = None
from collections import Counter
import nltk
import string
import plotly.express as px

#path = 'C:/Users/User/Karachi ai/Class5/Assignment/SMS_data.csv'
#data = pd.read_csv(path,encoding="ISO-8859-1")
data = pd.read_csv('SMS_data.csv',encoding="ISO-8859-1")

data['Month'] = pd.to_datetime(data['Date_Received']).apply(lambda x: x.month_name())

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
for text in data["text_wo_stop"].values:
    for word in text.split():
        spam_cnt[word] += 1
spam_cnt.most_common(15)

common_word_spam = pd.DataFrame(spam_cnt.most_common(15), columns=['Common Words Spam', 'count'])

spm_msg_count    = spam_data.groupby('Month')['Message_body'].count().sort_values(ascending=False)    
msg_count    = data.groupby('Month')['Message_body'].count().sort_values(ascending=False)    
##***NON-SPAM**##
from collections import Counter
no_spam_cnt = Counter()
for text in no_spam_data["text_wo_stop"].values:
    for word in text.split():
        no_spam_cnt[word] += 1
no_spam_cnt.most_common(15)

common_word_no_spam = pd.DataFrame(no_spam_cnt.most_common(15), columns=['Common Words Non-Spam', 'count'])

no_spam_msg_count = no_spam_data.groupby('Month')['text_wo_stop'].count().sort_values(ascending=False)    

def main():
    st.title('SMS Chat Analysis')
    st.caption("Created By: Muhamamd Shahzad")
    filterby = st.selectbox('Filter By',data.Label.unique()) 
    button  = st.button('Show Results')
    
    if button:
      

        if filterby == 'Spam':
            st.subheader("Most 15 Common Words (SPAM) uses in SMS Data new")

            fig = px.bar(common_word_spam, x='Common Words Spam', y='count')
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Number of Messages Recieved Over Months Spam")
            #st.line_chart(spm_msg_count)
            #st.line_chart(msg_count)
            fig = px.line(msg_count)
            st.plotly_chart(fig)
          
        elif filterby == 'Non-Spam':
            st.subheader("Most 15 Common Words (NON-SPAM) uses in SMS Data")

            fig = px.bar(common_word_no_spam, x='Common Words Non-Spam', y='count')
            st.plotly_chart(fig, use_container_width=True)
        
            
            st.subheader("Number of Messages Recieved Over Months Non-Spam")
            #st.line_chart(no_spam_msg_count)
            fig = px.line(no_spam_msg_count)
            st.plotly_chart(fig)
            
            #st.caption("Created By: Muhamamd Shahzad")

    
if __name__ == '__main__':
    main()
    
