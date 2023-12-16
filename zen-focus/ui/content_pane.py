from gi.repository import Adw, Gio, Gtk

from .temperature_pane import Temperature

# The content pane is a shell to swap panes in and out of the content area of the navigation split view
# The content pane must be a subclass of Adw.NavigationPage
# The content pane consists of a top_bar, content area, and bottom_bar
# For specific content panes, common bottom toolbar is used to control 
# the state of the data factory updating for linked panes class
# In other content panes, the common bottom toolbar can be hidden

# When a button is clicked in the sidebar, it should update the toolbar content and the bottom toolbar visibility
# It should be able to remove the bottom toolbar from the content pane using an empty widget

class Content(Adw.NavigationPage):
    """
    Content class creates the content pane structure

    Other pane classes update the content pane with their content
    """
    def __init__(self,):
        super().__init__()

        self.set_visible(True)
        
        self.pane = Adw.ToolbarView(top_bar_style=Adw.ToolbarStyle.FLAT)
        self.header = Adw.HeaderBar()
        self.header.set_decoration_layout('menu:close')

        self.menu = Gio.Menu()
        self.menu.append("Dark Mode", "app.dark_mode")
       
        self.menu_button = Gtk.MenuButton(icon_name="open-menu-symbolic", menu_model=self.menu)

        self.header.pack_start(self.menu_button)

        #self.pane.replace_data
        self.pane.add_top_bar(self.header)
        self.set_child(self.pane)

        start_button = Gtk.Button()
        start_button.set_label('Start')
        start_button.set_halign(Gtk.Align.CENTER)
        
        start_button.set_css_classes(['suggested-action'])

        bottom_bar = Gtk.Box()
        bottom_bar.set_margin_top(12)
        bottom_bar.set_margin_bottom(12)
        bottom_bar.set_margin_end(12)
        bottom_bar.set_halign(Gtk.Align.END)
        bottom_bar.append(start_button)
        bottom_bar.set_css_classes(['.toolbar'])
        
        self.pane.add_bottom_bar(bottom_bar)
        self.pane.set_reveal_bottom_bars(True)

        # Temperature is unable to resolve the Application object before the content pane is first created
        # So the content pane is passed as an argument to the set_content method
        self.set_title("Temperature Usage")
        temp = Temperature()
        temp.set_content(None, self)
