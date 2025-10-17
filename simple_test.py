"""
Simple test script - user specifies company name
Usage: python simple_test.py path/to/document.png company_name
"""
import sys
from pathlib import Path
from core.simple_extractor import extract_from_image, get_available_companies

def test_extraction(image_path, company_name):
    """Test extraction"""
    
    print("=" * 70)
    print("SIMPLE DATA EXTRACTION TEST")
    print("=" * 70)
    print(f"\nFile: {image_path}")
    print(f"Company: {company_name}")
    print()
    
    try:
        # Extract data
        data = extract_from_image(image_path, company_name)
        
        # Display results
        print("EXTRACTED DATA:")
        print("-" * 70)
        print(f"Insurance Company -> {data.get('insurance_company', 'N/A')}")
        print(f"Policy Number -> {data.get('policy_number', 'N/A')}")
        print(f"Date Prepared -> {data.get('date_prepared', 'N/A')}")
        print(f"Insurer Name -> {data.get('insurer_name', 'N/A')}")
        print(f"Insurer Address -> {data.get('insurer_address', 'N/A')}")
        print(f"Insurer City State -> {data.get('insurer_city_state', 'N/A')}")
        print(f"Insurance Amount -> {data.get('insurance_amount', 'N/A')}")
        print("-" * 70)
        print()
        
        return True
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python simple_test.py <image_path> [company_name]")
        print("\nExamples:")
        print("  python simple_test.py Nationwide_doc.pdf nationwide")
        print("  python simple_test.py StateFarm_doc.png state_farm")
        print(f"\nAvailable companies: {', '.join(get_available_companies())}")
        sys.exit(1)
    
    image_path = sys.argv[1]
    company_name = sys.argv[2] if len(sys.argv) > 2 else 'nationwide'
    
    if not Path(image_path).exists():
        print(f"Error: File not found: {image_path}")
        sys.exit(1)
    
    if company_name not in get_available_companies():
        print(f"Error: Unknown company '{company_name}'")
        print(f"Available companies: {', '.join(get_available_companies())}")
        sys.exit(1)
    
    success = test_extraction(image_path, company_name)
    sys.exit(0 if success else 1)