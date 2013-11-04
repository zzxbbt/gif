# ekron

Turn a movie segment into a gif!

## Dependencies

* [envoy](https://github.com/kennethreitz/envoy)
* [ffmpeg](http://www.ffmpeg.org/)

### Install them!

Install ffmpeg using your package manager, e.g. brew or apt-get:

    brew install ffmpeg
    apt-get install ffmpeg

You also need the *envy* python module:

    pip install -Ur envoy

## Creating your first gif

    ./ekron.py -i dQw4w9WgXcQ.mp4 -o rick.gif -s 00:00:05.5 -e 00:00:07.0

![rick](FIXME)
