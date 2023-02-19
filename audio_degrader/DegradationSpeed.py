import soundfile as sf
import logging
from .BaseDegradation import Degradation
import sox
import os


class DegradationSpeed(Degradation):

    name = "speed"
    description = "Change playback speed"
    parameters_info = [
        ("speed",
         "0.9",
         "Playback speed factor")]

    def apply(self, audio):
        speed_factor = float(self.parameters_values['speed'])
        logging.info('Modifying speed with factor %f' % speed_factor)

        tfm = sox.Transformer()
        tfm.speed(speed_factor)
        tfm.set_output_format(bits=audio.bits, channels=1)
        y = tfm.build_array(input_array = audio.samples, 
                            sample_rate_in = audio.sample_rate)
        audio.samples = y
