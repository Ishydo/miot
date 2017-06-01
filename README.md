# My Internet Of Things - miot

A simple but complete Web platform for you to create IoT / Physical Web oriented content. Beacons can provide an
additive second-screen experience for visitors in a lot of contexts or places. This platform allows you to easily
create optimized content for mobile devices with different templates and layouts. That means : you can propose a
unique experience for users / visitors / curious people by defining places, events and points of interest and
attach attractive content to it.

## How to deploy

## The docker way

First, create a ```docker.env``` file containing the environment vars :

**Do not change the ```MIOT_DB_HOST``` value !**

```
MIOT_DB_NAME=miot
MIOT_DB_USER=miotuser
MIOT_DB_PASSWORD=password
MIOT_DB_HOST=db
MIOT_SECRET=YOUR_DJANGO_SECRET_KEY_HERE
MIOT_GOOGLEMAP=YOUR_GOOGLE_MAP_API_KEY_HERE
```

Then all you got to do is ```docker-compose up```


## Manual local deployment

## Physical Web, feed it with good content

The concept of the Physical Web is to stream simple URLs using Beacons. The main advantage is that users do not need a specific
app anymore. This technology is supported by default on Android devices, all you need is to have a Beacon configured to stream your
URL and you are ready to go !

The question is what URL do I stream with my Beacon ? What content will be attached to my point of interest ?

A wikipedia page ? - _Nah, it's too technical and basique_

A youtube video ? - _Meh, you don't know if they will watch it... and it's too loudy_

A website homepage ? - _Totally out of context_

**What about a good miot Physical Web optimized page ? - Great idea !**


### Links

> Beacons will provide an additive second-screen experience for museum visitors

http://www.mobilemarketer.com/cms/news/software-technology/19672.html
