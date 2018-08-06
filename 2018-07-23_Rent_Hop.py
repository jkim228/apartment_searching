
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


# In[134]:


#html_page = requests.get('https://streeteasy.com/for-rent/nyc/beds%3C1?page=1')

html_page = requests.get('https://www.renthop.com/search/nyc?neighborhoods_str=1&max_price=50000&min_price=0&page=3&sort=hopscore&q=&search=0')


# In[135]:


soup = BeautifulSoup(html_page.content, 'html.parser')


# In[19]:


print(soup.prettify())


# In[ ]:


#https://streeteasy.com/for-rent/nyc/beds%3C1?page=2
#space each page or two a second apart 

for i in range(0,2):


# In[20]:


links = soup.find_all('a')


# In[21]:


len(links)


# In[25]:


links[70:74]


# In[35]:


#<a id="listing-12984637-title" class="font-size-11 listing-title-link b" href="https://www.renthop.com/listings/311-west-50th-st/1c/12984637">311 West 50th St, Apt 1C</a>
#<a id="listing-12943344-title" class="font-size-11 listing-title-link b" href="https://www.renthop.com/listings/west-30s/18ds/12943344">West 30's</a>
listings = soup.find_all('a', class_="font-size-11 listing-title-link b")


# In[37]:


listings[0]


# In[60]:


apts


# In[70]:


listing = []
url = []

for i in range(0,len(apts)):
    listing.append(apts[i].get_text())
    url.append(apts[i].get('href'))


# In[71]:


listing


# In[75]:


len(listing)


# In[76]:


listing_and_urls = pd.DataFrame({'listing':listing, 'url':url})


# In[92]:


name = []
price = []
bds = []
baths = []
neighborhood = []
urls = []
#<h1 class="d-block d-lg-none overflow-ellipsis vitals-title" style="font-weight: normal;">Studio/1BA at 311 West 50th St</h1>
for (n, url) in enumerate(listing_and_urls['url'][:2]):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    #get the apt name
    try:
        name.append(soup.find('h1', class_="d-block d-lg-none overflow-ellipsis vitals-title").get_text())
    except:
        name.append('')
        
    #get apt price 
    try:
        price.append(soup.find('div', class_="b vitals-title text-left text-lg-right").get_text())
    except:
        price.append('')


# In[78]:


response = requests.get('https://www.renthop.com/listings/311-west-50th-st/1c/12984637')


# In[80]:


soup = BeautifulSoup(response.content, 'html.parser')


# In[81]:


soup


# In[85]:


#<div class="b vitals-title text-left text-lg-right" style=""> $2,842 </div>
soup.find_all('div', class_="b vitals-title text-left text-lg-right")


# In[87]:


response2 = requests.get('https://www.renthop.com/listings/51-west-84-street/5/12994511')


# In[88]:


soup = BeautifulSoup(response2.content, 'html.parser')


# In[89]:


soup


# In[90]:


soup.find_all('div', class_="b vitals-title text-left text-lg-right")


# In[93]:


name


# In[94]:


price


# In[101]:


#pass in listing, return title
#pass in listing, return neighborhood
listing_id = '12984637'

response = requests.get('https://www.renthop.com/search/nyc?neighborhoods_str=1&max_price=50000&min_price=0&page=3&sort=hopscore&q=&search=0')


# In[102]:


soup = BeautifulSoup(response.content, 'html.parser')


# In[100]:


soup


# In[116]:


#<a id="listing-12984637-title" class="font-size-11 listing-title-link b" href="https://www.renthop.com/listings/311-west-50th-st/1c/12984637">311 West 50th St, Apt 1C</a>


soup.find_all('a', id="listing-12110146-title")


# In[107]:


print("listing-"+str(listing_id)+"-title")


# In[118]:


list_apts = soup.find_all('div', class_='search-listing font-size-10 my-4 my-md-0 py-0 py-md-4')


# In[119]:


len(list_apts)


# In[121]:


list_apts[0].get('listing_id')


# In[124]:


listing_ids = []

for i in range(0, len(list_apts)):
    listing_ids.append(list_apts[i].get('listing_id'))


# In[125]:


