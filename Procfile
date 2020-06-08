#####################
# HEROKU DEPLOYMENT #
#####################

# Spawn 3 workers: https://stackoverflow.com/questions/59391560/how-to-run-uvicorn-in-heroku
web: gunicorn backend.main:api -w 3 -k uvicorn.workers.UvicornWorker