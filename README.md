# custom-insurance-scanner
It extracts insurance data using exact coordinates within the documents, saving huge costs from using document intelligence in cloud services.

"""
# Enterprise Renters Insurance Data Extraction System

## Features
- ✅ 18 major US insurance companies supported
- ✅ Auto-company detection
- ✅ OpenCV image preprocessing
- ✅ Template-based extraction (95%+ accuracy)
- ✅ Generic fallback for unknown companies
- ✅ Excel/CSV/JSON export
- ✅ Human review workflow
- ✅ Database tracking

## Installation

### Prerequisites
```bash
# macOS
brew install tesseract poppler

# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils

# Windows
# Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
# Download Poppler: http://blog.alivate.com.au/poppler-windows/
```

### Setup
```bash
# Clone repository
git clone <your-repo>
cd renters-insurance-enterprise

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Run
python app.py
```

### Docker
```bash
docker-compose up -d
```

## Usage

### Web Interface
1. Open http://localhost:8000
2. Upload PDF or image
3. View extracted data
4. Export to Excel/CSV

### API
```bash
# Upload document
curl -X POST -F "file=@insurance.pdf" http://localhost:8000/api/upload

# Get records
curl http://localhost:8000/api/records

# Export to Excel
curl -X POST http://localhost:8000/api/export \\
  -H "Content-Type: application/json" \\
  -d '{"format":"excel","record_ids":[1,2,3]}'
```

## Supported Companies
State Farm, Allstate, Progressive, USAA, Nationwide, Travelers, 
Liberty Mutual, Farmers, GEICO, American Family, Erie, Amica, 
CSAA/AAA, Chubb, Hartford, Country Financial, Lemonade, Hanover

## Architecture
```
Document → OCR → Company Detection → Template Selection → 
Data Extraction → Validation → Database → Export
```

## Accuracy
- Known companies: 95%+
- Unknown companies: 70-85%
- Low confidence: Flagged for review

## Contributing
Add new company extractors in `extractors/` directory following 
the pattern in `state_farm_extractor.py`
"""