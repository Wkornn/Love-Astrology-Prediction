"""Mode Interface - Base class for all operational modes"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class ModeInterface(ABC):
    """
    Abstract base class for operational modes
    Implements Strategy Pattern for different analysis types
    """
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the mode's analysis
        
        Args:
            input_data: Mode-specific input data
            
        Returns:
            Analysis result dictionary
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        Validate input data for this mode
        
        Args:
            input_data: Input to validate
            
        Returns:
            True if valid, raises ValueError if invalid
        """
        pass
    
    @property
    @abstractmethod
    def mode_name(self) -> str:
        """Return the mode name"""
        pass
