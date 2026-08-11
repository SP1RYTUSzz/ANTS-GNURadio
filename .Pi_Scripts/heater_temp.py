#!/usr/bin/env python3
import csv
import re
import serial
import time
import subprocess
from datetime import datetime
from pathlib import Path

PORT = "/dev/ttyAMA0"
BAUD = 115200

# How often to update and log the Raspberry Pi CPU temperature.
PI_TEMP_INTERVAL = 1.0  # seconds

# The log file will be created in whichever folder you run this script from.
LOG_FILE = Path("pi_temperature_log.csv")

# Matches messages like:
# CH1: 23.75 C, Heater OFF, Duty 0%, Status OFF
MESSAGE_RE = re.compile(
    r"(CH[12]:\s*[-+]?\d+(?:\.\d+)?\s*C,\s*"
    r"Heater\s+(?:ON|OFF),\s*"
    r"Duty\s+\d+%,\s*"
    r"Status\s+(?:ON|OFF))"
)

latest = {
    "CH1": "CH1: waiting for data...",
    "CH2": "CH2: waiting for data...",
    "PI": "Raspberry Pi CPU temp: waiting...",
    "LOG": f"Logging temperature to: {LOG_FILE}",
}


def clean_text(data: bytes) -> str:
    """Convert UART bytes to text and remove garbage/non-printable characters."""
    text = data.decode("latin-1", errors="ignore")
    return "".join(ch for ch in text if ch in "\r\n\t" or 32 <= ord(ch) <= 126)


def get_pi_temp_c() -> float:
    """Return the Raspberry Pi CPU temperature in degrees Celsius."""
    # Fast Linux method: value is usually in thousandths of a degree C.
    temp_file = Path("/sys/class/thermal/thermal_zone0/temp")
    if temp_file.exists():
        milli_c = int(temp_file.read_text().strip())
        return milli_c / 1000

    # Fallback method on Raspberry Pi OS.
    output = subprocess.check_output(["vcgencmd", "measure_temp"], text=True).strip()
    match = re.search(r"temp=([-+]?\d+(?:\.\d+)?)'C", output)
    if not match:
        raise RuntimeError(f"Could not read temperature from: {output}")
    return float(match.group(1))


def prepare_log_file():
    """Open the CSV log file and add a header row if the file is new."""
    file_already_has_data = LOG_FILE.exists() and LOG_FILE.stat().st_size > 0
    log_file = LOG_FILE.open("a", newline="", buffering=1)
    writer = csv.writer(log_file)

    if not file_already_has_data:
        writer.writerow(["timestamp", "cpu_temp_c"])
        log_file.flush()

    return log_file, writer


def update_and_log_pi_temp(writer, log_file) -> None:
    """Read the Pi temperature, update the dashboard, and append it to the CSV file."""
    timestamp = datetime.now().isoformat(sep=" ", timespec="seconds")

    try:
        temp_c = get_pi_temp_c()
        latest["PI"] = f"Raspberry Pi CPU temp: {temp_c:.1f} C"
        latest["LOG"] = f"Last logged: {timestamp}, {temp_c:.1f} C"
        writer.writerow([timestamp, f"{temp_c:.3f}"])
    except Exception:
        latest["PI"] = "Raspberry Pi CPU temp: unavailable"
        latest["LOG"] = f"Last log attempt: {timestamp}, temperature unavailable"
        writer.writerow([timestamp, ""])

    # Make sure the data is written to the file immediately.
    log_file.flush()


def draw_screen() -> None:
    """Redraw the same terminal area instead of endlessly scrolling."""
    print("\033[2J\033[H", end="")  # clear screen and move cursor home
    print("Pico UART live view")
    print("Press Ctrl+C to stop\n")
    print(latest["CH1"])
    print(latest["CH2"])
    print(latest["PI"])
    print(latest["LOG"])
    print("", flush=True)


def main() -> None:
    buffer = ""
    last_temp_update = 0.0

    log_file, writer = prepare_log_file()

    try:
        with serial.Serial(PORT, BAUD, timeout=0.1) as uart:
            update_and_log_pi_temp(writer, log_file)
            last_temp_update = time.monotonic()
            draw_screen()

            while True:
                changed = False
                now = time.monotonic()

                if now - last_temp_update >= PI_TEMP_INTERVAL:
                    update_and_log_pi_temp(writer, log_file)
                    last_temp_update = now
                    changed = True

                data = uart.read(uart.in_waiting or 1)
                if data:
                    buffer += clean_text(data)

                    # Keep the buffer small in case junk/no-newline data arrives.
                    if len(buffer) > 2000:
                        buffer = buffer[-1000:]

                    matches = list(MESSAGE_RE.finditer(buffer))

                    for match in matches:
                        message = match.group(1)
                        channel = message.split(":", 1)[0]
                        latest[channel] = message
                        changed = True

                    # Remove processed data so old messages are not parsed repeatedly.
                    if matches:
                        buffer = buffer[matches[-1].end():]

                if changed:
                    draw_screen()
                    time.sleep(0.05)
    finally:
        log_file.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
