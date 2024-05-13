# make data D=path/to/network/storage
#     - Syncs online folder to data folder in this project
#     - network/folder/-> data/folder/
#     - Writes network path D to temp folder for future syncing
# make data
#     - Sync all network paths specified in temp/sync.txt
# make h5
#     - Generate h5 file from .SPE and .WIP pairs
# make hdf5
#     - Alias for make h5
#
# ASSUMPTIONS
# Network directory has structure network/folder/file
# Any .WIP file

SHELL = /bin/bash
ENV = witec
DATA_DIR ?= data
SOURCE_DIR ?= $D

SPE := $(wildcard data/*/*.SPE)
WIP := $(wildcard data/*/*2024*.WIP)
HDF5 := $(addsuffix .hdf5, $(basename $(subst $(DATA_DIR),results,$(WIP))))

environment:
ifneq ($(CONDA_DEFAULT_ENV),$(ENV))
	$(error ERROR: Activate the $(ENV) virtual environment first))
endif

hdf5: $(HDF5)
h5: $(HDF5)

$(HDF5): $(SPE)

results/%.hdf5: data/%.WIP | environment
	@mkdir -p $(@D)
	@echo "Generating $@"
	@python witec/convert.py $< --output $@ || true

tmp/sync.txt:
	@mkdir -p $(@D)
	@touch $@

data: tmp/sync.txt | environment
ifdef SOURCE_DIR
	@echo $(SOURCE_DIR) >> $<
	@sort -u -o $< $<
endif
	$(eval SOURCE_DIRS := $(shell cat $<))
	@$(foreach SOURCE_DIR,$(SOURCE_DIRS), rsync -Pavz $(SOURCE_DIR) $(DATA_DIR)/ &&) true

