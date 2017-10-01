import unittest
from configparser import JSONConfigParser
from jsonflattener import JSONFlattener


class TestJSONFlattener(unittest.TestCase):
    def test_00(self):
        """Dict

        Basic test
        """
        op_key, template = JSONConfigParser().parse({
            "__OP_KEY__": "ops",
            "template": '''{
                "user": {
                    "name": "delete",
                    "password": {"ops":""}
                }
            }'''
        })
        result = JSONFlattener(op_key, template).process({
            "user": {
                "name": "admin",
                "password": "123"
            }
        })
        self.assertDictEqual(result, {"user": "admin"})

    def test_01(self):
        """Dict

        For a dict, if template does not specify how to deal with any fields,
        the whole dict will be ignored.
        """
        op_key, template = JSONConfigParser().parse({
            "__OP_KEY__": "ops",
            "template": '''{
                "user": "delete"
            }'''
        })
        result = JSONFlattener(op_key, template).process({
            "user": {
                "name": "admin",
                "password": "123"
            }
        })
        self.assertDictEqual(result, {})

    def test_02(self):
        """Dict

        Delete a key whose value is not a dict will cause the value been
        returned instead of the dict in where the key stay, thus the other keys
        will ignored.
        """
        op_key, template = JSONConfigParser().parse({
            "__OP_KEY__": "__OP_An3Dk__",
            "template": '''{
                "user": {
                    "__OP_An3Dk__": "delete",
                    "name": "delete",
                    "password": {"__OP_An3Dk__":""}
                }
            }'''
        })
        result = JSONFlattener(op_key, template).process({
            "user": {
                "name": "admin",
                "password": "123"
            }
        })
        self.assertEqual(result, "admin")

    def test_04(self):
        """Dict

        Multiple levels with key renaming.
        """
        op_key, template = JSONConfigParser().parse({
            "__OP_KEY__": "__OP_An3Dk__",
            "template": '''{
                "user": {
                    "name": "other",
                    "educations": {
                        "__OP_An3Dk__": "rename:education",
                        "senior": "delete"
                    }
                }
            }'''
        })
        result = JSONFlattener(op_key, template).process({
            "user": {
                "name": "admin",
                "password": "123",
                "educations": {
                    "junior": "Shanghai No.3 Girls' Middle School",
                    "senior": "Peking University"
                }
            }
        })
        self.assertDictEqual(result, {
            "user": {
                "name": "admin",
                "education": "Peking University"
            }
        })

    def test_05(self):
        """List

        Basic test
        """
        op_key, template = JSONConfigParser().parse({
            "__OP_KEY__": "ops",
            "template": '''{
                "users": {
                    "ops": "list",
                    "0": ""
                }
            }'''
        })
        result = JSONFlattener(op_key, template).process({
            "users": ["admin1", "admin2"],
            "password": ["admin1", "admin2"]
        })
        self.assertDictEqual(result, {'users': ['admin1']})

    def test_06(self):
        """List

        Nested list
        """
        op_key, template = JSONConfigParser().parse({
            "__OP_KEY__": "ops",
            "template": '''{
                "users": {
                    "ops": "list;compact",
                    "all": {
                        "1": ""
                    }
                }
            }'''
        })
        result = JSONFlattener(op_key, template).process({
            "users": [[1, "admin1"], [2, "admin2"]]
        })
        self.assertDictEqual(result, {'users': ['admin1', 'admin2']})

    def test_07(self):
        """List

        Nested dictionary
        """
        op_key, template = JSONConfigParser().parse({
            "__OP_KEY__": "ops",
            "template": '''{
                "users": {
                    "ops": "list",
                    "all": {
                        "login": "delete"
                    }
                }
            }'''
        })
        result = JSONFlattener(op_key, template).process({
            "users": [{
                "id": 1,
                "login": "admin1"
            }, {
                "id": 2,
                "login": "admin2"
            }]
        })
        self.assertDictEqual(result, {'users': ['admin1', 'admin2']})

    def test_08(self):
        """Complex
        """
        op_key, template = JSONConfigParser().parse({
            "__OP_KEY__": "ops",
            "template": '''{
                "wlb_waybill_i_search_response": {
                    "ops": "delete",
                    "subscribtions": {
                        "ops": "rename:subscription",
                        "waybill_apply_subscription_info": {
                            "ops": "delete",
                            "all": {
                                "branch_account_cols": {
                                    "ops": "delete",
                                    "waybill_branch_account": {
                                        "ops": "rename:waybill_address;compact",
                                        "all": {
                                            "shipp_address_cols": {
                                                "ops": "delete",
                                                "waybill_address": {
                                                    "ops": "delete",
                                                    "all": {
                                                        "province": "",
                                                        "city": "",
                                                        "address_detail": "",
                                                        "town": "",
                                                        "area": ""
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "cp_type": "rename:express_type",
                                "cp_code": "rename:express_code"
                            }
                        }
                    }
                }
            }'''
        })
        result = JSONFlattener(op_key, template).process({
            "wlb_waybill_i_search_response": {
                "subscribtions": {
                    "waybill_apply_subscription_info": [{
                        "branch_account_cols": {
                            "waybill_branch_account": [{
                                "seller_id": 3221111,
                                "shipp_address_cols": {
                                    "waybill_address": [{
                                        "area": "jiading",
                                        "province": "shanghai province",
                                        "town": "tanghang",
                                        "address_detail": "shanghai jiading tanghang",
                                        "city": "shanghai city",
                                        "waybill_address_id": 123
                                    }]
                                },
                                "allocated_quantity": 123,
                                "branch_code": "1321",
                                "print_quantity": 32,
                                "cancel_quantity": 10,
                                "branch_name": "SHANGHAI"
                            }]
                        },
                        "cp_type": "EXPRESS",
                        "cp_code": "STO"
                    }, {
                        "branch_account_cols": {
                            "waybill_branch_account": [{
                                "seller_id": 3221111,
                                "shipp_address_cols": {
                                    "waybill_address": [{
                                        "area": "pudong",
                                        "province": "shanghai province",
                                        "town": "tanghang",
                                        "address_detail": "shanghai jiading tanghang",
                                        "city": "shanghai city",
                                        "waybill_address_id": 321
                                    }]
                                },
                                "quantity": 123,
                                "allocated_quantity": 123,
                                "branch_code": "1321",
                                "print_quantity": 32,
                                "cancel_quantity": 10,
                                "branch_name": "SHANGHAI"
                            }]
                        },
                        "cp_type": "EXPRESS",
                        "cp_code": "YUNDA"
                    }]
                }
            }
        })
        self.assertDictEqual(result, {
            "subscription": [{
                "waybill_address": [{
                    "province": "shanghai province",
                    "city": "shanghai city",
                    "address_detail": "shanghai jiading tanghang",
                    "town": "tanghang",
                    "area": "jiading"
                }],
                "express_code": "STO",
                "express_type": "EXPRESS"
            }, {
                "waybill_address": [{
                    "province": "shanghai province",
                    "city": "shanghai city",
                    "address_detail": "shanghai jiading tanghang",
                    "town": "tanghang",
                    "area": "pudong"
                }],
                "express_code": "YUNDA",
                "express_type": "EXPRESS"
            }]
        })
