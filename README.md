# Dukaan Prototype - A Production Grade Dukaan MVP 
## **Django+PostgreSQL+Redis+Nginx+Gunicorn+Docker Compose 🔥 🔥 🔥**

## Quick Introduction:
This project is a production grade MVP of [Dukaan](https://mydukaan.io/)(DIY platform to create your own E-Commerce store).\
In this project I've used Django for the backend, PostgreSQL for production database, Introduced caching(Redis) mechanism  \
for increasing the throughput of the server and used event+time driven caching invalidation mechanism for invalidating cache. \
Used Gunicorn for the production server, Nginx for revrese proxy and for serving static files. \
Then I have Dockerize my project into 4 containers. i.e Web(Django+Gunicorn), db(PostgreSQL), redis_db(Redis), nginx(Nginx). \
And finally I've used Docker Compose for running multiple containers as a single service. 

## Infrastructre Diagram of Dukaan Prototype:

![Screenshot_20220413_132548](https://user-images.githubusercontent.com/43638955/163128761-9b3b7830-f47a-41af-b9e0-bca5f602f1b9.png)

## Web App walkthrough
(Note: While creating the project my aim was to focus enterily in the Backend part and to implement state of the art Backend Infra. \
So, I've created a very simple frontend by using just html and css. I'm able to do this by leveraging DTL and using my engineering jugadu mind) \
\
The web app is having minimal functionality of [Dukaan](https://mydukaan.io/). i.e Vendors can add their products and manage them using a dashboard. \
Then there is a unique link for each vendor which they can send to their customers. By using this unique link, customers can place the order \
by entering the neccesary details. Each placed orders then are displayed in the order's dashboard of vendor. \
Below are the snapshot of the web app. \

Signup Page (``` ```)
![Screenshot_20220413_163418](https://user-images.githubusercontent.com/43638955/163236389-9ca3a6fd-738d-49c5-a9a4-dd6afc2b1061.png)

Login Page (``` ```)
![Screenshot_20220413_163433](https://user-images.githubusercontent.com/43638955/163238161-c0d5ca4e-4c3b-4f0a-8495-1d510c69499b.png)

Vendor's "Your Product Dashboard" (``` ```)
![Screenshot_20220413_163450](https://user-images.githubusercontent.com/43638955/163243533-a14b686f-344a-4b52-b197-f6451000ebec.png)

Vendor's Add NeW Product Form  (``` ```)
![Screenshot_20220413_163732](https://user-images.githubusercontent.com/43638955/163243670-22fa5c72-704b-4101-8b3a-68f1299abde8.png) 

Unique Link To Buy Product From vendors (``` ```) 
![Screenshot_20220413_163830](https://user-images.githubusercontent.com/43638955/163243921-0fd9450b-41a3-4e38-8462-19d3afac5d0e.png)

Vendor's Your Orders Dashboard (``` ```)
![Screenshot_20220413_164202](https://user-images.githubusercontent.com/43638955/163244767-b4fc0925-1954-440e-9d4b-087ae108753f.png)

## Optimization using caching mechanism 
Suppose there's a sale for a vendor's dukaan shop. Then there's gonna be high traffic for our backend server. \
For each request of client django is going to do costly query in the db. Because of this the throughput of the \
server is gonna be decrease drastically. \ 
Let's test throughput speed by bursting 100 requests in the vendor's unique link(I have already populated the db with dummy data) 
\
![ezgif com-gif-maker](https://user-images.githubusercontent.com/43638955/163250445-dbf53914-c072-4979-8e98-e52bf2344f74.gif) \
For completing 100 requesting it's taking around ``` 3.38 sec ```. Pretty slow right? \
\
For copinng with this problem I've implemented caching mechanism(redis). Which create a view level cache for each vendors \
```order``` view.
\
Now, let's again test throughput speed by bursting 100 requests in the vendor's unique link but this time having cache enabled .
\
![ezgif com-gif-maker(1)](https://user-images.githubusercontent.com/43638955/163252685-5f4f7f4f-770a-4468-ac4e-50b7a5c78bad.gif)

Insane, this time it take only ```0.95 sec``` to process 100 requests. Which is roughly ```72%``` increase in throughput 🔥 🔥 🔥 \

But what happened when the vendor added a new product or make the product unavailable? The customers are still geting the cached page. \
For this problem we've to invalidate cache. Cache Invalidation is a crucial part in any caching mechanism. 
I've implemented two cache Invalidation technique.
1. Event based cahce invalidation.
2. Time Based cache Invalidation.

Let's see it in action and monitor what is happening underhood using ```redis-cli monitor``` command. \
When the customer first visits the unique url ``` ``` then django will accept the request do some query in the ```Product``` model \
and then first **cahced** the response and then send the response back to the customer.
After that any subsequent request to the unique url will not hit the db rather than it'll get the requested page from the cache which is stored\
in Redis memory.
\
1. When the customer first the unique url ``` ``` then this request hit the db do the query and generate the page. \
and this page is then stored in the Redis Memory. \
You can see the ```$SET``` redis command is executed for storing the cache.
![r1](https://user-images.githubusercontent.com/43638955/163332657-a2887bd3-5ff9-4a99-8c71-8a7fc4bc02e5.png)
2. When we reload the page you can see that this time django is not hitting the db and doing  the costly query \ 
but rather than it's getting the requested page from Redis Memory.
You can see the ```$GET``` redis command is executed for sending the requested page.
![r2](https://user-images.githubusercontent.com/43638955/163333322-f5d7f8eb-b583-4005-9eec-16799f319d7c.png)
3. Whenever the vendor is doing any modification in the ```Product``` model we're inavalidating the stored cahce.\
   i) Event Based Cache Invalidation: Whenever the vendor is adding "New Product" or making the available product \
    available/unvaliable by using toogle "yes" or "no" buttons, we're Invalidating the cache.\
   ii) Time Based Cache Invalidation: All the stores cached will automatically gets invalidated after ```15 mins```\ 
 When we're making one of the product unavailable the cache are getting Invalidated.
 You can see the ```$DEL``` redis command is executed for Invalidating the cache.
![r3](https://user-images.githubusercontent.com/43638955/163333354-fec19299-23a6-4b82-880e-157abf2e4fd7.png)










