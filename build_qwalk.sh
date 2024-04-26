#/bin/bash
# author: Gustavo Becerra <gustavo.becerra>

set -x

REG="local"
APP="qwalk"
TAG="00"

podman build --tag ${REG}/${APP}:${TAG} -f ${WDIR}/${APP}.Dockerfile .

