import xml.etree.ElementTree as ET
import json
import re

def parse_sms_body(body):
    amount = "0.0"
    sender = "Unknown"
    receiver = "Unknown"

    if not body:
        return amount, sender, receiver

    # 1. Payment format
    pay_match = re.search(r"payment of ([\d,]+)\s*RWF to ([A-Za-z\s]+?)(?=\s+\d|\s+has|\s+at|$)", body, re.IGNORECASE)
    if pay_match:
        amount = pay_match.group(1).replace(",", "")
        receiver = pay_match.group(2).strip()
        sender = "Account Holder"
        return amount, sender, receiver

    # 2. Transfer format
    tx_match = re.search(r"([\d,]+)\s*RWF transferred to ([A-Za-z\s]+?)\s*\(", body, re.IGNORECASE)
    if tx_match:
        amount = tx_match.group(1).replace(",", "")
        receiver = tx_match.group(2).strip()
        sender = "Account Holder"
        return amount, sender, receiver

    # 3. Received money format
    rec_match = re.search(r"received ([\d,]+)\s*RWF from ([A-Za-z\s]+?)(?=\s+\(|\s+on|\s+\*|$)", body, re.IGNORECASE)
    if rec_match:
        amount = rec_match.group(1).replace(",", "")
        sender = rec_match.group(2).strip()
        receiver = "Account Holder"
        return amount, sender, receiver

    return amount, sender, receiver


def parse_xml_to_json():
    tree = ET.parse("modified_sms_v2.xml")
    root = tree.getroot()
    transactions = []

    for index, sms in enumerate(root.findall("sms"), start=1):
        record_id = index
        address = sms.get("address", "")
        date = sms.get("date", "")
        msg_type = sms.get("type", "")
        body_text = sms.get("body", "")


        amount, sender, receiver = parse_sms_body(body_text)

        record = {
            "id": record_id,
            "address": address,
            "date": date,
            "type": msg_type,
            "body": body_text,
            "amount": amount,
            "sender": sender,
            "receiver": receiver
        }

        transactions.append(record)

    matched = sum(1 for t in transactions if t["amount"] != "0.0" or t["sender"] != "Unknown")
    unmatched = len(transactions) - matched

    with open("api/mock_db.json", "w") as f:
        json.dump(transactions, f, indent=4)

    print(f"Parsed {len(transactions)} records -> api/mock_db.json")
    print(f"Matched by regex : {matched} ({matched/len(transactions)*100:.1f}%)")
    print(f"Unmatched (Unknown/0.0): {unmatched} ({unmatched/len(transactions)*100:.1f}%) - mostly bank-deposit messages")

if __name__ == "__main__":
    parse_xml_to_json()