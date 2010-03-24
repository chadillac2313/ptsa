import os.path
import numpy as np
import pylab as pl

from ptsa.data import EdfWrapper, Events
from ptsa.wavelet import phase_pow_multi

# load in example data
if os.path.exists('examples/example_data/sinus.bdf'):
    edfw = EdfWrapper('examples/example_data/sinus.bdf')
elif os.path.exists('example_data/sinus.bdf'):
    edfw = EdfWrapper('example_data/sinus.bdf')
else:
    raise IOError('Example data file sinus.bdf not found! '+
                  'This file must be in example_data folder!')

for chan_num in [0,1]:
    samplerate = edfw.get_samplerate(chan_num)
    nsamples = samplerate*100
    event_dur = samplerate*1
    buf_dur = 1.0
    
    
    # generate fake event
    eoffset = np.arange(20)# np.array([0.])
    esrc = [edfw]*len(eoffset)
    events = Events(np.rec.fromarrays([esrc,eoffset],
                                      names='esrc,eoffset'))
    
    # load in data with events (filter at the same time)
    dat = events.get_data(chan_num, # channel
                          1.0, # duration in sec
                          0.0, # offset in sec
                          buf_dur, # buffer in sec
                          # filt_freq = 20.,
                          filt_type = 'low',
                          keep_buffer=True
                          )
    # calc wavelet power
    freqs = np.arange(2,50,2)
    datpow = phase_pow_multi(freqs,dat,to_return='power')
    
    # remove the buffer now that we have filtered and calculated power
    # for ts in [rdat,ndat,rpow,npow]:
    #     ts = ts.remove_buffer(buf_dur)
    # why does the above not work?
    dat = dat.remove_buffer(buf_dur)
    datpow = datpow.remove_buffer(buf_dur)
    
    # plot ERP
    pl.figure()
    pl.clf()
    pl.plot(dat['time'],dat.nanmean('events'),'r')
    pl.xlabel('Time (s)')
    pl.ylabel('Voltage')
    
    # plot power spectrum
    pl.figure()
    pl.clf()
    pl.plot(datpow['freqs'],datpow.nanmean('events').nanmean('time'),'r')
    pl.xlabel('Frequency (Hz)')
    pl.ylabel('Power')

pl.show()
