# PostWeather

This is a Python package for getting the "weather" at a given "postcode" on a given "date"!

## Installation

To use this extension, you can install it via pip:

```bash
pip install git+https://github.com/ajrlewis/post_weather.git
```

## Usage

```python
from post_weather import PostWeather
api_key = "your-api-key"
dates = ["2020-01-20", "2020-01-21"]
postcodes = ["W4 1LW"]
pw = PostWeather(api_key, dates, postcodes)
```

The weather is stored as data frame in the `pw.weather` attribute:

| index | date | postcode | temperature | precipitation
| --- | --- | --- | --- | --- |
| 0 | 2020-01-20 | W4 1LW | 3.0 | 0.018 |
| 1 | 2020-01-21 | W4 1LW | 2.1 | 0.000 |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Note that the usage of this code is still under the MIT license, but you must also comply with the license terms of "VisualCrossingWebServices" from "Visual Crossing Corporation".
