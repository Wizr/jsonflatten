from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from configparser import Node


class JSONFlattener:
    def __init__(self, op_key: str, template: 'Node'):
        self.op_key: str = op_key
        self.template: Node = template

    def process(self, input_json: dict) -> dict:
        assert isinstance(input_json, dict)
        return self._process_dict(input_json, self.template)

    def _process_dict(self,
                      cur_dict: dict,
                      template: 'Node',
                      out_dict: dict = None):
        """
        Process a dict according to the template

        :param cur_dict: a (sub) dict from the input json
        :param template: template corresponding to `cur_dict`
        :param out_dict: a dict or None
            dict: this method will return nothing (None) but update this dict
            None: this method will return a new dict
        :return: a new dict or nothing (None) according to `out_dict`
                or a value if key deleted
        """
        # for a dict, if template does not specify how to deal with any field,
        # the whole dict will be ignored.
        if template.key_nodes is None:
            return {}

        if out_dict is None:
            ret = {}
        else:
            ret = out_dict

        for key, node in template.key_nodes.items():
            if key in cur_dict:
                value = cur_dict[key]
                ops: dict = node.ops if node.ops is not None else {}

                if 'rename' in ops:
                    key = ops['rename'][0]

                if isinstance(value, dict):
                    if 'list' in ops or 'other' in ops:
                        continue
                    if 'delete' in ops:
                        _t = self._process_dict(value, node, ret)
                        if _t is not None:
                            return _t
                    else:
                        ret[key] = self._process_dict(value, node)

                elif isinstance(value, list):
                    if 'dict' in ops or 'other' in ops:
                        continue
                    if 'delete' in ops:
                        return self._process_list(value, node)
                    else:
                        ret[key] = self._process_list(value, node)

                else:
                    if 'list' in ops or 'dict' in ops:
                        continue
                    if 'delete' in ops:
                        return value
                    ret[key] = value

        # if out_dict is not None, we just add new key/value pairs, no need to
        # return it.
        if out_dict is None:
            return ret

    def _process_list(self,
                      cur_list: list,
                      template: 'Node',
                      out_list: list = None):
        if template.key_nodes is None:
            return []

        if out_list is None:
            ret = []
        else:
            ret = out_list

        ops: dict = template.ops if template.ops is not None else {}
        if 'all' in template.key_nodes:
            node = template.key_nodes['all']
            for value in cur_list:
                if isinstance(value, dict):
                    if 'compact' in ops:
                        _t = self._process_dict(value, node)
                        assert isinstance(_t, list)
                        ret.extend(_t)
                    else:
                        ret.append(self._process_dict(value, node))
                elif isinstance(value, list):
                    if 'compact' in ops:
                        ret.extend(self._process_list(value, node))
                    else:
                        ret.append(self._process_list(value, node))
                else:
                    ret.append(value)
        else:
            list_len = len(cur_list)
            for index, node in template.key_nodes.items():
                ops: dict = node.ops if node.ops is not None else {}
                i = int(index)
                if i >= list_len:
                    continue
                value = cur_list[i]
                if isinstance(value, dict):
                    if 'compact' in ops:
                        _t = self._process_dict(value, node)
                        assert isinstance(_t, list)
                        ret.extend(_t)
                    else:
                        ret.append(self._process_dict(value, node))
                elif isinstance(value, list):
                    if 'compact' in ops:
                        ret.extend(self._process_list(value, node))
                    else:
                        ret.append(self._process_list(value, node))
                else:
                    ret.append(value)

        if out_list is None:
            return ret
