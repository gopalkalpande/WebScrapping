import os
import random
import jsonschema
import json
from genson import SchemaBuilder
import pandas as pd
import time

dfKeys = ['fileId', 'giataId', 'names_locale', 'names_value', 'country_code', 'source', 'country_locale', 'country_value', 'destination_giataId', 'destination_locale', 'destination_value', 'addresses_cityName', 'addresses_federalState', 'addresses_federalStateCode', 'addresses_federalStateName', 'addresses_poBox', 'addresses_street', 'addresses_streetNum', 'addresses_value_addressLines', 'addresses_zip', 'chains_giataId', 'chains_names', 'city_giataId', 'city_locale', 'city_value', 'emails', 'urls', 'facts_attributes_attributeDefId', 'facts_attributes_unitDefId', 'facts_attributes_value', 'facts_factDefId', 'geoCodes_accuracy', 'geoCodes_latitude', 'geoCodes_longitude', 'images_baseName', 'images_herf', 'images_heroImage', 'images_id', 'images_lastUpdate', 'images_motifType', 'images_sizes', 'phones_fax', 'phones_phone', 'ratings_value', 'roomTypes_category', 'roomTypes_categoryInformation_attributeDefId', 'roomTypes_categoryInformation_name', 'roomTypes_code', 'roomTypes_imageRelations', 'roomTypes_name', 'roomTypes_type', 'roomTypes_typeInformation_attributeDefId', 'roomTypes_typeInformation_name', 'roomTypes_variantId', 'roomTypes_view', 'roomTypes_viewInformation_attributeDefId', 'roomTypes_viewInformation_name', 'texts_en_Facilities', 'texts_en_Location', 'texts_en_Meals', 'texts_en_Payment', 'texts_en_Rooms', 'texts_en_Sports/Entertainment', 'texts_en-US_Facilities', 'texts_en-US_Location', 'texts_en-US_Meals', 'texts_en-US_Payment', 'texts_en-US_Rooms', 'texts_en-US_Sports/Entertainment', 'variantGroups']
output = []

min_ = 0
max_ = 0000
writeCSV = './data/extractedTableFromUpdatedCode.csv'  # _'+str(min_)+'_'+ str(max_)+'

# Path to the input JSONs folder
folder_path = './data/inputJSONs'

# Get a list of all hjson files in the folder
hjson_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

start = time.time()

