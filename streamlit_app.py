import streamlit as st
from streamlit_option_menu import option_menu
from calculator import CarbonCalculator
import pandas as pd
import altair as alt
from fpdf import FPDF
import base64

# --- Helper Functions ---
def create_pdf(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(200, 20, txt="CarbonZero Report", ln=True, align='C')
    
    # Total Emissions
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"Total Monthly Emissions: {results['total']:.2f} kg CO2e", ln=True, align='L')
    pdf.ln(10)

    # Breakdown
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Emission Breakdown:", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    for category, emission in results['breakdown'].items():
        pdf.cell(200, 10, txt=f"- {category.title()}: {emission:.2f} kg CO2e", ln=True, align='L')
    pdf.ln(10)

    # Recommendations
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Recommendations:", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    recommendations = CarbonCalculator().get_recommendations(results['total'])
    if recommendations:
        for rec in recommendations:
            pdf.multi_cell(0, 10, txt=f"- {rec}")
    else:
        pdf.cell(200, 10, txt="Great job! Your emissions are low.", ln=True, align='L')

    return pdf.output(dest='S').encode('latin-1')

# --- Page Config ---
st.set_page_config(
    page_title="CarbonZero - Sustainability Calculator",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    /* Global Settings */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        font-size: 18px; /* Increased base font size */
    }
    
    /* Background & Main Container */
    .stApp {
        background-color: #f0f4f8;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #1b5e20;
        font-weight: 600;
    }
    
    h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 2.2rem;
        margin-top: 1.5rem;
    }
    
    h3 {
        font-size: 1.8rem;
    }
    
    /* Card-like Containers */
    .card {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2e7d32 0%, #43a047 100%);
        color: white;
        border: none;
        border-radius: 10px;
        height: 3.5em;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(46, 125, 50, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(46, 125, 50, 0.4);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Custom Highlights */
    .highlight-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #a5d6a7;
        text-align: center;
        margin: 2rem 0;
    }
    
    .metric-value {
        font-size: 3.5rem;
        font-weight: 700;
        color: #1b5e20;
    }
    
    .metric-label {
        font-size: 1.2rem;
        color: #388e3c;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
</style>
""", unsafe_allow_html=True)

# --- Initialize Calculator ---
calculator = CarbonCalculator()

# --- Navigation (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913465.png", width=100) # Optional placeholder logo
    selected = option_menu(
        menu_title="CarbonZero",
        options=["Home", "About", "Contact"],
        icons=["house", "info-circle", "envelope"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#2e7d32", "font-size": "20px"}, 
            "nav-link": {"font-size": "18px", "text-align": "left", "margin":"5px", "--hover-color": "#e8f5e9"},
            "nav-link-selected": {"background-color": "#2e7d32"},
        }
    )

# --- Home / Calculator ---
if selected == "Home":
    # st.container()  # Use container for logical grouping if needed, or just let flow naturally
    with st.container(border=True):
        st.title("🌱 CarbonZero Calculator")
        st.markdown("### Calculate Your Carbon Footprint")
        st.write("Discover your impact on the planet and find ways to reduce it.")

    with st.form("emission_form"):
        # Transport
        st.subheader("🚗 Transportation")
        col1, col2 = st.columns(2)
        with col1:
            transport_mode = st.selectbox(
                "Primary Mode of Transport",
                ["car_petrol", "car_diesel", "bus", "train", "flight"],
                format_func=lambda x: x.replace("_", " ").title()
            )
        with col2:
            distance = st.number_input("Distance Travelled (km/month)", min_value=0.0, step=10.0)
        
        st.divider()

        # Electricity
        st.subheader("⚡ Electricity")
        electricity_usage = st.number_input("Monthly Usage (kWh)", min_value=0.0, step=10.0)

        st.divider()

        # Diet
        st.subheader("🍽️ Diet")
        diet_type = st.selectbox(
            "Dietary Preference",
            ["heavy_meat", "medium_meat", "low_meat", "vegetarian", "vegan"],
            format_func=lambda x: x.replace("_", " ").title()
        )

        st.divider()

        # Fuel
        st.subheader("🔥 Fuel Usage")
        col3, col4 = st.columns(2)
        with col3:
            fuel_type = st.selectbox(
                "Fuel Type",
                ["lpg", "natural_gas", "coal"],
                format_func=lambda x: x.replace("_", " ").title()
            )
        with col4:
            fuel_usage = st.number_input("Usage (kg or m³/month)", min_value=0.0, step=1.0)
        
        # Calculate Button
        submitted = st.form_submit_button("Calculate Emissions")

    if submitted:
        # Prepare data
        data = {
            "transport_mode": transport_mode,
            "distance": distance,
            "electricity": electricity_usage,
            "diet": diet_type,
            "fuel_type": fuel_type,
            "lpg": fuel_usage
        }

        # Calculate
        result = calculator.calculate(data)
        
        st.markdown("---")
        st.header("🌍 Your Environmental Impact")
        
        # Display Total
        st.markdown(f"""
        <div class="highlight-box">
            <div class="metric-label">Total Monthly Emissions</div>
            <div class="metric-value">{result['total']:.2f} <span style="font-size: 1.5rem">kg CO₂e</span></div>
        </div>
        """, unsafe_allow_html=True)

        col_chart, col_recs = st.columns([1, 1])
        
        with col_chart:
            with st.container(border=True):
                st.markdown("### Emission Breakdown")
                # Charts
                breakdown = result['breakdown']
                df = pd.DataFrame(list(breakdown.items()), columns=['Category', 'Emissions'])
                
                c = alt.Chart(df).mark_arc(innerRadius=60).encode(
                    theta=alt.Theta("Emissions", stack=True),
                    color=alt.Color("Category", scale=alt.Scale(scheme='greens')),
                    tooltip=["Category", "Emissions"]
                )
                st.altair_chart(c, use_container_width=True)

        with col_recs:
             with st.container(border=True):
                st.subheader("💡 Recommendations")
                recommendations = calculator.get_recommendations(result['total'])
                if recommendations:
                    for rec in recommendations:
                        st.info(rec)
                else:
                    st.success("Great job! Your emissions are relatively low.")

        # --- The Carbon Time Machine ---
        st.markdown("---")
        st.markdown("## ⏳ The Carbon Time Machine")
        st.write("If everyone lived like you, what would the world look like in 2050?")
        
        footprint_stats = calculator.get_ecological_footprint(result['total'])
        earths = footprint_stats['earths_needed']
        temp = footprint_stats['temp_rise']
        
        tm_col1, tm_col2, tm_col3 = st.columns(3)
        
        with tm_col1:
            st.metric(label="Earths Needed", value=f"{earths}x 🌍")
        
        with tm_col2:
            st.metric(label="2050 Temp Rise", value=f"+{temp}°C 🌡️", delta_color="inverse", delta=f"{temp-1.5:.1f}°C vs Target")
            
        with tm_col3:
             if earths <= 1:
                 st.success("✅ Sustainable! You are living within planetary boundaries.")
             elif earths <= 3:
                 st.warning("⚠️ Overshoot! We'd need more resources than Earth has.")
             else:
                 st.error("🚨 Critical! This lifestyle is highly unsustainable.")

        # Visual Progress Bar for Earths
        st.write("### Resource Consumption")
        st.progress(min(earths / 5, 1.0)) # Cap visual at 5 earths
        st.caption(f"You are using {earths}x the renewable resources Earth generates in a year.")
            
        # Download Report
        st.markdown("---")
        pdf_bytes = create_pdf(result)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_bytes,
            file_name="carbon_zero_report.pdf",
            mime="application/pdf"
        )

# --- About Page ---
elif selected == "About":
    with st.container(border=True):
        st.title("ℹ️ About CarbonZero")
        st.markdown("""
        ### Project Mission
        **CarbonZero** is designed to raise awareness about individual carbon footprints. We believe that understanding your impact is the first step towards a sustainable future.

        ### How It Works
        Our calculator uses standard emission factors to estimate your monthly CO₂e (Carbon Dioxide Equivalent) emissions based on:
        
        *   **🚗 Transport:** Car, bus, train, and flight data.
        *   **⚡ Electricity:** Household energy consumption.
        *   **🍽️ Diet:** Impact of different dietary choices.
        *   **🔥 Fuel:** LPG and other fuel sources.
        """)

# --- Contact Page ---
elif selected == "Contact":
    with st.container(border=True):
        st.title("📬 Contact Us")
        with st.form("contact_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            message = st.text_area("Message")
            
            submit_contact = st.form_submit_button("Send Message")
            if submit_contact:
                st.success("Thank you for your message! We will get back to you soon.")
                st.markdown(f"**Sent by:** {name} ({email})")

        st.markdown("---")
        st.markdown("Or email us directly at: [support@carbonzero.test](mailto:support@carbonzero.test)")
