
import gi, os
gi.require_version('Gtk', '4.0')
from typing import Optional
from gi.repository import Gtk, Adw, Gio, Gdk


class Config():
    """
    The Config class presents persistent Zen Focus application settings stored
    in dconf/GSettings and exposes them in the Application class

    The schema for this application contains nested elements to be addressed
    independently. The schema is defined in the zen-focus.gschema.xml file.
    """
    def __init__(self) -> None:

        schema_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        schema_source = Gio.SettingsSchemaSource.new_from_directory(
            schema_dir,
            Gio.SettingsSchemaSource.get_default(),
            False,
        )
        # Load Window config schema
        schema = schema_source.lookup('com.github.berglh.zen-focus.window', False)
        self.window = Gio.Settings.new_full(schema, None, None)
        # Load Settings config schema
        schema = schema_source.lookup('com.github.berglh.zen-focus.settings', False)
        self.settings = Gio.Settings.new_full(schema, None, None)
