import soundfile as sf
import logging
import os
import sox
from .BaseDegradation import Degradation


class DegradationDynamicRangeCompression(Degradation):

    name = "dr_compression"
    description = "Apply dynamic range compression"
    parameters_info = [
        ("degree",
         "0",
         "Degree of compression. Presets from 0 (soft) to 3 (hard)")]

    def apply(self, audio):
        
        degree = int(self.parameters_values['degree'])
        if degree == 1:
          attack_time = 0.01
          decay_time = 0.20
          tf_points = [(-100,-100),(-40,-40), (-10,-30)]
          gain = 5

        elif degree == 2:
          attack_time = 0.01
          decay_time = 0.20
          tf_points = [(-100,-100),(-50.01,-50.01),(-50,-40), 
                       (-30,-40),(-10,-30)]
          gain = 12
        elif degree == 3:
          attack_time = 0.01
          decay_time = 0.10
          tf_points = [(-100,-100),(-70,-70),(-30,-70),(0,-70)]
          gain = 45
    
        tfm = sox.Transformer()
        tfm.compand(attack_time = attack_time, decay_time = decay_time, 
                    tf_points = tf_points)
        tfm.gain(gain, normalize = False, limiter = False)
        tfm.set_output_format(bits=32, channels=2)
        y = tfm.build_array(input_array = audio.samples.T, 
                            sample_rate_in = audio.sample_rate)
        y = y.T

        assert audio.samples.shape == y.shape
        audio.samples = y
