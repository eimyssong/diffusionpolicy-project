# Examples:
# bash Validation.sh Hang_Coat 100 100

# 'task_name' e.g. Hang_Coat, Hang_Tops, Wear_Scarf, etc.
# 'validation_num' The episodes number you need to validate. e.g. 50, 100, etc.
# 'training_data_num' The expert data number used for training policy. e.g. 100, 200, 300, etc.

# when you run this script, you need to input the checkpoint number parameters according to task.
# for example:
# As for Fold Dress which has three stages, 
# you need to input the stage_1_checkpoint_num, stage_2_checkpoint_num, stage_3_checkpoint_num.

#!/bin/bash

# 获取参数
task_name=$1
validation_num=$2
training_data_num=$3

if [[ "$task_name" == "Fold_Dress" || "$task_name" == "Fold_Tops" ]]; then
    read -p "Please Input <stage_1_checkpoint_num>: " stage_1_checkpoint_num
    read -p "Please Input <stage_2_checkpoint_num>: " stage_2_checkpoint_num
    read -p "Please Input <stage_3_checkpoint_num>: " stage_3_checkpoint_num
elif [[ "$task_name" == "Fling_Dress" || "$task_name" == "Fling_Tops" || "$task_name" == "Fold_Trousers" ]]; then
    read -p "Please Input <stage_1_checkpoint_num>: " stage_1_checkpoint_num
    read -p "Please Input <stage_2_checkpoint_num>: " stage_2_checkpoint_num
    stage_3_checkpoint_num=0
else
    read -p "Please Input <stage_1_checkpoint_num>: " stage_1_checkpoint_num
    stage_2_checkpoint_num=0
    stage_3_checkpoint_num=0
fi

type=HALO
# isaac_path=~/isaacsim_4.5.0/python.sh
# isaac_path=/isaac-sim/python.sh
# isaac_path=/workspace/isaaclab/isaaclab.sh
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

# 创建目录和文件
base_dir="/workspace/isaaclab/scripts/DexGarmentLab/Data/${task_name}_Validation_${type}"
mkdir -p "${base_dir}/final_state_pic"
mkdir -p "${base_dir}/video"
touch "${base_dir}/validation_log.txt"

# 获取当前数据数量
current_num=$(ls "${base_dir}/final_state_pic" | wc -l)

# 进度条函数（写 stderr）
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

    # 输出任务名和进度条
    printf "\rTask: %-20s |%s| %3d%% (%d/%d)" "$task" "$bar" "$percent" "$current" "$total" >&2
}

# 数据采集循环
while [ "$current_num" -lt "$validation_num" ]; do

    # 打印进度条
    print_progress "$current_num" "$validation_num" "$task_name"

    # 执行 isaac 命令（stdout 保留）
    $ISAAC_PATH Env_Validation/${task_name}_${type}.py \
        --env_random_flag True \
        --garment_random_flag True \
        --record_video_flag True \
        --validation_flag True \
        --training_data_num "$training_data_num" \
        --stage_1_checkpoint_num "$stage_1_checkpoint_num" \
        --stage_2_checkpoint_num "$stage_2_checkpoint_num" \
        --stage_3_checkpoint_num "$stage_3_checkpoint_num"

    # 更新数量
    current_num=$(ls "${base_dir}/final_state_pic" | wc -l)

    sleep 5
done

# 打印进度条
print_progress "$current_num" "$validation_num" "$task_name"

# 完成后换行
echo >&2
