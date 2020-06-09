# PROJECT TITLE

TODO: Add a short description of the project.
It should include the following:
- What this repository is
- Who is it for
- What are the dependencies 

## Usage

- Have python 3.7
- Create virtual environment:
  
  ```shell
  python3 -m venv .venv
  source .venv/bin/activate
  ```

- Install required dependencies:
  - PostgreSQL
  - Redis
  - `pip install -r requirements.txt`
- Setup environment variables - in an `.env` file in the root directory
  
  ```shell
  POSTGRES_CONNECT="postgresql://DB_USER_NAME:@localhost:5432/DB_NAME"
  IEX_ACCOUNT="YOUR_IEX_PUBLIC_KEY"
  IEX_KEY="YOUR_IEX_SECRET_KEY"
  SKEY="SOMETHING"
```

- Make sure Postgres is running
- Make migrations
  - `flask db init` <-- likely unnecessary
  - `flask db migrate`
  - `flask db upgrade`

- `flask run`

----

- visit /login -> create user (this should redirect)
- visit /build_portfolio -> pick some stocks (this should redirect to / -> dashboard with suggestions for stocks)
- visit / -> dashboard, see stocks being suggested


TODO: Specify how to use this project
This can include running the scripts, or where to find API docs if it's a library, command line tool, or similar.

## Repository Contents

TODO: Specify what this repository contains, for example if it contains multiple self contained sub-projects, like with Notebooks scripts that can be used independently.

In some cases you can skip this section.

## Setup/Installation

TODO: Specify what's required to set this project up for usage

In some cases you can skip this section.

## Development and Contributing

If you'd like to report an issue or bug, suggest improvements, or contribute code to this project, please refer to [CONTRIBUTING.md](CONTRIBUTING.md).


# Code of Conduct

This project has adopted the Contributor Covenant for its Code of Conduct. 
See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) to read it in full.

# License

Licensed under the Apache License 2.0. 
See [LICENSE](LICENSE) to read it in full.


