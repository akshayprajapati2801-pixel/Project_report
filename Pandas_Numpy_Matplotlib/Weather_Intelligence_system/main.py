
# ============================================
# WEATHER INTELLIGENCE & CLIMATE ANALYTICS
# Code 1: Project Setup
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Project information
PROJECT_NAME = "Weather Intelligence & Climate Analytics System"
PROJECT_VERSION = "1.0"

# Visual theme
BACKGROUND_COLOR = "#0B1220"
PANEL_COLOR = "#111C2E"
TEAL_COLOR = "#14B8A6"
TEXT_COLOR = "#E5E7EB"

# Display settings
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

# Verify libraries and project setup
print("=" * 55)
print(PROJECT_NAME)
print("=" * 55)

print(f"Project Version : {PROJECT_VERSION}")
print(f"Pandas Version  : {pd.__version__}")
print(f"NumPy Version   : {np.__version__}")
print(f"Matplotlib      : Ready")

print("\nProject setup completed successfully!")
print("Weather analysis environment is ready.")

# ============================================
# CODE 2: GENERATE WEATHER DATA
# ============================================

# Make results reproducible
np.random.seed(42)

# Generate dates for one full year
dates = pd.date_range(
    start="2025-01-01",
    end="2025-12-31",
    freq="D"
)

# Number of days in the dataset
days = len(dates)

# Simulate seasonal temperature changes
day_number = np.arange(days)

seasonal_temperature = (
    24 + 10 * np.sin(2 * np.pi * (day_number - 100) / 365)
)

# Generate weather measurements
temperature = seasonal_temperature + np.random.normal(0, 3, days)

humidity = np.random.uniform(35, 95, days)

rainfall = np.random.gamma(shape=1.5, scale=3.0, size=days)

wind_speed = np.random.uniform(2, 25, days)

air_pressure = np.random.normal(1013, 6, days)

# Create a Pandas DataFrame
weather_data = pd.DataFrame({
    "Date": dates,
    "Temperature_C": np.round(temperature, 2),
    "Humidity_Percent": np.round(humidity, 2),
    "Rainfall_mm": np.round(rainfall, 2),
    "Wind_Speed_kmh": np.round(wind_speed, 2),
    "Air_Pressure_hPa": np.round(air_pressure, 2)
})

# Display the generated dataset
print("\n" + "=" * 55)
print("SYNTHETIC WEATHER DATA GENERATED")
print("=" * 55)

print(f"Total records: {len(weather_data)}")
print(f"Total columns: {len(weather_data.columns)}")

print("\nFirst 5 records:")
print(weather_data.head())

print("\nDataset information:")
print(weather_data.info())

print("\nBasic statistical summary:")
print(weather_data.describe().round(2))


# ============================================
# CODE 3: DATA QUALITY AND VALIDATION
# ============================================

print("\n" + "=" * 55)
print("WEATHER DATA QUALITY REPORT")
print("=" * 55)

# 1. Check dataset dimensions
print(f"\nDataset shape: {weather_data.shape}")
print(f"Total rows: {weather_data.shape[0]}")
print(f"Total columns: {weather_data.shape[1]}")

# 2. Check missing values
missing_values = weather_data.isnull().sum()

print("\nMissing values per column:")
print(missing_values)

total_missing = int(missing_values.sum())
print(f"\nTotal missing values: {total_missing}")

# 3. Check duplicate records
duplicate_rows = int(weather_data.duplicated().sum())
duplicate_dates = int(weather_data["Date"].duplicated().sum())

print(f"\nDuplicate records: {duplicate_rows}")
print(f"Duplicate dates: {duplicate_dates}")

# 4. Validate measurement ranges
invalid_temperature = (
    (weather_data["Temperature_C"] < -50) |
    (weather_data["Temperature_C"] > 60)
).sum()

invalid_humidity = (
    (weather_data["Humidity_Percent"] < 0) |
    (weather_data["Humidity_Percent"] > 100)
).sum()

invalid_rainfall = (
    weather_data["Rainfall_mm"] < 0
).sum()

invalid_wind = (
    weather_data["Wind_Speed_kmh"] < 0
).sum()

print("\nInvalid measurement checks:")
print(f"Temperature outside -50 to 60 C: {invalid_temperature}")
print(f"Humidity outside 0 to 100%: {invalid_humidity}")
print(f"Negative rainfall readings: {invalid_rainfall}")
print(f"Negative wind-speed readings: {invalid_wind}")

# 5. Check whether every day is represented
expected_days = 365
actual_days = weather_data["Date"].nunique()

print("\nDate coverage:")
print(f"Expected days: {expected_days}")
print(f"Unique dates: {actual_days}")

# 6. Overall quality status
quality_passed = (
    total_missing == 0
    and duplicate_rows == 0
    and duplicate_dates == 0
    and invalid_temperature == 0
    and invalid_humidity == 0
    and invalid_rainfall == 0
    and invalid_wind == 0
    and actual_days == expected_days
)

print("\n" + "-" * 55)

if quality_passed:
    print("STATUS: PASSED")
    print("Weather dataset passed all quality checks.")
else:
    print("STATUS: REVIEW REQUIRED")
    print("Some data quality checks need attention.")

print("-" * 55)


# ============================================
# CODE 4: CLIMATE KPIs AND MONTHLY ANALYSIS
# ============================================

print("\n" + "=" * 60)
print("CLIMATE INTELLIGENCE REPORT")
print("=" * 60)

# Extract month information from the Date column
weather_data["Month"] = weather_data["Date"].dt.month
weather_data["Month_Name"] = weather_data["Date"].dt.strftime("%B")

# 1. Calculate overall climate KPIs
average_temperature = weather_data["Temperature_C"].mean()
maximum_temperature = weather_data["Temperature_C"].max()
minimum_temperature = weather_data["Temperature_C"].min()

average_humidity = weather_data["Humidity_Percent"].mean()
total_rainfall = weather_data["Rainfall_mm"].sum()
average_wind_speed = weather_data["Wind_Speed_kmh"].mean()
average_pressure = weather_data["Air_Pressure_hPa"].mean()

rainy_days = int((weather_data["Rainfall_mm"] >= 1.0).sum())

print("\nOVERALL CLIMATE KPIs")
print("-" * 60)
print(f"Average temperature : {average_temperature:.2f} °C")
print(f"Maximum temperature : {maximum_temperature:.2f} °C")
print(f"Minimum temperature : {minimum_temperature:.2f} °C")
print(f"Average humidity    : {average_humidity:.2f} %")
print(f"Total rainfall      : {total_rainfall:.2f} mm")
print(f"Average wind speed  : {average_wind_speed:.2f} km/h")
print(f"Average air pressure: {average_pressure:.2f} hPa")
print(f"Rainy days          : {rainy_days}")

# 2. Create monthly summaries
monthly_summary = (
    weather_data
    .groupby(["Month", "Month_Name"], sort=True)
    .agg(
        Average_Temperature=("Temperature_C", "mean"),
        Maximum_Temperature=("Temperature_C", "max"),
        Minimum_Temperature=("Temperature_C", "min"),
        Average_Humidity=("Humidity_Percent", "mean"),
        Total_Rainfall=("Rainfall_mm", "sum"),
        Average_Wind_Speed=("Wind_Speed_kmh", "mean")
    )
    .reset_index()
)

# Round values for easier reading
numeric_columns = monthly_summary.select_dtypes(
    include="number"
).columns

monthly_summary[numeric_columns] = (
    monthly_summary[numeric_columns].round(2)
)

print("\nMONTHLY WEATHER SUMMARY")
print("-" * 60)
print(
    monthly_summary[
        [
            "Month_Name",
            "Average_Temperature",
            "Total_Rainfall",
            "Average_Humidity"
        ]
    ].to_string(index=False)
)

# 3. Identify important climate patterns
hottest_month = monthly_summary.loc[
    monthly_summary["Average_Temperature"].idxmax(),
    "Month_Name"
]

coolest_month = monthly_summary.loc[
    monthly_summary["Average_Temperature"].idxmin(),
    "Month_Name"
]

wettest_month = monthly_summary.loc[
    monthly_summary["Total_Rainfall"].idxmax(),
    "Month_Name"
]

print("\nKEY CLIMATE INSIGHTS")
print("-" * 60)
print(f"Hottest month by average temperature : {hottest_month}")
print(f"Coolest month by average temperature : {coolest_month}")
print(f"Wettest month by total rainfall       : {wettest_month}")

print("\nClimate KPI analysis completed successfully!")


# ============================================
# CODE 5: PROFESSIONAL CLIMATE VISUALIZATION
# ============================================

# Configure the dark theme
plt.rcParams.update({
    "figure.facecolor": BACKGROUND_COLOR,
    "axes.facecolor": PANEL_COLOR,
    "axes.edgecolor": "#334155",
    "axes.labelcolor": TEXT_COLOR,
    "xtick.color": TEXT_COLOR,
    "ytick.color": TEXT_COLOR,
    "text.color": TEXT_COLOR,
    "grid.color": "#334155",
    "grid.alpha": 0.5,
    "font.size": 10
})

# --------------------------------------------
# CHART 1: DAILY TEMPERATURE TREND
# --------------------------------------------

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    weather_data["Date"],
    weather_data["Temperature_C"],
    color=TEAL_COLOR,
    linewidth=1.5,
    label="Daily temperature"
)

# Add average temperature reference line
ax.axhline(
    average_temperature,
    color="#F59E0B",
    linestyle="--",
    linewidth=1.8,
    label=f"Yearly average: {average_temperature:.1f} °C"
)

ax.set_title(
    "Daily Temperature Trend — 2025",
    fontsize=15,
    fontweight="bold",
    pad=15
)
ax.set_xlabel("Date")
ax.set_ylabel("Temperature (°C)")
ax.grid(True, linestyle="--")
ax.legend(frameon=False)

fig.autofmt_xdate()
fig.tight_layout()
plt.show()

# --------------------------------------------
# CHART 2: MONTHLY AVERAGE TEMPERATURE
# --------------------------------------------

fig, ax = plt.subplots(figsize=(11, 5))

bars = ax.bar(
    monthly_summary["Month_Name"],
    monthly_summary["Average_Temperature"],
    color=TEAL_COLOR,
    width=0.65
)

# Highlight the hottest month
hottest_index = monthly_summary[
    "Average_Temperature"
].idxmax()

bars[hottest_index].set_color("#F59E0B")

ax.set_title(
    "Monthly Average Temperature",
    fontsize=15,
    fontweight="bold",
    pad=15
)
ax.set_xlabel("Month")
ax.set_ylabel("Average temperature (°C)")
ax.grid(axis="y", linestyle="--")
ax.set_axisbelow(True)
ax.tick_params(axis="x", rotation=35)

fig.tight_layout()
plt.show()

# --------------------------------------------
# CHART 3: MONTHLY TOTAL RAINFALL
# --------------------------------------------

fig, ax = plt.subplots(figsize=(11, 5))

bars = ax.bar(
    monthly_summary["Month_Name"],
    monthly_summary["Total_Rainfall"],
    color="#38BDF8",
    width=0.65
)

# Highlight the wettest month
wettest_index = monthly_summary[
    "Total_Rainfall"
].idxmax()

bars[wettest_index].set_color("#F59E0B")

ax.set_title(
    "Monthly Total Rainfall",
    fontsize=15,
    fontweight="bold",
    pad=15
)
ax.set_xlabel("Month")
ax.set_ylabel("Rainfall (mm)")
ax.grid(axis="y", linestyle="--")
ax.set_axisbelow(True)
ax.tick_params(axis="x", rotation=35)

fig.tight_layout()
plt.show()

print("\nClimate charts generated successfully!")


# ============================================
# CODE 6: ADVANCED WEATHER ANALYTICS
# ============================================

print("\n" + "=" * 60)
print("ADVANCED WEATHER ANALYTICS")
print("=" * 60)

# --------------------------------------------
# 1. CLASSIFY HUMIDITY LEVELS
# --------------------------------------------

weather_data["Humidity_Level"] = np.select(
    [
        weather_data["Humidity_Percent"] < 40,
        weather_data["Humidity_Percent"] < 70
    ],
    [
        "Low",
        "Moderate"
    ],
    default="High"
)

humidity_counts = (
    weather_data["Humidity_Level"]
    .value_counts()
    .reindex(["Low", "Moderate", "High"], fill_value=0)
)

print("\nHUMIDITY DISTRIBUTION")
print("-" * 40)

for level, count in humidity_counts.items():
    percentage = count / len(weather_data) * 100
    print(f"{level:10s}: {count:3d} days ({percentage:.1f}%)")

# --------------------------------------------
# 2. CLASSIFY RAINFALL PATTERNS
# --------------------------------------------

weather_data["Rainfall_Category"] = np.select(
    [
        weather_data["Rainfall_mm"] < 1,
        weather_data["Rainfall_mm"] < 10
    ],
    [
        "Dry",
        "Light Rain"
    ],
    default="Heavy Rain"
)

rainfall_counts = (
    weather_data["Rainfall_Category"]
    .value_counts()
    .reindex(
        ["Dry", "Light Rain", "Heavy Rain"],
        fill_value=0
    )
)

print("\nRAINFALL DISTRIBUTION")
print("-" * 40)

for category, count in rainfall_counts.items():
    percentage = count / len(weather_data) * 100
    print(f"{category:12s}: {count:3d} days ({percentage:.1f}%)")

# --------------------------------------------
# 3. DETECT TEMPERATURE ANOMALIES USING Z-SCORE
# --------------------------------------------

temperature_mean = weather_data["Temperature_C"].mean()
temperature_std = weather_data["Temperature_C"].std()

if temperature_std > 0:
    weather_data["Temperature_ZScore"] = (
        weather_data["Temperature_C"] - temperature_mean
    ) / temperature_std
else:
    weather_data["Temperature_ZScore"] = 0.0

# Flag values more than 2 standard deviations from the mean
weather_data["Temperature_Anomaly"] = (
    weather_data["Temperature_ZScore"].abs() > 2
)

anomalies = weather_data.loc[
    weather_data["Temperature_Anomaly"],
    ["Date", "Temperature_C", "Temperature_ZScore"]
].copy()

print("\nTEMPERATURE ANOMALY REPORT")
print("-" * 40)
print(f"Average temperature: {temperature_mean:.2f} °C")
print(f"Temperature standard deviation: {temperature_std:.2f} °C")
print(f"Anomalies detected: {len(anomalies)}")

if not anomalies.empty:
    print("\nFirst 10 unusual temperature readings:")
    print(anomalies.head(10).round(2).to_string(index=False))
else:
    print("No temperature anomalies detected.")

# --------------------------------------------
# 4. IDENTIFY THE HOTTEST AND COLDEST DAYS
# --------------------------------------------

hottest_day = weather_data.loc[
    weather_data["Temperature_C"].idxmax()
]

coldest_day = weather_data.loc[
    weather_data["Temperature_C"].idxmin()
]

print("\nTEMPERATURE EXTREMES")
print("-" * 40)
print(
    f"Hottest day: {hottest_day['Date'].strftime('%d %B %Y')} "
    f"({hottest_day['Temperature_C']:.2f} °C)"
)
print(
    f"Coldest day: {coldest_day['Date'].strftime('%d %B %Y')} "
    f"({coldest_day['Temperature_C']:.2f} °C)"
)

# --------------------------------------------
# 5. DISPLAY ANOMALY SUMMARY
# --------------------------------------------

anomaly_percentage = len(anomalies) / len(weather_data) * 100

print("\nANALYTICS SUMMARY")
print("-" * 40)
print(f"Total observations: {len(weather_data)}")
print(f"Unusual temperature days: {len(anomalies)}")
print(f"Anomaly percentage: {anomaly_percentage:.2f}%")
print("\nAdvanced weather analytics completed!")


# ============================================
# CODE 7: EXPORT ANALYTICS REPORTS
# ============================================

from pathlib import Path

# Create output folder automatically
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("\n" + "=" * 60)
print("EXPORTING WEATHER ANALYTICS REPORTS")
print("=" * 60)

# --------------------------------------------
# 1. EXPORT DAILY WEATHER DATA
# --------------------------------------------

weather_file = OUTPUT_DIR / "weather_data.csv"

weather_data.to_csv(
    weather_file,
    index=False,
    date_format="%Y-%m-%d"
)

print(f"\nDaily weather data saved to: {weather_file}")

# --------------------------------------------
# 2. EXPORT MONTHLY SUMMARY
# --------------------------------------------

monthly_file = OUTPUT_DIR / "monthly_summary.csv"

monthly_summary.to_csv(
    monthly_file,
    index=False
)

print(f"Monthly summary saved to: {monthly_file}")

# --------------------------------------------
# 3. EXPORT TEMPERATURE ANOMALIES
# --------------------------------------------

anomaly_file = OUTPUT_DIR / "temperature_anomalies.csv"

anomalies.to_csv(
    anomaly_file,
    index=False,
    date_format="%Y-%m-%d"
)

print(f"Temperature anomalies saved to: {anomaly_file}")

# --------------------------------------------
# 4. VERIFY EXPORTED FILES
# --------------------------------------------

print("\nEXPORT VERIFICATION")
print("-" * 40)

export_files = [
    weather_file,
    monthly_file,
    anomaly_file
]

for file_path in export_files:
    if file_path.exists():
        file_size = file_path.stat().st_size
        print(f"[OK] {file_path} ({file_size:,} bytes)")
    else:
        print(f"[ERROR] Missing file: {file_path}")

# --------------------------------------------
# 5. VERIFY DAILY DATA CAN BE READ BACK
# --------------------------------------------

verification_data = pd.read_csv(
    weather_file,
    parse_dates=["Date"]
)

print("\nREAD-BACK VALIDATION")
print("-" * 40)
print(f"Original daily records: {len(weather_data)}")
print(f"Exported daily records: {len(verification_data)}")

if len(verification_data) == len(weather_data):
    print("PASS: Daily records exported successfully.")
else:
    print("WARNING: Record counts do not match.")

print("\nReport export process completed!")



# ============================================
# CODE 8: CLIMATE DASHBOARD
# ============================================

print("\n" + "=" * 60)
print("BUILDING CLIMATE ANALYTICS DASHBOARD")
print("=" * 60)

# Create a 2x2 dashboard layout
fig, axes = plt.subplots(
    2, 2,
    figsize=(16, 10)
)

fig.patch.set_facecolor(BACKGROUND_COLOR)

ax1, ax2, ax3, ax4 = axes.flatten()

# --------------------------------------------
# CHART 1: DAILY TEMPERATURE TREND
# --------------------------------------------

ax1.plot(
    weather_data["Date"],
    weather_data["Temperature_C"],
    color=TEAL_COLOR,
    linewidth=1.2
)

ax1.axhline(
    average_temperature,
    color="#F59E0B",
    linestyle="--",
    linewidth=1.5,
    label=f"Average: {average_temperature:.1f} °C"
)

ax1.set_title("Daily Temperature Trend", fontweight="bold", pad=10)
ax1.set_ylabel("Temperature (°C)")
ax1.grid(True, linestyle="--")
ax1.legend(frameon=False)
ax1.tick_params(axis="x", rotation=25)

# --------------------------------------------
# CHART 2: MONTHLY AVERAGE TEMPERATURE
# --------------------------------------------

monthly_colors = [
    "#F59E0B"
    if value == monthly_summary["Average_Temperature"].max()
    else TEAL_COLOR
    for value in monthly_summary["Average_Temperature"]
]

ax2.bar(
    monthly_summary["Month_Name"],
    monthly_summary["Average_Temperature"],
    color=monthly_colors
)

ax2.set_title("Monthly Average Temperature", fontweight="bold", pad=10)
ax2.set_ylabel("Temperature (°C)")
ax2.grid(axis="y", linestyle="--")
ax2.set_axisbelow(True)
ax2.tick_params(axis="x", rotation=40)

# --------------------------------------------
# CHART 3: MONTHLY TOTAL RAINFALL
# --------------------------------------------

rainfall_colors = [
    "#F59E0B"
    if value == monthly_summary["Total_Rainfall"].max()
    else "#38BDF8"
    for value in monthly_summary["Total_Rainfall"]
]

ax3.bar(
    monthly_summary["Month_Name"],
    monthly_summary["Total_Rainfall"],
    color=rainfall_colors
)

ax3.set_title("Monthly Total Rainfall", fontweight="bold", pad=10)
ax3.set_ylabel("Rainfall (mm)")
ax3.grid(axis="y", linestyle="--")
ax3.set_axisbelow(True)
ax3.tick_params(axis="x", rotation=40)

# --------------------------------------------
# CHART 4: HUMIDITY DISTRIBUTION
# --------------------------------------------

humidity_labels = humidity_counts.index.tolist()
humidity_values = humidity_counts.values.tolist()

ax4.bar(
    humidity_labels,
    humidity_values,
    color=["#60A5FA", TEAL_COLOR, "#A78BFA"]
)

ax4.set_title("Humidity Distribution", fontweight="bold", pad=10)
ax4.set_ylabel("Number of Days")
ax4.grid(axis="y", linestyle="--")
ax4.set_axisbelow(True)

# --------------------------------------------
# DASHBOARD TITLE AND KPI HEADER
# --------------------------------------------

fig.suptitle(
    "WEATHER INTELLIGENCE & CLIMATE ANALYTICS",
    fontsize=18,
    fontweight="bold",
    color=TEXT_COLOR,
    y=0.98
)

fig.text(
    0.5,
    0.935,
    (
        f"2025 Overview  |  "
        f"Avg Temp: {average_temperature:.1f} °C  |  "
        f"Total Rainfall: {total_rainfall:.1f} mm  |  "
        f"Rainy Days: {rainy_days}  |  "
        f"Temperature Anomalies: {len(anomalies)}"
    ),
    ha="center",
    fontsize=10,
    color=TEAL_COLOR
)

# Improve spacing
fig.tight_layout(rect=[0.02, 0.02, 0.98, 0.90])

# --------------------------------------------
# SAVE DASHBOARD IMAGE
# --------------------------------------------

dashboard_file = OUTPUT_DIR / "climate_dashboard.png"

fig.savefig(
    dashboard_file,
    dpi=300,
    facecolor=fig.get_facecolor(),
    bbox_inches="tight"
)

print(f"\nDashboard saved to: {dashboard_file}")
print(f"File exists: {dashboard_file.exists()}")

# Display dashboard
plt.show()

print("\nClimate dashboard created successfully!")


# ============================================
# CODE 9: AUTOMATED CLIMATE INSIGHTS REPORT
# ============================================

print("\n" + "=" * 60)
print("GENERATING AUTOMATED CLIMATE REPORT")
print("=" * 60)

# --------------------------------------------
# 1. IDENTIFY KEY MONTHLY INSIGHTS
# --------------------------------------------

