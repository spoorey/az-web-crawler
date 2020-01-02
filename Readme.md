# AZ-Crawler
A script that crawls through the articles on aargauerzeitung.ch, visualising the amount of articles per municipality on a html map.

This script is my personal project work for the `matl` module at the FHNW.

## How it works

![Example map](data/example.png)

These scripts work by first fetching all the required data using aargauerzeitung's json api.
Then these articles are matched with a part of the html vector graphic in `data/map.html`, and a color is calculated based on the amount of articles per municipality.
These colors are then displayed on the html map using javascript.
Due to the massive amount of articles for the city of Aarau, it is not included in the visualization.

## Running the script
It is recommended to use anaconda to run the script. An anaconda environment is included in the repository.
Run these command to activate the anaconda environment:

`conda env create -f conda-environment.yaml`

`conda activate spoorey-azcrawler`

Then run these scripts in this order:
1. `python crawl-cities.py` To store all the cities locally
2. `python crawl-news.py` To store the articles of the last three months for each city
3. `python visualize-articles.py` To visualize the amount of articles on the map. optionally, add a an argument `blue` or `sqrt` (see `colorcodes.py`) e.g.: `python visualize-articles.py blue`

Then open `vendor/map.html` in your browser.

## File structure
### `cache` directory
This directory contains cached versions of all the data required by the az api.
### `data` directory
This contains all data required to display the map (`vendor/map.html`). This includes a js script that was used to assign the city names to the vector paths (`data/map-names-and-ids.js`) as well as the manually corrected list of paths and city names which was created by manually improving the result of said script ('data/names-and-ids.json`)
### `vendor/map.html`
This is a map converted from a vector file provided by [Kanton Aargau](https://www.ag.ch/de/dfr/geoportal/themenkarten/download/Kartendownload.jsp)
### `colorcodes.py`
This contains a functions to calculate a colorcode based on the amount of articles about a city and the maximum amount of articles for a single city.
### `conda-environment.yaml`
The anaconda environment configuration used to run these scripts
### `config.py`
Contains basic configuration
### `crawl-cities.py`
Loads all cities from aargauerzeitungs API.
### `crawl-news.py`
Loads the required articles from aargauerzeitungs API.
### `visualize-articles.py`
Creates a javascript to color the map.
