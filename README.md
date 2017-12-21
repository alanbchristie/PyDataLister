# PyDataLister
A very simple Python 3 container test application that lists files in the
directory defined by the `DATA_PATH` environment (`/data' by default) before
optionally consuming memory and CPU cycles using multiple threads for the
purpose of _stress-testing_ a container run-time environment.

Basically something can be launched as an [OpenShift] v3.6 [Job].

The image is configured using a number of environment variables,
documented in `app.py`:

-   DATA_PATH
-   PRE_LIST_SLEEP
-   POST_LIST_SLEEP
-   POST_SLEEP_BUSY_PERIOD
-   BUSY_PROCESSES
-   USE_MEMORY_M

You should be able to build and run the containerised app using
any suitably equipped Docker host. I used a `Mac` and Docker
community edition `v17.09.1`.

## Building
Build and tag the image...

    $ docker-compose build

And run it locally (in detached/non-blocking mode)...

    $ docker-compose up

## Deploying
Here, we'll deploy to the Docker hub. It's free and simple. We just need to
tag our image (with something useful like `2017.1`) and then push it.

    $ docker login -u alanbchristie
    [...]
    $ docker-compose push

---

[Job]: https://www.openshift.org
[OpenShift]: https://www.openshift.org

_Alan B. Christie_  
_December 2017_  