listing_ids


# In[1264]:


#listing-12984637-title
#listing-12984637-neighborhoods
#listing-12984637-info which has listing-12984637-price, bedrooms, bathrooms 

#FUNCTIONS
def get_listing_str(list_id, attribute):
    return "listing-"+str(list_id)+"-"+attribute


def get_num(string, amenity):
    if string == 'Studio' or string == 'Loft':
        return 0
    elif string == 'Share':
        return 1
    else:
        try:
            return int(string.replace(' '+amenity, ''))
        except:
            return float(string.replace(' '+amenity, ''))

def get_price(string):
    return int(string.replace(',','').replace('$',''))


# In[313]:


get_num('1.5 Bath', 'Bath')


# In[133]:


#get # of photos from the listing id="gallery-slider"

get_listing_str('12937293', 'title')


# In[136]:


soup.find_all('a')


# In[137]:


list_apts = soup.find_all('div', class_='search-listing font-size-10 my-4 my-md-0 py-0 py-md-4')


# In[191]:


list_apts[0]


# In[156]:


title = []
neighborhood = []

#get the titles and neighborhoods for list_apts
for i in range(0,len(list_apts)):
    x = get_listing_str(list_apts[i].get('listing_id'),'title')
    title.append(soup.find('a', id=x).get_text())
    
    y = get_listing_str(list_apts[i].get('listing_id'), 'neighborhoods')
    neighborhood.append(soup.find('div', id=y).get_text())
    
    z = get_listing_str(list_apts[i].get('listing_id'), 'info')
    print(soup.find('table', id=z))


# In[147]:


title


# In[151]:


neighborhood


# In[154]:


print(soup.find('table', id='12509090'))


# In[177]:


table = soup.find("table", {"id":"listing-12676114-info"})


# In[178]:


type(table)


# In[180]:


#get child
#get sibling 

l = table.findChildren()


# In[181]:


len(l)


# In[192]:


l[5].text


# In[ ]:


#1. Get the request into soup format 
#2. Loop through each page and call the get_listing_str function 
# -- Price
# -- Neighborhood
# -- Bds 
# -- Baths 
# -- N2H: # of photos 
# -- N2H: lat / long 


# In[193]:


response1 = requests.get('https://www.renthop.com/search/nyc?neighborhoods_str=1&max_price=50000&min_price=0&page=1&sort=hopscore&q=&search=0')


# In[194]:


soup = BeautifulSoup(response1.content, 'html.parser')


# In[195]:


soup


# In[196]:


soup.find_all('a')


# In[198]:


#List of listings: each item in this list contains all the apt attributes needed 
list_of_listings = soup.find_all('div', class_='search-listing font-size-10 my-4 my-md-0 py-0 py-md-4')


# In[855]:


#loop through each of the listings, and append attributes to the list
listing_id = []
title = []
neighb = []
greater_neighb = []
borough = []
price = []
bds = []
baths = []

#NOT get request
for i in range(0, len(list_of_listings)):
    list_id = list_of_listings[i].get('listing_id')
    list_title = get_listing_str(list_id,'title')
    
    if list_id not in listing_id:
        listing_id.append(list_id)
        title.append(soup.find('a', id=list_title).get_text())

        list_hood = get_listing_str(list_of_listings[i].get('listing_id'), 'neighborhoods')
        areas = []
        areas.append(soup.find('div', id=list_hood).get_text()) #'\nUpper East Side, Upper Manhattan, Manhattan\n'
        for a in areas:
            l = a.strip('\n').split(',')
            neighb.append(l[0])
            greater_neighb.append(l[1])
            borough.append(l[-1].strip())
        #list_info = get_listing_str(list_apts[i].get('listing_id'), 'info')
        #print(soup.find('table', id=list_info))
        x = list_of_listings[i].find('table').findChildren()
        price.append(get_price(x[1].get_text().strip('\n')))
        bds.append(get_num(x[2].get_text().strip('\n'),"Bed"))
        baths.append(get_num(x[4].get_text().strip('\n'),"Bath"))
    else:
        pass


# In[856]:


listing_id


# In[288]:


bds2


# In[279]:


bds


# In[230]:


bds


# In[263]:


apts = pd.DataFrame({'title':title, 
                     'neighb':neighb,
                     'greater_neighb':greater_neighb,
                     'borough':borough,
                     'price':price,
                     'bds':bds,
                     'baths':baths})


# In[264]:


apts


# In[240]:


for i in neighborhood:
    print(i.split(","))
    


# In[ ]:


neighborhood[0]


# In[623]:


# i = 1
# while i < 100:
#     print(i)
#     i += 1 # i = i + 1


# In[661]:


page = requests.get('https://www.renthop.com/search/nyc?max_price=50000&min_price=0&page=10000000&sort=hopscore&q=&search=0')


# In[663]:


soup = BeautifulSoup(page.content, 'html.parser')


# In[667]:


#<input class="d-none d-md-inline-block" style="width: 38px; text-align: center" id="page_input_box" type="text" value="3459">

soup.find('input', class_="d-none d-md-inline-block").get('value')


# In[664]:


list_of_listings = soup.find_all('div', class_='search-listing font-size-10 my-4 my-md-0 py-0 py-md-4')


# In[665]:


len(list_of_listings)


# In[715]:


j=3558
l = []

while True:
    url = 'https://www.renthop.com/search/nyc?max_price=50000&min_price=0&page=4000&sort=hopscore&q=&search=0'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    page_num = soup.find('input', class_="d-none d-md-inline-block").get('value') #3458
    l.append(page_num)
    j+=1
    j==page_num


# In[711]:


page_num


# In[713]:


x = 4000


# In[714]:


x == page_num


# In[662]:


page.status_code


# In[ ]:


listing_id = []
title = []
neighb = []
greater_neighb = []
borough = []
price = []
bds = []
baths = []


# In[1327]:


j


# In[1326]:


#1. gets the request!!


j=1501
page_num = 1501
status_boolean = True

while status_boolean == True : #checks if there's a next page
#while j<1500:
    url = 'https://www.renthop.com/search/nyc?max_price=50000&min_price=0&page='+str(j)+'&sort=hopscore&q=&search=0'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    page_num = int(soup.find('input', class_="d-none d-md-inline-block").get('value')) #used to check because pages stop incrementing 
    
    list_of_listings = soup.find_all('div', class_='search-listing font-size-10 my-4 my-md-0 py-0 py-md-4') #list of all the listings on the current page
    
    for i in range(0, len(list_of_listings)):
        list_id = list_of_listings[i].get('listing_id')
        list_title = get_listing_str(list_id,'title')
    
        if list_id not in listing_id:
            listing_id.append(list_id)
            title.append(soup.find('a', id=list_title).get_text())

            list_hood = get_listing_str(list_of_listings[i].get('listing_id'), 'neighborhoods')
            areas = []
            areas.append(soup.find('div', id=list_hood).get_text()) #'\nUpper East Side, Upper Manhattan, Manhattan\n'
            for a in areas:
                l = a.strip().split(',')
                neighb.append(l[0].strip())
                try:
                    greater_neighb.append(l[1].strip())
                except:
                    greater_neighb.append(l[0].strip())
                borough.append(l[-1].strip())
                
            #list_info = get_listing_str(list_apts[i].get('listing_id'), 'info')
            #print(soup.find('table', id=list_info))
            x = list_of_listings[i].find('table').findChildren()
            price.append(get_price(x[1].get_text().strip('\n')))
            try:
                bds.append(get_num(x[2].get_text().strip('\n'),"Bed"))
            except:
                bds.append(0)
            baths.append(get_num(x[4].get_text().strip('\n'),"Bath"))
            
        else:
            pass
    
    status_boolean = j == int(page_num)
    
#    if j%20==0:
#        print("j: "+str(j)+", page_num: "+str(page_num))

   
    j+=1 #update the page to the next page 


# In[1324]:


len(baths)


# In[1301]:


url = 'https://www.renthop.com/search/nyc?min_price=0&max_price=50000&bedrooms%5B0%5D=-1&q=&sort=hopscore&page=2&search=0'
response = requests.get(url)
soup = BeautifulSoup(page.content,'html.parser')
page_num = int(soup.find('input', class_="d-none d-md-inline-block").get('value'))
list_of_listings = soup.find_all('div', class_='search-listing font-size-10 my-4 my-md-0 py-0 py-md-4')


# In[1296]:


list_of_listings


# In[1304]:


listing_id = []
title = []
neighb = []
greater_neighb = []
borough = []
price = []
bds = []
baths = []
shared = []

for i in range(0, len(list_of_listings)):
        list_id = list_of_listings[i].get('listing_id') 
        list_title = get_listing_str(list_id,'title')
    
        if list_id not in listing_id: #checks if the listing has already been added to the list
            listing_id.append(list_id)
            title.append(soup.find('a', id=list_title).get_text())

            list_hood = get_listing_str(list_of_listings[i].get('listing_id'), 'neighborhoods')
            
            areas = []
            areas.append(soup.find('div', id=list_hood).get_text()) #'\nUpper East Side, Upper Manhattan, Manhattan\n'
            for a in areas:
                l = a.strip('\n').split(',')
                neighb.append(l[0].strip())
                try:
                    greater_neighb.append(l[1].strip())
                except:
                    greater_neighb.append(l[0].strip())
                borough.append(l[-1].strip())
                
            #list_info = get_listing_str(list_apts[i].get('listing_id'), 'info')
            #print(soup.find('table', id=list_info))
            x = list_of_listings[i].find('table').findChildren()
            print(x)
            price.append(get_price(x[1].get_text().strip('\n')))
            try:
                bds.append(get_num(x[2].get_text().strip('\n'),"Bed"))
            except:
                bds.append(0)
            baths.append(get_num(x[4].get_text().strip('\n'),"Bath"))
            
            #if x[2].get_text() == "Share":
             #   shared.append('yes')
            #else:
             #   shared.append('no')


# In[1335]:


len(baths)


# In[1289]:


shared


# In[ ]:


listing_id = []
title = []
neighb = []
greater_neighb = []
borough = []
price = []
bds = []
baths = []


# In[1274]:


len(baths)


# In[1276]:


l = [1,2,3,4]


# In[1284]:


type(l[4])


# In[841]:


j=3574
page_num=3574
status = True



while status == True:
    url = 'https://www.renthop.com/search/nyc?max_price=50000&min_price=0&page='+str(j)+'&sort=hopscore&q=&search=0'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    page_num = int(soup.find('input', class_="d-none d-md-inline-block").get('value')) #3458

    list_of_listings = soup.find_all('div', class_='search-listing font-size-10 my-4 my-md-0 py-0 py-md-4')

    status = j == page_num
    print("status: " + str(status))
    j+=1 #update the page to the next page 


# In[627]:


response.status_code == 200


# In[442]:


def price_per_bed(price_list, beds_list):
    new_list = []
    for x in range(0,len(price_list)):
        if beds_list[x] == 0:
            new_list.append(price_list[x])
        else: 
            new_list.append(int(price_list[x]/beds_list[x]))
    return new_list


# In[990]:


for i in range(0,len(price)):
    print("listing_id: "+str(listing_id[i])+" $"+str(price[i])+" "+str(bds[i])+" beds")


# In[963]:


len(price_per_bed(price,bds))


# In[971]:


len(bds)


# In[861]:


len(apts.groupby('listing_id')['listing_id'].transform('count'))


# In[1023]:


len(baths)


# In[1024]:


apts = pd.DataFrame({'listing_id':listing_id,
                     'title':title, 
                     'neighb':neighb,
                     'greater_neighb':greater_neighb,
                     'borough':borough,
                     'price':price,
                     'price_per_bed': price_per_bed(price,bds),
                     'bds':bds,
                     'baths':baths })


# In[585]:


len(apts)


# In[1027]:


apts['count'] = apts.groupby('listing_id')['listing_id'].transform('count')


# In[632]:


apts['price_per_bed'] = price_per_bed(price,bds)


# In[592]:


apts['greater_neighb']


# In[864]:


apts


# In[593]:


apts.groupby('greater_neighb')['price'].mean()


# In[ ]:


#make a dataframe with average price and count of available apartments 


