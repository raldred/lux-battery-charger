"""Constants for lux_battery_charger."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

API_BASE = "https://api.octopus.energy/v1/products/"

NAME = "Lux Battery Charger"
AUTHOR = "Rob Aldred"
DOMAIN = "lux_battery_charger"
VERSION = "0.0.1"
ATTRIBUTION = "Data provided by Octopus Energy"

ATTR_ENTRY_TYPE = "entry_type"

TARIFF_REGION = "region"
IMPORT_TARIFF = "import_tariff"
EXPORT_TARIFF = "export_tariff"
UPDATE_INTERVAL = "update_interval"

DEFAULT_TARIFF_REGION = "H" # North-West
DEFAULT_IMPORT_TARIFF = "AGILE-FLEX-22-11-25" # Latest as of 8 Nov 2023
DEFAULT_EXPORT_TARIFF = "AGILE-OUTGOING-19-05-13"  # Latest as of 8 Nov 2023
DEFAULT_UPDATE_INTERVAL=30 # Refresh prices every 30 minutes
