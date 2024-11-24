#!/bin/bash

prompts=("'a rabbit'" "'a duck'" "'a kitten'" "'a puppy'" "'marylin monroe'" "'albert einstein'" "'houseplants'" "'a deer'" "'a kitchen'" "'a giraffe'" "'a penguin'" "'a botanical garden'" "'an old woman'" "'a dress'" "'a truck'" "'vases'" "'a sloth'" "'a fish'" "'a duck'" "'an old man'" "'people at a campfire'" "'a forest fire'" "'a car'" "'a horse'" "'a snowy landscape'" "'a table'" "'a waterfall'" "'a library'" "'a theater'" "'a canyon'" "'a maine coon'" "'a goldfish'" "'the queen of england'" "'a snowy mountain village'" "'a mountain landscape'" "'a teddy bear'" "'a man'" "'a woman'" "'a chair'" "'a skull'" "'a tudor portrait'" "'a lemur'" "'a kangaroo'" "'a young man'" "'a beach'" "'a farm'" "'elvis'")
styles=("'a watercolor of'" "'an oil painting of'" "'a drawing of'" "'a photo of'" "'a pencil sketch of'" "'a painting of'" "'a pop art of'" "'a lithograph of'" "'a mosaic of'" "'a charcoal drawing of'" "'a pixel art of'" "'a digital art of'" "'a stained glass of'" "'a tapestry of'" "'a 3d render of'" "'a ceramic tile of'" "'a cubist artwork of'" "'a graffiti art of'" "'an impressionist painting of'" "'a collage of'" "'a woodcut of'")
views=("'color_rotate_gbr'" "'color_rotate_brg'")
result_file="result_configs/color_rotate_results.txt"
rm -f $result_file

for i in ${!prompts[@]}; do
  for j in ${!prompts[@]}; do
    # if prompts are equal: continue
    if (($i == $j)); then
      continue
    fi
    for k in ${!styles[@]}; do
      for l in ${!views[@]}; do
        prompt=${prompts[$i]}" "${prompts[$j]}
        style=${styles[$k]}
        view=${views[$l]}
        name=${prompt// /_}"-"${style// /_}"-"${view// /_}
        cmd="python generate.py --name "$name" --prompts "$prompt" --views 'identity' "$view" --style "$style" --num_samples 1 --num_inference_steps 30 --guidance_scale 10.0 --generate_1024"

        echo "executing "$cmd

        # write the command into a file
        echo "#!/bin/bash" > color_run.sh
        echo $cmd >> color_run.sh

        # change the rights of the file : make it executable
        chmod 755 color_run.sh

        # run the file
        ./color_run.sh

        image_dir=`pwd`/results/${name//\'}
		line_count=`ls -la $image_dir/ | wc -l`
		echo $line_count
		if (($line_count >= 4)); then
          picture=$image_dir/0000/sample_1024.png

		  echo "analysing image"
		  cmd2="python poseval.py --path "$picture" --targets "$prompt" --views 'identity' "$view
  
		  echo "#!/bin/bash" > color_run.sh
		  echo $cmd2 >> color_run.sh
		  ./color_run.sh
		  result_poseval=$?
		  echo "result poseval: "$result_poseval

		  if (($result_poseval == 1)); then

			cmd3="python negeval.py --path "$picture" --targets "$prompt" --views 'identity' "$view" --fault is"
			echo "#!/bin/bash" > color_run.sh
			echo $cmd3 >> color_run.sh
			./color_run.sh
			result_negeval_is=$?
			echo "result negeval is: "$result_negeval_is


			cmd4="python negeval.py --path "$picture" --targets "$prompt" --views 'identity' "$view" --fault ds"
			echo "#!/bin/bash" > color_run.sh
			echo $cmd4 >> color_run.sh
			./color_run.sh
			result_negeval_ds=$?
			echo "result negeval ds: "$result_negeval_ds
		  
			if (($result_negeval_is == 0 && $result_negeval_ds == 0 )) ; then
			  echo "success"
			  echo "prompts: "$prompt >> $result_file
			  echo "style: "$style >> $result_file
			  echo "views: 'identity' "$view >> $result_file
			  echo "" >> $result_file
			fi
		  fi
		fi
        rm -rf $image_dir
      done
    done
  done
done
rm -rf color_run.sh
echo "process finished"

#tmux: color
