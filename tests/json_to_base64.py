"""
JSON to Base64 Converter

This module provides utilities to convert JSON data to base64 encoded strings
and vice versa. Useful for encoding JSON data for transmission or storage.
"""

import json
import base64
from typing import Any, Union


class JSONBase64Converter:
    """A utility class for converting JSON data to/from base64 strings."""
    
    @staticmethod
    def json_to_base64(data: Union[dict, list, str, int, float, bool, None]) -> str:
        """
        Convert JSON data to base64 encoded string.
        
        Args:
            data: JSON serializable data (dict, list, str, int, float, bool, None)
            
        Returns:
            str: Base64 encoded string
            
        Raises:
            TypeError: If data is not JSON serializable
            ValueError: If JSON encoding fails
        """
        try:
            # Convert data to JSON string
            json_string = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
            
            # Encode JSON string to bytes
            json_bytes = json_string.encode('utf-8')
            
            # Convert bytes to base64 string
            base64_string = base64.b64encode(json_bytes).decode('utf-8')
            
            return base64_string
            
        except TypeError as e:
            raise TypeError(f"Data is not JSON serializable: {e}")
        except Exception as e:
            raise ValueError(f"Failed to convert JSON to base64: {e}")
    
    @staticmethod
    def base64_to_json(base64_string: str) -> Any:
        """
        Convert base64 encoded string back to JSON data.
        
        Args:
            base64_string: Base64 encoded string
            
        Returns:
            Any: Original JSON data
            
        Raises:
            ValueError: If base64 decoding or JSON parsing fails
        """
        try:
            # Decode base64 string to bytes
            json_bytes = base64.b64decode(base64_string.encode('utf-8'))
            
            # Convert bytes to JSON string
            json_string = json_bytes.decode('utf-8')
            
            # Parse JSON string back to original data
            data = json.loads(json_string)
            
            return data
            
        except Exception as e:
            raise ValueError(f"Failed to convert base64 to JSON: {e}")
    
    @staticmethod
    def is_valid_base64_json(base64_string: str) -> bool:
        """
        Check if a base64 string contains valid JSON data.
        
        Args:
            base64_string: Base64 encoded string to validate
            
        Returns:
            bool: True if valid base64 JSON, False otherwise
        """
        try:
            JSONBase64Converter.base64_to_json(base64_string)
            return True
        except ValueError:
            return False


def json_to_base64(data: Union[dict, list, str, int, float, bool, None]) -> str:
    """
    Convenience function to convert JSON data to base64 string.
    
    Args:
        data: JSON serializable data
        
    Returns:
        str: Base64 encoded string
    """
    return JSONBase64Converter.json_to_base64(data)


def base64_to_json(base64_string: str) -> Any:
    """
    Convenience function to convert base64 string to JSON data.
    
    Args:
        base64_string: Base64 encoded string
        
    Returns:
        Any: Original JSON data
    """
    return JSONBase64Converter.base64_to_json(base64_string)


# Example usage and testing
if __name__ == "__main__":
    # Example data
    sample_data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York",
        "hobbies": ["reading", "coding", "traveling"],
        "is_active": True,
        "metadata": {
            "created_at": "2024-01-01",
            "updated_at": "2024-01-15"
        }
    }
    
    print("Original JSON data:")
    print(json.dumps(sample_data, indent=2))
    print()
    
    # Convert to base64
    base64_encoded = json_to_base64(sample_data)
    print(f"Base64 encoded: {base64_encoded}")
    print()
    
    # Convert back to JSON
    decoded_data = base64_to_json(base64_encoded)
    print("Decoded JSON data:")
    print(json.dumps(decoded_data, indent=2))
    print()
    
    # Verify round-trip conversion
    print(f"Round-trip conversion successful: {sample_data == decoded_data}")
    
    # Test validation
    print(f"Valid base64 JSON: {JSONBase64Converter.is_valid_base64_json(base64_encoded)}")
    print(f"Invalid base64 JSON: {JSONBase64Converter.is_valid_base64_json('invalid_base64')}")
