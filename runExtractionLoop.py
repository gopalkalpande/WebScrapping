#!/usr/bin/env python
# coding: utf-8

# In[3120]:


#!/usr/bin/env python
# coding: utf-8


# In[1]:

# In[3121]:


# import json


# Specify the path to the JSON file

# In[3122]:


# file_path = "data/inputJSONs/9.json"


# In[3123]:


import os
import random
import jsonschema, json
from genson import SchemaBuilder
import pandas as pd 
import time



dfKeys = ['fileId', 'giataId', 'names_locale', 'names_value', 'country_code', 'source', 'country_locale', 'country_value', 'destination_giataId', 'destination_locale', 'destination_value', 'addresses_cityName', 'addresses_federalState', 'addresses_federalStateCode', 'addresses_federalStateName', 'addresses_poBox', 'addresses_street', 'addresses_streetNum', 'addresses_value_addressLines', 'addresses_zip', 'chains_giataId', 'chains_names', 'city_giataId', 'city_locale', 'city_value', 'emails', 'urls', 'facts_attributes_attributeDefId', 'facts_attributes_unitDefId', 'facts_attributes_value', 'facts_factDefId', 'geoCodes_accuracy', 'geoCodes_latitude', 'geoCodes_longitude', 'images_baseName', 'images_herf', 'images_heroImage', 'images_id', 'images_lastUpdate', 'images_motifType', 'images_sizes', 'phones_fax', 'phones_phone', 'ratings_value', 'roomTypes_category', 'roomTypes_categoryInformation_attributeDefId', 'roomTypes_categoryInformation_name', 'roomTypes_code', 'roomTypes_imageRelations', 'roomTypes_name', 'roomTypes_type', 'roomTypes_typeInformation_attributeDefId', 'roomTypes_typeInformation_name', 'roomTypes_variantId', 'roomTypes_view', 'roomTypes_viewInformation_attributeDefId', 'roomTypes_viewInformation_name', 'texts_en_Facilities', 'texts_en_Location', 'texts_en_Meals', 'texts_en_Payment', 'texts_en_Rooms', 'texts_en_Sports/Entertainment', 'texts_en-US_Facilities', 'texts_en-US_Location', 'texts_en-US_Meals', 'texts_en-US_Payment', 'texts_en-US_Rooms', 'texts_en-US_Sports/Entertainment', 'variantGroups']
output = pd.DataFrame(columns=dfKeys)

min_ = 0
max_ = 0000
writeCSV = './data/extractedTable.csv'  # _'+str(min_)+'_'+ str(max_)+'

# Path to the input JSONs folder
folder_path = './data/inputJSONs'

# Get a list of all hjson files in the folder
hjson_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

# Select 50 random hjson files
# random_files = random.sample(hjson_files, 50)

start = time.time()

