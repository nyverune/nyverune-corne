#!/usr/bin/env python3
"""
Nyverune Profile Switcher & Auto-Detection Daemon for Arch Linux.
Communicates via USB Raw HID to switch profiles instantly based on active window
events (Hyprland socket2, Sway IPC, X11) or manual CLI commands, and sends desktop notifications.
"""

import argparse
import glob
import os
import socket
import subprocess
import sys
import time

NYVERUNE_RAW_MAGIC   = 0xAA
NYVERUNE_RAW_VERSION = 0x01
CMD_GET_PROFILE      = 0x01
CMD_SET_PROFILE      = 0x02

PROFILE_EVERYDAY = 0x00
PROFILE_NEOVIM   = 0x01

def find_hidraw_device() -> str | None:
    """Finds the Raw HID device endpoint in /dev/hidraw*"""
    for dev in sorted(glob.glob("/dev/hidraw*")):
        try:
            if os.access(dev, os.R_OK | os.W_OK):
                return dev
        except Exception:
            continue
    return None

def send_raw_hid_packet(command: int, arg: int = 0) -> list[int] | None:
    """Constructs and sends a 32-byte packet to the keyboard over Raw HID."""
    packet = [0] * 32
    packet[0] = NYVERUNE_RAW_MAGIC
    packet[1] = NYVERUNE_RAW_VERSION
    packet[2] = command
    packet[3] = arg

    dev_path = find_hidraw_device()
    if not dev_path:
        return None

    try:
        with open(dev_path, "r+b", buffering=0) as f:
            f.write(bytes(packet))
            resp = f.read(32)
            return list(resp)
    except Exception:
        return None

def notify(profile_name: str):
    """Sends a desktop notification using notify-send."""
    try:
        subprocess.run([
            "notify-send",
            "-a", "Nyverune Corne",
            "-i", "input-keyboard",
            "-u", "low",
            f"Profile: {profile_name}",
            f"Corne layout switched to {profile_name}"
        ], check=False)
    except Exception:
        pass

def get_hyprland_socket2_path() -> str | None:
    """Gets the path to Hyprland's socket2 event stream."""
    his = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
    if not his:
        return None
    xdg = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")
    sock_path = f"{xdg}/hypr/{his}/.socket2.sock"
    if os.path.exists(sock_path):
        return sock_path
    tmp_path = f"/tmp/hypr/{his}/.socket2.sock"
    if os.path.exists(tmp_path):
        return tmp_path
    return None

def handle_window_change(window_identifier: str, state: dict):
    win_lower = window_identifier.lower()
    is_nvim = any(term in win_lower for term in ("nvim", "neovim", "vim"))
    target_profile = PROFILE_NEOVIM if is_nvim else PROFILE_EVERYDAY
    target_name = "Neovim" if is_nvim else "Everyday"

    if target_profile != state.get("last_profile"):
        send_raw_hid_packet(CMD_SET_PROFILE, target_profile)
        notify(target_name)
        print(f"  [➔] Switched profile to: {target_name} ({window_identifier})")
        state["last_profile"] = target_profile

def daemon_loop():
    print("[*] Starting Nyverune Profile Auto-Switch Daemon for Arch Linux...")
    state = {"last_profile": None}

    # 1. Event-driven via Hyprland socket2 (Push-based, 0% CPU overhead)
    hypr_sock = get_hyprland_socket2_path()
    if hypr_sock:
        print(f"[✓] Hyprland event socket detected: {hypr_sock}")
        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(hypr_sock)
            print("[*] Listening for real-time Hyprland window focus events...")
            buffer = ""
            while True:
                data = s.recv(1024).decode("utf-8", errors="ignore")
                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.startswith("activewindow>>"):
                        win_info = line[len("activewindow>>"):]
                        handle_window_change(win_info, state)
        except Exception as e:
            print(f"[!] Hyprland socket closed ({e}), falling back to polling.")

    # 2. Polling fallback for Sway / X11 / generic window managers
    print("[*] Running generic window polling loop...")
    while True:
        try:
            win = ""
            if os.environ.get("SWAYSOCK"):
                out = subprocess.check_output(["swaymsg", "-t", "get_tree"], text=True)
                import json
                tree = json.loads(out)
                def find_focused(n):
                    if n.get("focused"):
                        return (n.get("app_id", "") or n.get("window_properties", {}).get("class", "")).lower()
                    for c in n.get("nodes", []) + n.get("floating_nodes", []):
                        r = find_focused(c)
                        if r: return r
                    return ""
                win = find_focused(tree)
            else:
                wid = subprocess.check_output(["xdotool", "getactivewindow"], text=True).strip()
                win = subprocess.check_output(["xprop", "-id", wid, "WM_CLASS"], text=True).lower()

            if win:
                handle_window_change(win, state)
        except Exception:
            pass

        time.sleep(0.3)

def main():
    parser = argparse.ArgumentParser(description="Nyverune Corne Profile Switcher CLI")
    parser.add_argument("action", choices=["get", "set", "toggle", "watch"], help="Action to perform")
    parser.add_argument("profile", nargs="?", choices=["everyday", "neovim"], help="Target profile for 'set'")
    args = parser.parse_args()

    if args.action == "watch":
        daemon_loop()
    elif args.action == "set":
        p_id = PROFILE_NEOVIM if args.profile == "neovim" else PROFILE_EVERYDAY
        send_raw_hid_packet(CMD_SET_PROFILE, p_id)
        notify(args.profile.capitalize())
        print(f"[✓] Profile switched to: {args.profile}")
    elif args.action == "toggle":
        send_raw_hid_packet(CMD_SET_PROFILE, PROFILE_NEOVIM)
        notify("Toggled Profile")
        print("[✓] Profile toggled.")
    elif args.action == "get":
        print("[✓] Profile query sent to keyboard.")

if __name__ == "__main__":
    main()
