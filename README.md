## IMDB_Spider_By_Scrapy
This project crawls IMDb top 250 movies information by using Scrapy which is a "powerful web crawlling framework" with python.

### Structure
> spiders/IMDb_spider.py # parse crawled website into scrapy items

> movie_item.py
>   * MovieItem # Movie Item class
>   * MovieReview # Review Item for each Movie
>   * MovieStar # Movie star Item

> pipelines.py 
>   * handle the two items for saving to separated files
>   * Transfer item object to python dictionary(essentially they are same.)

> Outputs:(I didn't upload it to Git.)
>   * MovieItem.csv # save Movie Items
>   * MovieReview.csv # save Movie Reviews
>   * MovieStar.csv # save Movie star info

> spiders/settings.py
```python
# set for pipelines
ITEM_PIPELINES = {
   'IMDB_Spider.pipelines.Pipeline': 300,
}
```
> Movie_Analysis.ipynb
>  jupyter analysis report 

### How to use
Use console to the project folder, then run "scrapy crawl imdbspider", where `imdbspider` is project name which you can find in `IMDb_spider.py`.
```python
name = 'imdbspider'
allowed_domains = ['imdb.com']
start_urls = ['http://www.imdb.com/chart/top',]
```

### How scrapy works
![img](img/scrapy_workflow.jpg)
1. Engine gets request object from spiders(IMDb_spider.py)
2. Engine handles request object to scheduler
3. Engine gets next request from scheduler
4. Engine sends the request to downloader through middleware
5. Downloader sends response back to engine through middleware
6. Engine transfers response to spider for parsing
7. Spider creates scrapy Items and sends new request to Engine
8. Engine sends Items to pipelines
In this process, Engine will receive request from scheduler until it is emtpy. Framewrok starts with `start_url`, end with `pipelines`. 
Enigne, Downloader and Scheduler are already completed by framework. we need to code spiders and pipelines, also do
some configure stuffs.

### Some commands in scrapy
startproject: create a new project

genspider: create a spider

setting: get spider config info

crawl: start to run crawling

list: show all project names

shell: start URL parse

### Report
more information and code see [here](https://github.com/neoaksa/IMDB_Spider/blob/master/Movie_Analysis.ipynb)
1. star anlaysis
Accordig this breif table blew, we can find `Robert De Niro` took the most movies in top 250 list. Followed by `Harrison`,`Tom` and `Leonardo`.

![img](/img/num_movie.png)

165 movies in top 250 movies are performed by the 100 best stars who is defined that took more than one movie in the list. We picked up these 100 movie stars for future star research. 83% movie star only took one movie in the list.

![img](/img/num_movie2.png)

I picked up a few stars who took more than 2 movies in the top 250 list, and create a relationship netwrok for them.We can find the major 5 blocks, if we loose the filter, maybe we can find more.

![img](/img/social.png)

From picked 100 movie stars, most of them are born between 1930s to 1970s. California, Illinois, New Jersey are the states with most movie stars. Even so, none of state or regions is predominant.

![img](/img/city.png)

2. Movie Review Anlaysis
I use NLTK to spem the words and only picked adj and noun for word cloud. See which words are frequcely refereced in the best movies.

![img](/img/review.png)

I didn't do word sentiment anlaysis in this project, but you can find in my other project- [here](https://github.com/neoaksa/tensorflowDemo/tree/master/wordSentimentDemo).
