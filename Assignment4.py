
# coding: utf-8

# # Assignment 4
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# This assignment requires that you to find **at least** two datasets on the web which are related, and that you visualize these datasets to answer a question with the broad topic of **economic activity or measures** (see below) for the region of **Ann Arbor, Michigan, United States**, or **United States** more broadly.
# 
# You can merge these datasets with data from different regions if you like! For instance, you might want to compare **Ann Arbor, Michigan, United States** to Ann Arbor, USA. In that case at least one source file must be about **Ann Arbor, Michigan, United States**.
# 
# You are welcome to choose datasets at your discretion, but keep in mind **they will be shared with your peers**, so choose appropriate datasets. Sensitive, confidential, illicit, and proprietary materials are not good choices for datasets for this assignment. You are welcome to upload datasets of your own as well, and link to them using a third party repository such as github, bitbucket, pastebin, etc. Please be aware of the Coursera terms of service with respect to intellectual property.
# 
# Also, you are welcome to preserve data in its original language, but for the purposes of grading you should provide english translations. You are welcome to provide multiple visuals in different languages if you would like!
# 
# As this assignment is for the whole course, you must incorporate principles discussed in the first week, such as having as high data-ink ratio (Tufte) and aligning with Cairo’s principles of truth, beauty, function, and insight.
# 
# Here are the assignment instructions:
# 
#  * State the region and the domain category that your data sets are about (e.g., **Ann Arbor, Michigan, United States** and **economic activity or measures**).
#  * You must state a question about the domain category and region that you identified as being interesting.
#  * You must provide at least two links to available datasets. These could be links to files such as CSV or Excel files, or links to websites which might have data in tabular form, such as Wikipedia pages.
#  * You must upload an image which addresses the research question you stated. In addition to addressing the question, this visual should follow Cairo's principles of truthfulness, functionality, beauty, and insightfulness.
#  * You must contribute a short (1-2 paragraph) written justification of how your visualization addresses your stated research question.
# 
# What do we mean by **economic activity or measures**?  For this category you might look at the inputs or outputs to the given economy, or major changes in the economy compared to other regions.
# 
# ## Tips
# * Wikipedia is an excellent source of data, and I strongly encourage you to explore it for new data sources.
# * Many governments run open data initiatives at the city, region, and country levels, and these are wonderful resources for localized data sources.
# * Several international agencies, such as the [United Nations](http://data.un.org/), the [World Bank](http://data.worldbank.org/), the [Global Open Data Index](http://index.okfn.org/place/) are other great places to look for data.
# * This assignment requires you to convert and clean datafiles. Check out the discussion forums for tips on how to do this from various sources, and share your successes with your fellow students!
# 
# ## Example
# Looking for an example? Here's what our course assistant put together for the **Ann Arbor, MI, USA** area using **sports and athletics** as the topic. [Example Solution File](./readonly/Assignment4_example.pdf)

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

get_ipython().magic('matplotlib notebook')

plt.style.use('seaborn-notebook')

df = pd.read_csv('GDP_Growth_World.csv', skiprows = 4);

#clean data
years = np.arange(1960,1996,1);
dropcols = np.array([str(x) for x in years]);
dropcols = np.concatenate((dropcols , ['2017']))

df.drop(['Indicator Name', 'Indicator Code', 'Country Code', 'Unnamed: 62'], axis=1, inplace = True)
df.drop(dropcols, axis =1, inplace = True)

df.set_index('Country Name', inplace = True);

# get data for the countries that we're interested in
data = df.loc[['Canada', 'China', 'India', 'United States']].T

data = data.set_index(np.arange(1996,2017,1))

# plot data
ax = data.plot(figsize=(10,6), style=['-', '-', '-','-.']);
ax.set_title('Comparison of GDP Growth of the USA with Canada, China, and India over last 20 years (1996-2016)');
plt.yticks(np.arange(-4, 17, 4))
plt.xticks(np.arange(1996,2017,2))

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
ax.set_xticks(np.arange(1997,2017,2), minor=True)

# add a label to the x axis
plt.xlabel('Year')
# add a label to the y axis
plt.ylabel('Percentage %')

plt.axhline(y=0, color='#DCDCDC', linestyle=':')


#update USA's line width
lines = ax.get_lines()
for l in lines:
    if l.get_label() == 'United States':
        l.set_linewidth(3)
    else :
        l.set_linewidth(1)
        
    


# In[ ]:




# In[ ]:



