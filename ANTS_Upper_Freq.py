#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import sip
import threading
import time



class ANTS_Upper_Freq(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "ANTS_Upper_Freq")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.vec_len = vec_len = 4096
        self.samp_rate = samp_rate = 30.72E+06
        self.filesink_freq = filesink_freq = 10
        self.threshold2 = threshold2 = 10
        self.threshold1 = threshold1 = 6
        self.threshold0 = threshold0 = 3
        self.lna_makeup_gain = lna_makeup_gain = -12
        self.gain = gain = 20
        self.func_probe_noise = func_probe_noise = 0
        self.freq = freq = 2.435E+09
        self.filesink_directory = filesink_directory = r"C:/.ANTS_6-16-26_Test_Results/"
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
        self.soapy_limesdr_source_0.set_gain(0, min(max(gain, -12.0), 61.0))
        self.qtgui_vector_sink_f_0_0_0_0 = qtgui.vector_sink_f(
            vec_len,
            (freq - (samp_rate)/2),
            (samp_rate/vec_len),
            "Frequency (Hz)",
            "Number of sample crossed threshold",
            "Spectral Occupancy Threshold 2 vs. Frequency",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_0_0.set_y_axis(0, 600)
        self.qtgui_vector_sink_f_0_0_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0_0_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_0_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_0_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_0_0_0_win, 3, 0, 1, 4)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0_0_0 = qtgui.vector_sink_f(
            vec_len,
            (freq - (samp_rate)/2),
            (samp_rate/vec_len),
            "Frequency (Hz)",
            "Number of sample crossed threshold",
            "Spectral Occupancy Threshold 1 vs. Frequency",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0_0.set_y_axis(0, 600)
        self.qtgui_vector_sink_f_0_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_0_0_win, 2, 0, 1, 4)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0_0 = qtgui.vector_sink_f(
            vec_len,
            (freq - (samp_rate)/2),
            (samp_rate/vec_len),
            "Frequency (Hz)",
            "Number of sample crossed threshold",
            "Spectral Occupancy Threshold 0 vs. Frequency",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0_0.set_y_axis(0, 600)
        self.qtgui_vector_sink_f_0_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0_0.enable_grid(True)
        self.qtgui_vector_sink_f_0_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_0_win, 1, 0, 1, 4)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            vec_len,
            (freq - (samp_rate)/2),
            (samp_rate/vec_len),
            "Frequency (Hz)",
            "Power (dBm)",
            "Integrated FFT vs. Frequency",
            1, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis((-140), 10)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_win, 0, 0, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_VERT,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("Average Noise Power across Spectrum")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -120)
            self.qtgui_number_sink_0.set_max(i, 0)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win, 0, 4, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_add_const_vxx_1, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_threshold_ff_0_0, 0))
        self.connect((self.blocks_add_const_vxx_1_0, 0), (self.blocks_threshold_ff_0_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_multiply_const_xx_1, 0))
        self.connect((self.blocks_integrate_xx_1, 0), (self.blocks_multiply_const_xx_1_0, 0))
        self.connect((self.blocks_integrate_xx_2, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_integrate_xx_2, 0), (self.qtgui_vector_sink_f_0_0, 0))
        self.connect((self.blocks_integrate_xx_2_0, 0), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.blocks_integrate_xx_2_0, 0), (self.qtgui_vector_sink_f_0_0_0, 0))
        self.connect((self.blocks_integrate_xx_2_0_0, 0), (self.blocks_file_sink_0_0_0_0, 0))
        self.connect((self.blocks_integrate_xx_2_0_0, 0), (self.qtgui_vector_sink_f_0_0_0_0, 0))
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


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "ANTS_Upper_Freq")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

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
        self.qtgui_vector_sink_f_0.set_x_axis((self.freq - (self.samp_rate)/2), (self.samp_rate/self.vec_len))
        self.qtgui_vector_sink_f_0_0.set_x_axis((self.freq - (self.samp_rate)/2), (self.samp_rate/self.vec_len))
        self.qtgui_vector_sink_f_0_0_0.set_x_axis((self.freq - (self.samp_rate)/2), (self.samp_rate/self.vec_len))
        self.qtgui_vector_sink_f_0_0_0_0.set_x_axis((self.freq - (self.samp_rate)/2), (self.samp_rate/self.vec_len))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_filesink_decimation(round(self.samp_rate / self.vec_len / self.filesink_freq))
        self.qtgui_vector_sink_f_0.set_x_axis((self.freq - (self.samp_rate)/2), (self.samp_rate/self.vec_len))
        self.qtgui_vector_sink_f_0_0.set_x_axis((self.freq - (self.samp_rate)/2), (self.samp_rate/self.vec_len))
        self.qtgui_vector_sink_f_0_0_0.set_x_axis((self.freq - (self.samp_rate)/2), (self.samp_rate/self.vec_len))
        self.qtgui_vector_sink_f_0_0_0_0.set_x_axis((self.freq - (self.samp_rate)/2), (self.samp_rate/self.vec_len))
        self.soapy_limesdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_filesink_freq(self):
        return self.filesink_freq

    def set_filesink_freq(self, filesink_freq):
        self.filesink_freq = filesink_freq
        self.set_filesink_decimation(round(self.samp_rate / self.vec_len / self.filesink_freq))

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

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.soapy_limesdr_source_0.set_gain(0, min(max(self.gain, -12.0), 61.0))

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
        self.qtgui_vector_sink_f_0.set_x_axis((self.freq - (self.samp_rate)/2), (self.samp_rate/self.vec_len))
        self.qtgui_vector_sink_f_0_0.set_x_axis((self.freq - (self.samp_rate)/2), (self.samp_rate/self.vec_len))
        self.qtgui_vector_sink_f_0_0_0.set_x_axis((self.freq - (self.samp_rate)/2), (self.samp_rate/self.vec_len))
        self.qtgui_vector_sink_f_0_0_0_0.set_x_axis((self.freq - (self.samp_rate)/2), (self.samp_rate/self.vec_len))
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




def main(top_block_cls=ANTS_Upper_Freq, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
