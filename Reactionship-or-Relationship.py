#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import json
import nltk
import re

##### PLS ENTER YOU INSTA NAME, IF YOU ARE NOT SURE, REFER TO CELL 4 FOR INSTRUCTIONS, 

sender_name = 'washeem'

# In[2]:


## THIS FUNCTION TAKES IN THE FOLDER NAME OF INTEREST YOU HAVE CHOSEN AND THE CORRESPONG JSON FILE YOU WANNA ACCESS
## AND ASSIGNS THE VALUES TO THE data variable

def read_my_data(folder_name_of_interest,folder_name_of_interest_contents):
    with open(folder_name_of_interest + '/'+ folder_name_of_interest_contents) as json_file:
        data = json.load(json_file)
    return(data)

def dm_stats_generator(list_of_msgs):
    sent_content = 0;
    recieved_content = 0;
    sent_not_a_text_msg = 0;
    recieved_not_a_text_msg = 0;

    for idx in range (0, len(list_of_msgs)):
        msg_pkt = list_of_msgs[idx]
        if len(msg_pkt)==5:
            try:
                if msg_pkt['sender_name']==sender_name:
                    if msg_pkt['content'] == 'Liked a message':
                        sent_not_a_text_msg = sent_not_a_text_msg + 1
                    else:
                        sent_content = sent_content + 1
                elif msg_pkt['sender_name']!=sender_name:
                    if msg_pkt['content'] == 'Liked a message':
                        recieved_not_a_text_msg = recieved_not_a_text_msg + 1
                    else:
                        recieved_content = recieved_content + 1 
            except:
                if msg_pkt['sender_name']==sender_name:
                    sent_not_a_text_msg = sent_not_a_text_msg + 1
                else:
                    recieved_not_a_text_msg = recieved_not_a_text_msg + 1
        else:
            if msg_pkt['sender_name']==sender_name:
                sent_not_a_text_msg = sent_not_a_text_msg + 1
            else:
                recieved_not_a_text_msg = recieved_not_a_text_msg + 1
    return sent_not_a_text_msg,recieved_not_a_text_msg,recieved_content,sent_content

# In[4]:

folder_name_of_interest = 'messages'
folder_name_of_interest_contents = os.listdir(folder_name_of_interest)
# display(folder_name_of_interest_contents)

contacts_msged = os.listdir(folder_name_of_interest+'/'+folder_name_of_interest_contents[0])
# display(contacts_msged)

contact_list = []
sent_rxn_list = []
rec_rxn_list = []
rec_msg_list = []
sent_msg_list = []

for contacts in contacts_msged:
    
    contents_in_contact =  os.listdir(folder_name_of_interest+'/'+folder_name_of_interest_contents[0] +'/'+contacts)
    first = folder_name_of_interest+'/'+folder_name_of_interest_contents[0] +'/'+contacts ;
    second = 'message_1.json'
    data = read_my_data(first,second)
    list_of_msgs = data['messages']
    
    # display(list_of_msgs)

    ## IF YOU DONT KNOW YOUR INSTA NAME, 
    ## UNCOMMENT THE DISPLAY LINE ABOVE
    ## COMMENT EVERYTHIN BELOW THIS LINE TILL THE NEXT LINE BREAK AND RUN ENTIRE NOTEBOOK
    
    sent_rxn,rec_rxn,rec_msg,sent_msg = dm_stats_generator(list_of_msgs)
    
    contact_list.append(contacts)
    sent_rxn_list.append(sent_rxn)
    rec_rxn_list.append(rec_rxn)
    rec_msg_list.append(rec_msg)
    sent_msg_list.append(sent_msg)
#################################################################### END OF COMMENT SECTION FOR NAME FINDING ########


# In[5]:


contact_srs = pd.Series(contact_list)
sent_rxn_srs = pd.Series(sent_rxn_list)
rec_rxn_srs = pd.Series(rec_rxn_list)
rec_msg_srs = pd.Series(rec_msg_list)
sent_msg_srs = pd.Series(sent_msg_list)

insta_df = pd.concat([contact_srs,sent_rxn_srs,rec_rxn_srs,rec_msg_srs,sent_msg_srs],
                            axis=1,
                            keys=["Name", "Sent_rxns", "Rec_rxns","Rec_msgs","Sent_msgs"])


# insta_df.head()
insta_df


# In[6]:


## lETS DO SOME FILTERING
insta_df = insta_df[insta_df["Name"]!='goodthingsmustshare_tr5lvervha']

