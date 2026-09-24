CC ?= cc
CFLAGS ?= -std=c99 -Wall -Wextra -Wpedantic -Iinclude
BUILD=build
SOURCES=$(wildcard src/*.c)

all: $(BUILD)/autofactory

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/autofactory: $(SOURCES) | $(BUILD)
	$(CC) $(CFLAGS) $(SOURCES) -o $@

test: $(BUILD)/autofactory
	./tests/run_tests.sh

clean:
	rm -rf $(BUILD)