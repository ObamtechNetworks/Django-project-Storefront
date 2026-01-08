
from django.forms import ValidationError

def validate_file_size(file):
    max_size_kb = 2000 # 2000 KB
    
    if file.size > max_size_kb * 1024:
        raise ValidationError(f'Maximum file size is {max_size_kb}KB!')