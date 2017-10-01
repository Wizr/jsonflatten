README
======

本程序接收一个 json 模板，并根据这个模板扁平化一个 json 输入。

一个简单的例子（python 代码）：

模板：

.. code:: python

    {
        '__OP_KEY__': 'ops',
        'template': {
            'user': {
                'name': '',
                'password': '',
                'score': {
                    'ops': 'rename:avg_score',
                    'avg': 'delete'
                },
                'other': {
                    'ops': 'delete',
                    'address': '',
                    'class': ''
                },
                'books': {
                    'software': {
                        'ops': 'delete;compact',
                        'all': {
                            '1': ''
                        }
                    }
                }
            }
        }
    }

输入：

.. code:: python

    {
        'user': {
            'name': 'admin',
            'password': 'admin123',
            'gender': 'male',
            'score': {
                'math': 100,
                'english': 50,
                'avg': 75
            },
            'other': {
                'address': 'Shanghai',
                'class': '2'
            },
            'books': {
                'software': [['45$', 'C#'], ['50$', 'Python']]
            }
        }
    }

输出：

.. code:: python

    {
        'user': {
            'address': 'Shanghai',
            'avg_score': 75,
            'books': ['C#', 'Python'],
            'class': '2',
            'name': 'admin'
        }
    }

基本概念
-------

（假设一个 json 由字典组成）

模板有个特殊的 key ``__OP_KEY__``，其值用于指定一个特殊的 key，这个 key 的值表示一系列 operation（操作），如例中：``'ops': 'dict'``。

模板中没有涉及到的 key，在输出中被忽略，包括其 value，如例中：``password`` 和 ``gender``。

模板中如果一个 key 的 value 不是一个字典，则一定是一个字符串，表示一系列 operation，可以认为它一种缩写形式，如：``'name': ''`` 是 ``'name': {'ops': ''}`` 的缩写，``'avg': 'delete'`` 类似。

Operation
---------

允许的 operation 有如下：

.. code:: python
    
    OP_ALLOWED = ['dict', 'list', 'other', 'delete', 'rename', 'compact']

其中 ``dict``, ``list``, ``other`` 表示 key 所对应的 value 的数据类型，如字面意思所示。如果输入的数据与模板指定的类型不符，则在输出中被忽略。如果例中的 ``'ops': 'dict'`` 被改为另外两个类型中的一个，则输出中没有 ``score`` 这个 key。

``delete``  表示删除某个 key，如果其值是字典，则字典向上合并，否则其值向上传递，如例中：``avg`` 是向上传递，而 ``address`` 和 ``class`` 是向上合并。

``rename`` 表示重命名某个 key，如例中的 ``score``。

``compact`` 仅对 **list** 有效，关于 list 有特殊的设定，参见下节。

list
----

``list`` 作为字典的 value 与 ``other`` 具有相同的属性，例如其 key 被 ``delete`` 删除，则会被向上传递。

``list`` 本身也具体与 ``dict`` 类似的属性，例如可以被看作是以索引为 key 的 ``dict``。

因此程序中对 ``list`` 有特殊的安排，用 key ``all`` 指代所有的元素，用索引指定特定元素，两者不可混用。通常 ``all`` 适用于个数不限的 ``list``，而索引适用于结构固定的 ``list``，如例中所示。

``compact`` 仅适用于 ``list``，表示将子 ``list`` 合并进当前 ``list``，如例中 ``software``。

.. note:: 更多示例参见 unittest
