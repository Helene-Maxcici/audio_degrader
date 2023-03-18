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
        if abs(time_stretch_factor - 1.0) > 0.1:
          tfm.tempo(time_stretch_factor)
        else:
          tfm.stretch(time_stretch_factor)
        tfm.set_output_format(bits=audio.bits, channels=1)
        y = tfm.build_array(input_array = audio.samples, 
                            sample_rate_in = audio.sample_rate)
        audio.samples = y
