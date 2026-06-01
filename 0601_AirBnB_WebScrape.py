# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] id="8-RdQuRek3tU"
# # Web parsing the Air BnB Rome Page

# %% [markdown] id="_y4R6ai1k_RU"
# ### 1. Scrape Airbnb page

# %% [markdown] id="x0E8PDiRVvdE"
# Let's get to the website and look for some apartments (modeling starts on line 70!)

# %% [markdown]
# ## ------------ROME-------------

# %% id="jQaQOXZQnm7j"
from bs4 import BeautifulSoup
import requests

airbnb_url = 'https://www.airbnb.com/s/Rome--Italy/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type=flexible_dates&flexible_trip_lengths%5B%5D=one_month&flexible_trip_dates%5B%5D=june&source=structured_search_input_header&search_type=autocomplete_click&query=Rome%2C%20Italy&place_id=ChIJu46S-ZZhLxMROG5lkwZ3D7k'

# %% id="mN68-cGPuIWn"
soup = BeautifulSoup(requests.get(airbnb_url).content, 'html.parser')

# %% id="IG7YjnIDuIZf"
print(soup.prettify())

# %% [markdown] id="o87Q3B2Ik_iU"
# ### 2. Scrape tag

# %% id="8giGyc5LntCe"
soup.find_all('div', '_1ify1icq')

# %% id="vGN6ju9mxfeT"
# we can also extract its child tag
soup.find_all('div', 'c4mnd7m dir dir-ltr')

# %% id="5WLbqzHsxfjF"
listings = soup.find_all('div', 'c4mnd7m dir dir-ltr')

# %% id="u4eSngGcxfox"
listings[0]

# %% id="dwLVy8DD0IHO"
listings[0].get_text()

# %% [markdown] id="2RQ2DGq-0cua"
# ### 3. Inspect the iD for each listing

# %% id="n8jQrsh8_-Lv"

for tag in soup.find_all(class_= 'ts5gl90 tl3qa0j t1nzedvd dir dir-ltr') :
    print(tag.get('id'))

# %% [markdown] id="ATnJssp40e6C"
# ### 4. Scraping function

# %% id="13W65EWn0gMD"


def extract_basic_features(listing_html):
    features_dict = {} 
    

    try:
        id_ = listing_html.find("div", {"class": "t1jojoys dir dir-ltr"}).get('id')
    except:
        id_ = 'empty'
    try:
        name = listing_html.find("div", {"class": "t1jojoys dir dir-ltr"}).text
    except:
        name = 'empty'
    try:
        find_superhost = listing_html.find("div", {"class": 't1mwk1n0 dir dir-ltr'}).text
    except:
        find_superhost = 'empty'
    try:
        rating = listing_html.find("span", {"class": 'ru0q88m dir dir-ltr'}).text #.get_text()
    except:
        rating= 'empty'

        
    features_dict['id'] = id_
    features_dict['name'] = name
    features_dict['find_superhost'] = find_superhost
    features_dict['rating'] = rating

    
    return features_dict

# %% id="5Hzy5KCoBWq8"
for i in list(range(40,60)):
    a = extract_basic_features(listings[i]) #need more
    print(a)

# %%
#print sample output
import pandas as pd
output1 = pd.DataFrame()
for i in list(range(40,60)):
    output1 = output1.append(extract_basic_features(listings[i]), ignore_index=True)

# %%
output1[['id', 'name', 'rating', 'find_superhost']]


# %% [markdown] id="9T1QCX-U0ggn"
# ### 5. Explore scraping by page

# %% id="Yo6OYalILIn8"
# Reference: https://smithio.medium.com/scraping-airbnb-website-with-python-beautiful-soup-and-selenium-8ec86e327b6c
def get_listings(search_page):
    soup = BeautifulSoup(requests.get(search_page).content, 'html.parser')
    listings = soup.find_all('div', 'c4mnd7m dir dir-ltr')

    return listings


