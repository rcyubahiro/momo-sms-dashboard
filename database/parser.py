# dsa/parser.py
import xml.etree.ElementTree as ET
import json
import os

XML_FILE = 'modified_sms_v2.xml'
JSON_FILE = 'examples/json_schemas.json'

def parse_xml_to_json(xml_file=XML_FILE, json_file=JSON_FILE):
    " Parses XML and converts to a list of JSON objects (list of dicts)."
    if not os.path.exists(xml_file):
        print(f"Error: XML file '{xml_file}' not found.")
        return []

    tree = ET.parse(xml_file)
    root = tree.getroot()
    transactions = []

    for i, sms_record in enumerate(root.findall('sms')):
        # Simple ID generation for the API and DSA tasks
        transaction_id = i + 1
        transaction = {
            'id': transaction_id,
            'type': sms_record.find('transaction_type').text,
            'amount': float(sms_record.find('amount').text),
            'sender': sms_record.find('sender').text,
            'receiver': sms_record.find('receiver').text,
            'timestamp': sms_record.find('timestamp').text,
            # Add any other relevant fields
        }
        transactions.append(transaction)

    with open(json_file, 'w') as f:
        json.dump(transactions, f, indent=4)
        
    print(f"Successfully parsed {len(transactions)} records and saved to {json_file}")
    return transactions

if __name__ == '__main__':
    # --- IMPORTANT CORRECTION ---
    # Assume the XML file is 'modified_sms_v2.xml'
    transactions_data = parse_xml_to_json(xml_file='modified_sms_v2.xml', json_file='examples/json_schemas.json')
    
    if transactions_data:
        print(f"Success! {len(transactions_data)} records parsed and saved to transactions.json.")
    else:
        print("Parsing failed. Check if modified_sms_v2.xml exists in the current directory.")



