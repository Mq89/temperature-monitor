# Temperature Monitor

Temperature monitor software for a Raspberry Pi that:

* monitors the temperature on two thermometers (inside and outside for me)
* saves the values into a database (MySQL)
* shows the current values on a 7 segment display connected via GPIO

## The Thermometers

I'm using two USB thermometers attached to a Raspberry Pi.
The driver can be found in https://github.com/padelt/temper-python.

## The 7 segment display

The display plugin drives a 7 segment display (LTC-4627G) and three LEDs.
The display shows the current temperature values.
Documentation for the display can be found in [docs/LITES11557-1.pdf](docs/LITES11557-1.pdf).
Two LEDs show whether the 7 segment display shows outside or inside temperature.
The third LED shows whether it is warmer outside than inside or whether the outside temperature is below 0°C.

## Install service

    install temperature-monitor.service /lib/systemd/system/

    # first install
    systemctl enable temperature-monitor.service

    # already installed
    systemctl daemon-reload

    systemctl start temperature-monitor.service
