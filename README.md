# User Settings Profiler

![Test Status](https://github.com/gnubyte/windows-profiler/actions/workflows/python-app.yml/badge.svg)
[Download release V1.0.0](https://github.com/gnubyte/windows-profiler/releases/download/V1.0.0/windowsprofiler.exe)

A Python-based GUI application for profiling and comparing system configurations, browser settings, installed software, printers, and mapped network drives on a Windows machine. Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for a modern dark theme and enhanced usability.

## Features
- **Profile System**: Capture information about installed software, printers, Windows configuration, browser favorites, and mapped drives.
- **Save/Load Profiles**: Export profiles as JSON files for future reference.
- **Profile Comparison**: Compare the current system profile against a previously saved profile, with a diff view highlighting changes.
- **Contextual Copying**: Copy profile details to the clipboard with right-click.

## Requirements
- Python 3.x
- **Libraries**:
  - `customtkinter`, `tkinter`
  - `psutil`, `wmi`, `win32print`, `win32api`, `deepdiff`, `json`, `os`, `platform`

## Installation
1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
