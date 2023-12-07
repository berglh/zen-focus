import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from typing import Optional
from gi.repository import Gtk, Adw, Gio, Gdk, GObject

from .sidebar_pane import Sidebar

class Application(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.github.berglh.zen_focus",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        
    def do_activate(self):
        self.window = Adw.ApplicationWindow(
            application=self,
            width_request=280,
            height_request=200,
            default_width=800,
            default_height=800
        )

        ## Add the custom icon paths
        self.icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        self.icon_theme.add_search_path(path='./icons')

        ## Style Manager (Detect OS Light/Dark Theme)
        self.style_manager = Adw.StyleManager.get_default()
        self.color_scheme = self.style_manager.get_color_scheme()

        ## Force light for debugging (TODO: add a toggle later)
        # print(self.style_manager.get_dark())
        # style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        # print(self.style_manager.get_dark())
        # print(self.scheme.value_name)

        ## UI CSS Provider
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_path('./css/gui_window.css')
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        ## Establish the navigation split view object & properties
        self.split_view = Adw.NavigationSplitView()
        self.split_view.set_vexpand(True)

        # The breakpoint is used to hide the sidebar when the window is resized
        self.breakpoint = Adw.Breakpoint.new(
            condition=Adw.BreakpointCondition.parse('max-width: 400px')
        )
        self.breakpoint.add_setter(self.split_view, property="collapsed", value=True)
        self.window.add_breakpoint(self.breakpoint)

        # In order to ge the split headerbar view in the navigation split view, 
        # we need to add a headerbar to the window and hide it first
        # TODO: Check if there is a way to avoid this
        self.dummy_header_bar = Adw.HeaderBar()
        self.dummy_header_bar.set_visible(False)

        self.main_window_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main_window_box.set_vexpand(True)

        self.split_view.set_sidebar(Sidebar(self))

        content_page = Adw.NavigationPage()
        content_page.set_title("Test")
        content_page.set_visible(True)
        
        content_toolbar = Adw.ToolbarView(top_bar_style=Adw.ToolbarStyle.FLAT)
        content_header = Adw.HeaderBar()
        content_header.set_decoration_layout('menu:close')

        content_toolbar.add_top_bar(content_header)
        content_page.set_child(content_toolbar)

        pbox = Gtk.Box()
        pbox.set_halign(Gtk.Align.CENTER)
        pbox.set_valign(Gtk.Align.CENTER)
        pbox.append(Gtk.Label(label='Content'))
        content_toolbar.set_content(pbox)

        self.main_window_box.append(self.dummy_header_bar)
        self.main_window_box.append(self.split_view)
        self.split_view.set_content(content_page)

        self.window.set_content(self.main_window_box)
        self.window.present()