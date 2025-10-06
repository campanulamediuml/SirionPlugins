# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Author     ：Campanula 梦芸 何
from typing import TypedDict


class RandomCreateParameter(TypedDict):
    sample_rate:int
    channel: int
    base_uuid: str

class RandomDataCreateSourceConf:
    def __init__(self, parameters:RandomCreateParameter):
        self.parameters = parameters
        self.sample_rate = parameters['sample_rate']
        self.channel = parameters['channel']
        self.base_uuid = parameters['base_uuid']