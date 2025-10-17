# 🏠 Renters Insurance Data Extractor

A powerful web application for automatically extracting data from renters insurance documents using OCR technology. Supports 18+ major insurance companies with intelligent company detection and coordinate-based extraction.

## ✨ Features

- **Multi-Company Support**: Works with 18+ major insurance providers
- **Automatic Company Detection**: AI-powered company identification
- **Coordinate-Based Extraction**: Precise data extraction using template matching
- **Multiple Export Formats**: Excel, CSV, and JSON export options
- **Data Validation**: Built-in validation for required fields
- **History Tracking**: SQLite database for record management
- **Drag & Drop Interface**: User-friendly web interface
- **Docker Support**: Easy deployment with Docker

## 🏢 Supported Insurance Companies

- State Farm
- Allstate
- Progressive
- USAA
- Nationwide
- Travelers
- Liberty Mutual
- Farmers Insurance
- GEICO
- American Family
- Erie Insurance
- Amica Mutual
- CSAA Insurance Group
- Chubb
- The Hartford
- COUNTRY Financial
- Lemonade
- The Hanover

## 📋 Prerequisites

- Python 3.10+
- Tesseract OCR
- OpenCV
- Flask

### Installing Tesseract OCR

**Windows:**
```bash
# Download and install from:
https://github.com/UB-Mannheim/tesseract/wiki
# Default path: C:\Program Files\Tesseract-OCR\tesseract.exe
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng
```

**macOS:**
```bash
brew install tesseract
```

## 🚀 Installation

### Method 1: Local Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd renters-insurance-extractor
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
```
http://localhost:5000
```

### Method 2: Docker Installation

1. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

2. **Access the application**
```
http://localhost:5000
```

## 📁 Project Structure

```
PROJECT ROOT/
├── app.py                      # Flask application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
│
├── core/                      # Core functionality
│   ├── image_processor.py     # Image preprocessing
│   ├── ocr_engine.py          # OCR text extraction
│   ├── company_detector.py    # Company identification
│   ├── template_manager.py    # Coordinate templates
│   └── exporter.py            # Data export utilities
│
├── extractors/                # Company-specific extractors
│   ├── base_extractor.py      # Base extractor class
│   ├── nationwide_extractor.py
│   ├── state_farm_extractor.py
│   ├── generic_extractor.py
│   └── [other extractors...]
│
├── models/                    # Data models
│   ├── database.py            # Database models
│   └── schemas.py             # Pydantic schemas
│
├── api/                       # API routes
│   └── routes.py              # Flask API endpoints
│
├── static/                    # Frontend assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
└── templates/                 # HTML templates
    └── index.html
```

## 🔧 Configuration

### Environment Variables

Edit `.env` file:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=False

# Upload Directories
UPLOAD_FOLDER=uploads
EXPORT_FOLDER=exports

# Tesseract Configuration
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

# Database
DATABASE_URL=sqlite:///renters_data.db

# OCR Settings
ZOOM_FACTOR=2
COMPANY_DETECTION_THRESHOLD=0.7
```

## 📖 Usage

### Web Interface

1. **Upload Document**
   - Drag and drop an insurance document
   - Or click to browse and select a file
   - Supported formats: PNG, JPG, JPEG, PDF, TIFF, BMP

2. **View Results**
   - Company automatically detected
   - All fields extracted and displayed
   - Validation messages shown

3. **Export Data**
   - Choose Excel, CSV, or JSON format
   - Download extracted data

### API Endpoints

#### Upload and Extract
```bash
POST /api/upload
Content-Type: multipart/form-data

Response:
{
  "success": true,
  "record_id": 1,
  "company": "nationwide",
  "confidence": 0.95,
  "data": {...},
  "is_valid": true,
  "validation_errors": [],
  "processing_time": 2.3
}
```

#### Get All Records
```bash
GET /api/records?limit=100&offset=0

Response:
{
  "success": true,
  "count": 10,
  "records": [...]
}
```

#### Get Single Record
```bash
GET /api/records/<record_id>

Response:
{
  "success": true,
  "record": {...}
}
```

#### Delete Record
```bash
DELETE /api/records/<record_id>

Response:
{
  "success": true,
  "message": "Record deleted successfully"
}
```

#### Export Data
```bash
POST /api/export/<format>
Content-Type: application/json

Body:
{
  "data": [...]
}

Formats: excel, csv, json
```

#### Search Records
```bash
GET /api/search?company=Nationwide&policy=ABC123

Response:
{
  "success": true,
  "count": 5,
  "records": [...]
}
```

## 🎯 Adding New Insurance Companies

1. **Create new extractor file**
```python
# extractors/new_company_extractor.py
from extractors.base_extractor import BaseExtractor

class NewCompanyExtractor(BaseExtractor):
    def get_company_name(self):
        return 'new_company'
    
    def post_process(self, data):
        # Custom processing
        return data
```

2. **Add template coordinates**
```python
# In core/template_manager.py
'new_company': {
    'insurance_company': (x, y, w, h),
    'policy_number': (x, y, w, h),
    # ... other fields
}
```

3. **Update company detector**
```python
# In core/company_detector.py
self.company_keywords = {
    'new_company': ['new company', 'newco'],
    # ...
}
```

## 🔍 How It Works

1. **Image Upload**: User uploads insurance document
2. **Company Detection**: System analyzes header region to identify company
3. **Template Selection**: Appropriate coordinate template is loaded
4. **Image Processing**: Document is preprocessed (zoom, grayscale, threshold)
5. **OCR Extraction**: Tesseract extracts text from defined regions
6. **Data Cleaning**: Text is cleaned and formatted by field type
7. **Validation**: Required fields are validated
8. **Storage**: Data is saved to database
9. **Export**: User can export in multiple formats

## 🛠️ Troubleshooting

### Tesseract Not Found
```bash
# Check Tesseract installation
tesseract --version

# Update TESSERACT_CMD in .env with correct path
```

### Low Extraction Accuracy
- Ensure image quality is high (300+ DPI recommended)
- Adjust ZOOM_FACTOR in config
- Check coordinate templates for specific company
- Verify document is not skewed

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📊 Performance Tips

- Use high-quality scans (300+ DPI)
- Ensure documents are properly aligned
- Adjust zoom factor for better OCR results
- Fine-tune coordinate templates per company

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Write/update tests
5. Submit a pull request

## 📄 License

MIT License - feel free to use this project for commercial purposes.

## 🐛 Known Issues

- PDF support requires additional dependencies
- Some handwritten documents may not extract well
- Coordinates may need adjustment for document variations

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Submit a pull request
- Contact the maintainer

## 🚀 Roadmap

- [ ] PDF native support
- [ ] Batch processing
- [ ] API authentication
- [ ] Cloud storage integration
- [ ] Machine learning-based field detection
- [ ] Mobile app
- [ ] Multi-language support

---

Built with ❤️ using Python, Flask, OpenCV, and Tesseract OCR