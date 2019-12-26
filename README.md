# HomematicToInflux

This project is a bridge between the [homematic XML-API Plugin](https://github.com/jens-maus/XML-API) and an InfluxDB. Mainly to visualize the sensor and actor states in Grafana.  

Feel free to contribute

## project structure

* `doc` *documentation*
* `hm` *[MODULE] wrapper classes for the homematic xml output*
* `hmtoinflux` *[MODULE] the actually \_\_main\_\_*
* `testdata` *[XML] real xml output for testing without homematic ccu*
* `tests` *yeah tests...*
  * `tests/hm` *tests for the hm module*
  * `tests/hm` *tests for the hmtoinflux module*

## install 

Make sure you had installed the [XML-API](https://github.com/jens-maus/XML-API) on your CCU. Than run `make init` to install the needed python packages.

## run test

`make test`

## run homematicToInflux

`make run-docker`

`make run`

## changelog

no version released

## license

MIT License

## authors

*david bauer*