for file_ in hjson_files:
    file_path = os.path.join(folder_path, file_)
    print(file_path)
    with open(file_path, "r") as file:
        json_data = json.load(file)

    json_keys = list(json_data.keys())

    keys = ['giataId', 'names', 'city', 'destination', 'country', 'source', 'ratings', 'addresses', 'phones', 'emails', 'urls', 'geoCodes', 'chains', 'roomTypes', 'images', 'facts', 'variantGroups', 'texts']

    finalKeysJsonLevel1 = set(keys).union(json_keys)

    try:
        
        plain_dict = {'fileId': file_, 'giataId': json_data['giataId']}

        plain_dict['names'+'_value'] = str
        plain_dict['names'+'_locale'] = str

        for dict_ in json_data['names']:
            if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
                plain_dict['names'+'_value'] = dict_['value']
                plain_dict['names'+'_locale'] = dict_['locale']

        plain_dict['city'+'_giataId'] = json_data['city']['giataId']

        for dict_ in json_data['city']['names']:
            if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
                plain_dict['city'+'_value'] = dict_['value']
                plain_dict['city'+'_locale'] = dict_['locale']

        key_id = 3
        plain_dict['destination'+'_giataId'] = json_data['destination']['giataId']

        for dict_ in json_data['destination']['names']:
            if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
                plain_dict['destination'+'_value'] = dict_['value']
                plain_dict['destination'+'_locale'] = dict_['locale']

        key_id = 4
        plain_dict['country'+'_code'] = json_data['country']['code']

        for dict_ in json_data['country']['names']:
            if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
                plain_dict['country'+'_value'] = dict_['value']
                plain_dict['country'+'_locale'] = dict_['locale']

        key_id = 5

        plain_dict['source'] = json_data['source']

        key_id = 6

        for dict_ in json_data['ratings']:
            if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
                plain_dict['ratings'+'_value'] = dict_['value']
                # plain_dict['ratings'+'_locale'] = dict_['locale']


        key_id = 7
        # plain_dict['addresses'+'_code'] = json_data['addresses']['code']

        for dict_ in json_data['addresses']:
            # if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
            plain_dict['addresses'+'_value_addressLines'] = ', '.join(dict_.get('addressLines'))
            plain_dict['addresses'+'_street'] = dict_.get('street') #
            plain_dict['addresses'+'_streetNum'] = dict_.get('streetNum')
            plain_dict['addresses'+'_zip'] = dict_.get('zip') #
            plain_dict['addresses'+'_cityName'] = dict_.get('cityName') #
            if dict_.get('federalState'):
                plain_dict['addresses'+'_federalStateName'] = dict_.get('federalState').get('name')
                plain_dict['addresses'+'_federalStateCode'] = dict_.get('federalState').get('code')
            plain_dict['addresses'+'_poBox'] = dict_.get('poBox')     # dict_['poBox']
            plain_dict['addresses'+'_zip'] = dict_.get('zip')
            

        key_id = 8
        # plain_dict['phones'+'_code'] = json_data['phones']['code']
        ph_ = []
        fax_ = []
        if 'phones' in json_keys:
            for dict_ in json_data['phones']:
                # print(type(ph_))
                # print('8', dict_)
                # print(dict_)
                if dict_['tech']=='phone':
                    # print('11',dict_['phone'])
                    ph_.append(str(dict_['phone']))
                    # print(ph_)
                else:
                    fax_.append(dict_['phone'])
            
        plain_dict['phones'+'_phone'] = ph_
        plain_dict['phones'+'_fax'] = fax_

        key_id = 9
        # plain_dict[json_keys[key_id]+'_code'] = json_data[json_keys[key_id]]['code']
        email_ = []

        if 'emails' in json_data.keys():
            
            for dict_ in json_data['emails']:
                # print(dict_)
                email_.append(str(dict_['email']))
            
        plain_dict['emails'] = email_

        key_id = 10
        # plain_dict['urls'+'_code'] = json_data['urls']['code']
        url_ = []

        for dict_ in json_data['urls']:
                url_.append(str(dict_['url']))
            
        plain_dict['urls'] = url_


        key_id = 11
        # plain_dict['geoCodes'+'_code'] = json_data['geoCodes']['code']

        for dict_ in json_data['geoCodes']:
            # if 'isDefault' in dict_.keys() and dict_['isDefault']==True:
                plain_dict['geoCodes'+'_latitude'] = dict_['latitude']
                plain_dict['geoCodes'+'_longitude'] = dict_['longitude']
                plain_dict['geoCodes'+'_accuracy'] = dict_['accuracy']


        key_id = 12

        giataId_ = []
        names_ = []
        if 'chains' in json_keys:
            # print('inside chains')
            for dict_ in json_data['chains']:
                giataId_.append(dict_['giataId'])
                if 'names' in dict_.keys():
                    for names_dict in dict_['names']:
                        if 'isDefault' in names_dict.keys() and names_dict['isDefault']==True and names_dict['locale'] =='en':
                            names_.append(names_dict['value'])
                            

        plain_dict['chains'+'_giataId'] = giataId_
        plain_dict['chains'+'_names'] = names_

        # 13
        # need to iterate overmultiple JSONs to learn about the variety of the attributes

        dictSet = {}
        if 'roomTypes' in json_keys:
            # print('inside roomType')
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


        # 14

        # need to iterate overmultiple JSONs to learn about the variety of the attributes

        if 'images' in json_keys:
            # print('inside images')
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


        plain_dict['variantGroups'] = json_data['variantGroups']

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



    except Exception as e:
        print(e)
        print(file_path)
    # else:
    #     pass
    # finally:
    #     pass
    # dfKeys = ['giataId', 'names_locale', 'names_value', 'country_code', 'source', 'country_locale', 'country_value', 'destination_giataId', 'destination_locale', 'destination_value', 'addresses_cityName', 'addresses_federalState', 'addresses_federalStateCode', 'addresses_federalStateName', 'addresses_poBox', 'addresses_street', 'addresses_streetNum', 'addresses_value_addressLines', 'addresses_zip', 'chains_giataId', 'chains_names', 'city_giataId', 'city_locale', 'city_value', 'emails', 'urls', 'facts_attributes_attributeDefId', 'facts_attributes_unitDefId', 'facts_attributes_value', 'facts_factDefId', 'geoCodes_accuracy', 'geoCodes_latitude', 'geoCodes_longitude', 'images_baseName', 'images_herf', 'images_heroImage', 'images_id', 'images_lastUpdate', 'images_motifType', 'images_sizes', 'phones_fax', 'phones_phone', 'ratings_value', 'roomTypes_category', 'roomTypes_categoryInformation_attributeDefId', 'roomTypes_categoryInformation_name', 'roomTypes_code', 'roomTypes_imageRelations', 'roomTypes_name', 'roomTypes_type', 'roomTypes_typeInformation_attributeDefId', 'roomTypes_typeInformation_name', 'roomTypes_variantId', 'roomTypes_view', 'roomTypes_viewInformation_attributeDefId', 'roomTypes_viewInformation_name', 'texts_en_Facilities', 'texts_en_Location', 'texts_en_Meals', 'texts_en_Payment', 'texts_en_Rooms', 'texts_en_Sports/Entertainment', 'texts_en-US_Facilities', 'texts_en-US_Location', 'texts_en-US_Meals', 'texts_en-US_Payment', 'texts_en-US_Rooms', 'texts_en-US_Sports/Entertainment', 'variantGroups']

    # # finalDfKeys = set()
    # print(len(finalDfKeys))
    # finalDfKeys = set(dfKeys).union(set(list(plain_dict.keys())))

    # print(finalDfKeys, len(finalDfKeys))

    # 54
    # {'texts_en-US_Meals', 'chains_giataId', 'facts_attributes_unitDefId', 'texts_en-US_Payment', 'texts_en-US_Location', 'geoCodes_latitude', 'country_code', 'addresses_poBox', 'phones_phone', 'facts_factDefId', 'texts_en_Payment', 'addresses_streetNum', 'country_value', 'country_locale', 'images_baseName', 'city_giataId', 'city_value', 'images_herf', 'texts_en_Location', 'images_sizes', 'texts_en_Meals', 'names_value', 'destination_value', 'ratings_value', 'addresses_cityName', 'texts_en_Rooms', 'texts_en_Sports/Entertainment', 'texts_en_Facilities', 'source', 'images_lastUpdate', 'images_heroImage', 'images_id', 'variantGroups', 'geoCodes_accuracy', 'images_motifType', 'chains_names', 'addresses_street', 'destination_locale', 'giataId', 'texts_en-US_Rooms', 'addresses_federalState', 'texts_en-US_Sports/Entertainment', 'facts_attributes_value', 'phones_fax', 'urls', 'names_locale', 'texts_en-US_Facilities', 'emails', 'facts_attributes_attributeDefId', 'addresses_value_addressLines', 'addresses_zip', 'geoCodes_longitude', 'destination_giataId', 'city_locale'}


    df_dictionary = pd.DataFrame([plain_dict])
    output = pd.concat([output, df_dictionary], ignore_index=True)
    print(output.shape)

print('time to execute: ', time.time()-start)

output.to_csv(writeCSV, index=False)

