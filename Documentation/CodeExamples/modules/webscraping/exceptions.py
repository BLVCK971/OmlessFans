
from typing import Optional

from pydantic import BaseModel




class ValidationError(Exception):
    def __init__(self, message, errors):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        # Now for your custom code...
        self.errors = errors


class TestError(ValueError):
    def __init__(self, message, errors):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        # Now for your custom code...
        self.errors = errors