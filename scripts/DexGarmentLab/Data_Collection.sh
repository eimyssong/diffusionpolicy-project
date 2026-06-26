#!/bin/bash

# get parameters
task_name=$1
demo_num=$2

# export isaac path. [!!] please change to your own path! 
# isaac_path=~/isaacsim_4.5.0/python.sh # changeable
isaac_path=/workspace/isaaclab/_isaac_sim/python.sh
export ISAAC_PATH=$isaac_path
export PYTHONPATH=$PYTHONPATH:/isaac-sim/extscache/omni.physx.demos-107.3.26+107.3.3.cp311.u353
export PYTHONPATH=$PYTHONPATH:/isaac-sim/extscache/omni.kit.stage_templates-2.0.0+69cbf6ad
export PYTHONPATH=$PYTHONPATH:/isaac-sim/extscache/omni.physx.ui-107.3.26+107.3.3.lx64.r.cp311.u353
export PYTHONPATH=$PYTHONPATH:/isaac-sim/extscache/omni.usdphysics.ui-107.3.26+107.3.3.lx64.r.cp311.u353
export PYTHONPATH=$PYTHONPATH:/isaac-sim/extscache/omni.physx.commands-107.3.26+107.3.3.cp311.u353
export PYTHONPATH=$PYTHONPATH:/isaac-sim/extscache/omni.debugdraw-0.1.4+69cbf6ad.lx64.r.cp311
export PYTHONPATH=$PYTHONPATH:/isaac-sim/extscache/omni.kit.widget.text_editor-1.1.1+69cbf6ad.lx64.r.cp311
export PYTHONPATH=$PYTHONPATH:/isaac-sim/extscache

# create target dir and file
base_dir="/workspace/isaaclab/scripts/DexGarmentLab/Data/${task_name}"
mkdir -p "${base_dir}/final_state_pic"
mkdir -p "${base_dir}/train_data"
mkdir -p "${base_dir}/video"
touch "${base_dir}/data_collection_log.txt"

# get current collected data number
current_num=$(ls "${base_dir}/train_data" | wc -l)

# progress bar function
print_progress() {
    local current=$1
    local total=$2
    local task=$3
    local width=50
    local percent=$((100 * current / total))
    local filled=$((width * current / total))
    local empty=$((width - filled))

    local bar=$(printf "%0.s█" $(seq 1 $filled))
    bar+=$(printf "%0.s " $(seq 1 $empty))

    # output task name and progress bar
    printf "\rTask: %-20s |%s| %3d%% (%d/%d)" "$task" "$bar" "$percent" "$current" "$total" >&2
}

# data collection loop
while [ "$current_num" -lt "$demo_num" ]; do

    # print progress bar
    print_progress "$current_num" "$demo_num" "$task_name"

    # execute
    $ISAAC_PATH Env_StandAlone/${task_name}_Env.py \
        --env_random_flag True \
        --garment_random_flag True \
        --data_collection_flag True \
        --record_video_flag True 

    # update collected data number
    current_num=$(ls "${base_dir}/train_data" | wc -l)

    sleep 5
done

# print final progress bar
print_progress "$current_num" "$demo_num" "$task_name"

# line break after completion
echo >&2
