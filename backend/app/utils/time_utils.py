"""Time parsing utilities"""

from datetime import datetime, timedelta
import re


def parse_relative_time(time_str: str) -> datetime:
    """
    Parse relative time strings like '2 hours ago', 'now', 'today at 9am'
    """
    
    time_str = time_str.lower().strip()
    now = datetime.now()
    
    # Handle 'now'
    if time_str == 'now':
        return now
    
    # Handle 'today', 'yesterday'
    if time_str == 'today':
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_str == 'yesterday':
        return (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Handle 'X hours/minutes/days ago'
    ago_pattern = r'(\d+)\s+(hour|minute|day|week)s?\s+ago'
    match = re.search(ago_pattern, time_str)
    if match:
        amount = int(match.group(1))
        unit = match.group(2)
        
        if unit == 'minute':
            return now - timedelta(minutes=amount)
        elif unit == 'hour':
            return now - timedelta(hours=amount)
        elif unit == 'day':
            return now - timedelta(days=amount)
        elif unit == 'week':
            return now - timedelta(weeks=amount)
    
    # Handle 'today at Xam/pm'
    time_pattern = r'today at (\d+)(am|pm)'
    match = re.search(time_pattern, time_str)
    if match:
        hour = int(match.group(1))
        period = match.group(2)
        
        if period == 'pm' and hour != 12:
            hour += 12
        elif period == 'am' and hour == 12:
            hour = 0
        
        return now.replace(hour=hour, minute=0, second=0, microsecond=0)
    
    # Try to parse as ISO format
    try:
        return datetime.fromisoformat(time_str)
    except:
        pass
    
    # Default to now
    return now
