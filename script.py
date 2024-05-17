from jinja2 import Environment, FileSystemLoader
import yaml
from netmiko import ConnectHandler

env = Environment(
    loader=FileSystemLoader('.')
)


def render_config(protocol):
    template_file = f'{protocol}.j2'
    input_file = f'{protocol}_input.yml'

    template = env.get_template(template_file)

    with open(input_file) as file:
        input_data = yaml.load(file, Loader=yaml.FullLoader)

    return template.render(input_data)


def push_config(device, config):
    try:
        net_connect = ConnectHandler(**device)
        output = net_connect.send_config_set(config)

        print("Configuration applied successfully:")
        print(output)

        net_connect.disconnect()

    except Exception as e:
        print("An error occurred:", str(e))

print("Welcome! Please choose a configuration protocol:")
print("1. BGP")
print("2. OSPF")
print("3. Static Routing")


choice = input("Enter your choice (1, 2, or 3): ")

device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'Router1',
    'password': 'Router123@',
}

if choice == '1':
    bgp_config = render_config('bgp')
    print("BGP configuration rendered successfully.")
    push_config(device, bgp_config)

elif choice == '2':
    ospf_config = render_config('ospf')
    print("OSPF configuration rendered successfully.")
    push_config(device, ospf_config)

elif choice == '3':
    static_config = render_config('static')
    print("Static routing configuration rendered successfully.")
    push_config(device, static_config)

else:
    print("Invalid choice. Please enter 1, 2, or 3.")

