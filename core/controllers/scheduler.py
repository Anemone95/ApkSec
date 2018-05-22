#!/usr/bin/env python
# -*- coding=utf-8 -*-
import logging

import copy

from core.controllers import plugin_category as catg, ctrl_main
from core.controllers.const import TYPE


def topsort(G):
    """
    Usage:
    G = {
        'a': 'bc',
        'b': 'd',
        'c': 'de',
        'd': 'e',
        'e': '',
    }

    print topsort(G)
    [['a'], ['c', 'b'], ['d'], ['e']]

    :param G: 图
    :return: [['a'], ['c', 'b'], ['d'], ['e']], 在同一列表中表示可以并行
    """
    in_degrees = dict((u, 0) for u in G)
    for u in G:
        for v in G[u]:
            in_degrees[v] += 1
            # 每一个节点的入度
    Q = [u for u in G if in_degrees[u] == 0]
    # 入度为 0 的节点
    S = []
    while Q:
        parallel_queue = []
        while Q:
            u = Q.pop()
            parallel_queue.append(u)
            # 默认从最后一个移除
        S.append(parallel_queue)
        for u in parallel_queue:
            for v in G[u]:
                in_degrees[v] -= 1
                # 并移除其指向
                if in_degrees[v] == 0:
                    Q.append(v)
    return S

def unpacker_schedule(unpackers):
    """
    根据unpacker的文件依赖安排执行顺序，考虑并行化，基于拓扑排序
    :param unpackers: [unpacker1,unpacker2,...]
    :return: [[unpacker1.name,unpacker2.name],[unpacker3.name],...]
    """
    logging.info("Calculate unpacker plugins schedule")

    dependence2plugins = dict((each, []) for each in TYPE)
    for each_unpacker in unpackers:
        for each_dependence in each_unpacker.plugin_object.dependencies:
            dependence2plugins[each_dependence].append(each_unpacker.name)

    graph = dict((each_unpacker.name, []) for each_unpacker in unpackers)
    for each_unpacker in unpackers:
        for each_ability in each_unpacker.plugin_object.ability:
            graph[each_unpacker.name] = copy.copy(dependence2plugins[each_ability])
            if each_unpacker.name in graph[each_unpacker.name]:
                graph[each_unpacker.name].remove(each_unpacker.name)
    return topsort(graph)


if __name__ == '__main__':
    manager = ctrl_main.get_manager()
    unpackers = manager.getPluginsOfCategory(catg.Unpacker.category)
    logging.info("Get unpacker plugins:" + str(map(lambda e: e.name, unpackers)))
    schedule = unpacker_schedule(unpackers)
    print schedule
