# This script is meant to cheange the System Color Theme in a Linux+Hyprland setup
# This script is using the Catppuccin palette as reference
# It will have a preset of 3 Colors: Green+Yellow, Blue+Purple, Red+Orange
# It will affect the following:
# - GTK Theme
# - Icon Theme
# - Waybar Colors
# - Tofi Colors
# - FiSH Colors
# - Hyprland Border Colors
# - SWWW Background Image (from set of 3)
import os
import sys
import subprocess

def run_command(command):
    print("Running command: " + " ".join(command))
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode("utf-8").strip()

def set_theme(theme):
    for key in theme:
        if key == "gtk":
            # edit file in .local/share/nwg-look/gsettings and change the value of the key gtk-theme
            run_command(["sed", "-i", "s/gtk-theme=.*/gtk-theme=" + theme[key] + "/g", os.path.expanduser("~/.local/share/nwg-panel/gsettings")])
        elif key == "icon":
            run_command(["sed", "-i", "s/icon-theme=.*/icon-theme=" + theme[key] + "/g", os.path.expanduser("~/.local/share/nwg-panel/gsettings")])
        elif key == "waybar":
            pass
        elif key == "tofi":
            # edit file in .config/tofi/config and change the value of the key selection-color
            run_command(["sed", "-i", "s/selection-color=.*/selection-color=" + theme[key] + "/g", os.path.expanduser("~/.config/tofi/config")])
        elif key == "fish":
            # edit the file in .config/fish/config.fish "echo -n (printf '\033[38;2;180;190;254m')" and change the values of the RGB
            run_command(["sed", "-i", "s/echo -n (printf '\\033\\[38;2;.*m')/echo -n (printf '\\033\\[38;2;" + theme[key] + "m')/g", os.path.expanduser("~/.config/fish/config.fish")])
            pass
        elif key == "hyprland":
            # edit the file in .config/hyprland/hyprland.conf and change "  col.active_border = rgba(89b4faee) rgba(cba6f7ee) 45deg" to the new values keeping the 'ee' at the end
            run_command(["sed", "-i", "s/col.active_border = rgba(.*ee) rgba(.*ee) 45deg/col.active_border = rgba(" + theme[key][0] + "ee) rgba(" + theme[key][1] + "ee) 45deg/g", os.path.expanduser("~/.config/hyprland/hyprland.conf")])
            # edit the file in .config/hyprland/hyprland.conf and change "GTK_THEME=catppuccin-mocha-*-standard+default" to the new value of the gtk theme
            run_command(["sed", "-i", "s/GTK_THEME=catppuccin-mocha-.*-standard+default/GTK_THEME=catppuccin-mocha-" + theme["gtk"][0] + "-standard+default/g", os.path.expanduser("~/.config/hyprland/hyprland.conf")])
            pass
        elif key == "swww":
            pass
        else:
            print("Unknown key: " + key)

    # Restart the following services
    run_command(["nwg-look", "-a"])
    run_command(["killall", "waybar;", "waybar", "&", "disown"])

def main():
    themes = {
        "green+yellow": {
            "gtk": "catppuccin-mocha-green-standard+default",
            "icon": "Reversal-green-dark",
            "waybar": ["#a6e3a1", "#f9e2af"],
            "tofi": "#a6e3a1",
            "fish": "166;227;Border 161",
            "hyprland": ["#a6e3a1", "#f9e2af"],
            "swww": "green"
        },
        "blue+purple": {
            "gtk": "catppuccin-mocha-blue-standard+default",
            "icon": "Papirus-Dark",
            "waybar": ["#89b4fa", "#cba6f7"],
            "tofi": "#89b4fa",
            "fish": "137;180;250",
            "hyprland": ["#89b4fa", "#cba6f7"],
            "swww": "blue"
        },
        "red+orange": {
            "gtk": "catppuccin-mocha-blue-standard+default",
            "icon": "Papirus-Dark",
            "waybar": ["#f38ba8", "#fab387"],
            "tofi": "#f38ba8",
            "fish": "#fab387",
            "hyprland": ["#f38ba8", "#fab387"],
            "swww": "red"
        }
    }
    # Get an array of only the keys
    themes_keys = list(themes.keys())
    # Check ENV Variables
    if "HYPLAND_THEME" not in os.environ:
        print("HYPLAND_THEME not set, assuming Blue+Purple")
        os.system("fish -c 'set -Ux HYPLAND_THEME blue+purple'")
    else:
        print("HYPLAND_THEME is: " + os.environ["HYPLAND_THEME"])
        print("Changing to: " + themes_keys[(themes_keys.index(os.environ["HYPLAND_THEME"]) + 1) % len(themes_keys)])
        os.system("fish -c 'set -Ux HYPLAND_THEME " + themes_keys[(themes_keys.index(os.environ["HYPLAND_THEME"]) + 1) % len(themes_keys)] + "'")

    set_theme(themes[os.environ["HYPLAND_THEME"]])


if __name__=="__main__":
    main()
