#!/bin/bash

ollama serve &

names=("rabbit-duck-flip", "abc")
prompts=("'a rabbit' 'a duck'", "'a horse' 'a house'")
styles=("'a sketch of'" "'a sketch of'")
views=("'identity' 'flip'" "'identity' 'flip'")
result_file="result_file.txt"
rm -f $result_file

for i in ${!names[@]}; do
  name=${names[$i]}
  prompt=${prompts[$i]}
  style=${styles[$i]}
  view=${views[$i]}
  cmd="python generate.py --name "$name" --prompts "$prompt" --views "$view" --style "$style" --num_samples 1 --num_inference_steps 30 --guidance_scale 10.0 --generate_1024"

  # write the command into a file
  echo $cmd > one_run.sh

  # change the rights of the file : make it executable 
  chmod 755 one_run.sh

  # run the file
  ./one_run.sh

  image_dir=`pwd`/results/$name
  picture=$image_dir/0000/sample_1024.views.png

  cmd2="python analyse_image_ollama.py --path "$picture" --targets "$prompt" --views "$view
  result=`python my_script.py`

  echo $cmd2 > one_run.sh
  ./one_run.sh
  result=$?

  if (($result == 1)) ; then
    echo "prompts: "$prompt >> $result_file
    echo "views: "$view >> $result_file
    echo "" >> $result_file
  fi

  rm -rf $image_dir
done
