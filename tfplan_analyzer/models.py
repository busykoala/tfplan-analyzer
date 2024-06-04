from typing import List, Optional

from pydantic import BaseModel


class Change(BaseModel):
    actions: List[str]
    before: Optional[dict]
    after: Optional[dict]


class ResourceChange(BaseModel):
    address: str
    mode: str
    type: str
    name: str
    change: Change


class Plan(BaseModel):
    resource_changes: List[ResourceChange]
