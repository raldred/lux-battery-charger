# Octopus Agile

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

_Integration to integrate with [octopus_agile][octopus_agile]._

**This integration will set up the following platforms.**

Platform | Description
-- | --
`binary_sensor` | Show something `True` or `False`.
`sensor` | Show info from blueprint API.
`switch` | Switch something `True` or `False`.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `octopus_agile`.
1. Download _all_ the files from the `custom_components/octopus_agile/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Octopus Agile"

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[octopus_agile]: https://github.com/raldred/octopus_agile
[buymecoffee]: https://www.buymeacoffee.com/raldred
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/raldred/octopus_agile.svg?style=for-the-badge
[commits]: https://github.com/raldred/octopus_agile/commits/main
[license-shield]: https://img.shields.io/github/license/raldred/octopus_agile.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Rob%20Aldred%20%40raldred-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/raldred/octopus_agile.svg?style=for-the-badge
[releases]: https://github.com/raldred/octopus_agile/releases