# In[478]:


apts2


# In[381]:


import time


# In[594]:


by_greater_neighb


# In[595]:


by_greater_neighb['count'] = by_greater_neighb.groupby('greater_neighb')['greater_neighb'].transform('count')


# In[467]:


type(by_greater_neighb)


# In[469]:


type(apts)


# In[765]:


#how do i know how many pages to get
#how to plot count and average price 

by_greater_neighb = apts.groupby('greater_neighb')


# In[766]:


by_greater_neighb.head()


# In[597]:


type(by_greater_neighb)


# In[598]:


by_greater_neighb.plot(kind='bar')


# In[489]:


by_greater_neighb


# In[611]:


[1,2,3]+[4,5,6]


# In[615]:


list_of_funcs = []
def percentile(df_col, i=.5):
        return df_col.quantile(q=i/10.0)
for i in range(10):    
    list_of_funcs.append(percentile(i=i))


# In[638]:


def percentile_10(df_col, i=.10):
        return df_col.quantile(q=i)
def percentile_25(df_col, i=.25):
        return df_col.quantile(q=i)
def percentile_50(df_col, i=.50):
        return df_col.quantile(q=i)
def percentile_75(df_col, i=.75):
        return df_col.quantile(q=i)
def percentile_90(df_col, i=.90):
        return df_col.quantile(q=i)


# In[865]:


#df = apts.groupby('greater_neighb')['price_per_bed'].agg(['count','mean', percentile_10, percentile_25, percentile_50, percentile_75, percentile_90]).reset_index()
df = apts.groupby('greater_neighb')['price_per_bed'].agg([percentile_10, percentile_25, percentile_50, percentile_75, percentile_90])


# In[658]:


#to remove a column in the dataframe 
df.drop(['mean'], axis=1)


# In[727]:


df['percentile_10'].min()


# In[672]:


df = df.set_index('greater_neighb')


# In[692]:


df.plot(kind='barh', stacked=True, figsize=(12,12))


# In[731]:


from itertools import cycle, islice


# In[751]:


my_colors = list(islice(cycle(['#e6e6e6', '#80aaff', '#1a66ff', '#1a66ff', '#80aaff']), None, len(df)))

# Specify this list of colors as the `color` option to `plot`.


# In[789]:


my_colors = list(islice(cycle(['#e6e6e6', '#80aaff', '#1a66ff', '#1a66ff', '#80aaff']), None, len(df)))
df.plot(kind='barh', figsize = (10,10), stacked=True, color=my_colors)


# In[ ]:


sns.swarmplot(x="greater_neighb", y="price", data=df)


# In[1031]:


by_manhattan = apts[apts['borough']=='Manhattan']
by_brooklyn = apts[apts['borough']=='Brooklyn']
by_queens = apts[apts['borough']=='Queens']


# In[1032]:


by_manhattan


# In[816]:


h = sns.barplot(x='greater_neighb', y='price', data=by_brooklyn)


# In[815]:


for item in h.get_xticklabels():
    item.set_rotation(45)


# In[820]:


h.set_xticklabels(h.get_xticklabels(), rotation=45)


# In[821]:


h = sns.barplot(x='greater_neighb', y='price', data=by_brooklyn)


# In[704]:


df2 = apts.groupby('greater_neighb')['price_per_bed'].agg(['sum'])


# In[705]:


df2.plot(kind='box', by='greater_neighb')


# In[546]:


type(apts['price'].count())


# In[599]:


type(get_quantile(apts))


# In[600]:


get_quantile(apts.groupby('greater_neighb'))


# In[640]:


import numpy as np
import matplotlib.pyplot as plt


# In[649]:





# In[677]:


df.plot(kind='box')


# In[716]:


df


# In[718]:


import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()


# In[719]:


current_palette = sns.color_palette()
sns.palplot(current_palette)


# In[753]:


df.head()


# In[755]:


by_greater_neighb.head()


# In[1030]:


apts.groupby('borough')['count'].sum().sort_values(ascending=False)


# In[1025]:


sns.swarmplot(x="borough", y="price_per_bed", data=apts)


# In[775]:


