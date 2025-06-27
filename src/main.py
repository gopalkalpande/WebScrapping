#!/usr/bin/env python3
"""
Main entry point for the Hotel Data Extraction Tool.

This script provides a command-line interface for extracting hotel data from JSON files
and converting them to structured CSV format.
"""

import os
import sys
import time
import argparse
from pathlib import Path
from typing import List, Optional

# Add src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import config
from utils.logger import setup_logger, get_logger
from utils.file_utils import get_json_files, ensure_directory
from extractors.hotel_extractor import HotelDataExtractor


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Hotel Data Extraction Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py --batch
  python src/main.py --file data/inputJSONs/hotel.json
  python src/main.py --input data/custom_input --output data/custom_output
  python src/main.py --verbose --batch
        """
    )
    
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Process all JSON files in the input directory'
    )
    
    parser.add_argument(
        '--file',
        type=str,
        help='Process a specific JSON file'
    )
    
    parser.add_argument(
        '--input',
        type=str,
        help='Input directory containing JSON files (overrides config)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Output directory for CSV files (overrides config)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be processed without actually processing'
    )
    
    return parser.parse_args()


def validate_environment():
    """Validate that the environment is properly set up."""
    logger = get_logger(__name__)
    
    # Check if required directories exist
    input_dir = config.get_data_dir()
    if not os.path.exists(input_dir):
        logger.warning(f"Input directory does not exist: {input_dir}")
        logger.info("Creating input directory...")
        ensure_directory(input_dir)
    
    # Ensure output directory exists
    output_dir = config.get_output_dir()
    ensure_directory(output_dir)
    
    # Ensure other required directories exist
    ensure_directory(config.get_temp_dir())
    ensure_directory(config.get_failed_dir())
    ensure_directory(config.get_cache_dir())
    
    logger.info("Environment validation completed")


def process_single_file(file_path: str, extractor: HotelDataExtractor) -> bool:
    """
    Process a single JSON file.
    
    Args:
        file_path: Path to the JSON file
        extractor: Hotel data extractor instance
        
    Returns:
        True if successful, False otherwise
    """
    logger = get_logger(__name__)
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return False
    
    if not file_path.endswith('.json'):
        logger.error(f"File is not a JSON file: {file_path}")
        return False
    
    try:
        result = extractor.process_single_file(file_path)
        if result:
            # Save single file result
            df = pd.DataFrame([result])
            output_path = os.path.join(
                config.get_output_dir(),
                f"extracted_{os.path.basename(file_path).replace('.json', '.csv')}"
            )
            extractor.save_results(df, output_path)
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return False


def process_batch(input_dir: str, extractor: HotelDataExtractor) -> bool:
    """
    Process all JSON files in a directory.
    
    Args:
        input_dir: Directory containing JSON files
        extractor: Hotel data extractor instance
        
    Returns:
        True if successful, False otherwise
    """
    logger = get_logger(__name__)
    
    # Get all JSON files
    json_files = get_json_files(input_dir)
    
    if not json_files:
        logger.warning(f"No JSON files found in {input_dir}")
        return False
    
    logger.info(f"Found {len(json_files)} JSON files to process")
    
    try:
        # Process files in batch
        df = extractor.process_batch(json_files)
        
        if not df.empty:
            # Save results
            output_path = os.path.join(config.get_output_dir(), 'extracted_hotels.csv')
            extractor.save_results(df, output_path)
            logger.info(f"Successfully processed {len(df)} hotels")
            return True
        else:
            logger.warning("No data was extracted")
            return False
            
    except Exception as e:
        logger.error(f"Error during batch processing: {e}")
        return False


def main():
    """Main function."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Set up logging
    log_level = "DEBUG" if args.verbose else None
    logger = setup_logger(level=log_level)
    
    logger.info("Starting Hotel Data Extraction Tool")
    
    try:
        # Validate environment
        validate_environment()
        
        # Initialize extractor
        extractor = HotelDataExtractor()
        
        # Determine input directory
        input_dir = args.input or config.get_data_dir()
        
        # Determine output directory
        if args.output:
            config.config['data']['output_dir'] = args.output
            ensure_directory(args.output)
        
        if args.dry_run:
            logger.info("DRY RUN MODE - No files will be processed")
            
            if args.file:
                logger.info(f"Would process file: {args.file}")
            elif args.batch:
                json_files = get_json_files(input_dir)
                logger.info(f"Would process {len(json_files)} files from {input_dir}")
            else:
                logger.info("No processing mode specified")
            
            return 0
        
        # Process files based on arguments
        start_time = time.time()
        
        if args.file:
            # Process single file
            logger.info(f"Processing single file: {args.file}")
            success = process_single_file(args.file, extractor)
            
        elif args.batch:
            # Process all files in directory
            logger.info(f"Processing all JSON files in: {input_dir}")
            success = process_batch(input_dir, extractor)
            
        else:
            # Default: process all files
            logger.info(f"Processing all JSON files in: {input_dir}")
            success = process_batch(input_dir, extractor)
        
        # Log completion
        end_time = time.time()
        duration = end_time - start_time
        
        if success:
            logger.info(f"Processing completed successfully in {duration:.2f} seconds")
            return 0
        else:
            logger.error("Processing failed")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    import pandas as pd
    sys.exit(main()) 