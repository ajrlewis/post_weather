# PostWeather

This is a Python package for getting the "weather" at a given "postcode"!

## Installation

To use this extension, you can install it via pip:

```bash
pip install git+https://github.com/ajrlewis/post_weather.git
```

## Input File

| Column | Value | Description
| --- | --- | --- |
| api_key | "you-api-key" | your Visual Crossing Corporation API key
| date      | "2020-01-20" | the date requested
| post_code | "W4 1LW" | the post code.


## Output File

| Column | Value | Description
| --- | --- | --- |
| date      | "2020-01-20" | the date requested
| post_code | "W4 1LW" | the post code
| weather_temp | 10.3 | the temperature
| weather_recip | 0.0 | the precipitation amount.


### Usage

```bash
python weather/weather.py <your-api-key> data/W4-1LW-input.csv data/W4-1LW-output.csv

```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Note that the usage of this code is still under the MIT license, but you must also comply with the license terms of "VisualCrossingWebServices" from "Visual Crossing Corporation".
