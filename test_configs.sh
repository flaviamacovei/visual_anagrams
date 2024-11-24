#!/bin/bash

ollama serve &

prompts=("'a rabbit'" "'a duck'" "'a kitten'" "'a puppy'" "'marylin monroe'" "'albert einstein'" "'houseplants'" "'a deer'" "'a kitchen'" "'a giraffe'" "'a penguin'" "'a botanical garden'" "'an old woman'" "'a dress'" "'a truck'" "'vases'" "'a sloth'" "'a fish'" "'a duck'" "'an old man'" "'people at a campfire'" "'a forest fire'" "'a car'" "'a horse'" "'a snowy landscape'" "'a table'" "'a waterfall'" "'a library'" "'a theater'" "'a canyon'" "'a maine coon'" "'a goldfish'" "'the queen of england'" "'a snowy mountain village'" "'a mountain landscape'" "'a teddy bear'" "'a man'" "'a woman'" "'a chair'" "'a skull'" "'a tudor portrait'" "'a lemur'" "'a kangaroo'" "'a young man'" "'a beach'" "'a farm'" "'elvis'")
styles=("'a watercolor of'" "'an oil painting of'" "'a drawing of'" "'a photo of'" "'a pencil sketch of'" "'a painting of'" "'a pop art of'" "'a lithograph of'" "'a mosaic of'" "'a charcoal drawing of'" "'a pixel art of'" "'a digital art of'" "'a stained glass of'" "'a tapestry of'" "'a 3d render of'" "'a ceramic tile of'" "'a cubist artwork of'" "'a graffiti art of'" "'an impressionist painting of'" "'a collage of'" "'a woodcut of'")
views=("'rotate_180'" "'rotate_cw'" "'rotate_ccw'" "'flip'" "'negate'" "'skew'" "'patch_permute'" "'pixel_permute'" "'inner_circle'" "'square_hinge'" "'jigsaw'")
result_file_is="result_configs/is_results.txt"
result_file_ds="result_configs/ds_results.txt"
rm -rf $result_file_is $result_file_ds "yap.txt" "yap2.txt"

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
        name=${name//\'/}
	cmd="python generate.py --name "$name" --prompts "$prompt" --views 'identity' "$view" --style "$style" --num_samples 1 --num_inference_steps 30 --guidance_scale 10.0 --generate_1024"
        #python generate.py --name "real" --prompts "a rabbit" "a duck" --style "a watercolor of" --views "identity" "color_rotate_brg" --num_samples 1 --num_inference_steps 30 --guidance_scale 10.0 --generate_1024

        echo "executing "$cmd

        # write the command into a file
        echo "#!/bin/bash" > negeval_run.sh
        echo $cmd >> negeval_run.sh

        # change the rights of the file : make it executable
        chmod 755 negeval_run.sh
        # run the file
        ./negeval_run.sh

        image_dir=`pwd`/results/${name//\'}
        line_count=`ls -la $image_dir/ | wc -l`
        echo $line_count
        if (($line_count < 4)); then
          continue
        fi
        picture=$image_dir/0000/sample_1024.png

        # check for independent synthesis
        echo "checking for independent synthesis on "$image_dir
        cmd2="python negeval.py --path "$picture" --targets "$prompt" --views 'identity' "$view" --fault is"
  
        echo "#!/bin/bash" > negeval_run.sh
        echo $cmd2 >> negeval_run.sh
        echo "third"
        ./negeval_run.sh
        result=$?
	echo "result is: "$result

        if (($result == 1)) ; then
	        echo "found independent synthesis on "$image_dir
          echo "prompts: "$prompt >> $result_file_is
          echo "style: "$style >> $result_file_is
          echo "views: 'identity' "$view >> $result_file_is
          echo "" >> $result_file_is
        fi

        # check for dominant synthesis
        echo "checking for dominant synthesis on "$image_dir
        cmd2="python negeval.py --path "$picture" --targets "$prompt" --views 'identity' "$view" --fault ds"

        echo "#!/bin/bash" > negeval_run.sh
        echo $cmd2 >> negeval_run.sh
        ./negeval_run.sh
        result=$?
	echo "result ds: "$result

        if (($result == 1)) ; then
          echo "found dominant synthesis on "$image_dir
          echo "prompts: "$prompt >> $result_file_ds
          echo "style: "$style >> $result_file_ds
          echo "views: 'identity' "$view >> $result_file_ds
          echo "" >> $result_file_ds
        fi
  
        rm -rf $image_dir
      done
    done
  done
done
rm -rf negeval_run.sh
echo "process finished"

#tmux: test_configs
