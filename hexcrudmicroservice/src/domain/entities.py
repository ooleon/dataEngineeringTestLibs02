from pydantic import BaseModel, Field
from datetime import datetime, UTC

class Item(BaseModel):
    id: str
    name: str
    value: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
