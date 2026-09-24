#include <stdio.h>
#include "factory.h"

void print_diagnostic(const MachineStatus *status) {
    printf(
        "Machine %d: %s; production=%s; reason=%s\n",
        status->machine_id,
        status->alarm_active ? "ALARM" : "OK",
        status->production_enabled ? "enabled" : "disabled",
        status->reason
    );
}