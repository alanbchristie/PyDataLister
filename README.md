# PyDataLister
A very simple Python application that lists files in the directory
defined by the `DATA_PATH` environment (`/data' by default) before
sleeping for a few seconds and leaving.

A super-simple OpenShift `Job`.

You should be able to build and run the containerised app using
any suitably equipped Docker host. I used a `Mac` and Docker
community edition `v17.06.2`.

## Building
Build and tag the image...

    $ docker-compose build

And run it (in detached/non-blocking mode)...

    $ docker-compose up

## Deploying
Here, we'll deploy to the Docker hub. It's free and simple. We just need to
tag our image (with something useful like `2017.1`) and then push it.

    $ docker login -u alanbchristie
    [...]
    $ docker-compose push

---

_Alan B. Christie_  
_October 2017_  
