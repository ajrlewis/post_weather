import pandas as pd
from post_weather import PostWeather


def from_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes the weather at given dates and post codes from a data frame.

    Parameters:
    - df (pd.DataFrame): The input DataFrame with columns: ["api_key", "date", "post_code"].

    Returns:
    - df_weather (pd.DataFrame): The output DataFrame with columns: ["date", "post_code", "weather_temp", "weather_precip"].
    """
    if "api_key" in df.columns:
        api_key = df.iloc[0]["api_key"]
    else:
        raise Exception("api_key column not in data frame.")
    dfs_weather = []
    for post_code, group_df in df.groupby("post_code"):
        if not group_df.empty:
            start_date, end_date = group_df["date"].agg(["min", "max"])
            pw = PostWeather(api_key=api_key, post_code=post_code)
            df_weather = pw.get(start_date, end_date)
            dfs_weather.append(df_weather)
    df_weather = pd.concat(dfs_weather)
    return df_weather


def main(input_filepath: str, output_filepath: str):
    df_in = pd.read_csv(input_filepath)
    df_out = from_df(df_in)
    df_out.to_csv(output_filepath, index=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get weather data for postcodes")
    parser.add_argument("input_file", type=str, help="input CSV file with postcodes")
    parser.add_argument(
        "output_file", type=str, help="output CSV file with weather data"
    )
    args = parser.parse_args()
    main(args.input_file, args.output_file)
