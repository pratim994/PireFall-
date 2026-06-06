import os
import csv

def compare_rules(primary_rule: str, secondary_rules: list):
    result = []
    for rule in secondary_rules:
        if str(primary_rule).strip() == str(rule).strip():
            result.append(True)

        else:
            result.append(False)

    return any(result)


def validate_with_route_table(src_addr, dst_addr, src_port, dst_port):
    try:
        rules_stream = open("./helper/Rules.csv", "r")
        rules = csv.reader(rules_stream)

        for rule in rules:

            if compare_rules(rules[1], [src_port, dst_port, "any"]) and compare_rules(rule[3], [dst_addr, src_addr, "any"]):

                if compare_rules(rule[2], [src_port, "any", 0]) and compare_rules(rule[4],[dst_port, "any", 0]):

                    if str(rule[0]).lower() == "allow":
                        return True
                    elif str(rule[0]).lower() == "deny" or str(rule[0]).lower() == "disable":
                        continue

        return False

    except Exception as e:
        print(f"[ERR] Error reading rules : {e}")
        return False



