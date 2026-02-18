# 🌱 CarbonZero - Sustainability Calculator

**CarbonZero** is a modern, Python-based web application designed to help individuals estimate their monthly carbon footprint. Built with [Streamlit](https://streamlit.io/), it offers a seamless and interactive experience to calculate emissions from various sources and provides personalized recommendations for a sustainable lifestyle.

## 🚀 Features

-   **Comprehensive Calculator**: Estimate emissions from:
    -   🚗 **Transportation**: Car (Petrol/Diesel), Bus, Train, Flight.
    -   ⚡ **Electricity**: Household energy consumption.
    -   🍽️ **Diet**: Impact of dietary choices (Meat-heavy to Vegan).
    -   🔥 **Fuel**: Usage of LPG, Natural Gas, coal, etc.
-   **⏳ The Carbon Time Machine**:
    -   Visualize how many **Earths** would be needed if everyone lived like you.
    -   See a projection of global **Temperature Rise by 2050** based on your lifestyle.
-   **Interactive Visualizations**: View a dynamic breakdown of your carbon footprint with beautiful charts.
-   **Personalized Recommendations**: Get actionable tips to reduce your environmental impact based on your results.
-   **PDF Report**: Download a detailed PDF summary of your footprint and recommendations.
-   **Premium UI/UX**: clean, responsive interface with a modern aesthetic, dark/light mode optimization, and smooth interactions.

## 🛠️ Installation

1.  **Clone the repository** (or download the source code):
    ```bash
    git clone <repository-url>
    cd carbonzero
    ```

2.  **Install Dependencies**:
    Make sure you have Python installed. Then run:
    ```bash
    pip install streamlit pandas altair fpdf
    ```

## ▶️ Usage

1.  **Run the Application**:
    Navigate to the project directory and execute:
    ```bash
    streamlit run streamlit_app.py
    ```

2.  **Access the Calculator**:
    The application will open in your default web browser at `http://localhost:8501`.

## 📂 Project Structure

-   `streamlit_app.py`: The main application entry point containing the UI and interaction logic.
-   `calculator.py`: Core logic for carbon emission calculations.
-   `data/emission_factors.json`: Database of emission factors used for calculations.
-   `templates/` & `static/`: (Legacy) Files from the previous Flask implementation.
-   `.streamlit/config.toml`: Configuration for the custom visual theme.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the calculator or add new features.

---
*Built with ❤️ for a Greener Planet.*
