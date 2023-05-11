import argparse
from datetime import datetime, timedelta
import sys
import pandas as pd
import requests

global API_KEY


def set_api_key(api_key: str):
    print(__name__, f'set_api_key(api_key="{api_key}")')
    global API_KEY
    API_KEY = api_key


def _chunk_dates(start_date: str, end_date: str, chunk_size: int = 365) -> list:
    print(
        __name__,
        f"_chunk_dates(start_date={start_date}, end_date={end_date}, chunk_size={chunk_size})",
    )
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end_date - start_date
    total_days = delta.days
    if total_days <= chunk_size:
        return [(f"{start_date.date()}", f"{end_date.date()}")]
    chunks = []
    current_date = start_date
    while current_date < end_date:
        chunk_end_date = min(current_date + timedelta(days=chunk_size), end_date)
        chunks.append((f"{current_date.date()}", f"{chunk_end_date.date()}"))
        current_date = chunk_end_date + timedelta(days=1)
    return chunks


def _get(post_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    print(
        __name__,
        f'_get(post_code="{post_code}", start_date="{start_date}", end_date="{end_date}")',
    )
    post_code = post_code.strip()
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{post_code}/{start_date}/{end_date}"
    params = {
        "key": API_KEY,
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
        df["post_code"] = post_code
        columns = [
            "date",
            "post_code",
            "weather_temp",
            "weather_precip",
        ]
        df = df[columns].copy()
        return df
    except requests.exceptions.RequestException as e:
        print(
            f"Error getting weather for {post_code} between {start_date} and {end_date}: {e}"
        )
        return pd.DataFrame()


def get_weather(post_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    print(
        __name__,
        f'get_weather(post_code="{post_code}", start_date="{start_date}", end_date="{end_date}")',
    )
    dates = _chunk_dates(start_date, end_date, chunk_size=365)
    dfs = []
    for (start_date, end_date) in dates:
        df = _get(post_code, start_date, end_date)
        dfs.append(df)
    df = pd.concat(dfs)
    return df


def from_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Input:
        + "date"
        + "post_code"

    Output:
        + "date"
        + "post_code"
        + "weather_temp"
        + "weather_precip"
    """
    print(__name__, f"from_df(df={df})")
    if "api_key" in df.columns:
        api_key = df.iloc[0]["api_key"]
        set_api_key(api_key)
    dfs_weather = []
    for post_code, group_df in df.groupby("post_code"):
        if not group_df.empty:
            start_date, end_date = group_df["date"].agg(["min", "max"])
            df_weather = get_weather(post_code, start_date, end_date)
            dfs_weather.append(df_weather)
    df_weather = pd.concat(dfs_weather)
    print(df_weather)
    return df_weather


def main(input_filepath: str, output_filepath: str):
    print(
        __name__,
        f'main(input_filepath="{input_filepath}", output_filepath="{output_filepath}")',
    )
    df = pd.read_csv(input_filepath)
    df_weather_data = from_df(df)
    df_weather_data.to_csv(output_filepath, index=False)


if __name__ == "__main__":
    print(__name__, f'__name__ == "__main__"')
    parser = argparse.ArgumentParser(description="Get weather data for postcodes")
    parser.add_argument("api_key", type=str, help="your OpenWeatherMap API key")
    parser.add_argument("input_file", type=str, help="input CSV file with postcodes")
    parser.add_argument(
        "output_file", type=str, help="output CSV file with weather data"
    )
    args = parser.parse_args()
    set_api_key(args.api_key)
    main(args.input_file, args.output_file)
