

import tempfile


# Create temporary directory
temp = tempfile.TemporaryDirectory()
PATH = temp.name

# Allowed extensions for files
ALLOWED_EXTENSIONS = ['bmp']
