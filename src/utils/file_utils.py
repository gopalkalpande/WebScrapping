"""
File utility functions for the hotel data extraction tool.
"""

import os
import json
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

from ..config.settings import config
from .logger import get_logger

logger = get_logger(__name__)


def ensure_directory(directory_path: str) -> None:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        directory_path: Path to the directory
    """
    Path(directory_path).mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {directory_path}")


def get_json_files(directory_path: str) -> List[str]:
    """
    Get all JSON files in a directory.
    
    Args:
        directory_path: Path to the directory
        
    Returns:
        List of JSON file paths
    """
    if not os.path.exists(directory_path):
        logger.warning(f"Directory does not exist: {directory_path}")
        return []
    
    json_files = []
    for file in os.listdir(directory_path):
        if file.endswith('.json'):
            json_files.append(os.path.join(directory_path, file))
    
    logger.info(f"Found {len(json_files)} JSON files in {directory_path}")
    return json_files


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load JSON data from a file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        JSON data as dictionary
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.debug(f"Successfully loaded JSON file: {file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {file_path}: {e}")
        raise


def save_json_file(data: Dict[str, Any], file_path: str) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        file_path: Path to the output file
    """
    ensure_directory(os.path.dirname(file_path))
    
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        logger.debug(f"Successfully saved JSON file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save JSON file {file_path}: {e}")
        raise


def save_csv_file(data: pd.DataFrame, file_path: str, **kwargs) -> None:
    """
    Save DataFrame to CSV file.
    
    Args:
        data: DataFrame to save
        file_path: Path to the output file
        **kwargs: Additional arguments for pandas to_csv
    """
    ensure_directory(os.path.dirname(file_path))
    
    try:
        # Get configuration values
        encoding = kwargs.get('encoding', config.get_output_encoding())
        index = kwargs.get('index', config.should_include_index())
        
        data.to_csv(
            file_path,
            encoding=encoding,
            index=index,
            **kwargs
        )
        logger.info(f"Successfully saved CSV file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save CSV file {file_path}: {e}")
        raise


def backup_file(file_path: str, backup_dir: str = None) -> str:
    """
    Create a backup of a file.
    
    Args:
        file_path: Path to the file to backup
        backup_dir: Directory to store backup (defaults to temp directory)
        
    Returns:
        Path to the backup file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    backup_dir = backup_dir or config.get_temp_dir()
    ensure_directory(backup_dir)
    
    filename = os.path.basename(file_path)
    backup_path = os.path.join(backup_dir, f"backup_{filename}")
    
    shutil.copy2(file_path, backup_path)
    logger.info(f"Created backup: {backup_path}")
    
    return backup_path


def move_failed_file(file_path: str, failed_dir: str = None) -> str:
    """
    Move a failed file to the failed files directory.
    
    Args:
        file_path: Path to the failed file
        failed_dir: Directory to move failed files to
        
    Returns:
        Path to the moved file
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    failed_dir = failed_dir or config.get_failed_dir()
    ensure_directory(failed_dir)
    
    filename = os.path.basename(file_path)
    failed_path = os.path.join(failed_dir, filename)
    
    # If file already exists, add timestamp
    if os.path.exists(failed_path):
        import time
        timestamp = int(time.time())
        name, ext = os.path.splitext(filename)
        failed_path = os.path.join(failed_dir, f"{name}_{timestamp}{ext}")
    
    shutil.move(file_path, failed_path)
    logger.info(f"Moved failed file to: {failed_path}")
    
    return failed_path


def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in bytes
    """
    try:
        return os.path.getsize(file_path)
    except OSError as e:
        logger.error(f"Failed to get file size for {file_path}: {e}")
        return 0


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"


def clean_temp_files(temp_dir: str = None) -> None:
    """
    Clean temporary files from the temp directory.
    
    Args:
        temp_dir: Temporary directory to clean
    """
    temp_dir = temp_dir or config.get_temp_dir()
    
    if not os.path.exists(temp_dir):
        return
    
    try:
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logger.debug(f"Removed temp file: {file_path}")
        logger.info(f"Cleaned temporary directory: {temp_dir}")
    except Exception as e:
        logger.error(f"Failed to clean temp directory {temp_dir}: {e}")


def validate_file_path(file_path: str, check_exists: bool = True) -> bool:
    """
    Validate if a file path is valid.
    
    Args:
        file_path: Path to validate
        check_exists: Whether to check if file exists
        
    Returns:
        True if valid, False otherwise
    """
    try:
        # Check if path is valid
        Path(file_path)
        
        # Check if file exists if required
        if check_exists and not os.path.exists(file_path):
            logger.warning(f"File does not exist: {file_path}")
            return False
        
        return True
    except Exception as e:
        logger.error(f"Invalid file path {file_path}: {e}")
        return False


def get_file_extension(file_path: str) -> str:
    """
    Get file extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File extension (including the dot)
    """
    return os.path.splitext(file_path)[1].lower()


def is_json_file(file_path: str) -> bool:
    """
    Check if file is a JSON file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if JSON file, False otherwise
    """
    return get_file_extension(file_path) == '.json'


def is_csv_file(file_path: str) -> bool:
    """
    Check if file is a CSV file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if CSV file, False otherwise
    """
    return get_file_extension(file_path) == '.csv' 