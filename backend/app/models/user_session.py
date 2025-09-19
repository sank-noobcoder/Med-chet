from dataclasses import dataclass, field
from typing import Dict, Optional
import time

@dataclass
class UserSession:
    phone_number: str
    state: str = "greeting"
    medical_data: Dict = field(default_factory=dict)
    last_active: float = field(default_factory=time.time)
    conversation_context: str = ""
    
    def update_activity(self):
        self.last_active = time.time()
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        return (time.time() - self.last_active) > (timeout_minutes * 60)