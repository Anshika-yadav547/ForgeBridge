#include "factory.h"

int temperature_exceeds_limit(float temperature_c, float limit_c) {
    return temperature_c >= limit_c;
}