import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# PAGE SETTINGS 
st.set_page_config(page_title="CSV Analyzer", layout="wide")

#  TITLE
st.title("📊 CSV Analyzer")
st.subheader("Upload your CSV file and analyze data easily")
st.write("Supported file type: CSV")

#  FILE UPLOAD
uploaded_file = st.file_uploader(
    "Browse CSV File",
    type=["csv"]
)

# Main app
if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Layout: Left = Main Area, Right = Stats Panel
    main_col, side_col = st.columns([3, 1])

   
    with main_col:

        st.success("File uploaded successfully!")

        # File Details
        st.write("## File Details")
        st.write("File Name:", uploaded_file.name)
        st.write("Rows:", df.shape[0])
        st.write("Columns:", df.shape[1])

        # Column Names
        st.write("## Column Names")
        st.write(list(df.columns))

        # Data Types
        st.write("## Data Types")
        st.write(df.dtypes)

        # Preview
        st.write("## Preview")
        st.dataframe(df.head())

        # Missing Values
        st.write("## Missing Values")
        missing_values = df.isnull().sum()
        st.write(missing_values)

        st.write("### Total Missing Values:", missing_values.sum())

        # Duplicate Rows
        st.write("## Duplicate Rows")
        duplicates = df.duplicated().sum()
        st.write(duplicates)

        if duplicates > 0:
            st.warning(f"{duplicates} duplicate rows found")
        else:
            st.success("No duplicate rows found")

       
        st.write("## Data Visualization")

        graph_column = st.selectbox(
            "Select Column for Graph",
            df.columns,
            key="graph_column"
        )

        graph_type = st.selectbox(
            "Select Graph Type",
            ["Bar Chart", "Line Chart", "Histogram"],
            key="graph_type"
        )

        # Bar Chart
        if graph_type == "Bar Chart":

            counts = df[graph_column].value_counts()

            x_vals = counts.index.astype(str).tolist()
            y_vals = counts.tolist()

            fig, ax = plt.subplots(figsize=(4,2))
            ax.bar(x_vals, y_vals)

            ax.set_xlabel(graph_column, fontsize=9)
            ax.set_ylabel("Count")
            ax.set_title(f"Bar Chart of {graph_column}")

            plt.xticks(rotation=20,fontsize=4)
            plt.yticks(fontsize=8)
            st.pyplot(fig)

        # Line Chart
        elif graph_type == "Line Chart":

            if pd.api.types.is_numeric_dtype(df[graph_column]):

                fig, ax = plt.subplots(figsize=(4,2))
                ax.plot(df.index, df[graph_column])

                ax.set_xlabel("Row Index")
                ax.set_ylabel(graph_column)
                ax.set_title(f"Line Chart of {graph_column}")

                st.pyplot(fig)

            else:
                st.warning("Line chart needs numeric column.")

        # Histogram
        elif graph_type == "Histogram":

            if pd.api.types.is_numeric_dtype(df[graph_column]):

                fig, ax = plt.subplots(figsize=(4,2))
                ax.hist(df[graph_column].dropna(), bins=10)

                ax.set_xlabel(graph_column)
                ax.set_ylabel("Frequency")
                ax.set_title(f"Histogram of {graph_column}")

                st.pyplot(fig)

            else:
                st.warning("Histogram needs numeric column.")

   
    with side_col:

        st.write("## Quick Stats")

        st.metric("Rows", df.shape[0])
        st.metric("Columns", df.shape[1])

        numeric_columns = df.select_dtypes(include=["number"]).columns

        if len(numeric_columns) > 0:

            selected_column = st.selectbox(
                "Stats Column",
                numeric_columns,
                key="stats_column"
            )

            st.metric("Mean", round(df[selected_column].mean(), 2))
            st.metric("Median", round(df[selected_column].median(), 2))
            st.metric("Mode", df[selected_column].mode()[0])
            st.metric("Min", df[selected_column].min())
            st.metric("Max", df[selected_column].max())
            st.metric("Std Dev", round(df[selected_column].std(), 2))

        else:
            st.warning("No numeric columns found.")
