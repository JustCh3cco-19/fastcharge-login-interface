### LINUX

**pyinstaller --onefile --collect-all pyzbar --collect-all PIL --add-data "resources:resources" --add-data ".env:."--add-binary "resources/libs/linux/libzbar.so.0:." --add-binary "resources/libs/linux/libzbar.so.0.3.0:." --hidden-import="PIL._tkinter_finder" --name "AccessiFCE" main.py**

### WINDOWS

**pyinstaller --onefile --collect-all pyzbar --collect-all PIL --add-data "resources:resources" --add-data ".env:." --add-binary "resources/libs/windows/libiconv.dll;." --hidden-import="PIL._tkinter_finder" --clean --name "AccessiFCE" main.py**