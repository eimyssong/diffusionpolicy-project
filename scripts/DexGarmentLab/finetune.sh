#!/usr/bin/env bash

# Examples:
# bash finetune_target_guided.sh Fold_Trousers_stage_3_target_guided 100 42 0 False
# bash finetune_target_guided.sh Fold_Trousers_stage_3_target_guided 100 42 0 True
#
# Optional full form:
# bash finetune_target_guided.sh \
#   Fold_Trousers_stage_3_target_guided 100 42 0 False \
#   Fold_Trousers_stage_1 Fold_Trousers_stage_1 3000 300
#
# task_name: output task name, e.g. Fold_Trousers_stage_3_target_guided
# expert_data_num: number of training data, e.g. 100
# seed: random seed, e.g. 42
# gpu_id: single gpu id, e.g. 0
# DEBUG: True or False
# data_task_name: dataset task to reuse, default Fold_Trousers_stage_1
# init_task_name: checkpoint task to initialize from, default Fold_Trousers_stage_1
# checkpoint_num: checkpoint number to load/save, default 3000
# epochs: fine-tuning epochs, default 300

set -e

task_name=${1}
expert_data_num=${2}
seed=${3}
gpu_id=${4}
DEBUG=${5}

data_task_name=${6:-Fold_Trousers_stage_1}
init_task_name=${7:-Fold_Trousers_stage_1}
checkpoint_num=${8:-3000}
epochs=${9:-300}

if [ -z "${task_name}" ] || [ -z "${expert_data_num}" ] || [ -z "${seed}" ] || [ -z "${gpu_id}" ] || [ -z "${DEBUG}" ]; then
    echo "Usage:"
    echo "  bash finetune_target_guided.sh <task_name> <expert_data_num> <seed> <gpu_id> <DEBUG> [data_task_name] [init_task_name] [checkpoint_num] [epochs]"
    echo ""
    echo "Example:"
    echo "  bash finetune_target_guided.sh Fold_Trousers_stage_3_target_guided 100 42 0 False"
    exit 1
fi

project_root=${PROJECT_ROOT:-/workspace/isaaclab/scripts/DexGarmentLab}
sadp_root=${SADP_ROOT:-${project_root}/Model_HALO/SADP_G}
data_root=${DATA_ROOT:-${sadp_root}/data}
python_path=${PYTHON_PATH:-/isaac-sim/python.sh}

export ISAAC_PATH=${python_path}
export HYDRA_FULL_ERROR=1
export CUDA_VISIBLE_DEVICES=${gpu_id}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
finetune_py=${FINETUNE_PY:-${script_dir}/finetune_sadp_g.py}

init_ckpt="${sadp_root}/checkpoints/${init_task_name}_${expert_data_num}/${checkpoint_num}.ckpt"
output_dir="${sadp_root}/checkpoints/${task_name}_${expert_data_num}"
final_ckpt_name="${checkpoint_num}.ckpt"

echo -e "\033[33mgpu id (to use): ${gpu_id}\033[0m"
echo -e "\033[33mproject root: ${project_root}\033[0m"
echo -e "\033[33mSADP_G root: ${sadp_root}\033[0m"
echo -e "\033[33mdata root: ${data_root}\033[0m"
echo -e "\033[33mdata task: ${data_task_name}_${expert_data_num}\033[0m"
echo -e "\033[33minit ckpt: ${init_ckpt}\033[0m"
echo -e "\033[33moutput dir: ${output_dir}\033[0m"

if [ "${DEBUG}" = "True" ]; then
    echo -e "\033[33mDebug mode!\033[0m"
    run_epochs=2
    max_train_steps_per_epoch=2
    val_every=1
    max_val_steps=1
else
    echo -e "\033[33mTarget-guided fine-tune mode\033[0m"
    run_epochs=${epochs}
    max_train_steps_per_epoch=0
    val_every=10
    max_val_steps=10
fi

${ISAAC_PATH} "${finetune_py}" \
    --project-root "${project_root}" \
    --sadp-root "${sadp_root}" \
    --data-root "${data_root}" \
    --data-task-name "${data_task_name}" \
    --init-task-name "${init_task_name}" \
    --output-task-name "${task_name}" \
    --expert-data-num "${expert_data_num}" \
    --checkpoint-num "${checkpoint_num}" \
    --init-ckpt "${init_ckpt}" \
    --output-dir "${output_dir}" \
    --final-ckpt-name "${final_ckpt_name}" \
    --epochs "${run_epochs}" \
    --seed "${seed}" \
    --device "cuda:0" \
    --max-train-steps-per-epoch "${max_train_steps_per_epoch}" \
    --val-every "${val_every}" \
    --max-val-steps "${max_val_steps}" \
    --lr 1e-5 \
    --lambda-dir 0.50 \
    --lambda-target 0.20 \
    --lambda-progress 0.10 \
    --lambda-motion 0.02 \
    --lambda-keep 0.02 \
    --bc-left-arm-weight 0.03 \
    --bc-left-hand-weight 1.0 \
    --bc-right-side-weight 1.0 \
    --target-affordance-sigma 0.08 \
    --left-base-pos="-0.8,0.0,0.5" \
    --left-base-yaw 0.0
