#!/bin/bash
source virtualenvwrapper.sh
export PATH=/root/.virtualenvs/canivote/bin:$PATH
export PYTHONPATH=/root/.virtualenvs/canivote/lib:/home/canivote/can-i-vote/vote
killall gunicorn
/root/.virtualenvs/canivote/bin/gunicorn -w 4 www:app -D --log-file /tmp/gunicorn.log -b 127.0.0.1:8000