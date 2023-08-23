from typing import List
import pandas as pd
import requests
import post_weather.utils as utils


class PostWeather:
    def __init__(self, api_key: str, dates: List[str], postcodes: List[str]):
        self.api_key = api_key
        self.dates = dates
        self.postcodes = postcodes
        self.weather = self.get()

    def _get(self, postcode: str, start_date: str, end_date: str) -> pd.DataFrame:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{postcode}/{start_date}/{end_date}"
        params = {
            "key": self.api_key,
            "unitGroup": "metric",
            "include": "days",
            "contentType": "json",
            "options": "preview",
            "elements": "datetime,temp,precip",
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            data = data["days"]
            df = pd.DataFrame(data)
            df = df.rename(
                columns={
                    "datetime": "date",
                    "temp": "temperature",
                    "precip": "precipitation",
                }
            )
            df["date"] = pd.to_datetime(df["date"])
            df["postcode"] = postcode
            df["temperature"] = df["temperature"].astype(float)
            df["precipitation"] = df["precipitation"].astype(float)
            columns = [
                "date",
                "postcode",
                "temperature",
                "precipitation",
            ]
            df = df[columns].copy()
            return df
        except Exception as e:
            raise Exception(
                f"Error getting weather for {postcode} between {start_date} and {end_date}: {e}"
            )

    def get(self) -> pd.DataFrame:
        dates = utils.chunk_dates(min(self.dates), max(self.dates), chunk_size=365)
        weathers = []  # data frame of weathers
        for postcode in self.postcodes:
            for (start_date, end_date) in dates:
                weather = self._get(postcode, start_date, end_date)
                weathers.append(weather)
        weather = (
            pd.concat(weathers)
            .sort_values(by=["date", "postcode"])
            .reset_index(drop=True)
        )
        return weather
