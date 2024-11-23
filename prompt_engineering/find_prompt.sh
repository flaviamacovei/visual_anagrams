#!/bin/bash

ollama serve &

cmd="python find_best_prompt.py"

echo "#!/bin/bash" > find_run.sh
echo $cmd >> find_run.sh
chmod 755 find_run.sh
./find_run.sh
