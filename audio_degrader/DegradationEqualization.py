import soundfile as sf
import logging
import os
import sox
from .BaseDegradation import Degradation


class DegradationEqualization(Degradation):

    name = "equalize"
    description = "Apply a two-pole peaking equalisation (EQ) filter"
    parameters_info = [
        ("central_freq",
         "100",
         "Central frequency of filter in Hz"),
        ("bandwidth",
         "50",
         "Bandwith of filter in Hz"),
        ("gain",
         "-10",
         "Gain of filter in dBs")]

    def apply(self, audio):
        freq = float(self.parameters_values['central_freq'])
        bw = float(self.parameters_values['bandwidth'])
        q_factor = freq/(bw+1e-16)
        gain = float(self.parameters_values['gain'])
        logging.info("Equalizing. f=%f, bw=%f, gain=%f" % (freq, bw, gain))

        tfm = sox.Transformer()
        tfm.equalizer(frequency = bw, width_q = q_factor, gain_db = gain)
        tfm.set_output_format(bits=audio.bits, channels=1)
        y = tfm.build_array(input_array = audio.samples, 
                            sample_rate_in = audio.sample_rate)

        assert audio.samples.shape == y.shape
        audio.samples = y
