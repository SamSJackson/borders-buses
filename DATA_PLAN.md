# Live Data Storage Plan

We can scrape data from borders-buses every 30 seconds, theoretically. 

Our goal is to collect all travel information of borders-buses between 5am and 10pm, for 30 days.
This requires scraping for 17 hours, and not being active within the other periods.

Given that I do not want my computer on for 24 hours a day, for 30 days, this seems like a good opportunity to use cloud computing.

## Requested Data

The requested data returns information about each bus travelling on the given route.

For each bus, we are provided the following information:


| key | dtype | 
| --- | ----- | 
| coordinates | array[float64] |
| direction | string | 
| line | string | 
| operator | string | 
| vehicle | string | 
| href | string | 
| number\_plate | string | 
| fleet\_number| string | 
| type | string | 
| make | string | 
| model | string | 
| levels | int | 
| payments\_contactless | boolean |
| wheelchair\_capacity | int | 
| low\_floor | boolean | 
| tenant | string | 
| bearing | int |
| compassDirection | string | 
| background | string | 
| foreground | string | 

We don't need all of this information if our goal is simply to determine how late a bus isto a stop.

We strictly require: ```coordinates, direction, vehicle, bearing, fleet_number ```

``` bearing ``` and ``` fleet_number ``` are not strictly necessary but since this will take a month to run, I am going to err on the side of caution and take this information anyway. Furthemore, they are both ints, with bearing < 360, so it can be a 9-bit integer.

Hence, our table for data will look as follows: 

| vehicle | fleet_number | direction | bearing | coordinates        |
|---------|--------------|-----------|---------|--------------------|
| Y717JSW | 11719        | inbound   | 257     | [-2.5321, 55.3219] |

(The data is just an example and made-up, not valid data).

## Real-Time Running

How am I going to run this thing? I have spent time looking for a way to run this on the cloud at a cheap price.

The good news is that I can achieve this cheaply because the processing time is slow for the code - just need to make the request.

The bad news is that most cloud services don't provide the ability to spin-up instances tomake a request at sub-minute frequency. In fact, I have not found any that go lower than what cron-scheduling can provide.

However, Google Cloud and the fine internet have provided a solution.
Create a cron-scheduler which, every minute, schedules one service run (the python script)to happen now and create another service run that will run in 30 seconds. 

We can schedule a wait time on the service thanks to Google's Task Scheduler. On top of this, the Task Schedular and cron will provide warning if a service fails to run, which is useful.

However, since this is not high intensity and missing some data requests is not breaking, I will not be focusing on significantly on ensuring re-tries of service runs.

## Storage Plan

As I am forced into Google Cloud's ecosystem by the 30s request interval, my storage will also, inevitably, be a Google product.

From earlier, I already have a table and the frequent inputs (30s) suggest that we are best with a relational database, such as MySQL or PostgreSQL. 

I am fortunate in that I am only inserting data to the end of table. This means no sorting, no deleting, no updating, no indexing and no querying. Very fast.

The highly frequent insertions is what pushed me away from using BigQuery - despite being cheaper per GB - because BigQuery is not quick to insert and the more time spent inserting, the longer the service has to run for. 

Between MySQL and PostgreSQL, I am going to go for MySQL. Arguably, PostgreSQL is better for insertions but I believe that the difference is negligible for 3 insertions every 30 secnods. Furthermore, PostgreSQL will most likely be overcomplicated for a database with one schema and, at most, 3 tables.

The schema design is as follows:


