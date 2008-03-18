



class DataWrapper(object):
    """
    Base class to provide interface to timeseries data.  
    """
    def get_event_data(self,channels,eventOffsets,
                       dur,offset,buf,
                       resampledRate=None,
                       filtFreq=None,filtType='stop',filtOrder=4,
                       keepBuffer=False):
        raise NotImplementedError