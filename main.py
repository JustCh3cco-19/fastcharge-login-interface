import threading
from interfaccia import run_interface
from monitoraccessi import monitor_log

def main():
    # Start the access monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_log, daemon=True)
    monitor_thread.start()

    # Run the main interface
    run_interface()

if __name__ == "__main__":
    print("FastCharge Online")
    main()