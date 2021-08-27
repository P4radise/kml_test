import sys
import subprocess


subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'python_dependencies.txt'], stdout=subprocess.DEVNULL)


from jsonschema import validate
from import_kml import Integration, KML, CSV, Import
from integration_log import build_logger
import re
import json


with open('settings.json', "rb") as PFile:
    settings_data = json.loads(PFile.read().decode('utf-8'))

with open('settings_schema.json', 'rb') as PFile:
    data_schema = json.loads(PFile.read().decode('utf-8'))

try:
    validate(settings_data, data_schema)
except Exception as e:
    raise Exception(f'Incorrect value in the settings file\n{str(e)}')

url_kmz = settings_data['urlKMZ']
url_onevizion = settings_data['urlOneVizion']
ov_access_key = settings_data['ovAccessKey']
ov_secret_key = settings_data['ovSecretKey']
import_name = settings_data['importName']
import_action = settings_data['importAction']

url_onevizion_without_protocol = re.sub('^http://|^https://', '', settings_data['urlOneVizion'][:-1])

integration_log = build_logger()
kml_file = KML(url_kmz, integration_log)
csv_file = CSV(integration_log)
integration_import = Import(url_onevizion, url_onevizion_without_protocol, ov_access_key, ov_secret_key, import_name, import_action, integration_log)
integration = Integration(kml_file, csv_file, integration_import, integration_log)

try:
    integration.start_integration()
except Exception as e:
    integration_log.info(str(e))
    raise e
