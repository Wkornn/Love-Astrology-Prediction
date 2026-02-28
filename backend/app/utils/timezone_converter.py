"""Timezone Conversion Utility"""

from datetime import datetime
from zoneinfo import ZoneInfo
import logging

logger = logging.getLogger(__name__)

class TimezoneConverter:
    """Handle timezone conversions for birth chart calculations"""
    
    @staticmethod
    def convert_to_utc(date: str, time: str, timezone: str = 'UTC') -> datetime:
        """
        Convert local birth time to UTC
        
        Args:
            date: Birth date in 'YYYY-MM-DD' format
            time: Birth time in 'HH:MM' or 'HH:MM:SS' format
            timezone: IANA timezone string (e.g., 'America/New_York', 'Europe/London')
            
        Returns:
            datetime object in UTC
            
        Raises:
            ValueError: If timezone is invalid or conversion fails
        """
        # Handle HH:MM format
        if time.count(':') == 1:
            time += ':00'
        
        dt_str = f"{date} {time}"
        
        try:
            # Parse as naive datetime
            naive_dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
            
            # Handle UTC directly
            if timezone.upper() == 'UTC':
                return naive_dt.replace(tzinfo=ZoneInfo('UTC'))
            
            # Try to get timezone
            try:
                tz = ZoneInfo(timezone)
            except Exception as tz_error:
                logger.warning(
                    f"Invalid timezone '{timezone}', defaulting to UTC. Error: {tz_error}"
                )
                return naive_dt.replace(tzinfo=ZoneInfo('UTC'))
            
            # Localize to specified timezone
            local_dt = naive_dt.replace(tzinfo=tz)
            
            # Convert to UTC
            utc_dt = local_dt.astimezone(ZoneInfo('UTC'))
            
            logger.info(
                f"Converted {naive_dt} {timezone} to {utc_dt} UTC"
            )
            
            return utc_dt
            
        except Exception as e:
            logger.error(f"Failed to convert timezone: {e}")
            raise ValueError(f"Timezone conversion failed: {e}")
    
    @staticmethod
    def validate_timezone(timezone: str) -> bool:
        """
        Validate if timezone string is valid IANA timezone
        
        Args:
            timezone: Timezone string to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not timezone or timezone.upper() == 'UTC':
            return True
        
        try:
            ZoneInfo(timezone)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_safe_timezone(timezone: str = None) -> str:
        """
        Get safe timezone string, defaulting to UTC if invalid
        
        Args:
            timezone: Timezone string to validate
            
        Returns:
            Valid timezone string (original or 'UTC')
        """
        if not timezone:
            logger.warning("No timezone provided, defaulting to UTC")
            return 'UTC'
        
        if TimezoneConverter.validate_timezone(timezone):
            return timezone
        
        logger.warning(f"Invalid timezone '{timezone}', defaulting to UTC")
        return 'UTC'