# %% id="9TqYmtCtLIrg"

len(get_listings(airbnb_url))

# %% id="aLMKciXALcm1"
# next page
new_url = airbnb_url + '&items_offset=20'
len(get_listings(new_url))

# %% id="816wu53DLqm8"
print(extract_basic_features(get_listings(airbnb_url)[1]))
print(extract_basic_features(get_listings(new_url)[1]))

# %% [markdown] id="uLeff4kG0iNA"
# ### 6. Collect all urls

# %% id="3ynwY0LC0jTt"
# iterate through pages
# Reference: https://smithio.medium.com/scraping-airbnb-website-with-python-beautiful-soup-and-selenium-8ec86e327b6c
all_listings = []
for i in range(15):
    offset = 20 * i
    new_url = airbnb_url + f'&items_offset={offset}'
    new_listings = get_listings(new_url)
    all_listings.extend(new_listings)
    
    # check
    print(len(all_listings))

# %% id="TnlQHnzVMQ71"
# wait time
# Reference: https://smithio.medium.com/scraping-airbnb-website-with-python-beautiful-soup-and-selenium-8ec86e327b6c
import time

all_listings = []
for i in range(15):
    offset = 20 * i
    new_url = airbnb_url + f'&items_offset={offset}&section_offset=3'
    new_listings = get_listings(new_url)
    all_listings.extend(new_listings)
    
    #check
    print(len(all_listings))

    time.sleep(5)

# %% [markdown] id="NJ8YcdpCN11l"
# Not perfect but some improvement

# %% id="pt7Rri6YMU0U"
# check
print(extract_basic_features(all_listings[100]))

# %%
import pandas as pd
output = pd.DataFrame()
for i in list(range(1,974)):
    output = output.append(extract_basic_features(all_listings[i]), ignore_index=True)
    print(output)

# %%
len(output)

# %%
output.head()

# %%
b = output[output['id'] != 'empty']
data1 =b.copy()
data1['place'] = 'Rome'
data1.head()

