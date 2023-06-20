import json
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime

NIGHT_PATH = "ConfigurationDetails/2023_BatAudio192kHz_night.config"

def update_night_config(night_path: str) -> None:
    """
    Updates night config start and end time recordings based off of most recent sunset and sunrise values.

    Arguments:
        night_path: str; path to the night config file.
    """
    # Get sunrise and and sunset values
    loc = LocationInfo(name='Seattle', region='WA, USA', timezone='UTC',
                   latitude=47.606, longitude=-122.332)
    sun_dict = sun(loc.observer, date=datetime.now(), tzinfo=loc.timezone)
    sunset_hour = sun_dict['sunset'].hour
    sunset_minute = sun_dict['sunset'].minute
    sunrise_hour = sun_dict['sunrise'].hour
    sunrise_minute = sun_dict['sunrise'].minute
    sunset = (sunset_hour * 60) + sunset_minute
    sunrise = (sunrise_hour * 60) + sunrise_minute
    hour_before_sunset = sunset - 60
    hour_after_sunrise = sunrise + 60

    # Open and edit Night Configuration File
    night_config = open(night_path, 'r+', encoding='utf-8')
    data = json.load(night_config)
    data["timePeriods"][0]["startMins"] = hour_before_sunset
    data["timePeriods"][0]["endMins"] = hour_after_sunrise
    night_config.seek(0)
    json.dump(data, night_config, indent=0)
    night_config.close()

if __name__ == "__main__":
    night_path = NIGHT_PATH
    update_night_config(night_path)