import xml.etree.ElementTree as ET

tree = ET.parse("./exports/Lab5_TASK1.3.xml")  # create element tree object
root = (
    tree.getroot()
)  # Get root element. root is the highest level of an xml tree which includes all the elements with lower levels.

# Task 3.3_1: Print the values of "sender", "firstSequence", "nextSequence", and "lastSequence" in the Header element.
# Header is the element with index 0 under root. root[0].attrib is a dictionary with keys of "creationTime", "sender", etc.
print(f"Sender: {root[0].attrib['sender']}")
print(f"First Sequence: {root[0].attrib['firstSequence']}")
print(f"Next Sequence: {root[0].attrib['nextSequence']}")
print(f"Last Sequence: {root[0].attrib['lastSequence']}")

# Task 3.3_2: Print out each data element's 'name', 'timestamp' and 'value (or text)'

samples = root[1][0][0][0]
for data_item in samples:
    print(f"Name: {data_item.attrib['name']}")
    print(f"Timestamp: {data_item.attrib['timestamp']}")
    print(f"Value: {data_item.text}")