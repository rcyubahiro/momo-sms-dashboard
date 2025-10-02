import xml.etree.ElementTree as ET
import json
import os

# Step 1: Load and parse XML file
xml_file = 'modified_sms_v2.xml'
if not os.path.exists(xml_file):
    raise FileNotFoundError(f"{xml_file} not found in current directory")

tree = ET.parse(xml_file)
root = tree.getroot()

transactions = []

# Step 2: Loop through each <sms> element
for i, sms in enumerate(root.findall('sms')):
    transaction = {
        "id": i + 1,
        "type": sms.find('transaction_type').text,
        "amount": float(sms.find('amount').text),
        "sender": sms.find('sender').text,
        "receiver": sms.find('receiver').text,
        "timestamp": sms.find('timestamp').text
    }
    transactions.append(transaction)

# Step 3: Save the result into a JSON file
output_path = 'examples/json_schemas.json'
os.makedirs('examples', exist_ok=True)

with open(output_path, 'w') as f:
    json.dump(transactions, f, indent=4)

print(f" Parsed {len(transactions)} transactions and saved to {output_path}")
