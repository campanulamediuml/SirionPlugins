# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Author     ：Campanula 梦芸 何
from typing import Dict, Any, List

from SirionDep.sirion_dep_frame.data_object_frame.data_object import DataContext
from SirionDep.sirion_dep_frame.plugin_frame import PluginBase


class AvgAdapter(PluginBase):
    def __init__(self, global_config: Dict[str, Any]):
        super().__init__(global_config)
        self.results: List[DataContext] = []

    def initial_work(self, parameters: Dict[str, Any]):
        plugin = parameters['plugin']

    def run(self, data: List[DataContext]):
        for i in data:
            values = i.get_data()
            if not values:
                continue
            avg_value = sum(values) / len(values)
            result_ctx = DataContext(data_tag=i.get_data_tag(), data=[avg_value])
            self.results.append(result_ctx)


