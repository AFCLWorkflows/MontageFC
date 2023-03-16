# MontageFC
Montage workflow developed with AFCL (Abstract Function Choreography Language)

## Requirements
### AWS Lambda
<em>credentials.properties</em>
```
  aws_access_key=<aws_access_key_id>
  aws_secret_key=<aws_secret_access_key>
  aws_session_token=<aws_session_token>
```
<em>input_montage.json</em>
```
{
	"bucket" : "<bucket-name>",
	"header" : "<region.hdr>"
}
```
## Project Setup
### AWS
1. Create s3 bucket ```<bucket-name>```
2. Create in s3 bucket the folder ```/input```
3. Upload ```input fits files``` and ```region.hdr```to ```/input``` (see example [input](https://github.com/AFCLWorkflows/MontageFC/tree/main/development/example/AWS/input "Input example")) 
5. Create lambda functions from [functions](https://github.com/AFCLWorkflows/MontageFC/tree/main/development/python/AWS/functions "Lambda Functions")
6. Create lambda layers from [layers](https://github.com/AFCLWorkflows/MontageFC/tree/main/development/python/AWS/layers "Lambda Layers") and add the layers to each function as follows:
* ```m_ProjectPP```: MontagePy
* ```preparemDiffFit```: 
  * MontagePy
  * pandas from [Keith's Layers](https://github.com/keithrozario/Klayers/tree/master/deployments/python3.9 "Klayers")
* ```m_DiffFit```: 
  * MontagePy
  * mFitplane
* ```m_ConcatFit```:
  * mConcatFit
  * mStatFile
* ```m_BgModel```: MontagePy
* ```m_Background```: mBackground
* ```m_Imgtbl```: MontagePy
* ```m_Add```: MontagePy
* ```m_Shrink```: MontagePy
* ```m_Viewer```: MontagePy
7. Execute Enacment Engine with the command: ```java -jar enactment-engine-all.jar montage_workflow.yaml input_montage.json``` [xAFCL EE](https://github.com/sashkoristov/enactmentengine)
