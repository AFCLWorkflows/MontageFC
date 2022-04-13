REPO_NAME='montage-worker'
PREFIX='hyperflowwms'
JOB_EXECUTOR_SHORT='je'
HF_JOB_EXECUTOR_VERSION='1.1.4'

container: image

image:
	docker build --build-arg hf_job_executor_version=$(HF_JOB_EXECUTOR_VERSION) -t $(PREFIX)/$(REPO_NAME) .
clean:
