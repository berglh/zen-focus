from gi.repository import Adw, Gio, GLib

class ApplicationWindow(Adw.ApplicationWindow):
    """"
    ApplicationWindow is the primary window for Zen Focus
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Bind Application window dimensions to store state
        application = Gio.Application.get_default()
        application.config.window.bind("width", self, "default-width", Gio.SettingsBindFlags.DEFAULT)
        application.config.window.bind("height", self, "default-height", Gio.SettingsBindFlags.DEFAULT)
        application.config.window.bind("is-maximized", self, "maximized", Gio.SettingsBindFlags.DEFAULT)
        application.config.window.bind("is-fullscreen", self, "fullscreened", Gio.SettingsBindFlags.DEFAULT)

        # Dark Mode settings
        # TODO: Get this working, the menu currently doesn't toggle
        dark_mode = application.config.window.get_boolean("dark-mode")
        self.style_manager = Adw.StyleManager.get_default()

        if dark_mode:
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            self.style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)
        dark_mode_action = Gio.SimpleAction(name="dark-mode", state=GLib.Variant.new_boolean(dark_mode))

        dark_mode_action.connect("activate", self.toggle_dark_mode)
        dark_mode_action.connect("change-state", self.change_color_scheme)
        self.add_action(dark_mode_action)

    def toggle_dark_mode(self, action, _):
        state = action.get_state()
        old_state = state.get_boolean()
        new_state = not old_state
        action.change_state(GLib.Variant.new_boolean(new_state))
    
    def change_color_scheme(self, action, new_state):
        dark_mode = new_state.get_boolean()
        style_manager = Adw.StyleManager.get_default()
        if dark_mode:
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)
        action.set_state(new_state)
