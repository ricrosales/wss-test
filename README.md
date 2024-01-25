# wss-test

Pipeline used to test Aineko WSS Node. This pipeline can be used to manually verify that WebSockets return data as expected.

## Setup development environment

```
poetry install
```

## Running the pipeline

First, make sure that docker is running and run the required docker services in the background

```
poetry run aineko service start
```

Then start the pipeline using. Note you must prepend the aineko run command as shown in order 
to inject environment variables from the .env file into the pipeline.
```
env $(cat .env | xargs) poetry run aineko run conf/websocket.yml
```

## Observe the pipeline

To view the data flowing in the datasets

```
poetry run aineko stream wss_test.coinbase
```

To view all data in the dataset, from the start

```
poetry run aineko stream wss_test.coinbase -b
```


## Taking down a pipeline

In the terminal screen running the pipeline, you can press `ctrl-c` to stop execution.

Clean up background services
```
poetry run aineko service stop
```
