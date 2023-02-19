import soundfile as sf
import logging
import numpy as np
import sox
import os
from .BaseDegradation import Degradation


class DegradationPitchShifting(Degradation):

    name = "pitch_shift"
    description = "Apply pitch shifting"
    parameters_info = [
        ("pitch_shift_factor",
         "0.9",
         "Pitch shift factor")]
    
    def apply(self, audio):
        pitch_shift_factor = float(
            self.parameters_values["pitch_shift_factor"])
        n_semitones = 12 * np.log2(pitch_shift_factor)
        logging.info('Shifting pitch with factor %f, i.e. %f semitones' %
                     (pitch_shift_factor, n_semitones))

        tfm = sox.Transformer()
        tfm.pitch(n_semitones)
        tfm.set_output_format(bits=audio.bits, channels=1)
        
        y = tfm.build_array(input_array = audio.samples, 
                            sample_rate_in = audio.sample_rate)
        audio.samples = y