by_downtown = apts[apts['greater_neighb']=="Downtown Manhattan"]


# In[794]:


sns.swarmplot(x="neighb", y="price_per_bed", data=by_downtown)


# In[795]:


g = sns.swarmplot(x="greater_neighb", y="price_per_bed", data=apts)


# In[796]:


sns.swarmplot(x="greater_neighb", y="price_per_bed", data=apts)


# In[800]:


g.set_xticklabels(g.get_xticklabels, rotation=45)
#bbox_to_anchor sets the legend 


# In[828]:





# In[872]:


#df = apts.groupby('greater_neighb')['price_per_bed'].agg(['count','mean', percentile_10, percentile_25, percentile_50, percentile_75, percentile_90]).reset_index()
df2 = apts.groupby(['borough','greater_neighb'])


# In[873]:


df2.head()


# In[851]:


df2.reset_index()


# In[878]:


sns.swarmplot(x='greater_neighb', y='price_per_bed', data=apts)


# In[879]:


sns.set(,style="whitegrid")


# In[891]:


#1. set count of apartments by greater neighborhood
apts['greater_neighb'] = apts['greater_neighb'].str.strip()


# In[900]:


by_neighb = apts.groupby('greater_neighb')['count'].sum().sort_values(ascending = False)


# In[906]:


df_neighb = pd.DataFrame({'neighborhood':by_neighb.index, 'count':by_neighb.values})


# In[918]:


sns.barplot(x="count", y="neighborhood", data=df_neighb)


# In[919]:


apts

#find centroid of neighborhood 
#qgis if trying to outline neighborhoods 


# In[ ]:


#geopandas 


# In[1165]:


#z score for price (group by neighborhood) (group by apartment)
mean_price = apts['price_per_bed'].mean()
sd_price = apts['price_per_bed'].std()


# In[923]:


#distribution of price per bed 
sns.distplot(apts['price_per_bed'])


# In[925]:


#new column - normalized price per bed 
sd_price


# In[929]:


#(price - mean) / std 
#less is better
apts['z_score_price'] = (apts['price_per_bed']-mean_price) / sd_price


# In[928]:


apts.sort_values(by = 'z_score')


# In[942]:


count_neighb = apts.groupby('neighb')['count'].sum().reset_index()


# In[938]:


to_replace = {'neighb': {' Financial District': 'Financial District', ' Greenwich Village':'Greenwich Village', ' Murray Hill': 'Murray Hill', ' SoHo': 'SoHo', " Hell's Kitchen": "Hell's Kitchen"}}


# In[939]:


apts = apts.replace(to_replace)


# In[940]:


apts.groupby('neighb')['count'].sum()


# In[943]:


count_neighb


# In[944]:


mean_count = count_neighb['count'].mean()
sd_count = count_neighb['count'].std()


# In[945]:


sd_count = count_neighb['count'].std()


# In[946]:


mean_count = count_neighb['count'].mean()
sd_count = count_neighb['count'].std()

count_neighb['z_score_count'] = (count_neighb['count'] - mean_count) / sd_count


# In[947]:


count_neighb


# In[951]:


apts = apts.merge(count_neighb, on='neighb')


# In[949]:


#axis 0 means index, axis 1 means columns 
apts = apts.drop('z_score', axis=1)


# In[952]:


apts


# In[953]:


apts['score'] = -apts['z_score_price']+apts['z_score_count']


# In[955]:


apts.sort_values(by = 'score', ascending=False)


# In[ ]:


#z score price
#z score count 

#stacked z score price and z score count 


# In[1042]:


by_borough = apts.groupby('borough')['count'].sum().sort_values(ascending = False)
df_borough = pd.DataFrame({'borough':by_borough.index, 'count':by_borough.values})


# In[1054]:


sns.set(style="whitegrid")


plt.subplots(figsize=(8,8))
sns.barplot(x='count', y='borough', data=df_borough)


# In[1041]:


df_borough


# In[1074]:


apts = apts[(apts['borough'] == 'Manhattan') | (apts['borough'] == 'Queens') | (apts['borough'] == 'Brooklyn')]


# In[1075]:


len(apts)


# In[1132]:


