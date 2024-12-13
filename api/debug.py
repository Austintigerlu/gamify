# import sys
# import os

# print("Python Path:")
# for path in sys.path:
#     print(path)

# print("Current Working Directory:", os.getcwd())

import sys
import site

# Add virtual environment's site-packages to Python path
site_packages_path = '/Users/phoelandsiu/gamify/myenv/lib/python3.10/site-packages'
if site_packages_path not in sys.path:
    sys.path.append(site_packages_path)

# Verify the Python path
print("Python Path:", sys.path)

# Test importing dotenv
from dotenv import load_dotenv
print("dotenv imported successfully!")
