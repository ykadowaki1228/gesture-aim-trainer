import subprocess
import time
import sys
import os

TRACKING_FOLDER = "handTrack"
GAME_FOLDER = "game"

def main():
    python_exe = sys.executable
    base_dir = os.getcwd()

    print("Starting a whole system")

    # Start the tracking system
    track_path = os.path.join(base_dir, TRACKING_FOLDER)
    if not os.path.exists(track_path):
        print(f"Tracking folder '{TRACKING_FOLDER}' does not exist.")
        return
    
    print(f"[{TRACKING_FOLDER}] Starting tracking system...")

    # Run handTrack.py
    p1 = subprocess.Popen(
        [python_exe, "handTrack.py"], 
        cwd=track_path
    )

    print("For Camera Preparation, please wait 5 seconds...")
    time.sleep(3)

    game_path = os.path.join(base_dir, GAME_FOLDER)
    if not os.path.exists(game_path):
        print(f"Game folder '{GAME_FOLDER}' does not exist.")
        print("Stop tracking system.")
        p1.terminate()
        return
    
    print(f"[{GAME_FOLDER}] Starting game system...")
    # Run game.py
    p2 = subprocess.Popen(
        [python_exe, "game.py"],
        cwd=game_path
    )

    print("Both systems are running. Press ESC key to stop.")

    try:
        while True:
            #Check if game is still running(Working when None)
            if p2.poll() is not None:
                print("Game system has stopped. Stopping tracking system...")
                p1.terminate()
                break

            # Check if MediaPipe tracking is still running(Working when None)
            if p1.poll() is not None:
                print("Tracking system has stopped. Stopping game system...")
                p2.terminate()
                break


    except KeyboardInterrupt:
        print("Stopping both systems...")

    finally:
        if p1.poll() is None:
            p1.terminate()
            
        if p2.poll() is None:
            p2.terminate()

if __name__ == "__main__":
    main()