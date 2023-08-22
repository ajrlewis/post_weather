import pandas as pd
import requests
import utils


class PostWeather:
    def __init__(self, api_key: str, post_code: str):
        self.api_key = api_key
        self.post_code = post_code

    def _get(self, start_date: str, end_date: str) -> pd.DataFrame:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{self.post_code}/{start_date}/{end_date}"
        params = {
            "key": self.api_key,
            "unitGroup": "metric",
            "include": "days",
            "contentType": "json",
            "options": "preview",
            "elements": "datetime,temp,precip",
        }
        try:
            request = requests.get(url, params=params)
            request.raise_for_status()
            data = request.json()
            data = data["days"]
            df = pd.DataFrame(data)
            df = df.rename(
                columns={
                    "datetime": "date",
                    "temp": "weather_temp",
                    "precip": "weather_precip",
                }
            )
            df["date"] = pd.to_datetime(df["date"])
            df["weather_temp"] = df["weather_temp"].astype(float)
            df["weather_precip"] = df["weather_precip"].astype(float)
            df["post_code"] = self.post_code
            columns = [
                "date",
                "post_code",
                "weather_temp",
                "weather_precip",
            ]
            df = df[columns].copy()
            return df
        except Exception as e:
            raise Exception(
                f"Error getting weather for {self.post_code} between {start_date} and {end_date}: {e}"
            )
            return pd.DataFrame()

    def get(self, start_date: str, end_date: str) -> pd.DataFrame:
        dates = utils.chunk_dates(start_date, end_date, chunk_size=365)
        dfs = []
        for (start_date, end_date) in dates:
            df = self._get(start_date, end_date)
            dfs.append(df)
        df = pd.concat(dfs)
        return df
