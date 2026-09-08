import streamlit as st
import pandas as pd
import os

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Review History",
    page_icon="📋",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📋 Review History")

st.write(
    "Search and review previous Master Data duplicate decisions."
)

st.divider()

# --------------------------------------------------
# File Path
# --------------------------------------------------

file_path = "data/review_decisions.csv"

# --------------------------------------------------
# Check File
# --------------------------------------------------

if not os.path.exists(file_path):

    st.warning("⚠️ No review history file found.")

else:

    df = pd.read_csv(file_path)

    # --------------------------------------------------
    # Check if file has records
    # --------------------------------------------------

    if df.empty:

        st.warning("⚠️ No review records available yet.")

    else:

        # --------------------------------------------------
        # Search Customer Name
        # --------------------------------------------------

        search_customer = st.text_input(
            "🔍 Search Customer Name"
        )

        filtered_df = df.copy()

        if search_customer:

            filtered_df = filtered_df[
                filtered_df["customer_name"]
                .astype(str)
                .str.contains(
                    search_customer,
                    case=False,
                    na=False
                )
            ]

        # --------------------------------------------------
        # Filter Risk Level
        # --------------------------------------------------

        if "risk" in filtered_df.columns:

            risk_options = sorted(
                filtered_df["risk"]
                .dropna()
                .unique()
            )

            selected_risks = st.multiselect(
                "Filter by Risk Level",
                options=risk_options
            )

            if selected_risks:

                filtered_df = filtered_df[
                    filtered_df["risk"].isin(
                        selected_risks
                    )
                ]

        # --------------------------------------------------
        # Filter Reviewer Decision
        # --------------------------------------------------

        if "review_decision" in filtered_df.columns:

            decision_options = sorted(
                filtered_df["review_decision"]
                .dropna()
                .unique()
            )

            selected_decisions = st.multiselect(
                "Filter by Reviewer Decision",
                options=decision_options
            )

            if selected_decisions:

                filtered_df = filtered_df[
                    filtered_df["review_decision"].isin(
                        selected_decisions
                    )
                ]

        # --------------------------------------------------
        # Show Results
        # --------------------------------------------------

        st.write(
            f"### Showing {len(filtered_df)} review record(s)"
        )

        st.dataframe(
            filtered_df,
            use_container_width=True
        )

        # --------------------------------------------------
        # Download Filtered Audit Report
        # --------------------------------------------------

        csv_data = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Audit Report",
            data=csv_data,
            file_name="review_history_report.csv",
            mime="text/csv"
        )