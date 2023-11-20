# Octopus Agile

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

This integration is intended to pull pricing data from Octopus and automate battery charging of a connected lux inverter.
This relies on a lux integration, either lxp-bridge or LuxPython

Ispiration comes from other wonderful integrations, particularly
* Predbat
* Octoblock

**This integration will set up the following platforms.**

Entity | Description
-- | --
`sensor.lux_charger_import_prices` | Show Octopus Agile export price data
`sensor.lux_charger_export_prices` | Show Octopus Agile export price data
`sensor.lux_charger_battery_hours_left`
`sensor.lux_charger_low_import_start`|Start time of next low import block
`sensor.lux_charger_low_import_end`|End time of next low import block
`sensor.lux_charger_low_import_cost`|Average cost during the next low import block
`sensor.lux_charger_high_export_start`|Start time of next high export block
`sensor.lux_charger_high_export_end`|End time of next high export block
`sensor.lux_charger_high_export_cost`|Average cost during the next high export block
``

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `octopus_agile`.
1. Download _all_ the files from the `custom_components/lux_battery_charger/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Octopus Agile"

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[lux-battery-charger]: https://github.com/raldred/lux-battery-charger
[buymecoffee]: https://www.buymeacoffee.com/raldred
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/raldred/lux-battery-charger.svg?style=for-the-badge
[commits]: https://github.com/raldred/lux-battery-charger/commits/main
[license-shield]: https://img.shields.io/github/license/raldred/lux-battery-charger.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Rob%20Aldred%20%40raldred-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/raldred/lux-battery-charger.svg?style=for-the-badge
[releases]: https://github.com/raldred/lux-battery-charger/releases
