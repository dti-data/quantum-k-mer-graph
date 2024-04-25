# Quantum Walk DNA Pattern Matching

This repository contains the Supplementary Materials for research made into applying quantum computing to DNA processing. These materials are made available here for ease of replication.

The materials in this repository are intended to be executed in a container. It is necessary to have a suitable environment with the listed prerequisites.

## Prerequisites
- A machine with a **GNU/Linux** operating system.
- Internet connectivity.
- A healthy **podman** container environment intalled into the operating system.
- The **git** client to clone this repository.
- An IBM Quantum Platform **API Key**.

## Execution Instructions

The scripts and files in this repository construct a self contained environemnt intended for easy replication. To reproduce the output from the Coined Quantum Walk search follow these steps
- Clone this repository into the Linux machine.
- Copy the IBM Quantum Platform API Key contents into the file [./ibmq_apikey.dat](./ibmq_apikey.dat).
- Execute [./build_qwalk.sh](./build_qwalk.sh).
- Execute [./run_qwalk.sh](./run_qwalk.sh).

## QWalk.py
The [./bin/QWalk.py](./bin/QWalk.py) program is the main program being executed. It is first added to the container image in the build step. When the run is executed the container runs this program for each combination of initialization string and mark 32768 times in total.

## Results

If your podman environment is healthy the container will start running and the console will output information similar to:

```
dev@wrsp:~/wrsp.dti/git/dti-data/quantum-walk-dna-pattern-matching$ ./run_qwalk.sh 
qwalk
qwalk
++ podman run -it --name qwalk -h qwalk -e IBMQE_API=<your ibmqe api key> local/qwalk:00
Connecting to the IBM Quantum Platform
0 00 0000 0000   0000    893   7   4   6  10   8   9   7  11   5  12  13   7   8  10  14
0 00 0000 0000   0001      4 906   8   8   6   8  12   8   7   8  12   7   8   7   9   6
0 00 0000 0000   0010      4   5 909   7   4  15   9   9   9   9   6   7   6  12   6   7
```
Since quantum computing is ruled by probabilities the output data will not be exactly the same, but the pattern will be very similar.

## Previous Data Collected

The file [./data.csv](./data.csv) contains a complete previous run. These data was used to perform the analysis in the paper. 