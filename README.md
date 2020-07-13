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
| properties.coordinates.**longitude** | Longitude of location.                                                                                         | string  | 
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
            "2020-01-23": 1,
            ... 
          },
          "latest": 3199715
        },
        "deaths": {
          "history": {
            "2020-01-21": 0,
            "2020-01-22": 0,
            "2020-01-23": 0,
            ...
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
| locations.location.**last_updated** | Date for when the data was updated.                          | string         | 
| locations.location.**latest**    | Latest values for supported statistics.                         | string         | 
| locations.location.**properties**| Properties for a given location.                                | Properties     | 

----

#### State

Retrieve information on the state level.

```http
GET /api/state/all
```

**Query Parameters**

| Parameter  | Description                                                                           | Type    |
|------------|---------------------------------------------------------------------------------------|---------|
| source     | The data source to fetch data from.<br>Options: ["nyt", "jhu"]<br>**Default:** "nyt" | string  |
| timelines  | Display timeline for daily statistics.<br>**Default:** false                         | boolean |
| properties | Display properties associated with a given location.<br>**Default:** false           | boolean |
| fips       | Only show locations matching the fips code.                                           | number |
| state      | Only show locations matching state name. The name can be the **full name** or a [2-letter ANSI code](https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations).    | string |

**Sample Request**

```http
GET /api/state/all?timelines=true&properties=true
```

**Sample Response**

```json
{
  "latest": {
    "confirmed": 3199790,
    "deaths": 133906
  },
  "locations": [
    {
      "id": "US@Washington@53",
      "country": "US",
      "state": "Washington",
      "county": "",
      "fips": "53",
      "timelines": {
        "confirmed": {
          "history": {
            "2020-01-21": 1,
            "2020-01-22": 1,
            "2020-01-23": 1,
            ...
          },
          "latest": 41090
        },
        "deaths": {
          "history": {
            "2020-01-21": 0,
            "2020-01-22": 0,
            "2020-01-23": 0,
            ...
          },
          "latest": 1426
        }
      },
      "last_updated": "2020-07-11",
      "latest": {
        "confirmed": 41090,
        "deaths": 1426
      },
      "properties": {
        "uid": "84000053",
        "iso2": "US",
        "iso3": "USA",
        "code3": "840",
        "fips": "53",
        "county": "",
        "state": "Washington",
        "country": "US",
        "coordinates": {
          "latitude": "47.4009",
          "longitude": "-121.4905"
        },
        "combined_key": "Washington, US",
        "population": 7614893
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
| locations.location.**uid**       | (Optional depends on source) Unique identifier for location.    | string         | 
| locations.location.**iso2**      | (Optional depends on source) Country code following [alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) ISO country name standards.   | string         | 
| locations.location.**iso3**      | (Optional depends on source) Country code following [alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) ISO country name standards.   | string         | 
| locations.location.**code3**     | (Optional depends on source) A three digit numerical country code identifier.  | string         | 
| locations.location.**latitude**  | (Optional depends on source) Latitude of location               | string         | 
| locations.location.**longitude** | (Optional depends on source) Longitude of location.             | string         | 
| locations.location.**timelines** | Timeline for statistics in location.                            | Timeline       | 
| locations.location.**last_updated** | Date for when the data was updated.                          | string         | 
| locations.location.**latest**    | Latest values for supported statistics.                         | string         | 
| locations.location.**properties**| Properties for a given location.                                | Properties     | 

**Sample Request with Parameter**

```http
GET /api/state/all?state=WA
```

```json
{
  "latest": {
    "confirmed": 39218,
    "deaths": 1424
  },
  "locations": [
    {
      "id": "US@Washington",
      "country": "US",
      "state": "Washington",
      "county": "",
      "fips": "53",
      "uid": "84000053",
      "iso2": "US",
      "iso3": "USA",
      "code3": "840",
      "latitude": "47.4009",
      "longitude": "-121.4905",
      "last_updated": "2020-07-11",
      "latest": {
        "confirmed": 39218,
        "deaths": 1424
      }
    }
  ]
}
```
----

#### County

Retrieve information on the county level.

```http
GET /api/county/all
```

**Query Parameters**

| Parameter  | Description                                                                           | Type    |
|------------|---------------------------------------------------------------------------------------|---------|
| source     | The data source to fetch data from.<br>Options: ["nyt", "jhu"]<br>**Default:** "nyt" | string  |
| timelines  | Display timeline for daily statistics.<br>**Default:** false                         | boolean |
| properties | Display properties associated with a given location.<br>**Default:** false           | boolean |
| fips       | Only show locations matching the fips code.                                           | number |
| state      | Only show locations matching state name. The name can be the **full name** or a [2-letter ANSI code](https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations).           | string |
| county     | Only show locations matching county name.                                            | string |

**Sample Request**

```http
GET /api/county/all?source=jhu&timelines=true&properties=true
```

**Sample Response**

```json
{
  "latest": {
    "confirmed": 11568,
    "deaths": 633
  },
  "locations": [
    {
      "id": "US@Texas@King",
      "country": "US",
      "last_updated": "2020-07-11",
      "latest": {
        "confirmed": 0,
        "deaths": 0
      },
      "timelines": {
        "confirmed": {
          "latest": 0,
          "history": {
            "2020-01-22": 0,
            "2020-01-23": 0,
            ...
          }
        },
        "deaths": {
          "latest": 0,
          "history": {
            "2020-01-22": 0,
            "2020-01-23": 0,
            ...
          }
        }
      },
      "properties": {
        "uid": "84048269",
        "iso2": "US",
        "iso3": "USA",
        "code3": "840",
        "fips": "48269",
        "county": "King",
        "state": "Texas",
        "country": "US",
        "coordinates": {
          "latitude": "33.61643847",
          "longitude": "-100.2558057"
        },
        "combined_key": "King, Texas, US",
        "population": 272
      },
      "uid": "84048269",
      "iso2": "US",
      "iso3": "USA",
      "code3": "840",
      "state": "Texas",
      "county": "King",
      "fips": "48269.0",
      "latitude": "33.61643847",
      "longitude": "-100.2558057"
    },
    {
      "id": "US@Washington@King",
      "country": "US",
      "last_updated": "2020-07-11",
      "latest": {
        "confirmed": 11568,
        "deaths": 633
      },
      "timelines": {
        "confirmed": {
          "latest": 11568,
          "history": {
            "2020-01-22": 1,
            "2020-01-23": 1,
            ...
          }
        },
        "deaths": {
          "latest": 633,
          "history": {
            "2020-01-22": 0,
            "2020-01-23": 0,
            ...
          }
        }
      },
      "properties": {
        "uid": "84053033",
        "iso2": "US",
        "iso3": "USA",
        "code3": "840",
        "fips": "53033",
        "county": "King",
        "state": "Washington",
        "country": "US",
        "coordinates": {
          "latitude": "47.49137892",
          "longitude": "-121.8346131"
        },
        "combined_key": "King, Washington, US",
        "population": 2252782
      },
      "uid": "84053033",
      "iso2": "US",
      "iso3": "USA",
      "code3": "840",
      "state": "Washington",
      "county": "King",
      "fips": "53033.0",
      "latitude": "47.49137892",
      "longitude": "-121.8346131"
    },
    ...
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
| locations.location.**uid**       | (Optional depends on source) Unique identifier for location.    | string         | 
| locations.location.**iso2**      | (Optional depends on source) Country code following [alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) ISO country name standards.   | string         | 
| locations.location.**iso3**      | (Optional depends on source) Country code following [alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) ISO country name standards.   | string         | 
| locations.location.**code3**     | (Optional depends on source) A three digit numerical country code identifier.  | string         | 
| locations.location.**latitude**  | (Optional depends on source) Latitude of location               | string         | 
| locations.location.**longitude** | (Optional depends on source) Longitude of location.             | string         | 
| locations.location.**timelines** | Timeline for statistics in location.                            | Timeline       | 
| locations.location.**last_updated** | Date for when the data was updated.                          | string         | 
| locations.location.**latest**    | Latest values for supported statistics.                         | string         | 
| locations.location.**properties**| Properties for a given location.                                | Properties     | 

**Sample Request with Parameter**

```http
GET /api/state/all?source=jhu&county=King
```

```json{
  "latest": {
    "confirmed": 0,
    "deaths": 0
  },
  "locations": [
    {
      "id": "US@New York@Queens",
      "country": "US",
      "last_updated": "2020-07-12",
      "latest": {
        "confirmed": 0,
        "deaths": 0
      },
      "timelines": {
        "confirmed": {
          "latest": 0,
          "history": {
            "2020-01-22": 0,
            "2020-01-23": 0,
            ...
          }
        },
        "deaths": {
          "latest": 0,
          "history": {
            "2020-01-22": 0,
            "2020-01-23": 0,
            ...
          }
        }
      },
      "uid": "84036081",
      "iso2": "US",
      "iso3": "USA",
      "code3": "840",
      "state": "New York",
      "county": "Queens",
      "fips": "36081.0",
      "latitude": "40.71088124",
      "longitude": "-73.81684712"
    }
  ]
}
```

- **Note:** Multiple locations that share the same county name or share the same state will also be shown.

```http
GET /api/county/all?source=jhu&county=king&timelines=true&properties=true
```

```json
{
  "latest": {
    "confirmed": 11568,
    "deaths": 633
  },
  "locations": [
    {
      "id": "US@Texas@King",
      "country": "US",
      "last_updated": "2020-07-11",
      "latest": {
        "confirmed": 0,
        "deaths": 0
      },
      "timelines": {
        "confirmed": {
          "latest": 0,
          "history": {
            "2020-01-22": 0,
            "2020-01-23": 0,
            ...
          }
        },
        "deaths": {
          "latest": 0,
          "history": {
            "2020-01-22": 0,
            "2020-01-23": 0,
            ...
          }
        }
      },
      "properties": {
        "uid": "84048269",
        "iso2": "US",
        "iso3": "USA",
        "code3": "840",
        "fips": "48269",
        "county": "King",
        "state": "Texas",
        "country": "US",
        "coordinates": {
          "latitude": "33.61643847",
          "longitude": "-100.2558057"
        },
        "combined_key": "King, Texas, US",
        "population": 272
      },
      "uid": "84048269",
      "iso2": "US",
      "iso3": "USA",
      "code3": "840",
      "state": "Texas",
      "county": "King",
      "fips": "48269.0",
      "latitude": "33.61643847",
      "longitude": "-100.2558057"
    },
    {
      "id": "US@Washington@King",
      "country": "US",
      "last_updated": "2020-07-11",
      "latest": {
        "confirmed": 11568,
        "deaths": 633
      },
      "timelines": {
        "confirmed": {
          "latest": 11568,
          "history": {
            "2020-01-22": 1,
            "2020-01-23": 1,
            ...
          }
        },
        "deaths": {
          "latest": 633,
          "history": {
            "2020-01-22": 0,
            "2020-01-23": 0,
            ...
          }
        }
      },
      "properties": {
        "uid": "84053033",
        "iso2": "US",
        "iso3": "USA",
        "code3": "840",
        "fips": "53033",
        "county": "King",
        "state": "Washington",
        "country": "US",
        "coordinates": {
          "latitude": "47.49137892",
          "longitude": "-121.8346131"
        },
        "combined_key": "King, Washington, US",
        "population": 2252782
      },
      "uid": "84053033",
      "iso2": "US",
      "iso3": "USA",
      "code3": "840",
      "state": "Washington",
      "county": "King",
      "fips": "53033.0",
      "latitude": "47.49137892",
      "longitude": "-121.8346131"
    },
    ...
  ]
}
```

## Latest

Retrieve the latest statistics for the entire country.

```http
GET /api/country/latest
```

**Query Parameters**

| Parameter  | Description                                                                           | Type    |
|------------|---------------------------------------------------------------------------------------|---------|
| source     | The data source to fetch data from.<br>Options: ["nyt", "jhu"]<br>**Default:** "nyt" | string  |

**Sample Request**

```http
GET /api/county/latest?soruce=jhu
```

**Sample Response**

```json
{
  "latest": {
    "confirmed": 3184573,
    "deaths": 134092
  },
  "last_updated": "2020-07-12"
}
```

## Sources

Retrieve the list of sources that the API supports.

```http
GET /api/data/sources
```

**Sample Request**

```http
GET /api/data/sources
```

**Sample Response**

```json
{
  "sources": [
    "nyt",
    "jhu"
  ]
}
```

## Heartbeat

Endpoint to test service health.

```http
GET /api/health/heartbeat
```

**Sample Request**

```http
GET /api/data/sources
```

**Sample Response**

```json
{
  "is_alive": true
}
```

## Development

Below are some of the dependencies you will need:

- [Python 3.7+](https://www.python.org/downloads/)
- [Pipenv](https://pypi.org/project/pipenv/)

Then, clone the repository and create a Pipenv environment.

```sh
$ git clone git@github.com:Spiderpig86/coronavirus-us-api.git
$ cd ./coronavirus-us-api
```

[Install Pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv) and set up your virtual environment with the needed dependencies.

```sh
$ pip install --user pipenv
$ pipenv sync --dev
$ pipenv shell
```

Now that this is all setup, you can run the commands to run, test, and format the project. The project will start at `localhost:8000` by default (configurable in `backend/core/config/config.yml`):

**Debugging/Live Reloading**

```sh
$ pipenv run dev
```

**Running**

```sh
$ pipenv run start
```

**Formatting**

```sh
$ invoke black
```

**Sort Imports**

```sh
$ invoke sort
```

**Linting**

```sh
$ invoke check
```

**Unit Testing**

```sh
$ invoke test
```

**End to End Tests**

```sh
$ invoke e2e
```

**Generate Test Coverage**

```sh
$ invoke coverage
```

## License

See [LICENSE.md](https://github.com/Spiderpig86/coronavirus-us-api/blob/master/LICENSE) for information regarding usage and attribution.