# AZ-Crawler
A script that crawls through the articles on aargauerzeitung.ch, visualising the amount of articles per municipality on a html map.

These scripts work by first fetching all the required data using aargauerzeitung's json api, and the using html and javascript to display them on a map.

This script is my personal project work for the `matl` module at the FHNW.

## Running the script
It is recommended to use anaconda to run the script. An anaconda environment is included in the repository.
Run these command to activate the anaconda environment:

`conda env create -f conda-environment.yaml`

`conda activate spoorey-azcrawler`

Then run these scripts in this order:
1. `python crawl-cities.py` To store all the cities locally
2. `python crawl-news.py` To store the articles of the last three months for each city
3. `python visualize-articles.py` To visualize the amount of articles on the map

Then open `data/map.html` in your browser.
