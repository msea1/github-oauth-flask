# github-oauth-flask

## Environment Prep

1. Create a new virtualenv. This can be done using the python interpreter of your choice. E.g.
   `python3.10 -m venv $HOME/.virtualenvs/crescendo`, with the path arg being wherever you normally
   store venvs.
2. Active the virtual environment: (`source $HOME/.virtualenvs/crescendo/bin/activate`)
3. Upgrade the pip: `pip install --upgrade pip steuptools wheel`
4. Install requirements: `pip install -r requirements.txt`

## Heroku Deployment

1. If you do not already have a heroku account, create one
2. Run `heroku create realpython-example-app`
3. Run `git push heroku main`

An example of this is running [here](https://github-oath-flask.herokuapp.com/).


## Testing

Testing is done via `pytest` and `pytest-flask`. They are listed among the requirements. From the
repo directory, and working in your virtual environment, you can just run `pytest`.