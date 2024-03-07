#!/bin/bash
method=$1

domain=$2

agent_model_size=$3

learner_model_size=gpt-4



if [ $domain = 'robotic_planning' ]
then
    export dataset_list=(tyreworld barman blockworld gripper)
elif [ $domain = 'alfworld' ]
then
    export dataset_list=(alfworld_put alfworld_clean alfworld_heat alfworld_cool alfworld_examine alfworld_puttwo)
fi


if [ $method = 'learnact' ]
then
    if [ $domain = 'robotic_planning' ]
    then
        for dataset in "${dataset_list[@]}"; do
            for exp_id in `seq 0 2`; do
                python downstream_test.py  --exp_id $exp_id --dataset_name $dataset  --planning_method learnact_agent --learner_method learnact_learner --optimizer_do_learn --tool_in_context_style vanilla --get_tool_version free --get_tool_incontext_version precise --usage_version together --note_position before_example --tool_improve_version both --tool_improve_in_context_version both --step_sample_number 4 --optimize_iteration_number 2 --score_type step_correction_call_ratio_success --user_method learnact_user --example_order tool_first --no_tool_selfprompt --model_name gpt --model_size $learner_model_size --user_model_size $agent_model_size --max_steps 30 --memory_size 20  --do_learn --split_dataset_num 3 --test_on_all  --exp_id_on_train --batch_train --resume
            done
        done
    elif [ $domain = 'alfworld' ]
    then
        for dataset in "${dataset_list[@]}"; do
            for exp_id in `seq 0 2`; do
                python downstream_test.py  --exp_id $exp_id --dataset_name $dataset   --planning_method learnact_agent --learner_method learnact_learner --optimizer_do_learn --tool_in_context_style vanilla --get_tool_version decompose --get_tool_incontext_version precise --usage_version together_complete --same_usage --note_position before_example --tool_improve_version both --tool_improve_in_context_version both --tool_improve_target step --tool_improve_history full --step_sample_number 4 --optimize_iteration_number 2 --score_type call_ratio_success --user_method learnact_user --example_order tool_first --full_tool_subprocess --no_tool_selfprompt  --model_name gpt --model_size $learner_model_size --user_model_size $agent_model_size --max_steps 20 --memory_size 50  --do_learn --split_dataset_num 3 --test_on_all  --exp_id_on_train --batch_train --resume
            done
        done
    fi

elif [ $method = 'act' ]
then
    if [ $domain = 'robotic_planning' ]
    then
        for dataset in "${dataset_list[@]}"; do
            for exp_id in `seq 0 2`; do
                python downstream_test.py  --exp_id $exp_id --dataset_name $dataset  --planning_method py_agent --model_name gpt --model_size $agent_model_size --max_steps 30 --memory_size 20  --resume
            done
        done
    elif [ $domain = 'alfworld' ]
    then
        for dataset in "${dataset_list[@]}"; do
            for exp_id in `seq 0 2`; do
                python downstream_test.py  --exp_id $exp_id --dataset_name $dataset   --planning_method py_agent --model_name gpt --model_size $agent_model_size --max_steps 20 --memory_size 50  --resume
            done
        done
    fi

elif [ $method = 'react' ]
then
    if [ $domain = 'robotic_planning' ]
    then
        for dataset in "${dataset_list[@]}"; do
            for exp_id in `seq 0 2`; do
                python downstream_test.py  --exp_id $exp_id --dataset_name $dataset  --planning_method react_py_agent --model_name gpt --model_size $agent_model_size --max_steps 30 --memory_size 20  --resume
            done
        done
    elif [ $domain = 'alfworld' ]
    then
        for dataset in "${dataset_list[@]}"; do
            for exp_id in `seq 0 2`; do
                python downstream_test.py  --exp_id $exp_id --dataset_name $dataset  --planning_method react_py_agent --model_name gpt --model_size $agent_model_size --max_steps 20 --memory_size 50  --resume
            done
        done
    fi

elif [ $method = 'act_reflexion' ]
then
    if [ $domain = 'robotic_planning' ]
    then
        for dataset in "${dataset_list[@]}"; do
            for exp_id in `seq 0 2`; do
                python downstream_test.py  --exp_id $exp_id --dataset_name $dataset  --planning_method reflexion_agent --learner_method reflexion --user_method py_agent --optimize_iteration_number 2  --model_name gpt --model_size $learner_model_size --user_model_size $agent_model_size --max_steps 30 --memory_size 20 --do_learn --split_dataset_num 3 --test_on_all --exp_id_on_train --batch_train   --resume
            done
        done
    elif [ $domain = 'alfworld' ]
    then
        for dataset in "${dataset_list[@]}"; do
            for exp_id in `seq 0 2`; do
                python downstream_test.py  --exp_id $exp_id --dataset_name $dataset  --planning_method reflexion_agent --learner_method reflexion --user_method py_agent --optimize_iteration_number 2  --model_name gpt --model_size $learner_model_size --user_model_size $agent_model_size --max_steps 20 --memory_size 50 --do_learn --split_dataset_num 3 --test_on_all --exp_id_on_train --batch_train   --resume
            done
        done
    fi
    
elif [ $method = 'react_reflexion' ]
then
    if [ $domain = 'robotic_planning' ]
    then
        for dataset in "${dataset_list[@]}"; do
            for exp_id in `seq 0 2`; do
                python downstream_test.py  --exp_id $exp_id --dataset_name $dataset  --planning_method reflexion_agent --learner_method reflexion --user_method react_py_agent --optimize_iteration_number 2  --model_name gpt --model_size $learner_model_size --user_model_size $agent_model_size  --max_steps 30 --memory_size 20 --do_learn --split_dataset_num 3 --test_on_all --exp_id_on_train --batch_train   --resume
            done
        done
    elif [ $domain = 'alfworld' ]
    then
        for dataset in "${dataset_list[@]}"; do
            for exp_id in `seq 0 2`; do
                python downstream_test.py  --exp_id $exp_id --dataset_name $dataset  --planning_method reflexion_agent --learner_method reflexion --user_method react_py_agent --optimize_iteration_number 2  --model_name gpt --model_size $learner_model_size --user_model_size $agent_model_size  --max_steps 20 --memory_size 50 --do_learn --split_dataset_num 3 --test_on_all --exp_id_on_train --batch_train  --resume
            done
        done
    fi

elif [ $method = 'code_as_policy' ]
then
    if [ $domain = 'robotic_planning' ]
    then
        for dataset in "${dataset_list[@]}"; do
            for exp_id in `seq 0 2`; do
                python downstream_test.py  --exp_id $exp_id --dataset_name $dataset  --dataset_list gripper --planning_method code_as_policy --hier --model_name gpt --model_size $agent_model_size --max_steps 30 --memory_size 20  
            done
        done
    fi

fi

