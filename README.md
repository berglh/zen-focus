
## Zen Focus

This is currently under heavy development.

It is a Python GUI GTK4 application for Ubuntu 23.10+ using the Adw (libadwaita) library that monitors Ryzen CPUs via ryzen_smu and k10temp kernel modules.

It uses the latest features of `libadwaita 1.4+` to make a responsive, scalable, modern interface in the style of Ubuntu native applications.

## GUI Development

Update 2023-12-16: UI Class Refactoring

Many changes have been made to the initial GUI prototype:

  - Fleshed out UI classes and established content panes
  - Clicking buttons in the sidebar now changes the content pane
  - GSettings schema added for persistent window and application settings
  - Adjusted project layout for Python module distribution

Video:

https://github.com/berglh/zen-focus/assets/12455338/b4e92756-8880-4df2-83a7-e588521c5f43

## Testing

Requirements:

  - Ubuntu 23.10+ (or dist with GTK4 + libadwaita)
  - libadwaita 1.4+
  - GTK4
  - Python3

To launch the application, change into the repository folder and run:

```
python3 zen-focus/app.py 
```
