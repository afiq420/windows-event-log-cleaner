import json
import xmltodict
import argparse
from Evtx.Evtx import Evtx

def clean_data(data):
    if isinstance(data, list):
        return " ".join(str(d.get("#text", d)) if isinstance(d, dict) else str(d) for d in data)
    if isinstance(data, dict):
        return data.get("#text", "")
    return str(data)

def clean_event(xml_string):
    try:
        event = xmltodict.parse(xml_string).get("Event", {})
        system = event.get("System", {})
        eventdata = event.get("EventData", {})

        return {
            "EventID": system.get("EventID", {}).get("#text", ""),
            "Provider": system.get("Provider", {}).get("@Name", ""),
            "TimeCreated": system.get("TimeCreated", {}).get("@SystemTime", ""),
            "Message": clean_data(eventdata.get("Data", ""))
        }
    except:
        return None

def evtx_to_ndjson(evtx_path, output_path):
    count = 0
    with Evtx(evtx_path) as log, open(output_path, "w", encoding="utf-8") as outfile:
        for record in log.records():
            cleaned = clean_event(record.xml())
            if cleaned:
                outfile.write(json.dumps(cleaned) + "\n")
                count += 1
    print(f"Exported {count} cleaned events to NDJSON: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert .evtx log to clean NDJSON.")
    parser.add_argument("-i", "--input", required=True, help="Path to .evtx file")
    parser.add_argument("-o", "--output", required=True, help="Path to output file")
    args = parser.parse_args()
    evtx_to_ndjson(args.input, args.output)
