#include "factory.h"

float read_temperature(int machine_id, float raw_sensor_value) {
    (void)machine_id;

    /* The 2005 sensor board reports tenths of a degree. */
    return raw_sensor_value / 10.0f;
}