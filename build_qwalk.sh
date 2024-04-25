#/bin/bash
# author: Gustavo Becerra <gbecerra@mx1.ibm.com>

set -x

REG="local"
APP="qwalk"
TAG="00"

podman build --tag ${REG}/${APP}:${TAG} -f ${WDIR}/${APP}.Dockerfile .

