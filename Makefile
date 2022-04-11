REPO_NAME='montage-worker'
PREFIX='hyperflowwms'
JOB_EXECUTOR_SHORT='je'
HF_JOB_EXECUTOR_VERSION='1.1.4'
TAG=$(JOB_EXECUTOR_SHORT)-$(HF_JOB_EXECUTOR_VERSION)

all: push

container: image

image:
	docker build --build-arg hf_job_executor_version=$(HF_JOB_EXECUTOR_VERSION) -t $(PREFIX)/$(REPO_NAME) .
	docker tag $(PREFIX)/$(REPO_NAME) $(PREFIX)/$(REPO_NAME):$(TAG)  

push: image
	docker push $(PREFIX)/$(REPO_NAME) 
	docker push $(PREFIX)/$(REPO_NAME):$(TAG)
	
clean: