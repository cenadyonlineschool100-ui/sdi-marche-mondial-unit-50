#!/usr/bin/env python3
"""
Auto-deployment script for PythonAnywhere
Run this ONCE in PythonAnywhere bash console to fully set up your Django site
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command and report status"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print()
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True)
        print(f"\n✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - FAILED")
        print(f"Error: {e}")
        return False

def main():
    username = os.getenv('USER')
    
    print("""
╔════════════════════════════════════════════════════════════╗
║       PythonAnywhere Auto-Deployment Script               ║
║                                                            ║
║  This script will automatically:                          ║
║  1. Clone the GitHub repository                           ║
║  2. Create a virtualenv                                   ║
║  3. Install dependencies                                  ║
║  4. Run migrations                                        ║
║  5. Collect static files                                  ║
║                                                            ║
║  ⏱️  Total time: ~15-20 minutes                           ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    input("Press ENTER to continue...")
    
    steps = [
        ("cd ~ && git clone https://github.com/cenadyonlineschool100-ui/sdi-marche-mondial-unit-50.git sdi_site",
         "Step 1: Clone GitHub repository"),
        
        ("mkvirtualenv --python=/usr/bin/python3.10 sdi_venv",
         "Step 2: Create virtualenv"),
        
        ("cd ~/sdi_site/sdi_market && workon sdi_venv && pip install --upgrade pip setuptools wheel",
         "Step 3a: Upgrade pip"),
        
        ("cd ~/sdi_site/sdi_market && workon sdi_venv && pip install -r requirements.txt",
         "Step 3b: Install dependencies"),
        
        ("cd ~/sdi_site/sdi_market && workon sdi_venv && python manage.py migrate --noinput",
         "Step 4: Run migrations"),
        
        ("cd ~/sdi_site/sdi_market && workon sdi_venv && python manage.py collectstatic --noinput",
         "Step 5: Collect static files"),
    ]
    
    failed_steps = []
    
    for cmd, description in steps:
        if not run_command(cmd, description):
            failed_steps.append(description)
    
    print("\n" + "="*60)
    print("DEPLOYMENT SUMMARY")
    print("="*60)
    
    if failed_steps:
        print(f"\n❌ {len(failed_steps)} step(s) failed:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\n⚠️  Some steps failed. Please fix them manually.")
    else:
        print("\n✅ All steps completed successfully!")
    
    print("\n" + "="*60)
    print("NEXT STEPS IN PYTHONANYWHERE WEB INTERFACE")
    print("="*60)
    print("""
1. Go to: https://www.pythonanywhere.com/web_app_setup/

2. Add a new web app with:
   - Working directory: /home/{user}/sdi_site/sdi_market
   - WSGI file: sdi_market/sdi_market/wsgi.py

3. Add environment variables:
   - DJANGO_SETTINGS_MODULE = sdi_market.settings
   - DEBUG = False
   - ALLOWED_HOSTS = {user}.pythonanywhere.com
   - DJANGO_SECRET_KEY = (generate from generate_pythonanywhere_config.py)

4. Click "Reload {user}.pythonanywhere.com"

5. Visit: https://{user}.pythonanywhere.com

""".format(user=username))
    
    print("="*60)
    print("📞 If you have issues, send us:")
    print("   - The Error log from PythonAnywhere")
    print("   - The Server log from PythonAnywhere")
    print("="*60)

if __name__ == '__main__':
    main()
