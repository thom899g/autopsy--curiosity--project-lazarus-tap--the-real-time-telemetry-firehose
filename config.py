"""
Configuration module for the Telemetry Firehose system.
Centralizes all configuration to prevent import errors and provide type safety.
"""
import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration with validation."""
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    
    @classmethod
    def from_env(cls) -> Optional['FirebaseConfig']:
        """Create config from environment variables with validation."""
        try:
            # Handle multi-line private key from env
            private_key = os.getenv('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n')
            
            return cls(
                project_id=os.getenv('FIREBASE_PROJECT_ID', ''),
                private_key_id=os.getenv('FIREBASE_PRIVATE_KEY_ID', ''),
                private_key=private_key,
                client_email=os.getenv('FIREBASE_CLIENT_EMAIL', ''),
                client_id=os.getenv('FIREBASE_CLIENT_ID', '')
            )
        except Exception as e:
            print(f"Error loading Firebase config: {e}")
            return None

@dataclass
class TelemetryConfig:
    """Telemetry system configuration."""
    collection_name: str = 'telemetry_stream'
    batch_size: int = 100
    flush_interval_seconds: int = 30
    max_retries: int = 3
    retry_delay_seconds: int = 5
    
    @property
    def is_valid(self) -> bool:
        """Validate configuration."""
        return all([
            self.collection_name,
            self.batch_size > 0,
            self.flush_interval_seconds > 0,
            self.max_retries >= 0
        ])

# Global configuration instances
FIREBASE_CONFIG = FirebaseConfig.from_env()
TELEMETRY_CONFIG = TelemetryConfig()

def validate_config() -> bool:
    """Validate all configurations are properly loaded."""
    if not FIREBASE_CONFIG:
        print("ERROR: Firebase configuration is missing or invalid")
        print("Please set the following environment variables:")
        print("  FIREBASE_PROJECT_ID")
        print("  FIREBASE_PRIVATE_KEY_ID")
        print("  FIREBASE_PRIVATE_KEY")
        print("  FIREBASE_CLIENT_EMAIL")
        print("  FIREBASE_CLIENT_ID")
        return False
    
    if not TELEMETRY_CONFIG.is_valid:
        print("ERROR: Telemetry configuration is invalid")
        return False
    
    return True