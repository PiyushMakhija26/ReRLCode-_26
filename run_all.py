import subprocess
import time
import os
import sys

def run():
    print("Starting Neo-Grid Logistics RL System...")
    
    # 1. Start Training in background (light mode)
    # Redirecting to log so it doesn't clutter console
    train_proc = subprocess.Popen([sys.executable, "logic/train.py"], 
                                  stdout=open("train_log.txt", "w"), 
                                  stderr=subprocess.STDOUT)
    print("RL Brain training initialized...")

    # 2. Start FastAPI Server
    os.environ["PYTHONPATH"] = os.getcwd() # ensure imports work
    api_proc = subprocess.Popen([sys.executable, "logic/api.py"])
    print("Simulation API bridge active on http://localhost:8000")

    # 3. Inform about dashboard
    print("\n" + "="*50)
    print("DASHBOARD READY")
    print("Location: c:\\Users\\piyu4\\OneDrive\\Desktop\\RL_project\\dashboard")
    print("Action Required: In a new terminal, run:")
    print("  cd dashboard && npm run dev")
    print("="*50 + "\n")

    try:
        while True:
            time.sleep(1)
            if train_proc.poll() is not None:
                print("⚠️ Training process stopped. Check train_log.txt")
                break
    except KeyboardInterrupt:
        print("\nShutting down...")
        train_proc.terminate()
        api_proc.terminate()

if __name__ == "__main__":
    run()
