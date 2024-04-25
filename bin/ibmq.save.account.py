#!/usr/bin/python3

import os
from qiskit import IBMQ

IBMQ.save_account(os.getenv('IBMQE_API'), overwrite=True)