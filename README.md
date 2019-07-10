# knowledge-panel-scraper
knowledge-panel-scraper is a Python 3 command line tool that scrapes Google's [Knowledge Panels](https://support.google.com/business/answer/6331288?hl=en) to retrieve the phone numbers, addresses, and hours of an inputted list of businesses.

## Installation

Use git to clone the repository, then install required libraries with the package manager [pip](https://pip.pypa.io/en/stable/).

```bash
git clone https://github.com/jnovak98/knowledge-panel-scraper.git
cd knowledge-panel-scraper
pip install -r requirements.txt
```

## Usage
```bash
python knowledge-panel-scraper.py inputfile.csv
```

inputfile.csv should be a plain text CSV file with each row containing data to generate a search query for a specific business.
For example:
```csv
"Bobcat of Monroe,Monroe,NC",1711 MORGAN MILL ROAD,MONROE,NC,28110,(704) 289-2200
"Kelly's Garage,Perry,NY",2868 STATE ROUTE 246,PERRY,NY,14530,(585) 237-2504
"Hoxie Implement Co,Hoxie,KS",933 OAK AVENUE,HOXIE,KS,67740-0587,(785) 675-3201
"Duhon Machinery,St. Rose,LA",10460 WEST AIRLINE HIGHWAY,ST. ROSE,LA,70087,(504) 466-5495
```

The results will be saved in results.csv in the same directory.

## Contributing
Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)
