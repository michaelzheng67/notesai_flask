#!/bin/bash

curl -H 'Content-Type: application/json' \
      -d '{ "uid":"NmjO6WwswsbA5B8YTwFW8t1vzRw2"}' \
      -X POST \
     https://notesai-flask.onrender.com/create-chroma &>/dev/null &