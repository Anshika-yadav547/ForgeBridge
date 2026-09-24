#include "factory.h"

int production_can_run(const MachineStatus *status) {
    return status && status->production_enabled;
}