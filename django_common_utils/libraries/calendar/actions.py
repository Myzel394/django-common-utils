from datetime import datetime
from typing import Optional
from urllib.parse import urlencode

from . import constants

# Example
"""
https://www.google.com/calendar/render
?action=TEMPLATE&text=Your+Event+Name
&dates=20140127T224000Z/20140320T221500Z
&details=For+details,+link+here:+http://www.example.com&location=Waldorf+Astoria,+301+Park+Ave+,+New+York,+NY+10022
&sf=true
&output=xml

http://www.google.com/calendar/render?
action=TEMPLATE
&text=[event-title]
&dates=[start-custom format='Ymd\\THi00\\Z']/[end-custom format='Ymd\\THi00\\Z']
&details=[description]
&location=[location]
&trp=false
"""

__all__ = [
    "create_gce_url"
]


def create_gce_url(
        text: str,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        url: str = constants.URL,
        action: str = "TEMPLATE",
        date_format: str = "%Y%m%dT%H%M00",
        trp: bool = True,
        **kwargs
) -> str:
    """
    Creates a link to add an event to Google Calendar.
    Documentation: http://useroffline.blogspot.com/2009/06/making-google-calendar-link.html
    Stackoverflow answer: https://stackoverflow.com/a/23495015/9878135
    
    :param text: Parameter text
    :param start_date: Parameter start date, will be parsed with format date_format
    :param end_date: Parameter end_date, will be parsed with format date_format
    :param url: The url (works as prefix)
    :param action: Parameter action (default 'TEMPLATE')
    :param date_format: Date format that should be used to parse start_date and end_date
    :param trp: Parameter trp
    :param kwargs: Extra parameters that should be added to the link
    :return: str, ready-to-use link
    """
    
    date_string = start_date.strftime(date_format)
    
    if end_date:
        date_string += f"/{end_date.strftime(date_format)}"
    
    parsed = urlencode({
        "action": action,
        "text": text,
        "dates": date_string,
        "trp": trp,
        **kwargs
    })
    
    return f"{url}?{parsed}"
