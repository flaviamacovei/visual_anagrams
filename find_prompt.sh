#!/bin/bash

ollama serve &

cmd="python find_best_prompt.py"
echo $cmd > find.sh
chmod 755 find.sh
./find.sh