for file_ in hjson_files[0:10]:
    file_path = os.path.join(folder_path, file_)
    print(file_path)
    with open(file_path, "r") as file:
        json_data = json.load(file)

    plain_dict = {'fileId': file_, 'giataId': json_data['giataId']}

    plain_dict['names_value'] = next((dict_['value'] for dict_ in json_data['names'] if dict_.get('isDefault') and dict_['isDefault'] == True), '')
    plain_dict['names_locale'] = next((dict_['locale'] for dict_ in json_data['names'] if dict_.get('isDefault') and dict_['isDefault'] == True), '')

    plain_dict['city_giataId'] = json_data['city']['giataId']
    plain_dict['city_value'] = next((dict_['value'] for dict_ in json_data['city']['names'] if dict_.get('isDefault') and dict_['isDefault'] == True), '')
    plain_dict['city_locale'] = next((dict_['locale'] for dict_ in json_data['city']['names'] if dict_.get('isDefault') and dict_['isDefault'] == True), '')

    plain_dict['destination_giataId'] = json_data['destination']['giataId']
    plain_dict['destination_value'] = next((dict_['value'] for dict_ in json_data['destination']['names'] if dict_.get('isDefault') and dict_['isDefault'] == True), '')
    plain_dict['destination_locale'] = next((dict_['locale'] for dict_ in json_data['destination']['names'] if dict_.get('isDefault') and dict_['isDefault'] == True), '')

    plain_dict['country_code'] = json_data['country']['code']
    plain_dict['country_value'] = next((dict_['value'] for dict_ in json_data['country']['names'] if dict_.get('isDefault') and dict_['isDefault'] == True), '')
    plain_dict['country_locale'] = next((dict_['locale'] for dict_ in json_data['country']['names'] if dict_.get('isDefault') and dict_['isDefault'] == True), '')

    plain_dict['source'] = json_data['sources', 'roomTypes_name', 'roomTypes_type', 'roomTypes_typeInformation_attributeDefId', 'roomTypes_typeInformation_name', 'roomTypes_variantId', 'roomTypes_view', 'roomTypes_viewInformation_attributeDefId', 'roomTypes_viewInformation_name', 'texts_en_Facilities', 'texts_en_Location', 'texts_en_Meals', 'texts_en_Payment', 'texts_en_Rooms', 'texts_en_Sports/Entertainment', 'texts_en-US_Facilities', 'texts_en-US_Location', 'texts_en-US_Meals', 'texts_en-US_Payment', 'texts_en-US_Rooms', 'texts_en-US_Sports/Entertainment', 'variantGroups']

    plain_dict['ratings_value'] = next((dict_['value'] for dict_ in json_data['ratings'] if dict_.get('isDefault') and dict_['isDefault'] == True), '')

    addresses = json_data.get('addresses', [])
    plain_dict['addresses_value_addressLines'] = ', '.join([dict_.get('addressLines', '') for dict_ in addresses])
    plain_dict['addresses_street'] = next((dict_.get('street', '') for dict_ in addresses), '')
    plain_dict['addresses_streetNum'] = next((dict_.get('streetNum', '') for dict_ in addresses), '')
    plain_dict['addresses_zip'] = next((dict_.get('zip', '') for dict_ in addresses), '')
    plain_dict['addresses_cityName'] = next((dict_.get('cityName', '') for dict_ in addresses), '')
    plain_dict['addresses_federalStateName'] = next((dict_.get('federalState', {}).get('name', '') for dict_ in addresses if dict_.get('federalState')), '')
    plain_dict['addresses_federalStateCode'] = next((dict_.get('federalState', {}).get('code', '') for dict_ in addresses if dict_.get('federalState')), '')
    plain_dict['addresses_poBox'] = next((dict_.get('poBox', '') for dict_ in addresses), '')

    phones = json_data.get('phones', [])
    plain_dict['phones_phone'] = [str(dict_['phone']) for dict_ in phones if dict_.get('tech') == 'phone']
    plain_dict['phones_fax'] = [dict_['phone'] for dict_ in phones if dict_.get('tech') == 'fax']

    plain_dict['emails'] = [str(dict_['email']) for dict_ in json_data.get('emails', [])]

    plain_dict['urls'] = [str(dict_['url']) for dict_ in json_data.get('urls', [])]

    plain_dict['geoCodes_latitude'] = next((dict_['latitude'] for dict_ in json_data['geoCodes']), '')
    plain_dict['geoCodes_longitude'] = next((dict_['longitude'] for dict_ in json_data['geoCodes']), '')
    plain_dict['geoCodes_accuracy'] = next((dict_['accuracy'] for dict_ in json_data['geoCodes']), '')

    chains = json_data.get('chains', [])
    plain_dict['chains_giataId'] = [dict_['giataId'] for dict_ in chains]
    plain_dict['chains_names'] = [names_dict['value'] for dict_ in chains if 'names' in dict_ for names_dict in dict_['names'] if names_dict.get('isDefault') and names_dict['isDefault'] == True and names_dict['locale'] == 'en']

    roomTypes = json_data.get('roomTypes', [])
    roomTypesDict = {}
    for dict_ in roomTypes:
        for key_ in dict_.keys():
            if isinstance(dict_.get(key_), dict):
                for key__ in dict_.get(key_).keys():
                    roomTypesDict['_'.join([key_, key__])] = []
            else:
                roomTypesDict[key_] = []

    for dict_ in roomTypes:
        for key_ in roomTypesDict.keys():
            if '_' not in key_:
                roomTypesDict[key_].append(dict_.get(key_))
            elif isinstance(dict_.get(key_), dict):
                roomTypesDict[key_].append(dict_.get(key_.split('_')[0]).get(key_.split('_')[1]))
            else:
                roomTypesDict[key_].append(dict_.get(key_))

    for subKey in roomTypesDict.keys():
        plain_dict['_'.join(['roomTypes', subKey])] = roomTypesDict[subKey]

    images = json_data.get('images', [])
    imagesDict = {}
    for dict_ in images:
        for key_ in dict_.keys():
            if isinstance(dict_.get(key_), dict) and key_ != 'sizes':
                for key__ in dict_.get(key_).keys():
                    imagesDict['_'.join([key_, key__])] = []
            else:
                imagesDict[key_] = []
        imagesDict['herf'] = []

    for dict_ in images:
        hrefs = []
        for key_ in imagesDict.keys():
            if isinstance(dict_.get(key_), dict) and key_ == 'sizes':
                imagesDict[key_].append(list(dict_[key_].keys()))
                imgDict = dict_.get(key_)
                for key__ in imgDict.keys():
                    hrefs.append(imgDict[key__]['href'])
            elif key_ == 'herf':
                imagesDict[key_].append(hrefs)
            else:
                imagesDict[key_].append(dict_.get(key_))

    for subKey in imagesDict.keys():
        plain_dict['_'.join(['images', subKey])] = imagesDict[subKey]

    facts = json_data.get('facts', {})
    dataDict = {'factDefId': [], 'attributes_attributeDefId': [], 'attributes_value': [], 'attributes_unitDefId': []}

    for key_0, list_items in facts.items():
        for list_item in list_items:
            dataDict_ = {'factDefId': '', 'attributes_attributeDefId': '', 'attributes_value': '', 'attributes_unitDefId': ''}
            for key_1, value_1 in list_item.items():
                if isinstance(value_1, str):
                    dataDict_[key_1] = value_1
                elif isinstance(value_1, dict):
                    for key_2, value_2 in value_1.items():
                        if isinstance(value_2, str):
                            jointKey = '_'.join([key_1, key_2])
                            dataDict_[jointKey] = value_2
                        elif isinstance(value_2, dict):
                            for key_3, value_3 in value_2.items():
                                jointKey = '_'.join([key_1, key_3])
                                dataDict_[jointKey] = value_3
            for key in dataDict.keys():
                if dataDict_[key]:
                    dataDict[key].append(str(dataDict_[key]))
                else:
                    dataDict[key].append(None)

    for subKey in dataDict.keys():
        plain_dict['_'.join(['facts', subKey])] = dataDict[subKey]

    textsData = {}
    for data_ in json_data['texts']['en']['sections']:
        for key_, value_ in data_.items():
            if key_ == 'title':
                key = value_
            else:
                textsData['_'.join(['texts', 'en', key_])] = value_

    for data_ in json_data['texts']['en-US']['sections']:
        for key_, value_ in data_.items():
            if key_ == 'title':
                key = value_
            else:
                textsData['_'.join(['texts', 'en-US', key_])] = value_

    for subKey in textsData.keys():
        plain_dict[subKey] = textsData[subKey]

    output.append(plain_dict)

print('time to execute: ', time.time()-start)

output_df = pd.DataFrame(output, columns=dfKeys)
output_df.to_csv(writeCSV, index=False)
