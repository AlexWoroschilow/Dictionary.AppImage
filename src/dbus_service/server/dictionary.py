import dbus.service
import dbus.mainloop.glib
import logging
from threading import Thread
from _dbus_glib_bindings import DBusGMainLoop


class DictionaryServer(dbus.service.Object):
    def __init__(self, dispatcher):
        DBusGMainLoop(set_as_default=True)
        self._dispatcher = dispatcher

    def start(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus_name = dbus.service.BusName("org.sensey.Dictionary", dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, "/org/sensey/Dictionary")

    @dbus.service.method("org.sensey.Dictionary.Translate")
    def translate(self, word):
        logger = logging.getLogger('dbus-server')
        logger.debug('translate: %s' % word)

        event = self._dispatcher.new_event(word)
        self._dispatcher.dispatch('kernel_event.service_transate', event)
        return True
