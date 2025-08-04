Extracts only key fields from EVTX logs (`EventID`, `Provider`, `TimeCreated`, and `Message`) into NDJSON format — making it easier to use command-line tools like `grep` or `jq`.

GUI version will be added very soon.

---

## How to Use?
Install the Dependencies needed

```bash
pip install python-evtx xmltodict
````

Then 

```bash
python evtx_log_cleaner.py -i path/to/input.evtx -o path/to/output.ndjson
````
