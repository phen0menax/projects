import streamlit as st
import pandas as pd

# Load the data from the text file
@st.cache_data
def load_data():
    df = pd.read_csv("data.txt")
    df.columns = df.columns.str.strip()
    return df

def reset_filters():
    # Clear the session state keys for each widget
    for key in ["ext", "comp", "tube", "rod"]:
        st.session_state[key] = "All"

def main():
    st.set_page_config(page_title="Stabilus Gas Spring Reference", layout="wide")
    st.title("Stabilus Universal Specification Reference")
    
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("Data file 'data.txt' not found.")
        return

    # Sidebar for filters
    st.sidebar.header("Filter Specifications")
    
    # Reset button triggers the function to clear session state
    st.sidebar.button("Reset All Filters", on_click=reset_filters)
    st.sidebar.markdown("---")

    # 1. Extended Length Filter (A to B) [cite: 7]
    ext_options = ["All"] + sorted(df['Extended Length (in.)'].unique().tolist())
    selected_ext = st.sidebar.selectbox("Extended Length (in.)", options=ext_options, key="ext")

    # 2. Compressed Length Filter [cite: 9]
    comp_options = ["All"] + sorted(df['Compressed Length (in)'].unique().tolist())
    selected_comp = st.sidebar.selectbox("Compressed Length (in)", options=comp_options, key="comp")

    # 3. Tube End Fitting Filter [cite: 25, 33]
    tube_options = ["All"] + sorted(df['Tube End Fitting'].unique().astype(str).tolist())
    selected_tube = st.sidebar.selectbox("Tube End Fitting", options=tube_options, key="tube")

    # 4. Rod End Fitting Filter [cite: 25, 33]
    rod_options = ["All"] + sorted(df['Rod End Fitting'].unique().astype(str).tolist())
    selected_rod = st.sidebar.selectbox("Rod End Fitting", options=rod_options, key="rod")

    # Apply Filters logic
    filtered_df = df.copy()
    if selected_ext != "All":
        filtered_df = filtered_df[filtered_df['Extended Length (in.)'] == selected_ext]
    if selected_comp != "All":
        filtered_df = filtered_df[filtered_df['Compressed Length (in)'] == selected_comp]
    if selected_tube != "All":
        filtered_df = filtered_df[filtered_df['Tube End Fitting'] == selected_tube]
    if selected_rod != "All":
        filtered_df = filtered_df[filtered_df['Rod End Fitting'] == selected_rod]

    # Display Results
    st.subheader(f"Matching Results ({len(filtered_df)})")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # Technical Reminders from Documentation
    st.divider()
    st.info("💡 **Measurement Tip**: Measure your existing gas spring from center to center of attachment points when fully extended[cite: 7, 13].")
    st.warning("⚠️ **Safety**: Always replace gas springs in pairs if two are used in the application[cite: 18, 19].")

if __name__ == "__main__":
    main()