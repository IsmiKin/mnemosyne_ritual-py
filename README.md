# Name inspiration

In Greek mythology, Mnemosyne is the Titaness of memory and remembrance.
She embodies the concept of memory, both individual and collective, and is associated with the preservation of knowledge and stories. 


# Setup

## Pre-requisites

In order to run the script you will require Python v3.13 with Pipenv or use docker with docker-compose along.

```
brew install docker
brew install docker-compose

make build
```


## Data
You will need to prepare a `csv` file as the one provided in a folder, for example: `mock_data/reviews.csv`

## Up services
In order to make it easy, you can just use the instructions in the `Makefile`

There are different services setup in the `docker-compose.yaml`

The instructions are already prepared to up the required Python environment to run the script with the dependencies and also a PostgresSQL instance to store the results.

```
# to up the services
$ make up-dev

# to up all services and attach to the bash to run the CLI script
$ make attach-dev: up-dev
```

## Services

Just for the sake to give a bit more clarity in the orchestration, following is the descriptions of the services when the `docker-compose` scripts are runned through the `Makefile` instructions.

### db
This is an PostgresSQL instance to store the results of the "sitter_scores" calculated during the process. It's the same result that is being written in the new CSV file.

### adminer
A simple web application to connect to the PostgresSQL instance; in case you required to check the data stored in the database without using a SQL client.

### migration
This service is preparing the database structure using Alembic and a set of migrations. This allow to continue evolving the database tables structure.
It requires the db service is on.

### mnemosyne
It's the service container to run the CLI script, it's the one you will get attached with the `Makefile` instruction.

# Run

Once you are attached in the docker container you can get info regarding the CLI script methods:

```
$ python ./src/main.py --help
```

## Process a file

To process the file given as example you just need to run the "process_file" CLI method and given it as argument.

```
$ python ./src/main.py process-file mock_data/reviews.csv
```

This will create a "reviews-output.csv" following the `"{filename}-output.csv"` format.

### Persist in the DB
You must pass the flag `--db-persist` ; you don't need to do anything also due the fact all the configuration required it's on the `docker-compose.yaml` already.

```
$ python ./src/main.py process-file mock_data/reviews.csv --db-persist
```

## Run tests

The tests are setup for `pytest`, you can run then directly or with the make instruction (which also includes coverage report)

```
$ make tests
$ pytest
```

# Output file

The exercise output file is called "mnemosyne_ritual.csv" and in it's in the "output" folder