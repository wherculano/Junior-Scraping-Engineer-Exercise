# Junior Scraping Engineer exercise

Please complete the following exercise and deliver it using either a zip file, or a private GitHub repository shared with the
GitHub user “belvo-hiring”.

Please use either Python or Javascript to complete the exercise.

Thanks!

Mission

Your mission is to write a program that will extract, as quickly as possible (eg. using threads or async programming), 
information from a few different blogs and websites:    
- https://www.theverge.com/ 
- https://www.phoronix.com/ 
- https://es.gizmodo.com/ 
- https://www.engadget.com/

Specifically. the program should:

- For each one of the websites above:

- Fetch its HTML

- Extract the RSS or Atom feed URL from the HTML

- Fetch the feed contents

- Extract the <title>, <pubDate> / <published> and <link> from the first 10 feed entries. Please note that you might have to parse the publishing date and/or deal with timezones.

- Save a JSON file containing the extracted information, sorted by descending publishing date

The program should be able to run using Docker on a Linux x86-64 machine.

# How to run it:
### 1. If you want to run the project using Docker:    
You must change *<desired_name>* for any name. i.e **belvo**    
``` 
$ docker build -t <desired_name> .
```    

In this point you need to use the name created i.e **belvo**
``` 
$ docker run -p origin_port:dest_port -d <image name>
``` 

To check the container id you need to run:
```
$ docker ps -a
```   
Now that you get/see the container id, just use it with the follow command:
``` 
$ docker start <container_id>
``` 
Now run this command to get inside you docker container:
``` 
$ docker exec -it <container_id> bash
``` 
Now that you're inside docker, just run ```python main.py``` and wait few seconds to generate the JSON file called **feeds.json**.    
And to check the content, just run ```cat feeds.json```

#### If you don't want to use Docker:
First you need to create a virtualenv and activate it:
```
$ python -m venv .venv
$ source .venv/bin/activate
```
Now you need to install the dependencies of the project    
```
$ pip install -r requirements.txt
```
Just run it:
```
$ python main.py
```
In few seconds the JSON file will be created.
The file name is **feeds.json**

