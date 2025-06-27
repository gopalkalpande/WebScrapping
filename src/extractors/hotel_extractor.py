"""
Hotel data extraction module.

This module contains the main logic for extracting hotel information from JSON files
and converting them to structured CSV format.
"""

import os
import json
import pandas as pd
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..config.settings import config
from ..utils.logger import get_logger
from ..utils.file_utils import load_json_file, save_csv_file, move_failed_file

logger = get_logger(__name__)


class HotelDataExtractor:
    """
    Main class for extracting hotel data from JSON files.
    """
    
    def __init__(self):
        """Initialize the hotel data extractor."""
        self.df_keys = [
            'fileId', 'giataId', 'names_locale', 'names_value', 'country_code', 
            'source', 'country_locale', 'country_value', 'destination_giataId', 
            'destination_locale', 'destination_value', 'addresses_cityName', 
            'addresses_federalState', 'addresses_federalStateCode', 
            'addresses_federalStateName', 'addresses_poBox', 'addresses_street', 
            'addresses_streetNum', 'addresses_value_addressLines', 'addresses_zip', 
            'chains_giataId', 'chains_names', 'city_giataId', 'city_locale', 
            'city_value', 'emails', 'urls', 'facts_attributes_attributeDefId', 
            'facts_attributes_unitDefId', 'facts_attributes_value', 
            'facts_factDefId', 'geoCodes_accuracy', 'geoCodes_latitude', 
            'geoCodes_longitude', 'images_baseName', 'images_herf', 
            'images_heroImage', 'images_id', 'images_lastUpdate', 
            'images_motifType', 'images_sizes', 'phones_fax', 'phones_phone', 
            'ratings_value', 'roomTypes_category', 
            'roomTypes_categoryInformation_attributeDefId', 
            'roomTypes_categoryInformation_name', 'roomTypes_code', 
            'roomTypes_imageRelations', 'roomTypes_name', 'roomTypes_type', 
            'roomTypes_typeInformation_attributeDefId', 
            'roomTypes_typeInformation_name', 'roomTypes_variantId', 
            'roomTypes_view', 'roomTypes_viewInformation_attributeDefId', 
            'roomTypes_viewInformation_name', 'texts_en_Facilities', 
            'texts_en_Location', 'texts_en_Meals', 'texts_en_Payment', 
            'texts_en_Rooms', 'texts_en_Sports/Entertainment', 
            'texts_en-US_Facilities', 'texts_en-US_Location', 'texts_en-US_Meals', 
            'texts_en-US_Payment', 'texts_en-US_Rooms', 
            'texts_en-US_Sports/Entertainment', 'variantGroups'
        ]
        
        self.output_df = pd.DataFrame(columns=self.df_keys)
        self.default_locale = config.get_default_locale()
        self.default_only = config.get('extraction.default_only', True)
    
    def extract_hotel_data(self, json_data: Dict[str, Any], file_id: str) -> Dict[str, Any]:
        """
        Extract hotel data from JSON and convert to flat dictionary.
        
        Args:
            json_data: Hotel data in JSON format
            file_id: Identifier for the source file
            
        Returns:
            Extracted data as flat dictionary
        """
        try:
            plain_dict = {'fileId': file_id}
            
            # Extract basic information
            plain_dict.update(self._extract_basic_info(json_data))
            
            # Extract location information
            plain_dict.update(self._extract_location_info(json_data))
            
            # Extract contact information
            plain_dict.update(self._extract_contact_info(json_data))
            
            # Extract geographic information
            plain_dict.update(self._extract_geo_info(json_data))
            
            # Extract chain information
            plain_dict.update(self._extract_chain_info(json_data))
            
            # Extract room types
            plain_dict.update(self._extract_room_types(json_data))
            
            # Extract images
            plain_dict.update(self._extract_images(json_data))
            
            # Extract facts
            plain_dict.update(self._extract_facts(json_data))
            
            # Extract texts
            plain_dict.update(self._extract_texts(json_data))
            
            # Extract variant groups
            plain_dict.update(self._extract_variant_groups(json_data))
            
            return plain_dict
            
        except Exception as e:
            logger.error(f"Error extracting data from file {file_id}: {e}")
            raise
    
    def _extract_basic_info(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract basic hotel information."""
        plain_dict = {}
        
        # Giata ID
        plain_dict['giataId'] = json_data.get('giataId')
        
        # Names
        plain_dict['names_value'] = str
        plain_dict['names_locale'] = str
        
        for name_dict in json_data.get('names', []):
            if not self.default_only or name_dict.get('isDefault', False):
                plain_dict['names_value'] = name_dict.get('value')
                plain_dict['names_locale'] = name_dict.get('locale')
                if self.default_only:
                    break
        
        # Source
        plain_dict['source'] = json_data.get('source')
        
        # Ratings
        for rating_dict in json_data.get('ratings', []):
            if not self.default_only or rating_dict.get('isDefault', False):
                plain_dict['ratings_value'] = rating_dict.get('value')
                if self.default_only:
                    break
        
        return plain_dict
    
    def _extract_location_info(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract location information."""
        plain_dict = {}
        
        # City information
        city_data = json_data.get('city', {})
        plain_dict['city_giataId'] = city_data.get('giataId')
        
        for name_dict in city_data.get('names', []):
            if not self.default_only or name_dict.get('isDefault', False):
                plain_dict['city_value'] = name_dict.get('value')
                plain_dict['city_locale'] = name_dict.get('locale')
                if self.default_only:
                    break
        
        # Destination information
        dest_data = json_data.get('destination', {})
        plain_dict['destination_giataId'] = dest_data.get('giataId')
        
        for name_dict in dest_data.get('names', []):
            if not self.default_only or name_dict.get('isDefault', False):
                plain_dict['destination_value'] = name_dict.get('value')
                plain_dict['destination_locale'] = name_dict.get('locale')
                if self.default_only:
                    break
        
        # Country information
        country_data = json_data.get('country', {})
        plain_dict['country_code'] = country_data.get('code')
        
        for name_dict in country_data.get('names', []):
            if not self.default_only or name_dict.get('isDefault', False):
                plain_dict['country_value'] = name_dict.get('value')
                plain_dict['country_locale'] = name_dict.get('locale')
                if self.default_only:
                    break
        
        # Addresses
        addresses = json_data.get('addresses', [])
        if addresses:
            addr = addresses[0]  # Take first address
            plain_dict['addresses_value_addressLines'] = ', '.join(addr.get('addressLines', []))
            plain_dict['addresses_street'] = addr.get('street')
            plain_dict['addresses_streetNum'] = addr.get('streetNum')
            plain_dict['addresses_zip'] = addr.get('zip')
            plain_dict['addresses_cityName'] = addr.get('cityName')
            plain_dict['addresses_poBox'] = addr.get('poBox')
            
            federal_state = addr.get('federalState', {})
            if federal_state:
                plain_dict['addresses_federalStateName'] = federal_state.get('name')
                plain_dict['addresses_federalStateCode'] = federal_state.get('code')
        
        return plain_dict
    
    def _extract_contact_info(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract contact information."""
        plain_dict = {}
        
        # Phones
        phones = json_data.get('phones', [])
        phone_list = []
        fax_list = []
        
        for phone_dict in phones:
            if phone_dict.get('tech') == 'phone':
                phone_list.append(str(phone_dict.get('phone')))
            else:
                fax_list.append(phone_dict.get('phone'))
        
        plain_dict['phones_phone'] = phone_list
        plain_dict['phones_fax'] = fax_list
        
        # Emails
        emails = json_data.get('emails', [])
        email_list = [str(email_dict.get('email')) for email_dict in emails]
        plain_dict['emails'] = email_list
        
        # URLs
        urls = json_data.get('urls', [])
        url_list = [str(url_dict.get('url')) for url_dict in urls]
        plain_dict['urls'] = url_list
        
        return plain_dict
    
    def _extract_geo_info(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract geographic information."""
        plain_dict = {}
        
        geocodes = json_data.get('geoCodes', [])
        if geocodes:
            geo = geocodes[0]  # Take first geocode
            plain_dict['geoCodes_latitude'] = geo.get('latitude')
            plain_dict['geoCodes_longitude'] = geo.get('longitude')
            plain_dict['geoCodes_accuracy'] = geo.get('accuracy')
        
        return plain_dict
    
    def _extract_chain_info(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract chain information."""
        plain_dict = {}
        
        chains = json_data.get('chains', [])
        giata_ids = []
        names = []
        
        for chain_dict in chains:
            giata_ids.append(chain_dict.get('giataId'))
            
            for name_dict in chain_dict.get('names', []):
                if (not self.default_only or name_dict.get('isDefault', False)) and \
                   name_dict.get('locale') == self.default_locale:
                    names.append(name_dict.get('value'))
                    if self.default_only:
                        break
        
        plain_dict['chains_giataId'] = giata_ids
        plain_dict['chains_names'] = names
        
        return plain_dict
    
    def _extract_room_types(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract room type information."""
        plain_dict = {}
        
        room_types = json_data.get('roomTypes', [])
        if room_types:
            room = room_types[0]  # Take first room type
            plain_dict['roomTypes_category'] = room.get('category')
            plain_dict['roomTypes_code'] = room.get('code')
            plain_dict['roomTypes_name'] = room.get('name')
            plain_dict['roomTypes_type'] = room.get('type')
            plain_dict['roomTypes_variantId'] = room.get('variantId')
            plain_dict['roomTypes_view'] = room.get('view')
            plain_dict['roomTypes_imageRelations'] = room.get('imageRelations')
            
            # Category information
            cat_info = room.get('categoryInformation', {})
            plain_dict['roomTypes_categoryInformation_attributeDefId'] = cat_info.get('attributeDefId')
            plain_dict['roomTypes_categoryInformation_name'] = cat_info.get('name')
            
            # Type information
            type_info = room.get('typeInformation', {})
            plain_dict['roomTypes_typeInformation_attributeDefId'] = type_info.get('attributeDefId')
            plain_dict['roomTypes_typeInformation_name'] = type_info.get('name')
            
            # View information
            view_info = room.get('viewInformation', {})
            plain_dict['roomTypes_viewInformation_attributeDefId'] = view_info.get('attributeDefId')
            plain_dict['roomTypes_viewInformation_name'] = view_info.get('name')
        
        return plain_dict
    
    def _extract_images(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract image information."""
        plain_dict = {}
        
        images = json_data.get('images', [])
        if images:
            img = images[0]  # Take first image
            plain_dict['images_baseName'] = img.get('baseName')
            plain_dict['images_herf'] = img.get('herf')
            plain_dict['images_heroImage'] = img.get('heroImage')
            plain_dict['images_id'] = img.get('id')
            plain_dict['images_lastUpdate'] = img.get('lastUpdate')
            plain_dict['images_motifType'] = img.get('motifType')
            plain_dict['images_sizes'] = img.get('sizes')
        
        return plain_dict
    
    def _extract_facts(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract facts information."""
        plain_dict = {}
        
        facts = json_data.get('facts', [])
        if facts:
            fact = facts[0]  # Take first fact
            plain_dict['facts_factDefId'] = fact.get('factDefId')
            
            attributes = fact.get('attributes', [])
            if attributes:
                attr = attributes[0]  # Take first attribute
                plain_dict['facts_attributes_attributeDefId'] = attr.get('attributeDefId')
                plain_dict['facts_attributes_unitDefId'] = attr.get('unitDefId')
                plain_dict['facts_attributes_value'] = attr.get('value')
        
        return plain_dict
    
    def _extract_texts(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract text information."""
        plain_dict = {}
        
        texts = json_data.get('texts', {})
        
        # English texts
        en_texts = texts.get('en', {})
        plain_dict['texts_en_Facilities'] = en_texts.get('Facilities')
        plain_dict['texts_en_Location'] = en_texts.get('Location')
        plain_dict['texts_en_Meals'] = en_texts.get('Meals')
        plain_dict['texts_en_Payment'] = en_texts.get('Payment')
        plain_dict['texts_en_Rooms'] = en_texts.get('Rooms')
        plain_dict['texts_en_Sports/Entertainment'] = en_texts.get('Sports/Entertainment')
        
        # US English texts
        en_us_texts = texts.get('en-US', {})
        plain_dict['texts_en-US_Facilities'] = en_us_texts.get('Facilities')
        plain_dict['texts_en-US_Location'] = en_us_texts.get('Location')
        plain_dict['texts_en-US_Meals'] = en_us_texts.get('Meals')
        plain_dict['texts_en-US_Payment'] = en_us_texts.get('Payment')
        plain_dict['texts_en-US_Rooms'] = en_us_texts.get('Rooms')
        plain_dict['texts_en-US_Sports/Entertainment'] = en_us_texts.get('Sports/Entertainment')
        
        return plain_dict
    
    def _extract_variant_groups(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract variant groups information."""
        plain_dict = {}
        
        variant_groups = json_data.get('variantGroups', [])
        plain_dict['variantGroups'] = variant_groups
        
        return plain_dict
    
    def process_single_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Process a single JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Extracted data dictionary or None if failed
        """
        try:
            file_id = os.path.basename(file_path)
            logger.info(f"Processing file: {file_id}")
            
            json_data = load_json_file(file_path)
            extracted_data = self.extract_hotel_data(json_data, file_id)
            
            logger.info(f"Successfully processed file: {file_id}")
            return extracted_data
            
        except Exception as e:
            logger.error(f"Failed to process file {file_path}: {e}")
            
            if config.should_save_failed_files():
                try:
                    move_failed_file(file_path)
                except Exception as move_error:
                    logger.error(f"Failed to move failed file {file_path}: {move_error}")
            
            return None
    
    def process_batch(self, file_paths: List[str]) -> pd.DataFrame:
        """
        Process multiple JSON files in batch.
        
        Args:
            file_paths: List of JSON file paths
            
        Returns:
            DataFrame with extracted data
        """
        results = []
        total_files = len(file_paths)
        
        logger.info(f"Starting batch processing of {total_files} files")
        
        for i, file_path in enumerate(file_paths, 1):
            logger.info(f"Processing file {i}/{total_files}: {os.path.basename(file_path)}")
            
            result = self.process_single_file(file_path)
            if result:
                results.append(result)
            
            # Log progress
            if i % 10 == 0 or i == total_files:
                logger.info(f"Processed {i}/{total_files} files successfully")
        
        # Create DataFrame
        if results:
            df = pd.DataFrame(results)
            logger.info(f"Successfully processed {len(results)} out of {total_files} files")
            return df
        else:
            logger.warning("No files were processed successfully")
            return pd.DataFrame(columns=self.df_keys)
    
    def save_results(self, df: pd.DataFrame, output_path: str = None) -> None:
        """
        Save extracted results to CSV file.
        
        Args:
            df: DataFrame with extracted data
            output_path: Output file path
        """
        if output_path is None:
            output_path = os.path.join(config.get_output_dir(), 'extracted_hotels.csv')
        
        save_csv_file(df, output_path)
        logger.info(f"Results saved to: {output_path}") 