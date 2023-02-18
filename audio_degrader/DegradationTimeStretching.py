import soundfile as sf
import logging
import sox
import os
from .BaseDegradation import Degradation


class DegradationTimeStretching(Degradation):

    name = "time_stretch"
    description = "Apply time stretching"
    parameters_info = [
        ("time_stretch_factor",
         "0.9",
         "Time stretch factor")]

    def apply(self, audio):
        time_stretch_factor = float(
            self.parameters_values["time_stretch_factor"])
        logging.info(('Time stretching with factor %f' %
                      (time_stretch_factor)))

        tfm = sox.Transformer()
        tfm.tempo(time_stretch_factor)
        tfm.set_output_format(bits=32, channels=2)
        y = tfm.build_array(input_array = audio.samples.T, 
                            sample_rate_in = audio.sample_rate)
        y = y.T
        audio.samples = y
