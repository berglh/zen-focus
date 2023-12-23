from gi.repository import Gio, Gtk

class Processor():
    """
    Processor class defines the Processor information content pane

    It generates the structure in memory to apply to the navigation split view
    """

    def __init__(self):
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_vexpand(True)

        self.content_box = Gtk.Box()
        self.content_box.set_halign(Gtk.Align.CENTER)
        self.content_box.set_valign(Gtk.Align.CENTER)
        self.content_box.append(Gtk.Label(label='Processor Info'))

        self.scrolled_window.set_child(self.content_box)

    def set_content(self, button):
        """
        set_content sets the Processor Info pane content in the navigation split view
        """
        content = Gio.Application.get_default().split_view.get_content()
        content.set_title("Processor Info")
        content.set_visible(True)
        content.pane.set_content(self.scrolled_window)
        content.pane.set_reveal_bottom_bars(True)