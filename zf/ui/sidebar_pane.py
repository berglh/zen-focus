from gi.repository import Adw, Gdk, Gio, GObject, Gtk

from .about_pane import About
from .power_pane import Power
from .processor_pane import Processor
from .settings_pane import Settings
from .temperature_pane import Temperature

class ListItem():
    """
    ListItem class defines the sidebar button widget
    """
    def __init__(self, title: str, icon: str, pane: object) -> None:
        self.title = title
        self.icon = icon
        self.pane = pane

class Sidebar(Adw.NavigationPage):
    """
    Sidebar class defines the sidebar pane for Zen Focus
    """
    def __init__(self):
        super().__init__()

        # Primary Settings for Sidebar
        self.set_title("Zen Focus")
        self.set_vexpand(True)

        # Set menu bar min width
        self.set_size_request(220, -1)

        # Define sidebar header box
        self.header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        self.theme.add_search_path(path='icons')

        self.header_logo = Gtk.Image.new_from_icon_name("zen-focus-symbolic")
        self.header_label = Gtk.Label(label="Zen Focus")

        self.header_box.append(self.header_logo)
        self.header_box.append(self.header_label)

        # The sidebar show content button when collapsed
        self.show_button = Gtk.ToggleButton(
            icon_name="go-next-symbolic",
            active=False, visible=False, margin_top=0, margin_bottom=0
        )

        # Bind to the parent Window split view show-content property
        self.application = Gio.Application.get_default()
        self.show_button.bind_property(
            "active",
            self.application.split_view,
            "show-content",
            GObject.BindingFlags.BIDIRECTIONAL
        )

        # Connect to the 'notify::folded' signal of the Adw.NavigationSplitView to show the button
        self.application.split_view.connect("notify::collapsed", self.on_split_view_folded, self.show_button)

        # Add the toolbar and header to the sidebar
        self.toolbar = Adw.ToolbarView()
        self.header = Adw.HeaderBar()
        self.header.set_title_widget(self.header_box)
        self.header.set_show_back_button(True)
        self.header.set_can_focus(False)
        self.header.set_decoration_layout('menu:close')
        self.header.pack_end(self.show_button)

        self.toolbar.set_content()
        self.toolbar.add_top_bar(self.header)
        self.set_child(self.toolbar)

        self.list = Gtk.ListBox()
        self.list.set_vexpand(False)
        self.list.set_margin_top(12)
        self.list.set_margin_start(6)
        self.list.set_margin_end(6)
        self.list.set_selection_mode(Gtk.SelectionMode.SINGLE)

        # Connect the signal
        self.list.connect("row-activated", self.on_row_activated)

        # The sidebar list items to render as buttons
        # These need to be defined in the sidebar class otherwise the
        # the primary Adw.ApplicationWindow and settings is undefined
        top_list_items = [
            ListItem("Temperatures", 'temp-symbolic', Temperature()),
            ListItem("Power Usage", 'org.gnome.Settings-power-symbolic', Power()),
            ListItem("Processor Info", 'dialog-information-symbolic', Processor()),
        ]

        bottom_list_items = [
            ListItem("Settings", 'settings-symbolic', Settings()),
            ListItem("About", 'help-about-symbolic', About())
        ]

        separator = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL,
            margin_start=2,
            margin_end=2    
        )

        ## Populate the sidebar list buttons
        for k in top_list_items:
            button = Adw.ActionRow(
                activatable=True,
                title=k.title,
                icon_name=k.icon,
                margin_bottom=0,
                margin_top=0, 
                css_classes=['action-row-rounded']
            )
            button.set_focus_on_click(True)
            button.set_can_focus(True)
            button.connect("activated", self.on_button_activated, k.pane)
            self.list.append(
                button
            )
        # Separator
        self.list.append(separator)

        for k in bottom_list_items:
            button = Adw.ActionRow(
                activatable=True,
                title=k.title,
                icon_name=k.icon,
                margin_bottom=0,
                margin_top=0,
                css_classes=['action-row-rounded']
            )
            button.set_focus_on_click(True)
            button.set_can_focus(True)  
            button.connect("activated", self.on_button_activated, k.pane)
            self.list.append(
                button
            )

        # Assign the list to the sidebar
        self.toolbar.set_content(self.list)

    def on_button_activated(self, button, content):
        """
        Set the content of the content pane when a button is clicked
        """
        content.set_content(button)

    def on_row_activated(self, list_box, row):
        self.application.split_view.set_property("show-content", True)

    def on_split_view_folded(self, split_view, allocation, button):
        """
        on_split_view_folded shows a button to return to content view in collapsed sidebar mode
        """
        # If the Adw.NavigationSplitView is folded, show the button
        # If the Adw.NavigationSplitView is not folded, hide the button
        if self.application.split_view.get_collapsed():
            button.set_visible(True)
        else:
            button.set_visible(False)
