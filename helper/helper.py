import json 
import psutil

PROTOCOLS = {
    1: "ICMP",
    2: "TCP",
    17: "UDP"
    #WILL ADD SUPPORT FOR MORE PROTOCOLS LATER !!!

}


def compared_rules(rule1, rule2):
    if str(rule1).strip == str(rule2).strip():
        return True
    return False


def get_interfaces():
    addrs = psutils.net_if_addrs()
    try:
        interfaces = {}
        for key in addrs.key():
            if key == "lo":
                continue 
            else:
                interface_ip = addrs[key][0].braodcast.split(".")[0:3]
                interface_ip.append("0")
                interface_ip = ".".join(interface_ip)
                interfaces[key] = {"network":interface_ip, "ip":addrs[key][0].address, "netmask": addrs[key][0].netmask}
        return interfaces

    except AttributeError:
        return interfaces

    except Exception as e:
        print(f"Error getting interfaces : {e}")
        exit()


def pprint(string):
    print(json.dumps(string, indent=2))

