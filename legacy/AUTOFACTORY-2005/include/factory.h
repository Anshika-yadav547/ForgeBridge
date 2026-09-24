#ifndef FACTORY_H
#define FACTORY_H

#define MAX_MACHINES 16
#define TEMP_LIMIT_DEFAULT 85.0f

typedef struct {
    int machine_id;
    float temperature_c;
    float vibration_mm_s;
    int coolant_flow_lpm;
    int emergency_stop;
} SensorReading;

typedef struct {
    int machine_id;
    int alarm_active;
    int production_enabled;
    const char *reason;
} MachineStatus;

float read_temperature(int machine_id, float raw_sensor_value);

int temperature_exceeds_limit(
    float temperature_c,
    float limit_c
);

MachineStatus evaluate_machine(
    const SensorReading *reading,
    float temperature_limit_c
);

void print_diagnostic(const MachineStatus *status);

int production_can_run(const MachineStatus *status);

#endif