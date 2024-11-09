import os
import json
import platform
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
import winreg
import psutil
import win32print
import win32api
import wmi
from deepdiff import DeepDiff

# Initialize customtkinter
ctk.set_appearance_mode("dark")  # Set to dark mode
ctk.set_default_color_theme("blue")

class ProfileApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("User Settings Profiler")
        self.geometry("1400x800")

        # Define a custom style for Treeview with a larger font
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12))

        # Create Treeview sections with correctly named attributes
        self.create_treeview_section("This Computer's Profile", 0, "current_profile")
        self.create_treeview_section("Comparison Profile", 2, "compare_profile")
        self.create_treeview_section("Differences", 3, "diff")

        # Center Column: UI Buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        self.profile_button = ctk.CTkButton(self.button_frame, text="Profile this Computer", command=self.profile_computer)
        self.profile_button.pack(pady=10)

        self.load_button = ctk.CTkButton(self.button_frame, text="Load Comparison Profile", command=self.load_profile)
        self.load_button.pack(pady=10)

        self.save_button = ctk.CTkButton(self.button_frame, text="Save Profile", command=self.save_profile)
        self.save_button.pack(pady=10)

        self.diff_button = ctk.CTkButton(self.button_frame, text="Diff Profiles", command=self.diff_profiles)
        self.diff_button.pack(pady=10)

    def create_treeview_section(self, label_text, column, attribute_name):
        label = ctk.CTkLabel(self, text=label_text, anchor="w")
        label.grid(row=0, column=column, padx=10, pady=5, sticky="w")

        frame = tk.Frame(self)
        frame.grid(row=1, column=column, padx=10, pady=10, sticky="nsew")

        tree = ttk.Treeview(frame, style="Treeview")
        tree.heading("#0", text="Category / Item", anchor="w")
        tree.column("#0", width=600, stretch=True)

        scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Right-click menu for copying to clipboard
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Copy to Clipboard", command=lambda: self.copy_to_clipboard(tree))

        def show_context_menu(event):
            context_menu.post(event.x_root, event.y_root)

        tree.bind("<Button-3>", show_context_menu)

        # Set the attribute dynamically for future reference
        setattr(self, f"{attribute_name}_tree", tree)

    def copy_to_clipboard(self, treeview):
        data = []
        for child in treeview.get_children():
            data.append(self.treeview_to_string(treeview, child))
        clipboard_text = "\n".join(data)
        self.clipboard_clear()
        self.clipboard_append(clipboard_text)
        messagebox.showinfo("Copied", "Profile data copied to clipboard.")

    def treeview_to_string(self, treeview, item, level=0):
        text = "    " * level + treeview.item(item, "text")
        child_texts = [self.treeview_to_string(treeview, child, level + 1) for child in treeview.get_children(item)]
        return "\n".join([text] + child_texts)
    def get_browser_data(self):
        browser_data = {"favorites": [], "extensions": []}

        # Chrome favorites
        chrome_bookmarks = Path(os.getenv("LOCALAPPDATA"), r"Google\Chrome\User Data\Default\Bookmarks")
        if chrome_bookmarks.exists():
            with open(chrome_bookmarks, "r", encoding="utf-8") as f:
                bookmarks = json.load(f)
                browser_data["favorites"].append({"browser": "Chrome", "bookmarks": bookmarks})

        # Edge favorites
        edge_bookmarks = Path(os.getenv("LOCALAPPDATA"), r"Microsoft\Edge\User Data\Default\Bookmarks")
        if edge_bookmarks.exists():
            with open(edge_bookmarks, "r", encoding="utf-8") as f:
                bookmarks = json.load(f)
                browser_data["favorites"].append({"browser": "Edge", "bookmarks": bookmarks})

        # Chrome Extensions with names and IDs
        chrome_extensions_path = Path(os.getenv("LOCALAPPDATA"), r"Google\Chrome\User Data\Default\Extensions")
        for extension_folder in chrome_extensions_path.glob("*"):
            if extension_folder.is_dir():
                manifest_file = extension_folder / "manifest.json"
                extension_name = "Unknown Extension"
                try:
                    if manifest_file.exists():
                        with open(manifest_file, "r", encoding="utf-8") as f:
                            manifest_data = json.load(f)
                            extension_name = manifest_data.get("name", "Unknown Extension")
                except (FileNotFoundError, json.JSONDecodeError):
                    pass
                browser_data["extensions"].append({"browser": "Chrome", "name": extension_name, "id": extension_folder.name})

        # Edge Extensions with names and IDs
        edge_extensions_path = Path(os.getenv("LOCALAPPDATA"), r"Microsoft\Edge\User Data\Default\Extensions")
        for extension_folder in edge_extensions_path.glob("*"):
            if extension_folder.is_dir():
                manifest_file = extension_folder / "manifest.json"
                extension_name = "Unknown Extension"
                try:
                    if manifest_file.exists():
                        with open(manifest_file, "r", encoding="utf-8") as f:
                            manifest_data = json.load(f)
                            extension_name = manifest_data.get("name", "Unknown Extension")
                except (FileNotFoundError, json.JSONDecodeError):
                    pass
                browser_data["extensions"].append({"browser": "Edge", "name": extension_name, "id": extension_folder.name})

        return browser_data



    def profile_computer(self):
        # Replace 'self.profile_tree' with 'self.current_profile_tree'
        profile_data = self.get_current_profile()
        self.display_profile_data(profile_data, self.current_profile_tree)



    def load_profile(self):
        # Open file dialog to load a comparison profile
        file_path = filedialog.askopenfilename(title="Select Profile File", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "r") as file:
                profile_data = json.load(file)
                self.display_profile_data(profile_data, self.compare_profile_tree)

    def save_profile(self):
        # Open file dialog to save profile data
        file_path = filedialog.asksaveasfilename(title="Save Profile As", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            profile_data = self.get_current_profile()
            with open(file_path, "w") as file:
                json.dump(profile_data, file, indent=2)
            messagebox.showinfo("Save Profile", "Profile saved successfully!")

    def diff_profiles(self):
        # Compute differences between the current and comparison profile and display them
        current_profile = self.extract_data_from_treeview(self.profile_tree)
        comparison_profile = self.extract_data_from_treeview(self.compare_profile_tree)
        differences = self.get_diff(current_profile, comparison_profile)
        self.display_profile_data(differences, self.diff_tree)

    def display_profile_data(self, data, treeview):
        # Clear existing data in the treeview
        for item in treeview.get_children():
            treeview.delete(item)

        # Insert new data by section
        for section, items in data.items():
            section_id = treeview.insert("", "end", text=section, open=True)

            if section == "mapped_drives":
                # Display mapped drives or indicate if none are present
                if items:
                    for drive in items:
                        treeview.insert(section_id, "end", text=f"{drive['drive']}: {drive['path']}")
                else:
                    treeview.insert(section_id, "end", text="No Mapped Drives")

            elif section == "browsers":
                # Expand browser favorites and extensions
                if "favorites" in items:
                    favorites_id = treeview.insert(section_id, "end", text="Favorites", open=True)
                    for favorite in items["favorites"]:
                        if isinstance(favorite, dict):  # Each favorite as a dictionary
                            for name, url in favorite.items():
                                treeview.insert(favorites_id, "end", text=f"{name}: {url}")
                        else:
                            treeview.insert(favorites_id, "end", text=str(favorite))

                if "extensions" in items:
                    extensions_id = treeview.insert(section_id, "end", text="Extensions", open=True)
                    for extension in items["extensions"]:
                        treeview.insert(extensions_id, "end", text=str(extension))

            elif isinstance(items, list):
                # Display lists (like software, printers, etc.)
                for item in items:
                    if isinstance(item, dict):  # For dictionaries within lists
                        item_id = treeview.insert(section_id, "end", text="Item", open=True)
                        for key, value in item.items():
                            treeview.insert(item_id, "end", text=f"{key}: {value}")
                    else:  # For simple list items (like URLs or sync paths in SharePoint)
                        treeview.insert(section_id, "end", text=str(item))

            elif isinstance(items, dict):
                # Display nested dictionaries (like windows_info)
                for key, value in items.items():
                    treeview.insert(section_id, "end", text=f"{key}: {value}")


    def extract_data_from_treeview(self, treeview):
        # Extract data from the treeview to compare profiles
        data = {}
        for section in treeview.get_children():
            section_text = treeview.item(section, "text")
            items = []
            for item in treeview.get_children(section):
                items.append(treeview.item(item, "text"))
            data[section_text] = items
        return data

    # Replace these with your actual implementation functions
    def get_current_profile(self):
        return {
            "software": self.get_installed_software(),
            "printers": self.get_printers(),
            "windows_info": self.get_windows_info(),
            "browsers": self.get_browser_data(),
            "mapped_drives": self.get_mapped_drives()
        }

    def get_diff(self, current_profile, comparison_profile):
        # Simple diff function to illustrate changes
        diff = DeepDiff(current_profile, comparison_profile, ignore_order=True)
        return diff.to_dict()


    def get_installed_software(self):
        # Fetching MSI-installed applications from the Windows registry
        installed_software = []
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        for path in registry_paths:
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                for i in range(winreg.QueryInfoKey(registry_key)[0]):
                    try:
                        sub_key = winreg.EnumKey(registry_key, i)
                        app_key = winreg.OpenKey(registry_key, sub_key)
                        name, version = None, None
                        try:
                            name = winreg.QueryValueEx(app_key, "DisplayName")[0]
                            version = winreg.QueryValueEx(app_key, "DisplayVersion")[0]
                        except FileNotFoundError:
                            pass
                        if name:
                            installed_software.append({"name": name, "version": version})
                    except EnvironmentError:
                        pass
            except EnvironmentError:
                pass

        # Fetching MSIX apps using PowerShell
        command = "powershell", "Get-AppxPackage | Select-Object Name, Version"
        output = subprocess.run(command, capture_output=True, text=True).stdout
        for line in output.splitlines()[3:]:  # Skip header lines
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    installed_software.append({"name": parts[0], "version": parts[1]})
        
        return installed_software

    def get_printers(self):
        printers_info = []
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        
        for printer in printers:
            printer_name = printer[2]
            try:
                printer_handle = win32print.OpenPrinter(printer_name)
                printer_info = win32print.GetPrinter(printer_handle, 2)
                driver_name = printer_info["pDriverName"]
                port_name = printer_info["pPortName"]
                printer_ip = port_name if "IP_" in port_name else "N/A"
                printers_info.append({
                    "name": printer_name,
                    "port": port_name,
                    "ip_address": printer_ip,
                    "driver_path": printer_info["pDriverName"],
                    "driver_file": driver_name
                })
                win32print.ClosePrinter(printer_handle)
            except Exception as e:
                pass

        return printers_info

    def get_windows_info(self):
        """
        Gather detailed Windows information, including domain/workgroup and Azure AD status.
        """
        # Basic Windows information
        windows_version = platform.version()
        update_version = platform.release()
        computer_name = os.getenv("COMPUTERNAME")

        # Get domain/workgroup information
        try:
            c = wmi.WMI()
            system = c.Win32_ComputerSystem()[0]
            if system.PartOfDomain:
                domain_status = f"Domain Joined: {system.Domain}"
            else:
                domain_status = f"Workgroup: {system.Workgroup}"
        except Exception:
            domain_status = "Unable to determine domain/workgroup status"

        # Check Azure AD join status using `dsregcmd /status`
        azure_ad_status = "Not Azure AD Joined"  # Default
        try:
            azure_ad_check_cmd = ["dsregcmd", "/status"]
            result = subprocess.run(azure_ad_check_cmd, capture_output=True, text=True, shell=True)
            if "AzureAdJoined : YES" in result.stdout:
                azure_ad_status = "Azure AD Joined"
            elif "AzureAdJoined : NO" in result.stdout:
                azure_ad_status = "Not Azure AD Joined"
            else:
                azure_ad_status = "Unable to determine Azure AD status"
        except Exception:
            azure_ad_status = "Error retrieving Azure AD status"

        return {
            "windows_version": windows_version,
            "update_version": update_version,
            "computer_name": computer_name,
            "domain_status": domain_status,
            "azure_ad_status": azure_ad_status
        }


    def get_mapped_drives(self):
        mapped_drives = []
        for part in psutil.disk_partitions():
            if "network" in part.opts:
                mapped_drives.append({"drive": part.device, "path": part.mountpoint})
        return mapped_drives

    def get_sharepoint_syncs(self):
        sharepoint_syncs = []
        try:
            shell = win32com.client.Dispatch("Shell.Application")
            for folder in shell.Namespace(17).Items():  # CLSID for user folders
                if "OneDrive" in folder.Path:
                    sharepoint_syncs.append(folder.Path)
        except Exception:
            pass
        return sharepoint_syncs

if __name__ == "__main__":
    app = ProfileApp()
    app.mainloop()
