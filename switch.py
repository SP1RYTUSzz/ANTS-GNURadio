import subprocess
import sys
import time

files = ['/home/antfarm/Documents/Antman_GNURadio_Code/lower_freq.py', 
        '/home/antfarm/Documents/Antman_GNURadio_Code/upper_freq.py']
duration = 15
i = 0 

try:
    while True:
        script = files[i % len(files)]
        print(f"Starting {script}")

        proc = subprocess.Popen([sys.executable, script])

        time.sleep(duration)

        print(f"Stopping {script}")
        proc.terminate

        try: 
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        i+=1
except KeyboardInterrupt:
    proc.terminate()
    print("\nStopped.")
    try: 
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()