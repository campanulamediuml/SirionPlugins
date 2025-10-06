# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Author     ：Campanula 梦芸 何
import random
import time
import traceback
from queue import SimpleQueue
from typing import Dict, Any, TypedDict, Optional, List

import numpy as np

from SirionDep.sirion_dep_frame.data_object_frame.data_object import DataContext
from SirionDep.sirion_dep_frame.plugin_frame import PluginBase
from SirionDep.sirion_dep_thread_manager.thread_pool_manager import t_pool_manager
from sirion_plugin_logger.logger import dbg, error
from sirion_plugin_packages.source.random_data_create_source.conf import RandomCreateParameter, \
    RandomDataCreateSourceConf


class RandomDataCreateSourceAdapter(PluginBase):
    def __init__(self, global_config:Dict[str, Any]) -> None:
        super().__init__(global_config)
        self.conf:Optional[RandomDataCreateSourceConf] = None
        self.start_running_time = int(time.time()*1000)
        self.result_queue:SimpleQueue[List[DataContext]] = SimpleQueue()
        self.result:List[DataContext] = []

    def initial_work(self, parameters: RandomCreateParameter):
        self.conf = RandomDataCreateSourceConf(parameters)
        t_pool_manager.add_task(task_name="create_fake_data",
                                task_function=self.create_data_task,
                                is_interval=True,
                                )

    def create_data_task(self):
        try:
            now_time = int(time.time()*1000)
            res:List[DataContext] = []
            for i in range(0,self.conf.channel):
                data = {
                    "raw_wave":np.frombuffer(random.randbytes(self.conf.sample_rate*2)),
                    "timestamp":now_time,
                    "uuid":"%s-%s"%(self.conf.base_uuid,i)
                }
                data_ctx = DataContext(data=data,
                                       data_tag=data['uuid'],
                                       data_timestamp_watermark=now_time,
                                       ctx_info={}
                                       )
                res.append(data_ctx)
            self.result_queue.put(res)
            create_cost_time = int(time.time()*1000) - now_time
            dbg("创建假数据花费",create_cost_time,"毫秒")
            time.sleep((1000-create_cost_time)/1000)
        except Exception as e:
            error(traceback.format_exc())
            error("创造假数据失败",e)


    def run(self, _):
        data = self.result_queue.get()
        self.result = data

    def get_result(self):
        return self.result









