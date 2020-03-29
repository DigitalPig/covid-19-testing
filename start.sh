#!/bin/bash

source activate covid
gunicorn --bind 0.0.0.0:$PORT wsgi
