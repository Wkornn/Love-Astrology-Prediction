"""Mode Controller - Orchestrates operational mode selection and execution"""

from typing import Dict, Any
from enum import Enum
from .mode_interface import ModeInterface
from .single_person_mode import SinglePersonMode
from .celebrity_matching_mode import CelebrityMatchingMode
from .couple_compatibility_mode import CoupleCompatibilityMode

class OperationalMode(Enum):
    """Available operational modes"""
    SINGLE_PERSON = "single_person"
    CELEBRITY_MATCHING = "celebrity_matching"
    COUPLE_COMPATIBILITY = "couple_compatibility"

class ModeController:
    """
    Central controller for mode selection and execution
    Implements Strategy Pattern for different analysis modes
    """
    
    def __init__(self, celebrity_db_path: str = None):
        """
        Initialize mode controller with all available modes
        
        Args:
            celebrity_db_path: Optional path to celebrity database
        """
        self._modes: Dict[str, ModeInterface] = {
            OperationalMode.SINGLE_PERSON.value: SinglePersonMode(),
            OperationalMode.CELEBRITY_MATCHING.value: CelebrityMatchingMode(celebrity_db_path),
            OperationalMode.COUPLE_COMPATIBILITY.value: CoupleCompatibilityMode()
        }
    
    def execute_mode(self, mode: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute specified mode with input data
        
        Args:
            mode: Mode name (single_person, celebrity_matching, couple_compatibility)
            input_data: Mode-specific input data
            
        Returns:
            Analysis result dictionary
            
        Raises:
            ValueError: If mode is invalid or input validation fails
        """
        if mode not in self._modes:
            raise ValueError(
                f"Invalid mode: {mode}. "
                f"Available modes: {list(self._modes.keys())}"
            )
        
        mode_instance = self._modes[mode]
        
        try:
            # Validate input
            mode_instance.validate_input(input_data)
            
            # Execute mode
            result = mode_instance.execute(input_data)
            
            return {
                'success': True,
                'mode': mode,
                'result': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'mode': mode,
                'error': str(e)
            }
    
    def get_available_modes(self) -> list:
        """Get list of available modes"""
        return [
            {
                'name': mode_name,
                'description': self._get_mode_description(mode_name)
            }
            for mode_name in self._modes.keys()
        ]
    
    def _get_mode_description(self, mode_name: str) -> str:
        """Get description for a mode"""
        descriptions = {
            OperationalMode.SINGLE_PERSON.value: 
                "Single-person love personality analysis",
            OperationalMode.CELEBRITY_MATCHING.value: 
                "Match user with celebrities from database",
            OperationalMode.COUPLE_COMPATIBILITY.value: 
                "Compare two people for compatibility score"
        }
        return descriptions.get(mode_name, "Unknown mode")
    
    def add_mode(self, mode_name: str, mode_instance: ModeInterface):
        """
        Add custom mode (extension point)
        
        Args:
            mode_name: Unique mode identifier
            mode_instance: Mode implementation
        """
        if mode_name in self._modes:
            raise ValueError(f"Mode {mode_name} already exists")
        
        self._modes[mode_name] = mode_instance
