# MontageFC
Montage workflow developed with AFCL (Abstract Function Choreography Language)

## Running locally
There are two prepared folders with Montage workflow graphs and input data:
- Montage 0.25 (43 tasks)
- Montage 2.0 (1482 tasks)

To run the workflow locally using the <code>montage-workflow-worker</code> Docker image, you need to follow this steps:
- Build the image: <code>make</code>
- Start redis container: <code>docker run -d --name redis redis --bind 127.0.0.1</code>
- Do <code>cd montageX.XX</code>
- Run command <code>. run.sh</code>

All files, including the final <code>jpeg</code>, will be generated in the subdirectory <code>input</code>.

