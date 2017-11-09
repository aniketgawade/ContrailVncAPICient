import re
from vnc_api import vnc_api
from cfgm_common.exceptions import RefsExistError

def delete_recursively(client, del_uuid):
        try:
                client.network_ipam_delete(id = del_uuid)
        except RefsExistError as err:
                print (str(err))
                uuid = re.findall('([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', str(err))
                print(uuid)



def main():
        client = vnc_api.VncApi("127.0.0.1", 8082, False)
        delete_recursively(client, '9f657c8b-9523-4881-ae3a-96e1c846e49d')

if __name__ == "__main__":
        main()

