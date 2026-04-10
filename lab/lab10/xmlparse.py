import os
import xml.etree.ElementTree as ET
    
print(os.getcwd())
with open("sample_output.xml", "r") as f:
    xml_string = f.read()

def get_raw_sound_data(xml_string):
    root = ET.fromstring(xml_string)
    MTCONNECT_STR = root.tag.split("}")[0]+"}"    
    header = root.find("./"+MTCONNECT_STR+"Header") # get header of XML reponse
    header_attribs = header.attrib # get header attribute
    for device in root.iter(MTCONNECT_STR+'DeviceStream'):
        for sample in device.iter(MTCONNECT_STR+'Samples'): # for Sample category
            for tags in sample:
                tagName = tags.tag # get tag info
                tagName = tagName[40:] # tagname
                # print(timestamp, timestamp_mysql)
                name = tags.get('name') # get name info
                if name is None or name == " ": # in case name attribute is empty
                    name = "NULL"
                value = tags.text # get value (text)

        return value
    

window = []

window.append(get_raw_sound_data(xml_string))
window = window[-23:] # keep only the last 23 data points

model = tf.keras.models.load_model(export_name)
prediction = model.predict([window])
print(prediction)
