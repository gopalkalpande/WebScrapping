#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json

# Specify the path to the JSON file
file_path = "data/inputJSONs/9.json"

# Read the JSON file
with open(file_path, "r") as file:
    json_data = json.load(file)


# In[2]:


json_keys = list(json_data.keys())


# In[3]:


# 0
plain_dict = {'giataId': json_data['giataId']}


# In[4]:


plain_dict['names'+'_value'] = str
plain_dict['names'+'_locale'] = str
# plain_dict
# 1
for dict_ in json_data['names']:
    if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
        plain_dict['names'+'_value'] = dict_['value']
        plain_dict['names'+'_locale'] = dict_['locale']



# In[5]:


# 2

plain_dict['city'+'_giataId'] = json_data['city']['giataId']

for dict_ in json_data['city']['names']:
    if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
        plain_dict['city'+'_value'] = dict_['value']
        plain_dict['city'+'_locale'] = dict_['locale']


# In[6]:


# 3

key_id = 3
plain_dict['destination'+'_giataId'] = json_data['destination']['giataId']

for dict_ in json_data['destination']['names']:
    if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
        plain_dict['destination'+'_value'] = dict_['value']
        plain_dict['destination'+'_locale'] = dict_['locale']


# In[7]:


# 4

key_id = 4
plain_dict['country'+'_code'] = json_data['country']['code']

for dict_ in json_data['country']['names']:
    if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
        plain_dict['country'+'_value'] = dict_['value']
        plain_dict['country'+'_locale'] = dict_['locale']


# In[8]:


# 5
key_id = 5

plain_dict['source'] = json_data['source']


# In[9]:


# 6

key_id = 6
# plain_dict[json_keys[key_id]+'_code'] = json_data[json_keys[key_id]]['code']

for dict_ in json_data['ratings']:
    if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
        plain_dict['ratings'+'_value'] = dict_['value']
        # plain_dict['ratings'+'_locale'] = dict_['locale']


# In[10]:


# 7

key_id = 7
# plain_dict['addresses'+'_code'] = json_data['addresses']['code']

for dict_ in json_data['addresses']:
    # if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
    plain_dict['addresses'+'_value_addressLines'] = ', '.join(dict_['addressLines'])
    plain_dict['addresses'+'_street'] = dict_['street']
    plain_dict['addresses'+'_zip'] = dict_['zip']
    plain_dict['addresses'+'_cityName'] = dict_['cityName']
    plain_dict['addresses'+'_poBox'] = dict_['poBox']


# In[12]:


# 8

key_id = 8
# plain_dict['phones'+'_code'] = json_data['phones']['code']
ph_ = []
fax_ = []
for dict_ in json_data['phones']:
    # print(type(ph_))
    # print('8', dict_)
    
    if dict_['tech']=='phone':
        # print('11',dict_['phone'])
        ph_.append(str(dict_['phone']))
        # print(ph_)
    else:
        fax_.append(dict_['phone'])
    
    plain_dict['phones'+'_phone'] = ph_
    plain_dict['phones'+'_fax'] = fax_


# In[13]:

# 9

key_id = 9
# plain_dict[json_keys[key_id]+'_code'] = json_data[json_keys[key_id]]['code']
email_ = []

if 'emails' in json_data.keys():
    
    for dict_ in json_data['emails']:
            email_.append(str(dict_['email']))
    
plain_dict['emails'] = email_


# 10

key_id = 10
# plain_dict['urls'+'_code'] = json_data['urls']['code']
url_ = []

for dict_ in json_data['urls']:
        url_.append(str(dict_['url']))
    
plain_dict['urls'] = url_


# In[14]:


# 11

key_id = 11
# plain_dict['geoCodes'+'_code'] = json_data['geoCodes']['code']

for dict_ in json_data['geoCodes']:
    # if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
        plain_dict['geoCodes'+'_latitude'] = dict_['latitude']
        plain_dict['geoCodes'+'_longitude'] = dict_['longitude']
        plain_dict['geoCodes'+'_accuracy'] = dict_['accuracy']


# In[15]:


# 12

key_id = 12

giataId_ = []
names_ = []
for dict_ in json_data['chains']:
    giataId_.append(dict_['giataId'])
    if 'names' in dict_.keys():
        for names_dict in dict_['names']:
            if 'isDefault' in names_dict.keys() and names_dict['isDefault']==True and names_dict['locale'] =='en':
                names_.append(names_dict['value'])
                

plain_dict['chains'+'_giataId'] = giataId_
plain_dict['chains'+'_names'] = names_


# In[16]:


# 13

# need to iterate overmultiple JSONs to learn about the variety of the attributes
dictSet = {}
for dict_ in json_data['roomTypes']:
    # print(dict_.keys())
    for key_ in dict_.keys():
        if isinstance(dict_.get(key_), dict):
            for key__ in dict_.get(key_).keys():
                # print('_'.join([key_,key__]))
                dictSet['_'.join([key_,key__])] = []
                # print()
        else: 
            dictSet[key_] = []


for dict_ in json_data['roomTypes']:
    for key_ in dictSet.keys():
        if '_' not in key_: # isinstance(dict_.get(key_), dict):
            dictSet[key_].append(dict_.get(key_))
        elif isinstance(dict_.get(key_), dict):
            dictSet[key_].append(dict_.get(key_.split('_')[0]).get(key_.split('_')[1]))
            print(key_, '\t', key__, '\t', dict_.get(key_.split('_')[0]).get(key_.split('_')[1]))
        else:
            dictSet[key_].append(dict_.get(key_))
        # print(key_, dict_.get(key_), type(dict_.get(key_)))
    # print('-'*10)


