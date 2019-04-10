#!/bin/sh
ls
echo $PWD
python update_sched.py
python update_players.py
python app.py