cond1 = insta_df['Sent_rxns']!=0
cond2 = insta_df['Rec_rxns']!=0
cond3 = insta_df['Rec_msgs']!=0
cond4 = insta_df['Sent_msgs']!=0

insta_df = insta_df[cond1 & cond2 & cond3 & cond4]
insta_df


# In[7]:


insta_df['Sent_msgs_per_sent_rxn'] = insta_df['Sent_msgs']/insta_df['Sent_rxns']
insta_df['Recv_msgs_per_Rec_rxn'] = insta_df['Rec_msgs']/insta_df['Rec_rxns']
insta_df['Sent_msgs_per_Rec_rxn'] = insta_df['Sent_msgs']/insta_df['Rec_rxns']
insta_df['Recv_msgs_per_sent_rxn'] = insta_df['Rec_msgs']/insta_df['Sent_rxns']
# insta_df = insta_df.dropna(axis=0)
insta_df.to_csv('insta_stats.csv',index=False)


# In[8]:


analysis_tbl = insta_df.describe()
display(analysis_tbl)

a = insta_df[insta_df.Sent_rxns == analysis_tbl.Sent_rxns.loc['max']].Name
b = insta_df[insta_df.Rec_rxns == analysis_tbl.Rec_rxns.loc['max']].Name
c = insta_df[insta_df.Sent_msgs == analysis_tbl.Sent_msgs.loc['max']].Name
d = insta_df[insta_df.Rec_msgs == analysis_tbl.Rec_msgs.loc['max']].Name

print('Sent Most Rxns ' + str(int(analysis_tbl.Sent_rxns.loc['max'])) + ' to: ' + a)
print('--------')
print('Recieved Most Rxns '+ str(int(analysis_tbl.Rec_rxns.loc['max'])) +  ' from:',b)
print('--------')
print('Sent Most Msgs ' + str(int(analysis_tbl.Sent_msgs.loc['max'])) + ' to: ' + c)
print('--------')
print('Recieved Most Msgs ' + str(int(analysis_tbl.Rec_msgs.loc['max'])) + ' from: ' + d)
print('--------')


# In[9]:


# insta_df_rxnship = insta_df[insta_df['Sent_msgs_per_Rec_rxn'] > insta_df['Recv_msgs_per_sent_rxn']]
# insta_df_rxnship

cond1 = insta_df['Sent_msgs_per_sent_rxn'] < 1
cond2  = insta_df['Recv_msgs_per_Rec_rxn'] < 1
cond3 = insta_df['Sent_msgs_per_sent_rxn'] > 1
cond4 = insta_df['Recv_msgs_per_Rec_rxn'] > 1

cond5 = insta_df['Recv_msgs_per_sent_rxn'] > insta_df['Sent_msgs_per_Rec_rxn']

cond6 = insta_df['Recv_msgs_per_sent_rxn'] < 1

cond7 = insta_df['Sent_msgs_per_Rec_rxn'] > 1

cond7b = insta_df['Sent_msgs_per_Rec_rxn'] < 1

insta_df_rxnship_mutual = insta_df[cond1 & cond2]
# display(insta_df_rxnship_mutual)

insta_df_i_rsh_they_rxn = insta_df[cond3 & cond2]
# # display(insta_df_i_rsh_they_rxn)

insta_df_they_more_excited = insta_df[cond5]
# display(insta_df_they_more_exctied)

insta_df_trbl_them_responding = insta_df[cond6]
# display(insta_df_they_more_exctied)

insta_df_they_excite_u = insta_df[cond7]
# display(insta_df_they_excite_u)

insta_df_they_bore_u = insta_df[cond7b & cond6]
# display(insta_df_they_bore_u)

print('You have a mutual RXNship with ' + str(len(insta_df_rxnship_mutual)) + '/' + str(len(insta_df)) + ' ppl u dm' )
print('You want a Rship with ' + str(len(insta_df_i_rsh_they_rxn)) + '/' + str(len(insta_df)) + ' of em BUT THEY ONLY WANT A RXNSHIP' )
print( str(len(insta_df_they_more_excited)) + '/' + str(len(insta_df)) + ' Are more excited to talk to you than you are to them' )
print('You may have trouble sparking a convo with ' + str(len(insta_df_trbl_them_responding)) + '/' + str(len(insta_df)) + ' of ppl ' )
print(str(len(insta_df_they_excite_u)) + '/' + str(len(insta_df)) + ' Excite You!' )
print(str(len(insta_df_they_bore_u)) + '/' + str(len(insta_df)) + ' Bore each other' )

# In[ ]:





# In[ ]:




