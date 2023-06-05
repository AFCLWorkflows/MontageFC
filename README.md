# MontageFC
Montage workflow developed with AFCL (Abstract Function Choreography Language). This workflow uses the [Montage](http://montage.ipac.caltech.edu/ "Montage") toolkit to re-project, background correct and add astronomical images into custom mosaics.

## Project Setup
### AWS
1. Create s3 bucket ```<bucket-name>```
2. Create in s3 bucket the folder ```/input```
3. Create in s3 bucket the folder ```/input/gray```
4. Upload ```input fits files``` to ```/input/gray``` and ```region.hdr```to ```/input```
5. Create lambda functions from [functions](./Functions/AWS)
6. Create lambda layers from [layers](./AWS%20Layers) and add the layers "InspectorLayer" and "PyStorage" to each function and additional layers as follows:
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

### GCP
1. Create cloud bucket ```<bucket-name>```
2. Create in cloud bucket the folder ```/input```
3. Create in cloud bucket the folder ```/input/gray```
4. Upload ```input fits files``` to ```/input/gray``` and ```region.hdr```to ```/input``` 
5. Create cloud functions from [functions](./Functions/GCP)

## Execution
### Requirements
To configure the credentials, the setup for the execution and more requirements see [xAFCL EE](https://github.com/sashkoristov/enactmentengine) 

### Run the workflow
* Adapt the [inputMontage.json](./AFCL/inputMontage.json) file with the created bucket name and region header name 
* Run the workflow with the [xAFCL EE](https://github.com/sashkoristov/enactmentengine) with the command: ```java -jar enactment-engine-all.jar Montage.yaml inputMontage.json``` 
