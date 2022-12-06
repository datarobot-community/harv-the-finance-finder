**Please note:** The code in these repos is sourced from the DataRobot user community and is not owned or maintained by DataRobot, Inc. You may need to make edits or updates for this code to function properly in your environment.

# Harv the Finance Finder 📈

This is a demo application showcasing how to use DataRobot's machine learning products to find and filter items in a financial context.

This is intended as an educational, technology showcase app, uses fake data, and is in no way a recommendation service.

You can also read the accompanying tutorial at DataRobot's developer documentation site: https://api-docs.datarobot.com/docs/finance-finder-batch-predictions.

## Usage

You can access the deployed version at the following link: [harv-the-finance-finder.herokuapp.com](https://harv-the-finance-finder.herokuapp.com).

Alternatively, you can also run it yourself 👇

### Building it yourself

The app is a Flask application with a set of Python scripts to train and deploy a ML model. Follow these steps:

- Have python 3.7 (likely ships with your OS)
- Create virtual environment:
  
```shell
python3 -m venv .venv
source .venv/bin/activate
```
- Create a DataRobot account. You can request a trial at https://datarobot.com/lp/trial. 
- Create an IEX Cloud account (Optional) - they provide financial data. The app comes with pre-generated datasets already.

- Install required dependencies:
  - PostgreSQL
  - Python dependencies: `pip install -r requirements.txt`

- Make sure PostgreSQL is running 

- Setup environment variables - in an `.env` file in the root directory, replacing the following with your own:

```shell
  POSTGRES_CONNECT="postgresql://DB_USER_NAME:@localhost:5432/DATABASE_NAME"
  IEX_ACCOUNT="YOUR_IEX_PUBLIC_KEY"
  IEX_KEY="YOUR_IEX_SECRET_KEY"
  SKEY="ANY_SECURE_STRING_FOR_FLASK"

  DATAROBOT_API_KEY="YOUR_DR_API_KEY"
  DATAROBOT_URL="YOUR_DR_URL"
```

- For the DataRobot credentials and URL you can find where to find them in our documentation site: https://api-docs.datarobot.com/docs/api-access-guide

- Make sure Postgres is running and you have a database created.

- Run database migrations scripts: `flask db upgrade`
- Seed data in your database: `flask seed_data`
- `flask run` to run the app

- Visit the running app: `https://localhost:5000`

- visit /login -> create user (this should redirect automatically)
- visit /build_portfolio -> pick some stocks (this should redirect to / -> dashboard with suggestions for stocks)
- visit / -> dashboard, select a portfolio, see stocks that are suggested for you

### Steps to deploy on Heroku

You can deploy the app to Heroku.

1. Create new app: `heroku apps:create`
2. Push to git: `git push heroku master`. This will install all dependencies.
3. Add Heroku Postgres as Heroku addon in the dashboard
4. Copy over Postgres config var to `POSTGRES_CONNECT` - by default it's stored as `DATABASE_URL`
5. Run DB migrations: `heroku run "flask db upgrade"`
6. If using the attached dataset: `heroku run "flask seed_data"` - you can also optionally first run the script to generate and load new data. This should take a few minutes. The final message should say "Seed Esgs complete"
7. Set the rest of the environment variables: To run on Heroku you just need `SKEY` - set to anything. This isn't checked, but Flask requires it.
8. Head over to the app that Heroku has deployed.

## Development and Contributing

If you'd like to report an issue or bug, suggest improvements, or contribute code to this project, please refer to [CONTRIBUTING.md](CONTRIBUTING.md).


# Code of Conduct

This project has adopted the Contributor Covenant for its Code of Conduct. 
See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) to read it in full.

# License

Licensed under the Apache License 2.0. 
See [LICENSE](LICENSE) to read it in full.


