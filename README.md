<h1 align="center">coronavirus-us-api</h1>

<div align="center">

  [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

  <br />

  [![Build Status](https://travis-ci.com/Spiderpig86/coronavirus-us-api.svg?token=dbucBfxja2wDeWr8Bp7d&branch=master&style=flat-square)](https://travis-ci.com/Spiderpig86/coronavirus-us-api)
  [![MIT License](https://img.shields.io/github/license/Spiderpig86/coronavirus-us-api.svg)](https://opensource.org/licenses/GPL-3)
  [![codecov](https://codecov.io/gh/Spiderpig86/coronavirus-us-api/branch/master/graph/badge.svg?token=7KTLEKXSK5)](https://codecov.io/gh/Spiderpig86/coronavirus-us-api)
  [![Code style: black](https://img.shields.io/badge/code%20style-black-222.svg)](https://github.com/psf/black)
  [![Reviewed by Hound](https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg)](https://houndci.com)

</div>

## What

This API is designed to serve up to date information on confirmed cases and deaths across the United States at a country, state, and county level.

## Built With

* :zap: [FastAPI](https://fastapi.tiangolo.com/) - a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
* :moneybag: [Redis](https://redis.io/) - in-memory data structure store/cache.
* :ear_of_rice: [Swagger](https://swagger.io/) - open source documentation tools.

## Documentation

Since **coronavirus-us-api** is powered by FastAPI, the API specification strictly follows the [OpenAPI](https://swagger.io/docs/specification/about/) standard. The JSON file for this API can be found [here](https://coronavirus-us-api.herokuapp.com/openapi.json).

The API documentation comes in two flavors:

- [Swagger](https://coronavirus-us-api.herokuapp.com/) - standard way to test out the endpoints.
- [Redoc](https://coronavirus-us-api.herokuapp.com/doc) - mobile friendly documentation.

## Data Sources

The data used by the API comes from two sources:

- [New York Times](https://github.com/nytimes/covid-19-data)
- [John Hopkins University](https://github.com/CSSEGISandData/COVID-19)

## Endpoints

Before getting started, let's go over some of the common types you will see in the remainder of the documentation:

**Timlines**

| Key                               | Description                                                                                                                      | Type   | 
|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------|--------| 
| **timelines**                     | Object containing measured statistics and their historical values.                                                               | Object | 
| timelines.*statistic*             | Object that contains information for that statistic. For now, only `confirmed` and `deaths` are supported.                       | Object | 
| timelines.*statistic*.**history** | Object containing a list of key value pairs where the key is the date and the value is the number for that static for that date. | Object | 
| timelines.*statistic*.**latest** | Value of statistic at current date. | Object | 

**Properties**

| Key                                  | Description                                                                                                    | Type    | 
|--------------------------------------|----------------------------------------------------------------------------------------------------------------|---------| 
| **properties**                       | Object containing information regarding naming, classification, coordinates, and population.                   | Object  | 
| propertes.**uid**                    | Unique ID used by JHU CSSE to identify different locations.                                                    | string  | 
| properties.**iso2**                  | Country code following [alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) ISO country name standards. | string  | 
| properties.**iso3**                  | Country code following [alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) ISO country name standards. | string  | 
| properties.**code3**                 | A three digit numerical country code identifier.                                                               | string  | 
| properties.**fips**                  | A five digit identifier for US county and county-equivalents.                                                  | string  | 
| properties.**county**                | Name of US county if applicable.                                                                               | string  | 
| properties.**state**                 | Name of US state if applicable.                                                                                | string  | 
| properties.**country**               | Code for country.                                                                                              | string  | 
| properties.**coordinates**           | Object containing coordinates for given location.                                                              | object  | 
| properties.coordinates.**latitude**  | Latitude of location.                                                                                          | string  | 
| properties.coordinates.**longitude** | Longitude of location                                                                                          | string  | 
| properties.**combined_key**          | Unique key combining location names based on specificity of request result.                                    | string  | 
| properties.**population**            | Population of location.                                                                                        | number | 


### Location Data

Endpoints for fetching information (confirmed, deaths, etc) at the country, state, or county level. By default, these endpoints will show the latest statistic. Other fields such as the timeline and properties for the location can be enabled via query parameters.

#### Country

Retrieve information on the country level.

```http
GET /api/country/all
```

**Query Parameters**

| Parameter  | Description                                                                           | Type    |
|------------|---------------------------------------------------------------------------------------|---------|
| source     | The data source to fetch data from.<br>Options: ["nyt", "jhu"]<br>**Default:** "nyt" | string  |
| timelines  | Display timeline for daily statistics.<br>**Default:** false                         | boolean |
| properties | Display properties associated with a given location.<br>**Default:** false           | boolean |

**Sample Request**

```http
GET /api/country/all?timelines=true&properties=true
```

**Sample Response**

```json
{
  "latest": {
    "confirmed": 3199715,
    "deaths": 133901
  },
  "locations": [
    {
      "id": "US",
      "country": "US",
      "state": "",
      "county": "",
      "fips": "",
      "timelines": {
        "confirmed": {
          "history": {
            "2020-01-21": 1,
            "2020-01-22": 1,
            "2020-01-23": 1
          },
          "latest": 3199715
        },
        "deaths": {
          "history": {
            "2020-01-21": 0,
            "2020-01-22": 0,
            "2020-01-23": 0
          },
          "latest": 133901
        }
      },
      "last_updated": "2020-07-11",
      "latest": {
        "confirmed": 3199715,
        "deaths": 133901
      },
      "properties": {
        "uid": "840",
        "iso2": "US",
        "iso3": "USA",
        "code3": "840",
        "fips": "",
        "county": "",
        "state": "",
        "country": "US",
        "coordinates": {
          "latitude": "37.0902",
          "longitude": "-95.7129"
        },
        "combined_key": "United States",
        "population": 329466283
      }
    }
  ]
}
```

**Response**

| Key                              | Description                                                     | Type           | 
|----------------------------------|-----------------------------------------------------------------|----------------| 
| **latest**                       | Object containing latest measurements for supported statistics. | object         | 
| latest.*statistic*               | Contains the value for statistic at current date.               | number         | 
| **locations**                    | List of `Location` matching given criteria if present.          | List<Location> | 
| locations.location.**id**        | Unique ID for the country.                                      | string         | 
| locations.location.**country**   | Name of the country.                                            | string         | 
| locations.location.**state**     | State of the location if applicable.                            | string         | 
| locations.location.**county**    | County of the location if applicable.                           | string         | 
| locations.location.**fips**      | Fips code of location if applicable.                            | string         | 
| locations.location.**timelines** | Timeline for statistics in location.                            | Timeline       | 


## License

See [LICENSE.md](https://github.com/Spiderpig86/coronavirus-us-api/blob/master/LICENSE) for information regarding usage and attribution.