import tkinter as tk
import psutil
import GPUtil
import platform

if platform.system() == "Windows":
    import wmi


def update_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    cpu_temp = get_cpu_temperature()
    gpu_temp = get_gpu_temperature()

    cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
    memory_label.config(text=f"Memory Usage: {memory_usage}%")
    disk_label.config(text=f"Disk Usage: {disk_usage}%")
    cpu_temp_label.config(text=f"CPU Temperature: {cpu_temp}°C")
    gpu_temp_label.config(text=f"GPU Temperature: {gpu_temp}°C")

    root.after(1000, update_stats)  # Update every second


def get_cpu_temperature():
    try:
        if platform.system() == "Windows":
            try:
                w = wmi.WMI(namespace="root\\wmi")
                temperature_info = w.MSAcpi_ThermalZoneTemperature()
                for temp in temperature_info:
                    Temp = temp.CurrentTemperature / 10.0 - 273.15
                    return round(Temp, 2)
            except wmi.x_wmi as e:
                if "OLE error 0x80041003" in str(e):
                    return "Access Denied (Run as Admin)"
                return f"Error: {e}"
        else:
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                if 'coretemp' in temps:
                    return temps['coretemp'][0].current
                elif 'cpu-thermal' in temps:
                    return temps['cpu-thermal'][0].current
            return "N/A"
    except Exception as e:
        return f"Error: {e}"


def get_gpu_temperature():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            return gpus[0].temperature
        else:
            return "N/A"
    except Exception as e:
        return f"Error: {e}"


root = tk.Tk()
root.title("PC Stats Monitor")
root.overrideredirect(True)  # Remove the window border and title bar
root.attributes('-topmost', True)  # Keep the window on top
root.attributes('-alpha', 0.9)  # Set window transparency (0.0 to 1.0)

# Create a transparent frame
transparent_frame = tk.Frame(root, bg='black')
transparent_frame.pack(fill=tk.BOTH, expand=True)

font_settings = ("Helvetica", 12)  # Decrease font size

cpu_label = tk.Label(transparent_frame, text="CPU Usage: Calculating...", font=font_settings, bg='black', fg='white')
cpu_label.pack(pady=5)

memory_label = tk.Label(transparent_frame, text="Memory Usage: Calculating...", font=font_settings, bg='black', fg='white')
memory_label.pack(pady=5)

disk_label = tk.Label(transparent_frame, text="Disk Usage: Calculating...", font=font_settings, bg='black', fg='white')
disk_label.pack(pady=5)

cpu_temp_label = tk.Label(transparent_frame, text="CPU Temperature: Calculating...", font=font_settings, bg='black', fg='white')
cpu_temp_label.pack(pady=5)

gpu_temp_label = tk.Label(transparent_frame, text="GPU Temperature: Calculating...", font=font_settings, bg='black', fg='white')
gpu_temp_label.pack(pady=5)

update_stats()  # Initial call to start the update loop

root.mainloop()