apts.groupby('greater_neighb')['count'].sum()


# In[1133]:


by_greater_neighb = apts.groupby('greater_neighb')['count'].sum().sort_values(ascending = False)


# In[1125]:


df_greater_neighb = pd.DataFrame({'greater_neighb':by_greater_neighb.index, 'count':by_greater_neighb.values})


# In[1109]:


plt.subplots(figsize=(9,9))
sns.barplot(x='count', y='greater_neighb', data=df_greater_neighb)


# In[1135]:


by_greater_neighb = by_greater_neighb.reset_index()


# In[1120]:


to_replace = {'greater_neighb': {' Midtown Manhattan': 'Midtown Manhattan', 
                         ' Upper West Side':'Upper West Side', 
                         ' Upper Manhattan': 'Upper Manhattan', 
                         ' Kips Bay': 'Kips Bay', 
                         " Northwestern Queens": "Northwestern Queens",
                        " Northwestern Brooklyn": "Northwestern Brooklyn",
                        " East Village": "East Village",
                        " Downtown Manhattan": "Downtown Manhattan" }}

apts = apts.replace(to_replace)


# In[1146]:


#consider only neighborhoods that have more than 10 listings 
by_greater_neighb = by_greater_neighb[by_greater_neighb['count'] > 10]


# In[1148]:


plt.subplots(figsize=(9,9))

sns.barplot(x='count', y='greater_neighb', data=by_greater_neighb)


# In[1129]:


type(by_greater_neighb)


# In[1115]:


type(apts.groupby('greater_neighb')['count'].sum().sort_values(ascending = False))


# In[1124]:


by_greater_neighb


# In[1149]:


#df = apts.groupby('greater_neighb')['price_per_bed'].agg(['count','mean', percentile_10, percentile_25, percentile_50, percentile_75, percentile_90]).reset_index()
df = apts.groupby('greater_neighb')['price_per_bed'].agg([percentile_10, percentile_25, percentile_50, percentile_75, percentile_90])


# In[1161]:


df = df.sort_values('percentile_50', ascending=False)


# In[1155]:


df = df.iloc[2:]


# In[1159]:


df


# In[1164]:


my_colors = list(islice(cycle(['w', '#80aaff', '#1a66ff', '#1a66ff', '#80aaff']), None, len(df)))
df.plot(kind='barh', figsize = (9,9), stacked=True, color=my_colors, grid=False)


# In[1167]:


#z score for price (group by neighborhood) (group by apartment)
mean_price = apts['price_per_bed'].mean()
sd_price = apts['price_per_bed'].std()


# In[1170]:


apts['z_score_price'] = (apts['price_per_bed']-mean_price) / sd_price


# In[1175]:


count_neighb = apts.groupby('greater_neighb')['count'].sum().reset_index()


# In[1178]:


mean_count = count_neighb['count'].mean()
sd_count = count_neighb['count'].std()

count_neighb['z_score_count'] = (count_neighb['count'] - mean_count) / sd_count


# In[1232]:


sd_count


# In[1176]:


mean_count = apts['count'].mean()
sd_count = apts['count'].std()


# In[1173]:


apts['z_score_count'] = (apts['count'] - mean_count) / sd_count


# In[1174]:


apts.head()


# In[1168]:


sns.distplot(apts['price_per_bed'])


# In[1183]:


apts = apts.drop('z_score_count', axis=1)


# In[1184]:


apts.head()


# In[1185]:


apts = apts.merge(count_neighb, on='greater_neighb')


# In[1186]:


apts.head()


# In[1191]:


apts['z_score_count'].min()


# In[1238]:


apts['z_score_price'] = (apts['price_per_bed']-mean_price) / sd_price


# In[1408]:


apts['score'] = -6*apts['z_score_price']+apts['z_score_count']


# In[1412]:


apts = apts.sort_values(by='score', ascending=False)


# In[1421]:


top_10 = apts[:10]


# In[1422]:


top_10


# In[1429]:


plt.subplots(figsize=(12,9))

sns.barplot(data=top_10, x='price_per_bed', y='title', palette="rocket")


# In[ ]:


plt.subplots(figsize=(9,9))
sns.barplot(x='price_per_bed', y='title', data=top_10) 


