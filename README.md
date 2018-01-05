# webmc3
A web interface for exploring [PyMC3](https://github.com/pymc-devs/pymc3) traces, inspired by [ShinyStan](https://github.com/stan-dev/shinystan) and built with [Dash](https://github.com/plotly/dash).

![webmc3 demo](https://media.giphy.com/media/3ohc18OfTZ2poulJII/giphy.gif)

Consult the [quickstart notebook](/docs/notebooks/Quickstart.ipynb) to start using `webmc3`.

## Development

The simplest way to develop `webmc3` is to use the [Dockerfile](/Dockerfile).

First build the image.

```bash
docker build -t webmc3 .
```

Next launch a container using the image.

```bash
docker run -d \
    -p $JUPYTER_PORT:8888 \
    -p $DASH_PORT:8050 \
    -v `pwd`:/home/jovyan/webmc3 \
    --name webmc3 webmc3 \
    start-notebook.sh --NotebookApp.token=''
```

There will not be a Jupyter notebook server available at `http://localhost:$JUPYTER_PORT/tree` and, once running, the `webmc3` app will be available at `http://localhost:$DASH_PORT`.  Most importantly, your fork of `webmc3` is on the `PYTHONPATH` in the container.
