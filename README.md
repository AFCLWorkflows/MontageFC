# MontageFC
Montage workflow developed with AFCL (Abstract Function Choreography Language). This workflow uses the [Montage](http://montage.ipac.caltech.edu/ "Montage") toolkit to re-project, background correct and add astronomical images into custom mosaics.

## Project Setup
### AWS
1. Create s3 bucket ```<bucket-name>```
2. Create in s3 bucket the folder ```/input```
3. Create in s3 bucket the folder ```/input/gray```
4. Upload ```input fits files``` to ```/input/gray``` and ```region.hdr```to ```/input``` (for [0.25-degree](https://github.com/AFCLWorkflows/MontageFC/tree/main/Input%20Files%200.25 "Input 0.25") and for 2.0-degree it can be downloaded from [2.0-degree](https://github.com/hyperflow-wms/montage2-workflow "Input 2.0"))
5. Create lambda functions from [functions](https://github.com/AFCLWorkflows/MontageFC/tree/main/Functions/AWS "Lambda Functions")
6. Create lambda layers from [layers](https://github.com/AFCLWorkflows/MontageFC/tree/main/AWS%20Layers "Lambda Layers") and add the layers "InspectorLayer" and "PyStorage" to each function and additional layers as follows:
* ```m_ProjectPP```: montagePy
* ```prepare-mDiffFit```: montagePy, pandas and mDAGTbls
* ```m_DiffFit```: montagePy and mFitplane
* ```m_ConcatFit```: mConcatFit and mStatFile
* ```m_BgModel```: montagePy
* ```prepare-m_Background```: pandas
* ```m_Background```: mBackground
* ```m_Imgtbl```: montagePy
* ```m_Add```: montagePy
* ```m_Shrink```: montagePy
* ```m_Viewer```: montagePy

### AWS
1. Create cloud bucket ```<bucket-name>```
2. Create in cloud bucket the folder ```/input```
3. Create in cloud bucket the folder ```/input/gray```
4. Upload ```input fits files``` to ```/input/gray``` and ```region.hdr```to ```/input``` (for [0.25-degree](https://github.com/AFCLWorkflows/MontageFC/tree/main/Input%20Files%200.25 "Input 0.25") and for 2.0-degree it can be downloaded from [2.0-degree](https://github.com/hyperflow-wms/montage2-workflow "Input 2.0"))
5. Create cloud functions from [functions](https://github.com/AFCLWorkflows/MontageFC/tree/main/Functions/GCP "Google Cloud Functions Functions")

## Execution
### Requirements
To configure the credentials, the setup for the execution and more requirements see [xAFCL EE](https://github.com/sashkoristov/enactmentengine) 

### Run the workflow
* Adapt the input.JSON file with the created bucket name and region header name (example for [AWS](https://github.com/AFCLWorkflows/MontageFC/blob/main/input_montage_aws.json "Input JSON AWS") and [AWS](https://github.com/AFCLWorkflows/MontageFC/blob/main/input_montage_gcp.json "Input JSON GCP"))
* Run the workflow with the xACFL EE with the command: ```java -jar enactment-engine-all.jar montage_workflow.yaml input_montage.json``` 