hottest_month_row = monthly_summary.loc[
    monthly_summary["Average_Temperature"].idxmax()
]

coolest_month_row = monthly_summary.loc[
    monthly_summary["Average_Temperature"].idxmin()
]

wettest_month_row = monthly_summary.loc[
    monthly_summary["Total_Rainfall"].idxmax()
]

# --------------------------------------------
# 2. CALCULATE ADDITIONAL INSIGHTS
# --------------------------------------------

high_humidity_days = int(
    humidity_counts.get("High", 0)
)

heavy_rain_days = int(
    rainfall_counts.get("Heavy Rain", 0)
)

temperature_anomaly_days = len(anomalies)

# --------------------------------------------
# 3. CREATE REPORT CONTENT
# --------------------------------------------

report_lines = [
    "=" * 65,
    "WEATHER INTELLIGENCE & CLIMATE ANALYTICS SYSTEM",
    "AUTOMATED CLIMATE INSIGHTS REPORT",
    "=" * 65,
    "",
    "1. DATASET OVERVIEW",
    "-" * 45,
    f"Analysis period: {weather_data['Date'].min():%d %B %Y} "
    f"to {weather_data['Date'].max():%d %B %Y}",
    f"Total observations: {len(weather_data)}",
    f"Total weather variables: 6 original measurements",
    "",
    "2. OVERALL CLIMATE PERFORMANCE",
    "-" * 45,
    f"Average temperature: {average_temperature:.2f} °C",
    f"Maximum temperature: {maximum_temperature:.2f} °C",
    f"Minimum temperature: {minimum_temperature:.2f} °C",
    f"Average humidity: {average_humidity:.2f}%",
    f"Total rainfall: {total_rainfall:.2f} mm",
    f"Average wind speed: {average_wind_speed:.2f} km/h",
    f"Average air pressure: {average_pressure:.2f} hPa",
    f"Rainy days: {rainy_days}",
    "",
    "3. MONTHLY CLIMATE INSIGHTS",
    "-" * 45,
    f"Hottest month: {hottest_month_row['Month_Name']} "
    f"({hottest_month_row['Average_Temperature']:.2f} °C)",
    f"Coolest month: {coolest_month_row['Month_Name']} "
    f"({coolest_month_row['Average_Temperature']:.2f} °C)",
    f"Wettest month: {wettest_month_row['Month_Name']} "
    f"({wettest_month_row['Total_Rainfall']:.2f} mm)",
    "",
    "4. HUMIDITY AND RAINFALL PATTERNS",
    "-" * 45,
    f"High humidity days: {high_humidity_days}",
    f"Heavy rainfall days: {heavy_rain_days}",
    f"Dry days: {rainfall_counts.get('Dry', 0)}",
    "",
    "5. TEMPERATURE ANOMALY ANALYSIS",
    "-" * 45,
    f"Unusual temperature days: {temperature_anomaly_days}",
    f"Anomaly percentage: {anomaly_percentage:.2f}%",
    "Detection method: Absolute Z-score greater than 2",
    "",
    "6. KEY OBSERVATIONS",
    "-" * 45,
    f"The highest monthly average temperature occurred in "
    f"{hottest_month_row['Month_Name']}.",
    f"The lowest monthly average temperature occurred in "
    f"{coolest_month_row['Month_Name']}.",
    f"The greatest monthly rainfall occurred in "
    f"{wettest_month_row['Month_Name']}.",
    f"{temperature_anomaly_days} temperature observations "
    f"were flagged for further review.",
    "",
    "7. PROJECT METHODOLOGY",
    "-" * 45,
    "Libraries used: Pandas, NumPy, Matplotlib and Python built-ins.",
    "Data source: Synthetic weather data generated with NumPy.",
    "Analysis: Statistical summaries, monthly aggregation,",
    "classification and Z-score-based anomaly screening.",
    "",
    "=" * 65,
    "END OF AUTOMATED CLIMATE REPORT",
    "=" * 65
]

