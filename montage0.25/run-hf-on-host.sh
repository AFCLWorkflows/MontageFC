cp -r input work_dir
export HF_VAR_WORKER_CONTAINER="hyperflowwms/montage-worker"
export HF_VAR_WORK_DIR="$PWD/work_dir"
export HF_VAR_function="redisCommand"
hflow run .
