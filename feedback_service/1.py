# feedback_service/schemas/feedback.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class FeedbackCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    rating: int = Field(..., ge=1, le=5)
    category: str
    comments: Optional[str] = None
    timestamp: Optional[datetime] = None


payload = {"firstname":"Arun", "lastname":"Gupta", "email":"Arun_o_gupta@yahoo.com", "rating":1, "category":"In store"}

fc = FeedbackCreate(**payload)

def my_function(**kwargs):
    print(kwargs)

my_dict = {'a': 1, 'b': 2}
my_function(**my_dict)  # Output: {'a': 1, 'b': 2}

new_dict = {**my_dict, 'c': 3} # new_dict will be {'a': 1, 'b': 2, 'c': 3}
