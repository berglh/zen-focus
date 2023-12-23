import gi
gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')
gi.require_version('Rsvg', '2.0')
from gi.repository import Adw, Gdk, Gio, Gtk

from .application_window import ApplicationWindow
from .content_pane import Content
from .sidebar_pane import Sidebar
from config.config import Config

class Application(Adw.Application):
    """
    Application is the parent GTK class for Zen Focus
    """
    def __init__(self):
        super().__init__(application_id="com.github.berglh.zen-focus",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):

        ## Establish application config and window
        self.config = Config()
        self.window = ApplicationWindow(
            application=self,
            width_request=280,
            height_request=200
        )

        ## GTK UI CSS Provider
        self.css = Gtk.CssProvider()
        self.css.load_from_path('css/application.css')
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            self.css,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        ## Establish the navigation split view object & properties
        self.split_view = Adw.NavigationSplitView()
        self.split_view.set_vexpand(True)

        # The breakpoint is used to hide the sidebar when the window is resized
        self.breakpoint = Adw.Breakpoint.new(
            condition=Adw.BreakpointCondition.parse('max-width: 450px')
        )
        self.breakpoint.add_setter(self.split_view, property="collapsed", value=True)
        self.window.add_breakpoint(self.breakpoint)

        # In order to ge the split headerbar view in the navigation split view, 
        # an invisible headerbar is added to the window
        # TODO: Check if there is a way to avoid this
        self.dummy_header_bar = Adw.HeaderBar()
        self.dummy_header_bar.set_visible(False)

        # The main window box is the container for the navigation split view
        self.main_window_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main_window_box.set_vexpand(True)
        self.main_window_box.append(self.dummy_header_bar)
        self.main_window_box.append(self.split_view)
        self.window.set_content(self.main_window_box)

        # Set the sidebar and content panes
        self.split_view.set_sidebar(Sidebar())
        self.split_view.set_content(Content())

        # Show the window
        self.window.present()

        
