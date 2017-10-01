OP_ALLOWED = ['dict', 'list', 'other', 'delete', 'rename', 'compact']


class OPNotFoundError(ValueError):
    def __init__(self, op: str, op_string: str):
        super(OPNotFoundError, self).__init__('Operation "%s" in "%s" is not allowed' % (op, op_string))
