import logging
import sox
import numpy as np

class AudioArray(object):
    """ This class provides all needed methods to interact with an audio file
    """
    def __init__(self, samples_in, sample_rate_in, sample_rate_process = None):
        
        # Set and Normalize
        self.samples_in = samples_in / np.abs(samples_in).max()
        self.sample_rate_in = sample_rate_in
        if sample_rate_process is None:
          self.sample_rate = self.sample_rate_in
        else:
          self.sample_rate = sample_rate_process
        self.applied_degradations = []
        self._create_tmp_mirror_file()

    def _create_tmp_mirror_file(self):
        tfm = sox.Transformer()
        tfm.set_output_format(rate=self.sample_rate, 
                              bits=32, channels=2)
        self.samples = tfm.build_array(input_array = self.samples_in, 
                          sample_rate_in = self.sample_rate_in)
        self.samples = self.samples.T

    def apply_degradation(self, degradation):
        self.applied_degradations.append(degradation)
        logging.debug("Applying {0} degradation".format(degradation))
        degradation.apply(self)

    def resample(self, new_sample_rate):
        tfm = sox.Transformer()
        tfm.set_output_format(rate=new_sample_rate, 
                      bits=32, channels=2)
        self.samples = tfm.build_array(input_array = self.samples.T, 
                          sample_rate_in = self.sample_rate)
        self.samples = self.samples.T
