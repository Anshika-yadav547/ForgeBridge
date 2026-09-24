#include <stdio.h>
#include "factory.h"

int main(void)
{
    SensorReading machine7 = {7, 86.2f, 3.1f, 22, 0};

    MachineStatus status = evaluate_machine(
        &machine7,
        TEMP_LIMIT_DEFAULT
    );

    print_diagnostic(&status);

    return status.alarm_active ? 1 : 0;
}