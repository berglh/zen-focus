from gi.repository import Gtk, Adw, Gdk, GObject

top_list_items = [
    { "title": "Temperatures", "icon": 'temp-symbolic' },
    { "title": "Power Usage", "icon": 'org.gnome.Settings-power-symbolic' },
    { "title": "Processor", "icon": 'dialog-information-symbolic' },
]

bottom_list_items = [
    { "title": "Settings", "icon": 'settings-symbolic' },
    { "title": "About", "icon": 'help-about-symbolic' }
]

class Sidebar(Adw.NavigationPage):
    def __init__(self, window):
        super().__init__()

        ## Add the custom icon paths
        self.theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        self.theme.add_search_path(path='./icons')

        self.set_title("Zen Focus")
        self.set_vexpand(True)

        self.header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.header_logo = Gtk.Image.new_from_icon_name("zen-focus-symbolic")
        self.header_label = Gtk.Label(label="Zen Focus")

        self.header_box.append(self.header_logo)
        self.header_box.append(self.header_label)

        self.show_button = Gtk.ToggleButton(
            icon_name="go-next-symbolic",
            active=False,
            visible=False,
            margin_top=0,
            margin_bottom=0
        )

        # Bind to the parent Window split view show-content property
        self.ui_window = window
        self.show_button.bind_property(
            "active",
            window.split_view,
            "show-content",
            GObject.BindingFlags.BIDIRECTIONAL
        )

        # Connect to the 'notify::folded' signal of the Adw.NavigationSplitView
        self.ui_window.split_view.connect("notify::collapsed", self.on_split_view_folded, self.show_button)

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

        separator = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL,
            margin_start=2,
            margin_end=2    
        )

        ## Populate the sidebar list buttons
        for b in top_list_items:
            self.list.append(
                Adw.ActionRow(
                    title=b['title'],
                    icon_name=b['icon'],
                    margin_bottom=0,
                    margin_top=0, 
                    css_classes=['action-row-rounded']
                )
            )
        self.list.append(separator)
        for b in bottom_list_items:
            self.list.append(
                Adw.ActionRow(
                    title=b['title'],
                    icon_name=b['icon'],
                    margin_bottom=0,
                    margin_top=0, 
                    css_classes=['action-row-rounded']
                )
            )

        self.toolbar.set_content(self.list)

    def on_split_view_folded(self, split_view, allocation, button):
        # If the Adw.NavigationSplitView is folded, show the button
        # If the Adw.NavigationSplitView is not folded, hide the button
        if self.ui_window.split_view.get_collapsed():
            button.set_visible(True)
        else:
            button.set_visible(False)
