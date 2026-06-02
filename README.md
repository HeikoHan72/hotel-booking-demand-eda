# Exploratory Data Analysis (EDA) – Hotel Bookings Demand

This project features a comprehensive and robust Exploratory Data Analysis (EDA) of a hotel booking dataset. The primary objective is to uncover business-critical patterns in booking behavior, compare cancellation rates, and analyze the impact of lead times to enable data-driven decision-making for hotel management.

## 🛠️ Key Technical Competencies
* **Data Cleansing**: Professional handling of missing values and elimination of anomalous records (zero-guest bookings) using `pandas`.
* **Robust Path-Handling**: Seamless and platform-independent directory configuration utilizing `os.path`.
* **Advanced Visualizations**: Integration of interactive geospatial plots (`plotly`) alongside high-resolution statistical charts (`seaborn` & `matplotlib`).
* **Reporting**: Structured and clean tabular console outputs leveraging the `tabulate` library.

---

## 📈 Key Analyses & Insights

### 1. Global Guest Distribution & Origins
* **Methodology**: Analyzing the top 10 countries of origin based exclusively on effective, successful arrivals (`is_canceled == 0`).
* **Visualization**: Generating an interactive choropleth world map (`plotly.express`) featuring dynamic hover data (ISO code, absolute guest count, rank, and percentage share).
* **Business Value**: Identifying core target markets for optimized, region-specific marketing campaigns.

### 2. Cancellation Analysis by Hotel Type
* **Methodology**: Constructing cross-tabulations to calculate the exact cancellation rates for both *City Hotels* and *Resort Hotels*.
* **Visualization**: Deploying a high-resolution `countplot` for a direct visual comparison of checked-in vs. canceled bookings.
* **Business Value**: Revealing variations in booking risks depending on the specific hotel category.

### 3. Impact of Lead Time on Cancellations
* **Methodology**: Aggregating key statistical metrics (mean, median, standard deviation, maximum) of the `lead_time` feature, segmented by booking status.
* **Visualization**: Utilizing a Kernel Density Estimate plot (`kdeplot`) to evaluate whether long-term bookings exhibit a higher probability of cancellation.
* **Business Value**: Optimizing overbooking models, dynamic pricing strategies, and cancellation policies.

---

## 🚀 Repository Structure

* `hotel_bookings.csv` – The core input dataset.
* `hotel_analysis.py` – The complete, modularized Python script (structured into executable Spyder code cells `#%%`).
* `README.md` – This comprehensive project documentation.

## 💻 Installation & Usage

1. Clone this repository:
   ```bash
   git clone https://github.com
   ```
2. Install the required dependencies:
   ```bash
   pip install pandas matplotlib seaborn plotly tabulate
   ```
3. Execute the `hotel_analysis.py` script inside Spyder or your preferred Python IDE.
