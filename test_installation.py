"""
Test script to verify installation of all dependencies
Run this after setup to ensure everything is working correctly
"""

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing package imports...\n")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test basic packages
    packages = [
        ("streamlit", "Streamlit"),
        ("pdfplumber", "PDF Plumber"),
        ("PIL", "Pillow (PIL)"),
        ("pytesseract", "PyTesseract"),
        ("spacy", "spaCy"),
        ("PyPDF2", "PyPDF2"),
        ("reportlab", "ReportLab"),
        ("plotly", "Plotly"),
        ("requests", "Requests"),
        ("git", "GitPython"),
        ("pandas", "Pandas")
    ]
    
    for package, name in packages:
        try:
            __import__(package)
            print(f"✅ {name} - OK")
            tests_passed += 1
        except ImportError as e:
            print(f"❌ {name} - FAILED: {str(e)}")
            tests_failed += 1
    
    print()
    
    # Test spaCy model
    print("🧠 Testing spaCy model...")
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy model 'en_core_web_sm' - OK")
        tests_passed += 1
    except Exception as e:
        print(f"❌ spaCy model 'en_core_web_sm' - FAILED: {str(e)}")
        print("   Run: python -m spacy download en_core_web_sm")
        tests_failed += 1
    
    print()
    
    # Test Tesseract (optional but recommended)
    print("📷 Testing Tesseract OCR (optional)...")
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract OCR - OK (version {version})")
        tests_passed += 1
    except Exception as e:
        print(f"⚠️  Tesseract OCR - NOT FOUND (optional for image resumes)")
        print(f"   Error: {str(e)}")
        print("   Install from: https://github.com/tesseract-ocr/tesseract")
    
    print()
    print("=" * 50)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print("=" * 50)
    
    if tests_failed == 0:
        print("\n🎉 All tests passed! You're ready to run the application.")
        print("\nRun the app with: streamlit run app.py")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("Run './setup.sh' again or install missing packages manually.")
        return False


def test_custom_modules():
    """Test if custom modules can be imported"""
    print("\n🔧 Testing custom modules...\n")
    
    modules = [
        "config",
        "utils",
        "skill_extractor",
        "evidence_analyzer",
        "github_analyzer",
        "credibility_scorer",
        "report_generator"
    ]
    
    all_ok = True
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}.py - OK")
        except Exception as e:
            print(f"❌ {module}.py - FAILED: {str(e)}")
            all_ok = False
    
    print()
    
    if all_ok:
        print("✅ All custom modules loaded successfully!")
    else:
        print("❌ Some custom modules failed to load. Check file structure.")
    
    return all_ok


def main():
    """Run all tests"""
    print("=" * 50)
    print("Resume Skill Credibility Analyzer")
    print("Installation Test")
    print("=" * 50)
    print()
    
    # Test package imports
    packages_ok = test_imports()
    
    # Test custom modules
    modules_ok = test_custom_modules()
    
    print()
    print("=" * 50)
    
    if packages_ok and modules_ok:
        print("✅ INSTALLATION SUCCESSFUL!")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Run the app: streamlit run app.py")
        print("2. Or use: ./run.sh")
        print("3. Open http://localhost:8501 in your browser")
        return 0
    else:
        print("❌ INSTALLATION INCOMPLETE")
        print("=" * 50)
        print("\nPlease fix the errors above and run this test again.")
        return 1


if __name__ == "__main__":
    exit(main())
