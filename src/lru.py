#!/usr/bin/env python3
from typing import Any, Optional
class Node:
    def __init__(self, key:str, value: Any):
        self.key=key
        self.value=value
        self.prev= None
        self.next= None

class LRUCache:
    """
    A Least Recently Used (LRU) cache keeps items in the cache until it reaches its size
    and/or item limit (only item in our case). In which case, it removes an item that was accessed
    least recently.
    An item is considered accessed whenever `has`, `get`, or `set` is called with its key.

    Implement the LRU cache here and use the unit tests to check your implementation.
    """

    def __init__(self, item_limit: int):
        if item_limit<=0:
            raise ValueError("item_limit must be greater than 0")
        self.capacity = item_limit
        self.cache={}
        self.head=_Node("",None)
        self.tail = _Node("",None)
        self.head.next=self.tail
        self.tail.prev = self.head
    def _remove(self, node: _Node):
        node.prev.next=node.next
        node.prev=self.head
        self.head.next.prev =node
        self.head.next=node
            

    def has(self, key: str) -> bool:
        if key not in self.cache:
            return False
        node=self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return True

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        node=self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.value


    def set(self, key: str, value: Any):
        if key in self.cache:
            node=self.cache[key]
            node.value=value
            self._remove(node)
            self._add_to_front(node)
            return 
        if len(self.cache)>=self.capacity:
            lru=self.trail.prev
            self._remove(lru)
            del self.cache[lru.key]
        new_node =_Node(key, value)
        self._add_to_front(new_node)
        self.cache[key]=new_node
