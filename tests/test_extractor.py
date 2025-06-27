import os
import sys
import pytest
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from extractors.hotel_extractor import HotelDataExtractor

@pytest.fixture
def sample_json():
    return {
        "giataId": 123,
        "names": [{"value": "Test Hotel", "locale": "en", "isDefault": True}],
        "city": {"giataId": 456, "names": [{"value": "Test City", "locale": "en", "isDefault": True}]},
        "destination": {"giataId": 789, "names": [{"value": "Test Destination", "locale": "en", "isDefault": True}]},
        "country": {"code": "IN", "names": [{"value": "India", "locale": "en", "isDefault": True}]},
        "source": "test_source",
        "ratings": [{"value": 5, "isDefault": True}],
        "addresses": [{"addressLines": ["Line 1", "Line 2"], "street": "Main St", "cityName": "Test City", "zip": "12345", "poBox": "PO123"}],
        "phones": [{"tech": "phone", "phone": "+911234567890"}],
        "emails": [{"email": "test@example.com"}],
        "urls": [{"url": "http://testhotel.com"}],
        "geoCodes": [{"latitude": 12.34, "longitude": 56.78, "accuracy": "high"}],
        "chains": [{"giataId": 111, "names": [{"value": "Test Chain", "locale": "en", "isDefault": True}]}],
        "roomTypes": [{"category": "Deluxe", "code": "DLX", "name": "Deluxe Room", "type": "Room", "variantId": "V1"}],
        "images": [{"baseName": "img1", "herf": "url", "heroImage": True, "id": 1, "lastUpdate": "2023-01-01", "motifType": "exterior", "sizes": ["large"]}],
        "facts": [{"factDefId": 1, "attributes": [{"attributeDefId": 2, "unitDefId": 3, "value": "Yes"}]}],
        "texts": {"en": {"Facilities": "Pool", "Location": "Beach"}},
        "variantGroups": ["Group1"]
    }

def test_extract_hotel_data(sample_json):
    extractor = HotelDataExtractor()
    result = extractor.extract_hotel_data(sample_json, file_id="test.json")
    assert result["giataId"] == 123
    assert result["names_value"] == "Test Hotel"
    assert result["city_value"] == "Test City"
    assert result["country_code"] == "IN"
    assert result["emails"] == ["test@example.com"]
    assert result["phones_phone"] == ["+911234567890"]
    assert result["urls"] == ["http://testhotel.com"]
    assert result["texts_en_Facilities"] == "Pool"
    assert result["variantGroups"] == ["Group1"]
