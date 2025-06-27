"""
Configuration settings for the hotel data extraction tool.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List


class Config:
    """Configuration manager for the application."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize configuration from YAML file."""
        self.config_path = config_path
        self.config = self._load_config()
        self._validate_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            return config
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}")
    
    def _validate_config(self):
        """Validate required configuration sections."""
        required_sections = ['data', 'processing', 'output', 'extraction', 'logging']
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required configuration section: {section}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_data_dir(self, subdir: str = None) -> str:
        """Get data directory path."""
        base_dir = self.get('data.input_dir', './data')
        if subdir:
            return os.path.join(base_dir, subdir)
        return base_dir
    
    def get_output_dir(self) -> str:
        """Get output directory path."""
        return self.get('data.output_dir', './data/output')
    
    def get_temp_dir(self) -> str:
        """Get temporary directory path."""
        return self.get('data.temp_dir', './data/temp')
    
    def get_failed_dir(self) -> str:
        """Get failed files directory path."""
        return self.get('error_handling.failed_files_dir', './data/failed')
    
    def get_cache_dir(self) -> str:
        """Get cache directory path."""
        return self.get('performance.cache_dir', './data/cache')
    
    def get_log_file(self) -> str:
        """Get log file path."""
        return self.get('logging.file', './logs/extraction.log')
    
    def get_extraction_fields(self) -> List[str]:
        """Get list of fields to extract."""
        return self.get('extraction.fields', [])
    
    def get_default_locale(self) -> str:
        """Get default locale for text extraction."""
        return self.get('extraction.default_locale', 'en')
    
    def get_batch_size(self) -> int:
        """Get batch processing size."""
        return self.get('processing.batch_size', 100)
    
    def get_max_workers(self) -> int:
        """Get maximum number of workers."""
        return self.get('processing.max_workers', 4)
    
    def get_timeout(self) -> int:
        """Get processing timeout."""
        return self.get('processing.timeout', 30)
    
    def get_retry_attempts(self) -> int:
        """Get number of retry attempts."""
        return self.get('processing.retry_attempts', 3)
    
    def should_continue_on_error(self) -> bool:
        """Check if processing should continue on error."""
        return self.get('error_handling.continue_on_error', True)
    
    def should_log_errors(self) -> bool:
        """Check if errors should be logged."""
        return self.get('error_handling.log_errors', True)
    
    def should_save_failed_files(self) -> bool:
        """Check if failed files should be saved."""
        return self.get('error_handling.save_failed_files', True)
    
    def get_output_format(self) -> str:
        """Get output format."""
        return self.get('output.format', 'csv')
    
    def get_output_encoding(self) -> str:
        """Get output encoding."""
        return self.get('output.encoding', 'utf-8')
    
    def should_include_index(self) -> bool:
        """Check if index should be included in output."""
        return self.get('output.include_index', False)
    
    def get_compression(self) -> str:
        """Get compression format."""
        return self.get('output.compression')
    
    def get_log_level(self) -> str:
        """Get logging level."""
        return self.get('logging.level', 'INFO')
    
    def get_log_format(self) -> str:
        """Get logging format."""
        return self.get('logging.format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    def get_log_max_size(self) -> str:
        """Get log file max size."""
        return self.get('logging.max_size', '10MB')
    
    def get_log_backup_count(self) -> int:
        """Get log backup count."""
        return self.get('logging.backup_count', 5)
    
    def get_memory_limit(self) -> str:
        """Get memory limit."""
        return self.get('performance.memory_limit', '2GB')
    
    def get_chunk_size(self) -> int:
        """Get chunk size for processing."""
        return self.get('performance.chunk_size', 1000)
    
    def should_cache_results(self) -> bool:
        """Check if results should be cached."""
        return self.get('performance.cache_results', True)
    
    def get_required_fields(self) -> List[str]:
        """Get list of required fields."""
        return self.get('validation.required_fields', [])
    
    def should_validate_schema(self) -> bool:
        """Check if schema validation should be performed."""
        return self.get('validation.schema_validation', True)
    
    def should_validate_data_integrity(self) -> bool:
        """Check if data integrity validation should be performed."""
        return self.get('validation.data_integrity', True)


# Global configuration instance
config = Config() 