# In[1211]:


df = apts.sort_values('price_per_bed')


# In[1218]:


apts = df.drop(df.index[[0,1]])


# In[1224]:


sns.distplot(apts['z_score_price'])


# In[1225]:


sns.distplot(apts['z_score_count'])


# In[1229]:





# In[ ]:


sns.scatterplot(x="carat", y="price",
                hue="clarity", size="depth",
                palette="ch:r=-.2,d=.3_r",
                hue_order=clarity_ranking,
                sizes=(1, 8), linewidth=0,
                data=diamonds, ax=ax)


# In[1245]:


plt.subplots(figsize=(9,9))

sns.regplot(x='bds', y='baths', data=apts, fit_reg=False)


# In[1249]:


plt.subplots(figsize=(9,9))
sns.swarmplot(x="greater_neighb", y="price", hue='bds', data=apts)


# In[1259]:


apts.melt(apts, "borough", var_name="measurement")


# In[1255]:


apts


# In[1263]:



plt.subplots(figsize=(9,9))

sns.violinplot(x='borough', y='price_per_bed', data=apts)


# In[1368]:


###TAKE THREE
#step3: put it into a dataframe
apts = pd.DataFrame({'listing_id':listing_id,
                     'title':title, 
                     'neighb':neighb,
                     'greater_neighb':greater_neighb,
                     'borough':borough,
                     'price':price,
                     'price_per_bed': price_per_bed(price,bds),
                     'bds':bds,
                     'baths':baths })


# In[1369]:


#adds a count column
apts['count'] = apts.groupby('listing_id')['listing_id'].transform('count')


# In[1342]:


by_borough = apts.groupby('borough')['count'].sum().sort_values(ascending=False)


# In[1344]:


by_borough = by_borough.reset_index()


# In[1346]:


#plot how many apartments are available in each neighborhood
plt.subplots(figsize=(9,9))

sns.barplot(x='count', y='borough', data=by_borough)


# In[1370]:


apts = apts[(apts['borough'] == 'Manhattan') | (apts['borough'] == 'Queens') | (apts['borough'] == 'Brooklyn')]


# In[1349]:


by_greater_neighb = apts.groupby('greater_neighb')['count'].sum().sort_values(ascending = False)


# In[1353]:


by_greater_neighb = by_greater_neighb.reset_index()


# In[1354]:


plt.subplots(figsize=(9,9))

sns.barplot(x='count', y='greater_neighb', data=by_greater_neighb)


# In[1355]:


apts2 = apts.groupby('greater_neighb')['price_per_bed'].agg([percentile_10, percentile_25, percentile_50, percentile_75, percentile_90])


# In[1365]:


apts2 = apts2.sort_values('percentile_50', ascending = False)


# In[1366]:


my_colors = list(islice(cycle(['w', '#80aaff', '#1a66ff', '#1a66ff', '#80aaff']), None, len(df)))
apts2.plot(kind='barh', figsize = (9,9), stacked=True, color=my_colors, grid=False)


# In[1371]:


#z score for price (group by neighborhood) (group by apartment)
mean_price = apts['price_per_bed'].mean()
sd_price = apts['price_per_bed'].std()


# In[1372]:


apts['z_score_price'] = (apts['price_per_bed']-mean_price) / sd_price


# In[1373]:


count_neighb = apts.groupby('greater_neighb')['count'].sum().reset_index()


# In[1374]:


mean_count = count_neighb['count'].mean()
sd_count = count_neighb['count'].std()

count_neighb['z_score_count'] = (count_neighb['count'] - mean_count) / sd_count


# In[1382]:


sns.distplot(apts['z_score_price'])


# In[1385]:


apts = apts.merge(count_neighb, on='greater_neighb')


# In[1386]:


apts


# In[1388]:


sns.swarmplot(x="bds", y="price", hue="greater_neighb", data=apts)


# In[1392]:


plt.subplots(figsize=(9,9))

sns.violinplot(data=apts, x='bds', y='price_per_bed')


# In[1401]:


apts['greater_neighb']['count_x'].sum()


# In[1400]:


apts

