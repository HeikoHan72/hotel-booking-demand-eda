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
* **Visualization**: Generating an interactive choropleth world map (`plotly.express`) featuring dynamic hover data.
* **Business Value**: Identifying core target markets for optimized, region-specific marketing campaigns.

🔗 **[👉 Click here to open the Interactive World Map (HTML)](./globale_verteilung.html)**
*(Note: Click the link above to view and interact with the dynamic guest distribution map directly in your browser)*

### 2. Cancellation Analysis by Hotel Type
* **Methodology**: Constructing cross-tabulations to calculate the exact cancellation rates for both *City Hotels* and *Resort Hotels*.
* **Visualization**: Deploying a high-resolution `countplot` for a direct visual comparison of checked-in vs. canceled bookings.
* **Business Value**: Revealing variations in booking risks depending on the specific hotel category.

🔗 **[👉 Click here to open the Interactive Target Group Analysis (HTML)](./zielgruppen_analyse.html)**
*(Note: Click the link above to explore the interactive target group breakdown)*

### 3. Impact of Lead Time on Cancellations
* **Methodology**: Aggregating key statistical metrics (mean, median, standard deviation, maximum) of the `lead_time` feature, segmented by booking status.
* **Visualization**: Utilizing a Kernel Density Estimate plot (`kdeplot`) to evaluate whether long-term bookings exhibit a higher probability of cancellation.
* **Business Value**: Optimizing overbooking models, dynamic pricing strategies, and cancellation policies.

#### Lead Time Density Distribution Plot:
![Lead Time Density Distribution](./vor%20Laufzeit_verteilung.png)

---

## 🚀 Repository Structure

* `EDA - Hotel Bookings Demand.py` – The complete, modularized Python script.
* `globale_verteilung.html` – Interactive global guest distribution map (Plotly HTML).
* `zielgruppen_analyse.html` – Interactive target group cancellation analysis (Plotly HTML).
* `vor Laufzeit_verteilung.png` – Static density distribution plot (Seaborn PNG).
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
3. Execute the `EDA - Hotel Bookings Demand.py` script inside Spyder or your preferred Python IDE.
