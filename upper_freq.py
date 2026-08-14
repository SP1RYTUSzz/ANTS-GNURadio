#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.12.0

from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import threading
import time




class upper_freq(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.vec_len = vec_len = 4096
        self.samp_rate = samp_rate = 30.72E+06
        self.filesink_freq = filesink_freq = 10
        self.upper_or_lower = upper_or_lower = "upper"
        self.threshold2 = threshold2 = 10
        self.threshold1 = threshold1 = 6
        self.threshold0 = threshold0 = 3
        self.lna_makeup_gain = lna_makeup_gain = -12
        self.func_probe_noise = func_probe_noise = 0
        self.freq = freq = 2.435E+09
        self.filesink_directory = filesink_directory = r"/home/antfarm/Documents/Antman_GNURadio_Code/Results/"
        self.filesink_decimation = filesink_decimation = round(samp_rate / vec_len / filesink_freq)

        ##################################################
        # Blocks
        ##################################################

        self.probe_noise_floor = blocks.probe_signal_f()
        def _func_probe_noise_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.probe_noise_floor.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_func_probe_noise,val))
              except AttributeError:
                self.set_func_probe_noise(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _func_probe_noise_thread = threading.Thread(target=_func_probe_noise_probe)
        _func_probe_noise_thread.daemon = True
        _func_probe_noise_thread.start()
        self.soapy_limesdr_source_0 = None
        dev = 'driver=lime'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_limesdr_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_source_0.set_bandwidth(0, 0.0)
        self.soapy_limesdr_source_0.set_frequency(0, freq)
        self.soapy_limesdr_source_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_source_0.set_gain(0, min(max(20.0, -12.0), 61.0))
        self.fft_vxx_0 = fft.fft_vcc(vec_len, True, window.blackmanharris(vec_len), True, 1)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, vec_len)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, vec_len)
        self.blocks_threshold_ff_0_0_0 = blocks.threshold_ff((func_probe_noise+threshold2), (func_probe_noise+threshold2), 0)
        self.blocks_threshold_ff_0_0 = blocks.threshold_ff((func_probe_noise+threshold1), (func_probe_noise+threshold1), 0)
        self.blocks_threshold_ff_0 = blocks.threshold_ff((func_probe_noise+threshold0), (func_probe_noise+threshold0), 0)
        self.blocks_stream_to_vector_1_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, vec_len)
        self.blocks_stream_to_vector_1_0 = blocks.stream_to_vector(gr.sizeof_float*1, vec_len)
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_float*1, vec_len)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_len)
        self.blocks_nlog10_ff_0_0_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, vec_len, 0)
        self.blocks_multiply_const_xx_1_0 = blocks.multiply_const_ff(1/vec_len, 1)
        self.blocks_multiply_const_xx_1 = blocks.multiply_const_ff(1/vec_len, vec_len)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(1/vec_len, vec_len)
        self.blocks_integrate_xx_2_0_0 = blocks.integrate_ff(filesink_decimation, vec_len)
        self.blocks_integrate_xx_2_0 = blocks.integrate_ff(filesink_decimation, vec_len)
        self.blocks_integrate_xx_2 = blocks.integrate_ff(filesink_decimation, vec_len)
        self.blocks_integrate_xx_1 = blocks.integrate_ff(vec_len, 1)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(filesink_decimation, vec_len)
        self.blocks_file_sink_0_1 = blocks.file_sink(gr.sizeof_float*1, filesink_directory+"avgNF-upper_"+__import__("time").strftime("%Y%m%d_%H")+".bin", True)
        self.blocks_file_sink_0_1.set_unbuffered(False)
        self.blocks_file_sink_0_0_0_0 = blocks.file_sink(gr.sizeof_float*vec_len, filesink_directory+"occupancy-upper2_"+__import__("time").strftime("%Y%m%d_%H")+".bin", True)
        self.blocks_file_sink_0_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_float*vec_len, filesink_directory+"occupancy-upper1_"+__import__("time").strftime("%Y%m%d_%H")+".bin", True)
        self.blocks_file_sink_0_0_0.set_unbuffered(False)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_float*vec_len, filesink_directory+"occupancy-upper0_"+__import__("time").strftime("%Y%m%d_%H")+".bin", True)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*vec_len, filesink_directory+"avgFFT-upper_"+__import__("time").strftime("%Y%m%d_%H")+".bin", True)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(vec_len)
        self.blocks_add_const_vxx_1_0 = blocks.add_const_ff(lna_makeup_gain)
        self.blocks_add_const_vxx_1 = blocks.add_const_vff([lna_makeup_gain]*vec_len)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(lna_makeup_gain)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_file_sink_0_1, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.probe_noise_floor, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_threshold_ff_0_0, 0))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_threshold_ff_0_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_multiply_const_xx_1, 0))
        self.connect((self.blocks_integrate_xx_1, 0), (self.blocks_multiply_const_xx_1_0, 0))
        self.connect((self.blocks_integrate_xx_2, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_integrate_xx_2_0, 0), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.blocks_integrate_xx_2_0_0, 0), (self.blocks_file_sink_0_0_0_0, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_multiply_const_xx_1, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_multiply_const_xx_1_0, 0), (self.blocks_nlog10_ff_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_add_const_vxx_1, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_nlog10_ff_0_0_0, 0), (self.blocks_add_const_vxx_1_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.blocks_integrate_xx_2, 0))
        self.connect((self.blocks_stream_to_vector_1_0, 0), (self.blocks_integrate_xx_2_0, 0))
        self.connect((self.blocks_stream_to_vector_1_0_0, 0), (self.blocks_integrate_xx_2_0_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_stream_to_vector_1, 0))
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_stream_to_vector_1_0, 0))
        self.connect((self.blocks_threshold_ff_0_0_0, 0), (self.blocks_stream_to_vector_1_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_integrate_xx_1, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_nlog10_ff_0_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.soapy_limesdr_source_0, 0), (self.blocks_stream_to_vector_0, 0))


    def get_vec_len(self):
        return self.vec_len

    def set_vec_len(self, vec_len):
        self.vec_len = vec_len
        self.set_filesink_decimation(round(self.samp_rate / self.vec_len / self.filesink_freq))
        self.blocks_add_const_vxx_1.set_k([self.lna_makeup_gain]*self.vec_len)
        self.blocks_multiply_const_xx_0.set_k(1/self.vec_len)
        self.blocks_multiply_const_xx_1.set_k(1/self.vec_len)
        self.blocks_multiply_const_xx_1_0.set_k(1/self.vec_len)
        self.fft_vxx_0.set_window(window.blackmanharris(self.vec_len))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_filesink_decimation(round(self.samp_rate / self.vec_len / self.filesink_freq))
        self.soapy_limesdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_filesink_freq(self):
        return self.filesink_freq

    def set_filesink_freq(self, filesink_freq):
        self.filesink_freq = filesink_freq
        self.set_filesink_decimation(round(self.samp_rate / self.vec_len / self.filesink_freq))

    def get_upper_or_lower(self):
        return self.upper_or_lower

    def set_upper_or_lower(self, upper_or_lower):
        self.upper_or_lower = upper_or_lower

    def get_threshold2(self):
        return self.threshold2

    def set_threshold2(self, threshold2):
        self.threshold2 = threshold2
        self.blocks_threshold_ff_0_0_0.set_hi((self.func_probe_noise+self.threshold2))
        self.blocks_threshold_ff_0_0_0.set_lo((self.func_probe_noise+self.threshold2))

    def get_threshold1(self):
        return self.threshold1

    def set_threshold1(self, threshold1):
        self.threshold1 = threshold1
        self.blocks_threshold_ff_0_0.set_hi((self.func_probe_noise+self.threshold1))
        self.blocks_threshold_ff_0_0.set_lo((self.func_probe_noise+self.threshold1))

    def get_threshold0(self):
        return self.threshold0

    def set_threshold0(self, threshold0):
        self.threshold0 = threshold0
        self.blocks_threshold_ff_0.set_hi((self.func_probe_noise+self.threshold0))
        self.blocks_threshold_ff_0.set_lo((self.func_probe_noise+self.threshold0))

    def get_lna_makeup_gain(self):
        return self.lna_makeup_gain

    def set_lna_makeup_gain(self, lna_makeup_gain):
        self.lna_makeup_gain = lna_makeup_gain
        self.blocks_add_const_vxx_0.set_k(self.lna_makeup_gain)
        self.blocks_add_const_vxx_1.set_k([self.lna_makeup_gain]*self.vec_len)
        self.blocks_add_const_vxx_1_0.set_k(self.lna_makeup_gain)

    def get_func_probe_noise(self):
        return self.func_probe_noise

    def set_func_probe_noise(self, func_probe_noise):
        self.func_probe_noise = func_probe_noise
        self.blocks_threshold_ff_0.set_hi((self.func_probe_noise+self.threshold0))
        self.blocks_threshold_ff_0.set_lo((self.func_probe_noise+self.threshold0))
        self.blocks_threshold_ff_0_0.set_hi((self.func_probe_noise+self.threshold1))
        self.blocks_threshold_ff_0_0.set_lo((self.func_probe_noise+self.threshold1))
        self.blocks_threshold_ff_0_0_0.set_hi((self.func_probe_noise+self.threshold2))
        self.blocks_threshold_ff_0_0_0.set_lo((self.func_probe_noise+self.threshold2))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.soapy_limesdr_source_0.set_frequency(0, self.freq)

    def get_filesink_directory(self):
        return self.filesink_directory

    def set_filesink_directory(self, filesink_directory):
        self.filesink_directory = filesink_directory
        self.blocks_file_sink_0.open(self.filesink_directory+"avgFFT-upper_"+__import__("time").strftime("%Y%m%d_%H")+".bin")
        self.blocks_file_sink_0_0.open(self.filesink_directory+"occupancy-upper0_"+__import__("time").strftime("%Y%m%d_%H")+".bin")
        self.blocks_file_sink_0_0_0.open(self.filesink_directory+"occupancy-upper1_"+__import__("time").strftime("%Y%m%d_%H")+".bin")
        self.blocks_file_sink_0_0_0_0.open(self.filesink_directory+"occupancy-upper2_"+__import__("time").strftime("%Y%m%d_%H")+".bin")
        self.blocks_file_sink_0_1.open(self.filesink_directory+"avgNF-upper_"+__import__("time").strftime("%Y%m%d_%H")+".bin")

    def get_filesink_decimation(self):
        return self.filesink_decimation

    def set_filesink_decimation(self, filesink_decimation):
        self.filesink_decimation = filesink_decimation




def main(top_block_cls=upper_freq, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.flowgraph_started.set()

    tb.wait()


if __name__ == '__main__':
    main()
