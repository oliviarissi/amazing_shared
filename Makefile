VENV := env
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
REQ := requirements.txt
SCRIPT := a_maze_ing.py
CONFIG ?= sample_config.txt
VENVDONE := $(VENV)/.venv_created
INSTALLED := $(VENV)/.requirements_installed

.PHONY: all run clean

all: $(INSTALLED)

$(VENVDONE):
	python3 -m venv $(VENV)
	touch $(VENVDONE)

$(INSTALLED): $(VENVDONE) $(REQ)
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQ)
	touch $(INSTALLED)

run: $(INSTALLED)
	$(PYTHON) $(SCRIPT) $(CONFIG)

clean:
	rm -rf $(VENV) $(VENVDONE) $(INSTALLED)