# Task [№17](https://devman.org/challenges/17/) from [devman](https://devman.org)
## Purpose
Script reads file with sites urls, then checks if site responds with status 200,
 and checks domain expiration date (is domain paid for at least a month), then
 print out results. 
## Requirements
```
Python 3.5.2+
python-whois
requests
python-dateutil
chardet
tqdm
```
## Setup
```
git clone https://github.com/ram0973/17_sites_monitoring.git
cd 17_sites_monitoring
pip3 install -r requirements.txt
```
## Usage
Specify the path to the file with the list of site urls, which should be checked.
Url must necessarily be with scheme, for example: https://
It's possible to use second-level domains and below (third, etc.).
Prints: url site, does the site responds with HTTP 200 code,
domain expiration date, whether the domain is paid for at least a month.
## Run
python3 check_sites_health.py --i file_with_urls
## License
[MIT](http://opensource.org/licenses/MIT)
