"""
Data models for telemetry system with Pydantic validation.
Ensures type safety and data consistency.
"""
from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, validator

class TelemetryEvent(BaseModel):
    """Base telemetry event model."""
    event_id: str = Field(..., description="Unique event identifier")
    event_type: str = Field(..., description="Type of event")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str = Field(..., description="Event source identifier")
    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('event_id')
    def validate_event_id(cls, v: str) -> str:
        """Validate event ID is not empty."""
        if not v or not v.strip():
            raise ValueError('Event ID cannot be empty')
        return v.strip()
    
    @validator('event_type')
    def validate_event_type(cls, v: str) -> str:
        """Validate event type is not empty."""
        if not v or not v.strip():
            raise ValueError('Event type cannot be empty')
        return v.strip()
    
    def to_firestore_dict(self) -> Dict[str, Any]:
        """Convert to Firestore-compatible dictionary."""
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'timestamp': self.timestamp,
            'source