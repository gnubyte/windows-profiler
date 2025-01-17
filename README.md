# User Settings Profiler

![Test Status](https://github.com/gnubyte/windows-profiler/actions/workflows/python-app.yml/badge.svg)
[Download release V1.0.0](https://github.com/gnubyte/windows-profiler/releases/download/V1.0.0/windowsprofiler.exe)

A portable executable application for profiling and comparing system configurations, browser settings, installed software, printers, and mapped network drives on a Windows machine. Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for a modern dark theme and enhanced usability.

![Screenshot of software](https://github.com/gnubyte/windows-profiler/blob/main/2025-01-09%2009_21_19-Release%20V1.0.0%20%C2%B7%20gnubyte_windows-profiler%20%E2%80%94%20Mozilla%20Firefox.png?raw=true)


## Features
- **Profile System**: Capture information about installed software, printers, Windows configuration, browser favorites, and mapped drives.
- **Save/Load Profiles**: Export profiles as JSON files for future reference.
- **Profile Comparison**: Compare the current system profile against a previously saved profile, with a diff view highlighting changes.
- **Contextual Copying**: Copy profile details to the clipboard with right-click.

## Using it

Download the exe from the [releases section](https://github.com/gnubyte/windows-profiler/releases)

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
