import json
from typing import List, Optional
from pydantic import BaseModel

class Response_Excel_Range(BaseModel):
    linking_elem: str
    element_selector: str
    element_interactive: bool