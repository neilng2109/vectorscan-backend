import pandas as pd
import matplotlib.pyplot as plt

# Corrected data from the screenshot (19 records)
data = {
    "Fault Entry ID": [
        "rec00uq1ykLPQ3s7T", "rec06tFhS0bLvuHw0", "rec0NGYTY0JK4VWQi",
        "rec1PFZ96qRG6LXV", "rec10XYuikHYxeSOj", "rec28VrYuFXWQZS3o",
        "rec2U8TEm5wmst9YP", "rec2X1Sa0oS3VIHr", "rec2Z0jaXC9Y6U5tF",
        "rec3A1F0t7arNQ9j", "rec3S6sy9LtQJPVDb", "rec41spQFy0o0ifR5",
        "rec4xU8yjehS76MDX", "rec5CA1HrheAApgPl", "rec5H1EKJvbWTwiQ",
        "rec5XZ9TE9R0k7Pp", "rec5hXW7gXFglaM8Z", "rec6HUHSVOtmZQRY",
        "rec6RSOshEN6sJuYZ"
    ],
    "Equipment Affected": [
        "Breaker Panel #3", "Cooling Pump #2", "Air Handler #1",
        "Hydraulic Pump #1", "Compressor", "Generator #3",
        "Main Engine", "Hydraulic Pump #1", "Cooling Pump #1",
        "Emergency Generator", "Emergency Generator", "Main Generator #1",
        "Emergency Generator", "Cooling Pump #2", "Cooling Pump #1",
        "Air Handler #1", "Battery Bank", "Cooling Pump #2", "Main Generator #1"
    ],
    "Fault Description": [
        "Vibration - Pump cavitation", "Low Pressure - Blocked filter", "Overheat - Oil cooler clogged",
        "Vibration - Pump cavitation", "Overheat â€“ Motor failure", "Leakage â€“ Cracked seal",
        "Intermittent Power â€“ Faulty valve", "Noise - Air in system", "Overheat - Fan motor failure",
        "Low Voltage - Alternator fault", "Low Pressure - Blocked filter", "Low Pressure - Blocked filter",
        "Overheat - Wiring fault", "Leaking - Seal worn out", "Low Pressure - Blocked filter",
        "Noise - Bearing misalignment", "No Output â€“ Sensor failure", "Short Circuit - Insulation failure",
        "Leaking - Seal worn out"
    ],
    "Cause (if known)": [
        "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Count the frequency of each fault description
fault_counts = df["Fault Description"].value_counts()

# Create a bar chart
plt.figure(figsize=(10, 6))
fault_counts.plot(kind="bar", color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD', '#D4A5A5', '#9B59B6', '#3498DB', '#E74C3C'])
plt.title("Frequency of Fault Descriptions")
plt.xlabel("Fault Description")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Save the chart
plt.savefig("fault_frequency_chart.png")
print("Chart saved as 'fault_frequency_chart.png'.")