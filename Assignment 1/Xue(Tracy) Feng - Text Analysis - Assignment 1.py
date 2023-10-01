#!/usr/bin/env python
# coding: utf-8

# ### Text Analysis - Assignment 1
# ### Xue (Tracy) Feng
# ### Sep 5, 2022
# 
# Web scraping is powerful and useful technique for collecting public data from the internet. For this assignment, you will scrape the the Wikipedia page of the list of largest banks in the world, by total assets:  https://en.wikipedia.org/wiki/List_of_largest_banks (Links to an external site.) 
# 
# You must prepare a Jupyter notebook that contains all necessary code as well as Markdown text to explain each question and step of the process below, how it works, and what is happening. You will save the notebook as an HTML report and submit it to Canvas. The script should run without errors. You should use tables and/or visualizations to show your results when appropriate. 

# ### Question 1
# 
# ##### Review the source code of the webpage using the inspector tool of your browser. List three types of HTML tags you found on the page and explain what elements of the page are created with those tags.
# 
# The first tag I saw in the source code is `<head>` tage. `<head>` creats the document metadata elements which are machine-readable info about the document. For example, from the source code I saw the metadata contains title which is the title of the whole document, scripts, and style sheets which defines text font, size, color, and etc.
#     
# The second tag I noticed is `<h1>`. This tag is used for a level 1 heading and it's the most important heading on the page. Inside the `<h1>` tag, it has the element of `<span>` which is a generic inline container for phrasing content that does not ingerently represent anything. Together with `<h1>`, it allows wikipedia to show its heading 'List of largest banks' on its page.
# 
# The third tag I want to mention is `<p>`. `<p>` is a paragraph with imprtant body text in it. The `<p>` tag I saw includes a paragraph under subtitle 'By total assets'. Inside the `<p>` tag, there are several elements such as link elements, reference cite special character elements, and etc. 

# ### Question 2
# ##### Issue a request for the webpage using the requests library and display the HTTP response code for the request. What does the response code indicate?

# In[2]:


import requests
from bs4 import BeautifulSoup


# In[3]:


# URL
link = requests.get("https://en.wikipedia.org/wiki/List_of_largest_banks")


# In[4]:


# get response code
link


# Response code 200 indicates OK, which means that the request has succeeded

# ### Question 3
# ##### Scrape the content from the table that has three columns (Rank, Bank Name, and Total Assets). Clean and process it so that the data is in a clean pandas dataframe with three columns that contain the rank, the text of the bank name, and the banks total assets (in US billions) and that there is one and only one value per cell. Each column must be the appropriate data type.

# In[5]:


import pandas as pd


# create a soup object

# In[23]:


soup = BeautifulSoup(link.text, 'lxml')


# print out each class

# In[7]:


print('Classes of each table:')
for table in soup.find_all('table'):
    print(table.get('class'))


# get the first table by specifying the class names

# In[8]:


table = soup.find('table', {"class":"wikitable sortable mw-collapsible"})


# initialize a new dataframe to save the result

# In[9]:


df_q3 = pd.DataFrame(columns=['Rank' , 'Bank Name', 'Total Assets(in US billions)'])


# save all the `<tr>` tags with its content into a list 

# In[10]:


list_tr = table.tbody.find_all('tr')


# a for loop to store the three elements we need from the tr list to our dataframe and at the same time use regex to clean the annotation. The last line removes all the commas from total asset strng values for the later data type transfer.

# In[11]:


for row in list_tr:
    columns = row.find_all('td')
    if (columns != []):
        rank = columns[0].text.strip()
        bank_name = columns[1].text.strip()
        total_assets = columns[2].text.strip()
        if (total_assets.find('[')): 
            total_assets = total_assets.split('[')[0] 
        
        df_q3 = df_q3.append({'Rank': rank, 'Bank Name': bank_name, "Total Assets(in US billions)": total_assets}, ignore_index = True)

df_q3 = df_q3.replace(',','', regex=True)


# change columns into proper data types

# In[12]:


df_q3['Rank'] = df_q3['Rank'].astype(int)
df_q3['Total Assets(in US billions)'] = df_q3['Total Assets(in US billions)'].astype(float)
df_q3['Bank Name'] = df_q3['Bank Name'].astype(str)


# In[13]:


df_q3.head(10)


# In[14]:


df_q3.info()


# ### Question 4
# ##### Plot the total assets and the banks from left to right in ascending order of total asset using altair, seaborn, matplotlib, or plotnine.

# In[15]:


from matplotlib import pyplot as plt


# sort total assets in ascending order and then use the matplot package to draw the bar chart. 

# In[21]:


df_q4 = df_q3.sort_values('Total Assets(in US billions)')
plt.bar('Bank Name', 'Total Assets(in US billions)', data=df_q4, color='orange')
plt.gcf().set_size_inches(20, 15)
plt.xticks(rotation=90)
plt.suptitle('Largest Banks by Total Assets', fontsize=30)
plt.xlabel('Bank', size=20)
plt.ylabel('Total Assets (in billion $)', size=20)
plt.dpi = 2000
plt.show()


# ### Question 5
# ##### Create a wordcloud that shows the bank names sized according to their total assets using [WordCloud](https://amueller.github.io/word_cloud/index.html)

# In[17]:


from wordcloud import WordCloud


# create a dictionary where key = bank name, value = total assets for the wordcloud method

# In[18]:


d = dict(zip(df_q3['Bank Name'], df_q3['Total Assets(in US billions)']))


# create a word cloud object and plot the word cloud

# In[22]:


wc = WordCloud(background_color="white",width=1000,height=1000, max_words=100,relative_scaling=0.5,normalize_plurals=False).generate_from_frequencies(d)
plt.gcf().set_size_inches(96, 64)
plt.axis("off")
plt.imshow(wc)


# In[ ]:




