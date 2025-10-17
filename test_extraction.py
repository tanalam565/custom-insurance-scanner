"""
Test script for renters insurance data extraction
Usage: python test_extraction.py path/to/image.png
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.image_processor import ImageProcessor
from core.ocr_engine import OCREngine
from core.company_detector import CompanyDetector
from core.template_manager import TemplateManager
from extractors.nationwide_extractor import NationwideExtractor
from extractors.state_farm_extractor import StateFarmExtractor
from extractors.generic_extractor import GenericExtractor
import time

def get_extractor(company_name):
    """Get the appropriate extractor for a company"""
    extractors = {
        'nationwide': NationwideExtractor(),
        'state_farm': StateFarmExtractor(),
        'generic': GenericExtractor()
    }
    return extractors.get(company_name, GenericExtractor())

def test_extraction(image_path):
    """Test extraction on a single image"""
    
    print("=" * 70)
    print("Renters Insurance Data Extraction Test")
    print("=" * 70)
    print()
    
    # Check if file exists
    if not Path(image_path).exists():
        print(f"❌ Error: File not found: {image_path}")
        return False
    
    print(f"📄 Testing file: {image_path}")
    print()
    
    try:
        # Initialize components
        print("Initializing components...")
        processor = ImageProcessor()
        detector = CompanyDetector()
        
        # Load image
        print("Loading image...")
        img = processor.load_image(image_path)
        print(f"✓ Image loaded: {img.shape}")
        print()
        
        # Detect company
        print("Detecting insurance company...")
        start_time = time.time()
        company_name, confidence = detector.detect_company(img)
        detection_time = time.time() - start_time
        
        print(f"✓ Company detected: {company_name}")
        print(f"  Confidence: {confidence:.2%}")
        print(f"  Detection time: {detection_time:.2f}s")
        print()
        
        # Get extractor
        print("Loading extractor...")
        extractor = get_extractor(company_name)
        print(f"✓ Using {extractor.__class__.__name__}")
        print()
        
        # Extract data
        print("Extracting data...")
        start_time = time.time()
        data = extractor.extract_all_fields(img)
        extraction_time = time.time() - start_time
        
        print(f"✓ Extraction completed in {extraction_time:.2f}s")
        print()
        
        # Post-process
        print("Post-processing data...")
        data = extractor.post_process(data)
        print("✓ Post-processing completed")
        print()
        
        # Validate
        print("Validating extraction...")
        is_valid, errors = extractor.validate_extraction(data)
        
        if is_valid:
            print("✓ Validation passed")
        else:
            print("⚠ Validation warnings:")
            for error in errors:
                print(f"  - {error}")
        print()
        
        # Display results
        print("=" * 70)
        print("EXTRACTED DATA")
        print("=" * 70)
        print()
        
        field_labels = {
            'insurance_company': 'Insurance Company',
            'policy_number': 'Policy Number',
            'date_prepared': 'Date Prepared',
            'insurer_name': 'Insurer Name',
            'insurer_address': 'Insurer Address',
            'insurer_city_state': 'City, State',
            'insurance_amount': 'Insurance Amount',
            'property_address': 'Property Address',
            'effective_date': 'Effective Date',
            'expiration_date': 'Expiration Date'
        }
        
        for field, label in field_labels.items():
            value = data.get(field, 'N/A')
            print(f"{label:.<30} {value}")
        
        print()
        
        # Custom fields
        custom_fields = {k: v for k, v in data.items() 
                        if k not in field_labels}
        if custom_fields:
            print("Custom Fields:")
            for field, value in custom_fields.items():
                print(f"  {field}: {value}")
            print()
        
        # Summary
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Total processing time: {detection_time + extraction_time:.2f}s")
        print(f"Fields extracted: {len([v for v in data.values() if v])}")
        print(f"Validation status: {'✓ Passed' if is_valid else '⚠ Warnings'}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    
    if len(sys.argv) < 2:
        print("Usage: python test_extraction.py <image_path>")
        print()
        print("Example:")
        print("  python test_extraction.py applicationImage/Nationwide_WIP.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    success = test_extraction(image_path)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()