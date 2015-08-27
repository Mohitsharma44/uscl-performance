
USCL Performance
========
This repository contains code that was written by me to serve the purpose of providing the input on CUSP's USCL students code quality.

This repository contains:
- Server: That uses [motor](https://motor.readthedocs.org/en/stable/) for performing asynchronous querry to the mongodb. The server is written in python using [tornado](http://tornado.readthedocs.org/en/latest/guide.html) package for serving asynchronous queries. This server does not perform any load balancing/ sanity check of the input etc. You need to implement your own checks (which shouldn't be difficult)
- Client: Client simply queries the server for students performance data and plots it using Matplotlib.
- pylintrc: This file provides configuration options for pylint which is being used to statically check the code quality.
- Some other helper functions that performs uncompressing the compressed files, removing special characters etc.

## Installation
### On Server:
**Running DB server:**

* `sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10`
* `echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list`
* `sudo apt-get update`
* `sudo apt-get install -y mongodb-org`

**Python wrapper for mongo:**

* `pip install pymongo==2.8`

**Hosting Asynchronous server:**

* `pip install tornado`

**Performing Asynchronous DB access:**

* `pip install motor`

**Performing Uncompression etc:**

* `pip install patool`
* `pip install pyunpack`

**Fancy progress bars: (Optional)**

* `pip install pyprind`

## Server
Using the server is really easy. The output provided by NYU for students submission is something in this format: 
```
<assignment name>/<Student name>/Submission Attachments/name of the file.py or .zip or .tar.gz etc
```
* First, I need to uncompress the files. For this I use `unzip_all.py` script which uses `pyunpack` and `patool`packages. This module traverses the entire `BASE_DIR` that you provide (recursively) and uncompresses any compressed file that it finds.

* Second, this has something to do with my OCD on finding special characters the filename or its path (base directories) etc. To convert all these special characters into `underscores`, I run `illegal_char_remove.py`. This file traverses the `BASE_DIR` and replaces special characters with underscores.

* Finally, I perform the sanity checks and store the output data in a mongo database. To do this, run `add_to_db.py` (I know.. I am bad with names for modules.) This module runs the code checker, stores the output in json format, adds the username to the object and pushes it to the database. Some students have copy pasted their code from ipython terminal (which I cannot analyze). My code will not push such codes to the database. 

* If you do not like seeing the scrolling list of usernames that my code is analyzing or adding to DB, you can uncomment the `pygrind` import and comment all the print statements and uncomment the syntax that uses `ProgBar` (These should be near the print statements).

* To host this database on your server, just run the `web.py` with optional command line parameters for specific port number (`--port`). If this optional argument is not provided, the server by default listens on port `8888`. If running locally, you can check the working of server on `http://localhost:8888/check` You should see a form asking for an input. This is where you enter the query that you would like to perform on the database (Depending on what you have created the database for)

* You can also type: `http://localhost:8888/api?username=<some_query>` This is basically the api part of the server parsing your request. 

## Client:
* Client code is very simple. You basically pass your querry as a dictionary in `query_args`. Then you parse the json object and (if multiple json objects) store the output as list of individual json objects.

* After this, I am parsing the students grades and plotting them using matplotlib. The code can currently only plot for single json object data (only one submission per student) but it shouldn't be difficult to modify this and plot data for multiple submissions.

* Take a look at `[using_uscl_api.ipynb](https://github.com/Mohitsharma44/uscl-performance/blob/master/using_uscl_api.ipynb)` for more information.

PS: If you are this server or modified version of this server, it is recommended to use it behind a load balancer (provided by [nginx](http://wiki.nginx.org/Main)) and monitored by [Supervisord](http://supervisord.org/)