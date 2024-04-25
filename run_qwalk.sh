#/bin/bash
# author: Gustavo Becerra

WRSP="$(cd $(dirname $0)/; pwd)"

REG="local"
APP="qwalk"
TAG="00"
CNT="qwalk"

IBMQE_API="$(cat ${WRSP}/ibmq_apikey.dat)"

podman stop ${CNT};
podman rm ${CNT};

set -x;

podman run -it --name ${CNT} \
    -h ${CNT} \
    -e IBMQE_API="${IBMQE_API}" \
    ${REG}/${APP}:${TAG}