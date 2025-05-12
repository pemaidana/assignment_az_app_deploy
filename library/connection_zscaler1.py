#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException

def main():
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True),
            device_type=dict(required=True),
            username=dict(required=True),
            password=dict(required=True, no_log=True),
            enable_password=dict(required=False, no_log=True),
            commands=dict(required=True, type='list')
        )
    )

    device_type = module.params["device_type"]
    host = module.params["host"]
    username = module.params["username"]
    password = module.params["password"]
    enable_password = module.params["enable_password"]
    commands = module.params["commands"]

    device = {
        "device_type": device_type,
        "host": host,
        "username": username,
        "password": password,
        "secret": enable_password
    }

    try:
        net_connect = ConnectHandler(**device)
        
        # Enter enable mode
        if enable_password:
            net_connect.enable()

        output = []
        for command in commands:
            output.append(net_connect.send_command_timing(command).splitlines())
            # cmd_output = net_connect.send_command(command)
            # output.extend(cmd_output.split('\n'))

        net_connect.disconnect()
        # module.exit_json(changed=False, stdout="\n".join(output), stdout_lines=output)
        module.exit_json(changed=False, stdout_lines=output)
    except (NetmikoAuthenticationException, NetmikoTimeoutException) as e:
        module.fail_json(msg=f"Connection error: {str(e)}")
    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()