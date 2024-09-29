# 复杂结构
# 将扁平结构marshal()转换为嵌套结构
import json

from flask_restful import fields, marshal

resource_fields = {'name': fields.String}
resource_fields['address'] = {}
resource_fields['address']['line 1'] = fields.String(attribute='addr1')
resource_fields['address']['line 2'] = fields.String(attribute='addr2')
resource_fields['address']['city'] = fields.String
resource_fields['address']['state'] = fields.String
resource_fields['address']['zip'] = fields.String
data = {'name': 'bob', 'addr1': '123 fake street', 'addr2': '', 'city': 'New York', 'state': 'NY', 'zip': '10468'}
dumps = json.dumps(marshal(data, resource_fields))
print(
    dumps)  # {"name": "bob", "address": {"line 1": "123 fake street", "line 2": "", "city": "New York", "state": "NY", "zip": "10468"}}

# 列表字段
resource_fields = {'name': fields.String, 'first_names': fields.List(fields.String)}
data = {'name': 'Bougnazal', 'first_names': ['Emile', 'Raoul']}
json_dumps = json.dumps(marshal(data, resource_fields))
print(json_dumps)  # {"name": "Bougnazal", "first_names": ["Emile", "Raoul"]}

# 嵌套字段
# 虽然使用字典嵌套字段可以将平面数据对象转换为嵌套响应，但您可以使用它Nested来解组嵌套数据结构并适当地呈现它们
address_fields = {}
address_fields['line 1'] = fields.String(attribute='addr1')
address_fields['line 2'] = fields.String(attribute='addr2')
address_fields['city'] = fields.String(attribute='city')
address_fields['state'] = fields.String(attribute='state')
address_fields['zip'] = fields.String(attribute='zip')

address_field2 = {
    'line 1': fields.String(attribute='addr1'),
    'line 2': fields.String(attribute='addr2'),
    'city': fields.String(attribute='city'),
    'state': fields.String(attribute='state'),
    'zip': fields.String(attribute='zip')
}

resource_fields = {}
resource_fields['name'] = fields.String
resource_fields['billing_address'] = fields.Nested(address_fields)
resource_fields['shipping_address'] = fields.Nested(address_field2)
address1 = {'addr1': '123 fake street', 'city': 'New York', 'state': 'NY', 'zip': '10468'}
address2 = {'addr1': '555 nowhere', 'city': 'New York', 'state': 'NY', 'zip': '10468'}
data = {'name': 'bob', 'billing_address': address1, 'shipping_address': address2}

s = json.dumps(marshal(data, resource_fields))
print(s)
# {"name": "bob", "billing_address": {"line 1": "123 fake street", "line 2": null, "city": "New York", "state": "NY", "zip": "10468"}, "shipping_address": {"line 1": "555 nowhere", "line 2": null, "city": "New York", "state": "NY", "zip": "10468"}}