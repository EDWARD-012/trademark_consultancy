import random
import datetime
from .models import TrademarkApplication

def generate_application_number():
    """
    Generates a unique Application Number in format: TM-YYYY-XXXX
    Example: TM20254829
    """
    current_year = datetime.date.today().year
    
    while True:
        # 1. Random 4 digit number (1000 to 9999)
        random_code = random.randint(1000, 9999)
        
        # 2. Create the ID
        new_app_number = f"TM{current_year}{random_code}"
        
        # 3. Check Database: Agar ye ID pehle se exist karti hai, toh loop dobara chalega
        if not TrademarkApplication.objects.filter(application_number=new_app_number).exists():
            return new_app_number