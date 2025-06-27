# Hotel Data Extraction Tool

A Python-based web scraping and data extraction tool designed to process hotel information from JSON files and convert them into structured CSV format.

## 🚀 Features

- **JSON to CSV Conversion**: Extracts hotel data from JSON files and converts to structured CSV format
- **Batch Processing**: Process multiple JSON files in a single run
- **Data Validation**: Includes JSON schema validation and data integrity checks
- **Flexible Configuration**: Configurable extraction parameters and output formats
- **Error Handling**: Robust error handling for malformed data

## 📋 Prerequisites

- Python 3.8+
- Required Python packages (see `requirements.txt`)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd WebScrapping
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
WebScrapping/
├── src/                    # Source code
│   ├── extractors/         # Data extraction modules
│   ├── utils/             # Utility functions
│   └── config/            # Configuration files
├── data/                  # Data directories
│   ├── inputJSONs/        # Input JSON files
│   └── output/            # Output CSV files
├── tests/                 # Test files
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── requirements.txt       # Python dependencies
├── config.yaml           # Configuration file
└── README.md             # This file
```

## 🚀 Usage

### Basic Usage

1. Place your JSON files in the `data/inputJSONs/` directory
2. Run the main extraction script:

```bash
python src/main.py
```

### Configuration

Edit `config.yaml` to customize:
- Input/output directories
- Batch processing settings
- Data extraction parameters
- Output format options

### Command Line Options

```bash
# Process all JSON files in input directory
python src/main.py --batch

# Process specific file
python src/main.py --file data/inputJSONs/specific_file.json

# Custom output directory
python src/main.py --output data/custom_output/

# Verbose logging
python src/main.py --verbose
```

## 📊 Data Schema

The tool extracts the following hotel information:
- Basic hotel details (ID, names, source)
- Location information (city, country, addresses)
- Contact details (phones, emails, URLs)
- Geographic coordinates
- Ratings and reviews
- Room types and amenities
- Images and media
- Chain affiliations

## 🧪 Testing

Run tests with:
```bash
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Missing dependencies**: Ensure all packages in `requirements.txt` are installed
2. **File permissions**: Check read/write permissions for data directories
3. **Memory issues**: For large datasets, consider processing in smaller batches

### Getting Help

- Check the [Issues](../../issues) page for known problems
- Create a new issue for bugs or feature requests
- Review the documentation in the `docs/` directory

## 📈 Performance

- Processing speed: ~100-500 JSON files per minute (depending on file size)
- Memory usage: Optimized for large datasets
- Output format: CSV with UTF-8 encoding

## 🔄 Version History

- **v1.0.0**: Initial release with basic JSON to CSV conversion
- **v1.1.0**: Added batch processing and error handling
- **v1.2.0**: Improved data validation and configuration management 