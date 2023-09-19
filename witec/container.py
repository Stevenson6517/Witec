from dataclasses import dataclass
import os
import pathlib
import numpy as np



@dataclass
class HDF5Container:
    file: str

    def __post_init__(self):
        filepath = pathlib.Path(self.file)
        self.spe = SpeFile(filepath.with_suffix(".SPE"))
        self.wip = Witec(filepath.with_suffix(".WIP"))

    @property
    def metadata(self):
        basename = os.path.splitext(self.file)[0] # path w/o extension
        return witec.utils.assemble_metadata(basename) 

    @property
    def main_dataset(self):
        return self.spe.data

    @property
    def position_dataset(self):
        


    def spectrum(self, index):
        """Return a single spectrum from the main dataset."""
        spectra = self.extract_main_dataset()
        return spectra[index]

