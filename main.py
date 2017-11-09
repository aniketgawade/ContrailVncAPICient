import re
from vnc_api import vnc_api
from cfgm_common.exceptions import RefsExistError

class Stack:
	def __init__(self):
		self.items = []
	def push(self, item):
		self.items.append(item)
	def pop(self):
		self.items.pop()
	def isEmpty(self):
		return self.items == []

stk = Stack()
		
def delete_recursively(client, del_uuid):
	try:
		_, res_type = client.id_to_fq_name_type(del_uuid)
		print(res_type, del_uuid)
		client._object_delete(res_type, id = del_uuid)
	except RefsExistError as err:
		print (str(err))
		stk.push(del_uuid)		
		uuids = re.findall('([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', str(err))
		print(uuids)
		for uuid in uuids:
			delete_recursively(client, uuid)
	except NoIdError:
		print("Uuid has already been deleted")


def delete_by_uuid(client, del_uuid):
	try:
		_, res_type = client.id_to_fq_name_type(del_uuid)
		print(res_type, del_uuid)
		client._object_delete(res_type, id = del_uuid)
	except RefsExistError as err:
		print (str(err))

def main():
	client = vnc_api.VncApi("127.0.0.1", 8082, False)
	delete_recursively(client, '9f657c8b-9523-4881-ae3a-96e1c846e49d')
	while stk.isEmpty() == False:
		print("Am clearing stack")
		pend_uuid = stk.pop()
		delete_by_uuid(client, pend_uuid)

if __name__ == "__main__":
	main()


