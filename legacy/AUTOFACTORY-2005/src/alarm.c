#include "factory.h"

MachineStatus evaluate_machine(
    const SensorReading *reading,
    float temperature_limit_c
) {
    MachineStatus status = {
        reading->machine_id,
        0,
        1,
        "normal"
    };

    if (reading->emergency_stop) {
        status.alarm_active = 1;
        status.production_enabled = 0;
        status.reason = "emergency stop engaged";
    } else if (
        temperature_exceeds_limit(
            reading->temperature_c,
            temperature_limit_c
        )
    ) {
        status.alarm_active = 1;
        status.production_enabled = 0;
        status.reason = "temperature limit exceeded";
    } else if (reading->coolant_flow_lpm < 10) {
        status.alarm_active = 1;
        status.production_enabled = 0;
        status.reason = "insufficient coolant flow";
    } else if (reading->vibration_mm_s > 7.5f) {
        status.alarm_active = 1;
        status.production_enabled = 0;
        status.reason = "excessive vibration";
    }

    return status;
}