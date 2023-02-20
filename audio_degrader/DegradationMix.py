import os
import soundfile as sf
import logging
import numpy as np
import sox
from .BaseDegradation import Degradation

class DegradationMix(Degradation):

    name = "mix"
    description = ("Mix input with a specified noise. " +
                   "The noise can be specified with its full path, URL " +
                   "(requires wget installed),  or "
                   "relative to the resources directory (see -l option)")
    parameters_info = [("noise",
                        "sounds/ambience-pub.wav",
                        "Full or relative path (to resources dir) of noise"),
                       ("snr",
                        "6",
                        "Desired Signal-to-Noise-Ratio [dB]")]

    def read_noise(self, noise_path, audio):
        """ Read samples of noise resampled at the sample_rate of input
        Args:
            audio (AudioArray): Input AudioArray
        Returns:
            (np.array): Samples of noise 1D
        """
        noise_samples, noise_sample_rate = sf.read(noise_path)
        tfm = sox.Transformer()
        tfm.set_output_format(rate=audio.sample_rate, 
                              bits=audio.bits, channels=1)
        noise_samples = tfm.build_array(input_array = noise_samples, 
                                sample_rate_in = noise_sample_rate)
        
        return noise_samples

    def adjust_noise_duration(self, noise_samples, audio):
        """ Adjust the duration of noise_samples to fit audio_file
        In case it is shorter, it repeats the noise.
        Args:
            noise_samples (np.array): Samples of noise with shape (1, nsamples)
            audio (AudioArray): Input audio
        Returns:
            (np.array): Samples of noise 1D
        """
        input_num_samples = audio.samples.shape[0]
        while noise_samples.shape[0] < input_num_samples:
            noise_samples = np.concatenate((noise_samples, noise_samples))
        noise_samples = noise_samples[:input_num_samples]
        return noise_samples

    def get_actual_noise_path(self):
        """ Resolve full path of noise
        The specified noise path could be a relative path
        """
        import audio_degrader
        resources_dir = os.path.join(audio_degrader.__path__[0],
                                     'resources')
        noise_path = self.parameters_values['noise']
        noise_path_resource = os.path.join(resources_dir, noise_path)
        if (not os.path.isfile(noise_path)
                and os.path.isfile(noise_path_resource)):
            return noise_path_resource
        else:
            return noise_path

    def get_noise_gain_factor(self, snr_dbs, rms_noise, rms_input):
        """ Get gain factor that should be applied to noise
        Args:
            snr_dbs (float): Desired SNR in dBs
            rms_noise (float): RMS value of noise
            rms_input (float): RMS value of input
        Returns:
            (float): Noise gain factor
        """
        logging.debug("RMS noise: %f" % rms_noise)
        logging.debug("RMS input: %f" % rms_input)
        snr_linear = 10 ** (snr_dbs / 20.0)
        logging.debug("SNR , SNR linear: %f , %f" % (snr_dbs, snr_linear))
        noise_gain_factor = rms_input / rms_noise / snr_linear
        logging.debug("noise_gain_factor: %f" % noise_gain_factor)
        return noise_gain_factor

    def apply(self, audio):
        noise_path = self.get_actual_noise_path()
        noise_samples = self.read_noise(noise_path, audio)
        noise_samples = self.adjust_noise_duration(noise_samples, audio)
        rms_noise = np.sqrt(np.mean(np.power(noise_samples, 2)))
        rms_input = np.sqrt(np.mean(np.power(audio.samples, 2)))
        noise_gain_factor = self.get_noise_gain_factor(
            float(self.parameters_values['snr']),
            rms_noise,
            rms_input)
        y = audio.samples + noise_samples * noise_gain_factor
        # Normalize output RMS to fit input RMS
        rms_y = np.sqrt(np.mean(np.power(y, 2)))
        y = y * rms_input / rms_y
        audio.samples = y
