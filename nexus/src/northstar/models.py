from dataclasses import dataclass, field
from typing import List

@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    active: bool = True
    tags: List[str] = field(default_factory=list)