# %%
#save rome as CSV just in case
from pathlib import Path  
filepath = Path('Documents/rome1.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
data1.to_csv(filepath) 

# %%
len(data1)

# %% [markdown]
# ## ------------VENICE-------------

# %%
from bs4 import BeautifulSoup
import requests


airbnb_url2 = 'https://www.airbnb.com/s/Venice--Italy/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type=flexible_dates&flexible_trip_lengths%5B%5D=one_month&flexible_trip_dates%5B%5D=june&source=structured_search_input_header&search_type=autocomplete_click&query=Venice%2C%20Italy&place_id=ChIJiT3W8dqxfkcRLxCSvfDGo3s'

# %%
soup = BeautifulSoup(requests.get(airbnb_url2).content, 'html.parser')
listings = soup.find_all('div', 'c4mnd7m dir dir-ltr')

# %%
listings = soup.find_all('div', 'c4mnd7m dir dir-ltr')

# %%


def extract_basic_features(listing_html):
    features_dict = {}  

    try:
        id_ = listing_html.find("div", {"class": "t1jojoys dir dir-ltr"}).get('id')
    except:
        id_ = 'empty'
    try:
        name = listing_html.find("div", {"class": "t1jojoys dir dir-ltr"}).text
    except:
        name = 'empty'
    try:
        find_superhost = listing_html.find("div", {"class": 't1mwk1n0 dir dir-ltr'}).text
    except:
        find_superhost = 'empty'
    try:
        rating = listing_html.find("span", {"class": 'ru0q88m dir dir-ltr'}).text #.get_text()
    except:
        rating= 'empty'

        
    features_dict['id'] = id_
    features_dict['name'] = name
    features_dict['find_superhost'] = find_superhost
    features_dict['rating'] = rating

    
    return features_dict

# %%

new_url2 = airbnb_url2 + '&items_offset=20'
len(get_listings(new_url2))

# %%

import time

all_listings = []
for i in range(15):
    offset = 20 * i
    new_url2 = airbnb_url2 + f'&items_offset={offset}&section_offset=3'
    new_listings = get_listings(new_url2)
    all_listings.extend(new_listings)
    
    #check 
    print(len(all_listings))

    time.sleep(2)

# %%
import pandas as pd
output = pd.DataFrame()
for i in list(range(1,910)):
    output = output.append(extract_basic_features(all_listings[i]), ignore_index=True)
    print(output)

# %%
b = output[output['id'] != 'empty']
data2 =b.copy()
data2['place'] = 'Venice'
data2.head()

# %%
#save  CSV just in case
from pathlib import Path  
filepath = Path('Documents/venice1.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
data2.to_csv(filepath) 

# %%
len(data2)

# %% [markdown]
# ## ------------MILAN-------------

# %%
from bs4 import BeautifulSoup
import requests

airbnb_url3 = 'https://www.airbnb.com/s/Milan--Italy/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type=flexible_dates&flexible_trip_lengths%5B%5D=one_month&flexible_trip_dates%5B%5D=june&source=structured_search_input_header&search_type=autocomplete_click&query=Milan%2C%20Italy&place_id=ChIJ53USP0nBhkcRjQ50xhPN_zw'

# %%
soup = BeautifulSoup(requests.get(airbnb_url3).content, 'html.parser')
listings = soup.find_all('div', 'c4mnd7m dir dir-ltr')

# %%


def extract_basic_features(listing_html):
    features_dict = {} 
    

    try:
        id_ = listing_html.find("div", {"class": "t1jojoys dir dir-ltr"}).get('id')
    except:
        id_ = 'empty'
    try:
        name = listing_html.find("div", {"class": "t1jojoys dir dir-ltr"}).text
    except:
        name = 'empty'
    try:
        find_superhost = listing_html.find("div", {"class": 't1mwk1n0 dir dir-ltr'}).text
    except:
        find_superhost = 'empty'
    try:
        rating = listing_html.find("span", {"class": 'ru0q88m dir dir-ltr'}).text #.get_text()
    except:
        rating= 'empty'

        
    features_dict['id'] = id_
    features_dict['name'] = name
    features_dict['find_superhost'] = find_superhost
    features_dict['rating'] = rating

    
    return features_dict

# %%
# next page
new_url3 = airbnb_url3 + '&items_offset=20'
len(get_listings(new_url3))

# %%

import time

all_listings = []
for i in range(15):
    offset = 20 * i
    new_url3 = airbnb_url3 + f'&items_offset={offset}&section_offset=3'
    new_listings = get_listings(new_url3)
    all_listings.extend(new_listings)
    
    #check
    print(len(all_listings))

    time.sleep(2)

# %%
import pandas as pd
output = pd.DataFrame()
for i in list(range(1,910)):
    output = output.append(extract_basic_features(all_listings[i]), ignore_index=True)
    print(output)

# %%
b = output[output['id'] != 'empty']
data3 =b.copy()
data3['place'] = 'Milan'
data3.head()

# %% [markdown]
# ## ------------FLORENCE-------------

# %%
from bs4 import BeautifulSoup
import requests

airbnb_url4 = 'https://www.airbnb.com/s/Florence--Tuscany--Italy/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type=flexible_dates&flexible_trip_lengths%5B%5D=one_month&flexible_trip_dates%5B%5D=june&source=structured_search_input_header&search_type=autocomplete_click&query=Florence%2C%20Tuscany%2C%20Italy&place_id=ChIJ30yk06BWKhMR2ZdgiWilRbo'

# %%
soup = BeautifulSoup(requests.get(airbnb_url4).content, 'html.parser')
listings = soup.find_all('div', 'c4mnd7m dir dir-ltr')

# %%

new_url4 = airbnb_url4 + '&items_offset=20'
len(get_listings(new_url4))

# %%
import time

all_listings = []
for i in range(15):
    offset = 20 * i
    new_url4 = airbnb_url4 + f'&items_offset={offset}&section_offset=3'
    new_listings = get_listings(new_url4)
    all_listings.extend(new_listings)
    
    #check 
    print(len(all_listings))

    time.sleep(2)

# %%
import pandas as pd
output = pd.DataFrame()
for i in list(range(1,839)):
    output = output.append(extract_basic_features(all_listings[i]), ignore_index=True)
    print(output)

# %%
b = output[output['id'] != 'empty']
data4 =b.copy()
data4['place'] = 'Florence'
data4.head()

# %% [markdown]
# ## ------------TURIN-------------

# %%
from bs4 import BeautifulSoup
import requests

airbnb_url5 = 'https://www.airbnb.com/s/Turin--Piedmont--Italy/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type=flexible_dates&flexible_trip_lengths%5B%5D=one_month&flexible_trip_dates%5B%5D=june&source=structured_search_input_header&search_type=autocomplete_click&query=Turin%2C%20Piedmont%2C%20Italy&place_id=ChIJJb4YZBJtiEcRv3ec1gP4A4k'

# %%
soup = BeautifulSoup(requests.get(airbnb_url5).content, 'html.parser')
listings = soup.find_all('div', 'c4mnd7m dir dir-ltr')

# %%
# next page
new_url5 = airbnb_url5 + '&items_offset=20'
len(get_listings(new_url5))

# %%
import time

all_listings = []
for i in range(15):
    offset = 20 * i
    new_url5 = airbnb_url5 + f'&items_offset={offset}&section_offset=3'
    new_listings = get_listings(new_url5)
    all_listings.extend(new_listings)
    
    #check
    print(len(all_listings))

    time.sleep(2)

# %%
import pandas as pd
output = pd.DataFrame()
for i in list(range(1,750)):
    output = output.append(extract_basic_features(all_listings[i]), ignore_index=True)
    print(output)

# %%
b = output[output['id'] != 'empty']
data5 =b.copy()
data5['place'] = 'Turin'
data5.head()

# %%
print(' The length of our first dataset is: ' + str(len(data1)) + '.\n'
     + ' The length of our second dataset is: ' + str(len(data2)) + '.\n'
     + ' The length of our third dataset is: ' + str(len(data3)) + '.\n'
     + ' The length of our fourth dataset is: ' + str(len(data4)) + '.\n'
     + ' The length of our fifth dataset is: ' + str(len(data5)) + '.\n\n'
     + ' This adds to a total of 1,493 records, but we must remove new listings (with no rating) this amunts to 1,148 records.')

# %%
data5.head()

# %%
test = pd.concat([data1, data2, data3, data4, data5])

# %%
test.head(3)

# %%
test['rare_or_superhost'] = test['find_superhost'].apply(lambda x: 1 if  str(x) != 'empty' else 0)
test['condo'] = test['name'].str.contains('Condo').astype(int)
test['private'] = test['name'].str.contains('Private').astype(int)
test['shared'] = test['name'].str.contains('Shared').astype(int)
test['vacation'] = test['name'].str.contains('Vacation').astype(int)
test['home'] = test['name'].str.contains('Home').astype(int)
test['apartment'] = test['name'].str.contains('Apartment').astype(int)

master = test[test['rating'] != 'New']
master.head()

# %%
master = master.astype({'rating':'float'})

# %%
master.info()

# %%
len(master)

# %%
# same master
filepath = Path('airbnb_master1.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
master.to_csv(filepath) 

# %%
import pandas as pd

master = pd.read_csv('airbnb_master1.csv')
master.head(5)

# %%
master['Rome'] = master['place'].str.contains('Rome').astype(int)
master['Venice'] = master['place'].str.contains('Venice').astype(int)
master['Milan'] = master['place'].str.contains('Milan').astype(int)
master['Turin'] = master['place'].str.contains('Turin').astype(int)
master['Florence'] = master['place'].str.contains('Florence').astype(int)
master['hotel'] = master['name'].str.contains('Hotel').astype(int)
master['villa'] = master['name'].str.contains('Villa').astype(int)
master['loft'] = master['name'].str.contains('Loft').astype(int) 
master['guest'] = master['name'].str.contains('Guest suite').astype(int)

# %%
master.head()

# %% [markdown]
# # -------- Modeling starts here --------

# %% [markdown]
# ## ----------------------------------------------

# %%
X = master[['rare_or_superhost', 'condo', 'private', 'shared', 'vacation', 'home', 'apartment', 'Rome', 'Venice', 'Milan', 'Turin', 'Florence', 'hotel', 'villa', 'loft', 'guest']]
y = master['rating']

# %%
import pandas
from sklearn import linear_model

regr = linear_model.LinearRegression()
regr.fit(X, y)

# %%
import numpy as np
import statsmodels.api as sm
model = sm.OLS(y,X)


# Here the Cities are causing noise in our data. we can drop them.
results = model.fit()

results.pvalues

# %%
results.params

# %%
results.rsquared_adj

# %%
results.rsquared

# %%
X = master[['rare_or_superhost', 'condo', 'private', 'shared', 'vacation', 'home', 'apartment', 'hotel', 'villa', 'loft', 'guest']]
y = master['rating']

# %%
import pandas
from sklearn import linear_model


# train test split here -- 


regr = linear_model.LinearRegression()
regr.fit(X, y)

# %%
#need to train test split this model

import numpy as np
import statsmodels.api as sm
model = sm.OLS(y,X)

from statsmodels import api as sm

model = sm.OLS(y,X)
result = model.fit()

#dropped cities
results = model.fit()
results.pvalues

# %%
results.rsquared # much better R^2

# %%
results.pvalues

# %%
results.params

# %%
results.summary()

# %%
#our best indicators are -> shared, vacation, home, hotel, villa, loft, rare and superhost, and guest
master.head()

# %% [markdown]
# ## Baseline Trained Model

# %%
from __future__ import division, print_function 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Lasso, Ridge, ElasticNet, LinearRegression

from sklearn.model_selection import (cross_val_score, train_test_split, 
                                     KFold, GridSearchCV)

# %matplotlib inline

# %%
X_train, X_holdout, y_train, y_holdout = train_test_split(X, y, test_size=.09, random_state=42)

# %%
lin_reg_est = LinearRegression()

# %%
regn = lin_reg_est.fit(X_train, y_train)

print(regn.intercept_)
print(regn.coef_)
print(regn.score(X_train, y_train))

# %%
#when we add a constant this gives us a much lower R^2

#model = sm.OLS(y_train, sm.add_constant(X_train)) 
model = sm.OLS(y_train, X_train) 
#Fit
fit = model.fit()

#Print out summary
fit.summary()

# %% [markdown]
# ## Lasso Regression

# %%
from __future__ import division, print_function  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from sklearn.datasets import load_diabetes
from sklearn.linear_model import Lasso, Ridge, ElasticNet, LinearRegression

from sklearn.model_selection import (cross_val_score, train_test_split, 
                                     KFold, GridSearchCV)

# %matplotlib inline

# %% [markdown]
# ### Repeated KFold

# %%
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.linear_model import Lasso 

#lasso
lasso = Lasso(alpha=0.05)
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
scores = cross_val_score(lasso, X, y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
scores = np.absolute(scores)
print('Repeat k-Fold MAE: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))

# %%
#regular
basic = LinearRegression()
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
scores = cross_val_score(basic, X, y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
scores = np.absolute(scores)
print('Repeat k-Fold MAE: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))

# %%
#ridge
ridge = Ridge(alpha=.05)
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
scores = cross_val_score(ridge, X, y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
scores = np.absolute(scores)
print('Repeat k-Fold MAE: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))

# %% [markdown]
# ### Single K-Fold

# %%
X_train, X_holdout, y_train, y_holdout = train_test_split(X, y, test_size=.09, random_state=42)

# %%
kfold = KFold(n_splits=10, shuffle=True, random_state=0)

# %%
#this model gives us a lower MSE


lin_reg_est = LinearRegression()

scores = cross_val_score(lasso, X_train, y_train, scoring='neg_mean_absolute_error', cv=kfold)
scores = np.absolute(scores)
print("Lasso Reg MAE Score: ", np.mean(scores))

lasso = lasso.fit(X_train, y_train)

# %%
scores = cross_val_score(basic, X_train, y_train, scoring='neg_mean_absolute_error', cv=kfold)
scores = np.absolute(scores)
print("Linear Reg MAE Score: ", np.mean(scores))

#X_train = sm.add_constant(X_train)
basic = basic.fit(X_train, y_train)

# %%
scores = cross_val_score(ridge, X_train, y_train, scoring='neg_mean_absolute_error', cv=kfold)
scores = np.absolute(scores)
print("Ridge Reg MAE Score: ", np.mean(scores))

#X_train = sm.add_constant(X_train)
ridge = ridge.fit(X_train, y_train)

# %%
predictors = X_train.columns

coef = pd.Series(lasso.coef_,predictors).sort_values()

coef.plot(kind='bar', title='Model Coefficients')

# %%
predictors = X_train.columns

coef = pd.Series(basic.coef_,predictors).sort_values()

coef.plot(kind='bar', title='Model Coefficients')

# %%
from sklearn.linear_model import Ridge
predictors = X_train.columns

coef = pd.Series(ridge.coef_,predictors).sort_values()

coef.plot(kind='bar', title='Model Coefficients')

# %%
#figure out R^2 score for lasso regression

# train_score = lin_reg_est.score(X_train, y_train)
# val_score = lin_reg_est.score(X_holdout, y_holdout)

# %%
# Fitted vs. Actual
#lin_reg_est
y_train_pred = ridge.predict(X_train)

#y_train_pred = lasso.predict(X_train)

plt.scatter(y_train, y_train_pred, alpha=0.2)
plt.plot([2.5, 5], [2.5, 5])

# %%
# Fitted vs. Actual
y_test_pred = ridge.predict(X_holdout)

plt.scatter(y_holdout, y_test_pred)
plt.plot([2.5, 5], [2.5, 5])

# %%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=0)

# %%
regressor = LinearRegression()  

regressor.fit(X_train, y_train)

# %%
#ridge

y_pred = ridge.predict(X_test)
df_ridge = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
df1 = df_ridge.head(25)
print(df1)

# %%
#normal

y_pred = regressor.predict(X_test)
df_basic = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
df1 = df_basic.head(25)
print(df1)

# %%
plt.scatter(df_ridge['Actual'], df_ridge['Predicted'])
plt.show()

# %%
import matplotlib.pyplot as plt

x = df_ridge['Actual']
y = df_ridge['Predicted']
#create basic scatterplot
plt.plot(x, y, 'o')

m, b = np.polyfit(x, y, 1)

#add linear regression line to scatterplot 
plt.plot(x, m*x+b)

# %%
import seaborn as sns

sns.regplot(x, y)

# %%
sns.set_theme(context="notebook", style="darkgrid")
plt.figure(clear=True, figsize=(15,6), facecolor="white")
plt.hist(x-y, color="cornflowerblue");
plt.xticks(fontsize=12)
plt.savefig("Residual hist")

# %%
a = master[['place', 'rating']].groupby(['place']).mean()
a = a.reset_index()

# %%
ax = a.plot.bar(x='place', y='rating', rot=0)
