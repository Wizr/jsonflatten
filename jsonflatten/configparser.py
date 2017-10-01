import json
from typing import Dict, Tuple
from abc import ABCMeta, abstractmethod
from operation import OPNotFoundError, OP_ALLOWED


class Node:
    def __init__(self, ops: dict = None, key_nodes: dict = None):
        self.ops = ops
        self.key_nodes = key_nodes


class AbstractConfigParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, cfg: Dict) -> Tuple[str, Dict]:
        pass


class JSONConfigParser(AbstractConfigParser):
    __OP_KEY__ = '__OP_KEY__'

    def parse(self, cfg: Dict) -> Tuple[str, Node]:
        """
        :param cfg: a dict containing two keys,
            'template': the value is a string of the template;
            `__OP_KEY__`: the value is the special key in 'template'
                representing operations for the nodes;
        :return: ('key whose value is operations', 'a Node instance').
        """
        assert isinstance(cfg, dict)
        assert JSONConfigParser.__OP_KEY__ in cfg and 'template' in cfg
        assert isinstance(cfg[JSONConfigParser.__OP_KEY__], str)
        op_key = cfg[JSONConfigParser.__OP_KEY__]
        if isinstance(cfg['template'], str):
            template = json.loads(cfg['template'])
        else:
            template = cfg['template']
            assert isinstance(template, dict)
        node = self._parse_template(op_key, template)
        return op_key, node

    def _parse_template(self, op_key: str, template_dict: dict) -> Node:
        if op_key in template_dict:
            ops = self._parse_operation(template_dict[op_key])
        else:
            ops = None

        key_nodes = {}
        for key, value in template_dict.items():
            if key == op_key:
                continue
            if isinstance(value, dict):
                key_nodes[key] = self._parse_template(op_key, value)
            elif isinstance(value, str):
                key_nodes[key] = Node(self._parse_operation(value))
            else:
                key_nodes[key] = Node()

        return Node(ops, key_nodes)

    def _parse_operation(self, ops_string: str) -> dict:
        """
        Parse an operation string
        :param ops_string: an string of operations
        :return: a dict with key as operation, value as the operation parameter;
            or None
        """
        # parse the operation string
        ops = {}
        for op_string in ops_string.split(';'):
            op_string = op_string.strip()
            if op_string is '':
                continue
            op_info = op_string.split(':')
            if op_info[0] not in OP_ALLOWED:
                raise OPNotFoundError(op_info[0], ops_string)
            ops[op_info[0]] = op_info[1:] if len(op_info) > 1 else None
        return None if ops == {} else ops
