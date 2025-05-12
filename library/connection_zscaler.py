#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
from netmiko import ConnectHandler

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True),
            device_type=dict(required=True),
            username=dict(required=True),
            password=dict(required=True, no_log=True),
            commands=dict(required=True, type='list')
        )
    )

    device_type = module.params["device_type"]
    host = module.params["host"]
    username = module.params["username"]
    password = module.params["password"]
    commands = module.params["commands"]

    device = {
        "device_type": device_type,
        "host": host,
        "username": username,
        "password": password
    }
    try:
        net_connect = ConnectHandler(**device)
        output = []
        for command in commands:
            cmd_output = (net_connect.send_command_timing(command))
            output.extend(cmd_output.split('\n'))
        net_connect.disconnect()
        module.exit_json(changed=False, stdout="\n".join(output), stdout_lines=output)
    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()