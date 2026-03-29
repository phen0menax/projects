import streamlit as st
import pandas as pd

# 1. Load the data
data = {
    "Fraction": [
        '1/16"',
        '1/8"',
        '3/16"',
        '1/4"',
        '5/16"',
        '3/8"',
        '7/16"',
        '1/2"',
        '9/16"',
        '5/8"',
        '11/16"',
        '3/4"',
        '13/16"',
        '7/8"',
        '15/16"',
        '1"',
    ],
    "Decimal": [
        0.0625,
        0.125,
        0.1875,
        0.25,
        0.3125,
        0.375,
        0.4375,
        0.5,
        0.5625,
        0.625,
        0.6875,
        0.75,
        0.8125,
        0.875,
        0.9375,
        1.0,
    ],
    "Millimeters": [
        1.5875,
        3.175,
        4.7625,
        6.35,
        7.9375,
        9.525,
        11.1125,
        12.7,
        14.2875,
        15.875,
        17.4625,
        19.05,
        20.6375,
        22.225,
        23.8125,
        25.4,
    ],
}
df = pd.DataFrame(data)

# 2. Initialize History in Session State
if "history" not in st.session_state:
    st.session_state.history = []

# --- Sidebar: History & Settings ---
st.sidebar.title("Settings & History")

# Tolerance Adjustment (Default 0.9, +/- 0.5 range)
tolerance = st.sidebar.slider(
    "Tolerance (mm):", min_value=0.4, max_value=1.4, value=0.9, step=0.1
)

st.sidebar.markdown("---")
st.sidebar.subheader("Recent Lookups")
if st.session_state.history:
    for item in reversed(st.session_state.history[-5:]):  # Show last 5
        st.sidebar.write(item)
else:
    st.sidebar.info("No lookups yet.")

if st.sidebar.button("Clear History"):
    st.session_state.history = []
    st.rerun()

# --- Main UI ---
st.title("📏 Smart Fraction & Metric Lookup")

tab1, tab2 = st.tabs(["Search by Fraction", "Find Closest Inch (Metric Input)"])

with tab1:
    search_query = st.text_input("Enter Fraction (e.g., 1/4):", key="frac_search")
    if search_query:
        results = df[df["Fraction"].str.contains(search_query, case=False)]
        st.dataframe(results, hide_index=True)
    else:
        st.dataframe(df, hide_index=True, use_container_width=True, height=598)

with tab2:
    st.subheader("Closest Inch Match")

    unit = st.radio(
        "Input Unit:", ("Millimeters (mm)", "Centimeters (cm)"), horizontal=True
    )
    user_val = st.number_input(
        f"Enter value in {unit}:", min_value=0.0, step=0.1, key="metric_input"
    )

    if user_val > 0:
        target_mm = user_val * 10 if "Centimeters" in unit else user_val

        # Calculate difference
        df["difference"] = (df["Millimeters"] - target_mm).abs()
        within_tolerance = df[df["difference"] <= tolerance].copy()

        if not within_tolerance.empty:
            closest_row = within_tolerance.loc[within_tolerance["difference"].idxmin()]

            # Display Results
            st.success(f"Match found within {tolerance} mm!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Fraction", closest_row["Fraction"])
            c2.metric("Decimal", f"{closest_row['Decimal']}\"")
            c3.metric("Table MM", f"{closest_row['Millimeters']} mm")

            # Update History
            history_entry = f"**{user_val}{'cm' if 'Cent' in unit else 'mm'}** → {closest_row['Fraction']}"
            if (
                not st.session_state.history
                or st.session_state.history[-1] != history_entry
            ):
                st.session_state.history.append(history_entry)
        else:
            st.error(f"No match found within {tolerance} mm.")