# Join all lines into one report
climate_report = "\n".join(report_lines)

# --------------------------------------------
# 4. SAVE REPORT AS A TEXT FILE
# --------------------------------------------

report_file = OUTPUT_DIR / "climate_insights_report.txt"

with open(report_file, "w", encoding="utf-8") as file:
    file.write(climate_report)

# --------------------------------------------
# 5. DISPLAY REPORT STATUS
# --------------------------------------------

print(f"\nReport saved to: {report_file}")
print(f"Report file exists: {report_file.exists()}")

print("\nAutomated climate report generated successfully!")

# Display the report in the terminal
print("\n")
print(climate_report)


# ============================================
# CODE 10: FINAL PROJECT VALIDATION
# ============================================

print("\n" + "=" * 65)
print("FINAL PROJECT VALIDATION")
print("=" * 65)

# --------------------------------------------
# 1. DEFINE PROJECT OUTPUT FILES
# --------------------------------------------

required_files = {
    "Daily Weather Dataset": OUTPUT_DIR / "weather_data.csv",
    "Monthly Climate Summary": OUTPUT_DIR / "monthly_summary.csv",
    "Temperature Anomaly Report": OUTPUT_DIR / "temperature_anomalies.csv",
    "Climate Dashboard": OUTPUT_DIR / "climate_dashboard.png",
    "Automated Insights Report": OUTPUT_DIR / "climate_insights_report.txt"
}

# --------------------------------------------
# 2. VERIFY OUTPUT FILES
# --------------------------------------------

print("\nOUTPUT FILE VERIFICATION")
print("-" * 65)

successful_files = 0

for file_name, file_path in required_files.items():

    if file_path.exists() and file_path.stat().st_size > 0:
        print(f"[PASS] {file_name}")
        successful_files += 1
    else:
        print(f"[FAIL] {file_name}")

# --------------------------------------------
# 3. VERIFY DATASET
# --------------------------------------------

print("\nDATASET VALIDATION")
print("-" * 65)

dataset_valid = (
    len(weather_data) == 365
    and len(monthly_summary) == 12
    and weather_data["Date"].is_unique
    and weather_data.isnull().sum().sum() == 0
)

print(f"Daily records: {len(weather_data)}")
print(f"Monthly records: {len(monthly_summary)}")
print(f"Temperature anomalies: {len(anomalies)}")

if dataset_valid:
    print("[PASS] Dataset validation successful")
else:
    print("[FAIL] Dataset validation needs attention")

# --------------------------------------------
# 4. FINAL PROJECT STATUS
# --------------------------------------------

total_files = len(required_files)

print("\n" + "=" * 65)
print("PROJECT COMPLETION SUMMARY")
print("=" * 65)

print(f"Output files verified: {successful_files}/{total_files}")

if successful_files == total_files and dataset_valid:

    print("\nSTATUS: PROJECT COMPLETED SUCCESSFULLY")

    print("\nYour Weather Intelligence & Climate Analytics System")
    print("has successfully completed all development stages.")

else:

    print("\nSTATUS: PROJECT NEEDS ATTENTION")
    print("Please review the failed validation checks.")

print("\nPROJECT TECHNOLOGY STACK")
print("-" * 65)
print("Python       : Core programming")
print("Pandas       : Data cleaning and analysis")
print("NumPy        : Numerical calculations and data generation")
print("Matplotlib   : Climate visualization")
print("Built-ins    : File and folder management")

print("\nPROJECT FEATURES")
print("-" * 65)
print("[OK] Synthetic weather data generation")
print("[OK] Data quality validation")
print("[OK] Climate KPI calculations")
print("[OK] Monthly weather analysis")
print("[OK] Temperature anomaly detection")
print("[OK] Professional climate charts")
print("[OK] CSV report exports")
print("[OK] Climate dashboard")
print("[OK] Automated insights report")

print("\n" + "=" * 65)
print("END OF PROJECT")
print("=" * 65)
