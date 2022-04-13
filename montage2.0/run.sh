# Before running this script you need to start the redis server:
# docker run -d --name redis redis --bind 127.0.0.1

docker run -a stdout -a stderr --rm --network container:redis -e HF_VAR_WORKER_CONTAINER="hyperflowwms/montage-worker" -e HF_VAR_WORK_DIR="$PWD/input" -e HF_VAR_HFLOW_IN_CONTAINER="true" -e HF_VAR_function="redisCommand" -e REDIS_URL="redis://127.0.0.1:6379" --name hyperflow -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/wfdir --entrypoint "/bin/sh" hyperflowwms/hyperflow -c "apk add docker && ls /wfdir && hflow run -s /wfdir"
