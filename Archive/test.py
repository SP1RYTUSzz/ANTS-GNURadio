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




class test(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.vec_len = vec_len = 4096
        self.samp_rate = samp_rate = 30.72E+06
        self.plot_rate = plot_rate = 15
        self.samp_rate_file = samp_rate_file = 24
        self.samp_per_plot = samp_per_plot = round(samp_rate / vec_len / plot_rate)
        self.freq = freq = 2405e6
        self.filesink_directory = filesink_directory = "/home/antfarm/Documents/Antman_GNURadio_Code/Results"

        ##################################################
        # Blocks
        ##################################################

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
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_len)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_short*1)
        self.blocks_nlog10_ff_1_0_1 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, vec_len, 0)
        self.blocks_multiply_const_xx_0 = blocks.multiply_const_cc(1/vec_len, vec_len)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff((1/vec_len))
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(samp_per_plot, (1/ samp_per_plot), samp_per_plot , vec_len)
        self.blocks_keep_one_in_n_1 = blocks.keep_one_in_n(gr.sizeof_float*vec_len, samp_per_plot)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 100)
        self.blocks_integrate_xx_0_0 = blocks.integrate_ff(vec_len, 1)
        self.blocks_file_sink_1_1 = blocks.file_sink(gr.sizeof_short*1, '"filesink_directory+"/test_spike_freq_"+__import__("time").strftime("%Y%m%d_%H%M%S")+".bin"', True)
        self.blocks_file_sink_1_1.set_unbuffered(True)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_float*vec_len, '""filesink_directory+"/avg_PSD"+__import__("time").strftime("%Y%m%d_%H%M%S")+".bin"', True)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, '"filesink_directory+"/test_avg_raw_"+__import__("time").strftime("%Y%m%d_%H%M%S")+".bin"', True)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(vec_len)
        self.blocks_argmax_xx_0 = blocks.argmax_fs(vec_len)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_argmax_xx_0, 0), (self.blocks_file_sink_1_1, 0))
        self.connect((self.blocks_argmax_xx_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_argmax_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.blocks_integrate_xx_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_keep_one_in_n_1, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_keep_one_in_n_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_nlog10_ff_1_0_1, 0))
        self.connect((self.blocks_multiply_const_xx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_nlog10_ff_1_0_1, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_integrate_xx_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_const_xx_0, 0))
        self.connect((self.soapy_limesdr_source_0, 0), (self.blocks_stream_to_vector_1, 0))


    def get_vec_len(self):
        return self.vec_len

    def set_vec_len(self, vec_len):
        self.vec_len = vec_len
        self.set_samp_per_plot(round(self.samp_rate / self.vec_len / self.plot_rate))
        self.blocks_multiply_const_vxx_0_0.set_k((1/self.vec_len))
        self.blocks_multiply_const_xx_0.set_k(1/self.vec_len)
        self.fft_vxx_0.set_window(window.blackmanharris(self.vec_len))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_per_plot(round(self.samp_rate / self.vec_len / self.plot_rate))
        self.soapy_limesdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_plot_rate(self):
        return self.plot_rate

    def set_plot_rate(self, plot_rate):
        self.plot_rate = plot_rate
        self.set_samp_per_plot(round(self.samp_rate / self.vec_len / self.plot_rate))

    def get_samp_rate_file(self):
        return self.samp_rate_file

    def set_samp_rate_file(self, samp_rate_file):
        self.samp_rate_file = samp_rate_file

    def get_samp_per_plot(self):
        return self.samp_per_plot

    def set_samp_per_plot(self, samp_per_plot):
        self.samp_per_plot = samp_per_plot
        self.blocks_keep_one_in_n_1.set_n(self.samp_per_plot)
        self.blocks_moving_average_xx_0.set_length_and_scale(self.samp_per_plot, (1/ self.samp_per_plot))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.soapy_limesdr_source_0.set_frequency(0, self.freq)

    def get_filesink_directory(self):
        return self.filesink_directory

    def set_filesink_directory(self, filesink_directory):
        self.filesink_directory = filesink_directory




def main(top_block_cls=test, options=None):
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
