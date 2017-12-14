'''
Created on Oct 28, 2016

@author: sensey
'''


class Loader(object):
    def __init__(self, options, args):
        """

        :param options: 
        :param args: 
        """
        self._options = options
        self._args = args

    def __enter__(self):
        """
        
        :return: 
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        
        :param type: 
        :param value: 
        :param traceback: 
        :return: 
        """
        pass

    @property
    def enabled(self):
        """

        :return: 
        """
        return True

    def config(self, binder):
        """

        :return: 
        """

    def boot(self):
        """
        
        :param event_dispatcher: 
        :return: 
        """
