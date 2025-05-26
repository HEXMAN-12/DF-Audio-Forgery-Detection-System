import os
import sys
import importlib.util
import subprocess

def check_directory_structure():
    """Check if the required directories exist"""
    print("Checking directory structure...")
    
    required_dirs = [
        "app",
        "app/static",
        "app/static/css",
        "app/static/img",
        "app/templates"
    ]
    
    all_exist = True
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"  [ERROR] Directory not found: {directory}")
            all_exist = False
        else:
            print(f"  [OK] Directory found: {directory}")
    
    return all_exist

def check_required_files():
    """Check if the required files exist"""
    print("\nChecking required files...")
    
    required_files = [
        "requirements.txt",
        "run.py",
        "run.sh",
        "run.bat",
        "gunicorn.conf.py",
        "app/__init__.py",
        "app/views.py",
        "app/forms.py",
        "app/audio_analysis.py",
        "app/static/css/styles.css",
        "app/templates/base.html",
        "app/templates/index.html",
        "app/templates/results.html",
        "app/templates/about.html",
        "app/templates/contact.html"
    ]
    
    all_exist = True
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"  [ERROR] File not found: {file_path}")
            all_exist = False
        else:
            print(f"  [OK] File found: {file_path}")
    
    return all_exist

def check_python_imports():
    """Check if required Python packages can be imported"""
    print("\nChecking Python dependencies...")
    
    required_packages = [
        "flask",
        "werkzeug",
        "numpy",
        "scipy",
        "librosa",
        "matplotlib",
        "flask_wtf",
        "wtforms",
        "dotenv"
    ]
    
    all_importable = True
    for package in required_packages:
        try:
            if importlib.util.find_spec(package) is None:
                print(f"  [WARNING] Package not found: {package}")
                all_importable = False
            else:
                print(f"  [OK] Package found: {package}")
        except ImportError:
            print(f"  [WARNING] Package cannot be imported: {package}")
            all_importable = False
    
    return all_importable

def create_instance_directory():
    """Create instance directory if it doesn't exist"""
    print("\nChecking instance directory...")
    
    instance_dir = "instance"
    uploads_dir = os.path.join(instance_dir, "uploads")
    
    if not os.path.exists(instance_dir):
        print(f"  Creating directory: {instance_dir}")
        os.makedirs(instance_dir)
    else:
        print(f"  [OK] Directory exists: {instance_dir}")
    
    if not os.path.exists(uploads_dir):
        print(f"  Creating directory: {uploads_dir}")
        os.makedirs(uploads_dir)
    else:
        print(f"  [OK] Directory exists: {uploads_dir}")

def create_placeholder_content():
    """Create placeholder images if they don't exist"""
    print("\nChecking placeholder content...")
    
    img_dir = os.path.join("app", "static", "img")
    forensics_img = os.path.join(img_dir, "audio-forensics.png")
    favicon = os.path.join(img_dir, "favicon.ico")
    
    if not os.path.exists(forensics_img) or not os.path.exists(favicon):
        print("  Creating placeholder images...")
        try:
            # Try to import PIL
            from PIL import Image
            # Run the create_images.py script
            import create_images
            create_images.create_placeholder_image()
        except ImportError:
            print("  [WARNING] PIL not installed, cannot create placeholder images")
            print("  You can install it with: pip install pillow")
        except Exception as e:
            print(f"  [WARNING] Error creating placeholder images: {e}")
    else:
        print("  [OK] Placeholder images exist")

def main():
    """Main function to check if the application is ready to run"""
    print("=== DF Audio Forensics Application Check ===\n")
    
    # Change to the project root directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check directory structure
    dirs_ok = check_directory_structure()
    
    # Check required files
    files_ok = check_required_files()
    
    # Check Python imports
    imports_ok = check_python_imports()
    
    # Create instance directory
    create_instance_directory()
    
    # Create placeholder content
    create_placeholder_content()
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Directory structure: {'OK' if dirs_ok else 'ERRORS FOUND'}")
    print(f"Required files: {'OK' if files_ok else 'ERRORS FOUND'}")
    print(f"Python dependencies: {'OK' if imports_ok else 'WARNINGS FOUND'}")
    
    if dirs_ok and files_ok:
        print("\n✅ The application structure is ready.")
        print("\nTo run the application:")
        if os.name == 'nt':  # Windows
            print("  - On Windows: run.bat")
        else:  # Linux/Mac
            print("  - On Linux/Mac: ./run.sh")
        print("\nFor more information, see README.md and DEPLOYMENT.md")
    else:
        print("\n❌ The application has structural issues that need to be fixed.")
        print("Please resolve the errors above before running the application.")
    
    return 0 if dirs_ok and files_ok else 1

if __name__ == "__main__":
    sys.exit(main())