for subKey in dictSet.keys():
    plain_dict['_'.join(['roomTypes', subKey])] = dictSet[subKey]


# In[17]:


# 14

# need to iterate overmultiple JSONs to learn about the variety of the attributes
dictSet = {}
for dict_ in json_data['images']:
    # print(dict_.keys())
    for key_ in dict_.keys():
        if isinstance(dict_.get(key_), dict) and key_!='sizes':
            for key__ in dict_.get(key_).keys():
                # print('_'.join([key_,key__]))
                dictSet['_'.join([key_,key__])] = []
                # print()
        else: 
            dictSet[key_] = []
dictSet['herf'] = []

for dict_ in json_data['images']:
    hrefs = []
    for key_ in dictSet.keys():
        # if '_' not in key_: # isinstance(dict_.get(key_), dict):
            # dictSet[key_].append(dict_.get(key_))
        if isinstance(dict_.get(key_), dict) and key_=='sizes':
            # print(key_, '\n', list(dict_[key_].keys()))
            dictSet[key_].append(list(dict_[key_].keys()))
            # print(dict_.get(key_))
            imgDict = dict_.get(key_)
            for key__ in imgDict.keys():
                # print(imgDict[key__].keys())
                hrefs.append(imgDict[key__]['href'])
            # print(key_, '\t', key__, '\t', dict_.get(key_.split('_')[0]).get(key_.split('_')[1]))
        elif key_ == 'herf':
            dictSet[key_].append(hrefs)
        else:
            dictSet[key_].append(dict_.get(key_))
        # print(key_, dict_.get(key_), type(dict_.get(key_)))
    # print('-'*10)


for subKey in dictSet.keys():
    plain_dict['_'.join(['images', subKey])] = dictSet[subKey]



# In[19]:


# 15

# need to iterate overmultiple JSONs to learn about the variety of the attributes
dictSet = set()
dictSetNested = set()
for key_ in json_data['facts'].keys():
    # print(json_data['facts'][key_], '\n\n')
    for list_item in json_data['facts'][key_]:
        for listKey in list_item.keys():
            dictSet.add(listKey)
            if isinstance(list_item[listKey], dict):
                # print(list_item[listKey])
                for nestedKey_ in list_item[listKey].keys():
                    # print(nestedKey_, list_item[listKey][nestedKey_])
                    for nestedKey__, value_ in list_item[listKey][nestedKey_].items():
                        # print(nestedKey__, value_)
                        dictSetNested.add(nestedKey__)
            
# print('\n\n', dictSet, '\n\n', dictSetNested)

# check inclusion 1
# Use this code for id 15
dataDict = {'factDefId':[], 'attributes_attributeDefId':[], 'attributes_value':[], 'attributes_unitDefId':[]}
# dictSet = set()
# dictSetNested = set()
json_ = json_data['facts']
# print(type(json_))
for key_0 in json_.keys():
    # print(json_data['facts'][key_], '\n\n')
    for list_item in json_[key_0]:
        dataDict_ = {'factDefId':[], 'attributes_attributeDefId':[], 'attributes_value':[], 'attributes_unitDefId':[]}
        for key_1, value_1 in list_item.items():
            # print(listKey)
            if isinstance(value_1, str):
                # dataDict[key_1].append(value_1)
                dataDict_[key_1] = value_1
            elif isinstance(value_1, dict):
                # print(list_item[listKey])
                for key_2, value_2 in value_1.items():
                    if isinstance(value_2, str):
                        jointKey = '_'.join([key_1, key_2])
                        # print('#18', jointKey)
                        # dataDict[jointKey].append(value_2)
                        dataDict_[jointKey] = value_2
                    elif isinstance(value_2, dict):
                        for key_3, value_3 in value_2.items():
                            jointKey = '_'.join([key_1, key_3])
                            # print('#23', jointKey)
                            # dataDict[jointKey].append(value_3)
                            dataDict_[jointKey] = value_3
                            # print(key_3, value_3)
                            # pass
        for key in dataDict.keys():
                        if dataDict_[key]:
                            dataDict[key].append(str(dataDict_[key]))
                        else:
                            dataDict[key].append(None)
# print('\n\n', dataDict)

for subKey in dataDict.keys():
    plain_dict['_'.join(['facts', subKey])] = dataDict[subKey]


# In[20]:


# 16

plain_dict['variantGroups'] = json_data['variantGroups']


# In[21]:


# 17

textsData = {}
for data_ in json_data['texts']['en']['sections']:
    dataItems = data_.items()
    key = ''
    value = ''
    for key_, value_ in dataItems:
        if key_ == 'title':
            key = value_
        else:
            textsData['_'.join(['texts','en',key])] = value_
# print(textsData)

for data_ in json_data['texts']['en-US']['sections']:
    dataItems = data_.items()
    key = ''
    value = ''
    for key_, value_ in dataItems:
        if key_ == 'title':
            key = value_
        else:
            textsData['_'.join(['texts','en-US',key])] = value_
# print(textsData)

for subKey in textsData.keys():
    plain_dict[subKey] = textsData[subKey]


# In[24]:


list(plain_dict.keys())


# In[ ]:




