#!/bin/bash

touch data.out

if [ -z "$IBMQE_API" ]; then
    echo "\$IBMQE_API is empty"
else
    echo "Connecting to the IBM Quantum Platform"

    /home/ops/bin/ibmq.save.account.py;
    /home/ops/bin/QWalk.py &
fi

tail -f data.out