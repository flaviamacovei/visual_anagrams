#!/bin/bash

prompts=("'a flower'" "'a dress'" "'a carrot'" "'marylin monroe'" "'albert einstein'" "'houseplants'" "'a deer'" "'a kitchen'" "'a giraffe'" "'a penguin'")
styles=("'a watercolor of'" "'a drawing of'" "'a photo of'")
views=("'rotate_180'" "'rotate_cw'" "'rotate_ccw'" "'flip'" "'negate'" "'skew'" "'jigsaw'")
untils=(50 40 30 20 10 0)

rm -rf "alignments.txt" "concealments.txt" "untils.txt" "yap_alternations.txt"

times_path="times.txt"
> "$times_path"


times=()


for i in ${!prompts[@]}; do
  for j in ${!prompts[@]}; do
    # if prompts are equal: continue
    if (($i == $j)); then
      continue
    fi
    prompt=${prompts[$i]}" "${prompts[$j]}
    for k in ${!styles[@]}; do
      style=${styles[$k]}
      for l in ${!views[@]}; do
        view=${views[$l]}
        dirnames=()
        for m in ${!untils[@]}; do
          until=${untils[$m]}
          name=${prompt// /_}"-"${style// /_}"-"${view// /_}"-"$until
          name=${name//\'}
          dirnames+=("\"results/$name\"")
          cmd="python generate_alt.py --name "$name" --prompts "$prompt" --views 'identity' "$view" --style "$style" --num_samples 1 --num_inference_steps 50 --alternate_until $until --guidance_scale 10.0 --generate_1024"

          echo "executing "$cmd

          # write the command into a file
          echo "#!/bin/bash" > alternations_run.sh
          echo $cmd >> alternations_run.sh

          # change the rights of the file : make it executable
          chmod 755 alternations_run.sh

           # run the file
          start=$(date +%s)
          ./alternations_run.sh
          end=$(date +%s)
          elapsed=$((end - start))
          echo $elapsed >> $times_path
        done

        echo ${dirnames[@]}

        cmd2="python compute_scores_alternations.py --dirnames ${dirnames[@]} --untils "${untils[@]}" --targets "$prompt" --views 'identity' "$view" --times_path "$times_path
        echo $cmd2
        echo "#!/bin/bash" > alternations_run.sh
        echo $cmd2 >> alternations_run.sh
        ./alternations_run.sh

        for dirname in ${dirnames[@]}; do
          to_remove=${dirname//\"}
          echo "removing ./$to_remove"
          rm -rf "./$to_remove"
        done
      done
    done
  done
  cmd3="python visualise_alternations.py"
  echo $cmd3
  echo "#!/bin/bash" > alternations_run.sh
  echo $cmd3 >> alternations_run.sh
  ./alternations_run.sh
done
rm -rf alternations_run.sh
echo "process finished"
#tmux session: alternations
