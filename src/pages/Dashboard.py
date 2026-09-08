import streamlit as st
import pandas as pd
import os

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📊 Customer Master Data Dashboard")

st.write(
    "Overview of duplicate detection and Master Data review activity."
)

st.divider()

# --------------------------------------------------
# Load Review History
# --------------------------------------------------

file_path = "data/review_decisions.csv"

if not os.path.exists(file_path):

    st.warning("⚠️ No review history available yet.")

else:

    df = pd.read_csv(file_path)

    # --------------------------------------------------
    # Ensure Required Columns Exist
    # --------------------------------------------------

    if "review_decision" not in df.columns:
        df["review_decision"] = "Not Available"

    if "risk" not in df.columns:
        df["risk"] = "Not Available"

    # --------------------------------------------------
    # Dashboard Metrics
    # --------------------------------------------------

    total_reviews = len(df)

    high_risk = len(
        df[df["risk"] == "HIGH"]
    )

    medium_risk = len(
        df[df["risk"] == "MEDIUM"]
    )

    low_risk = len(
        df[df["risk"] == "LOW"]
    )

    # --------------------------------------------------
    # Display Metrics
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Reviews",
        total_reviews
    )

    col2.metric(
        "🔴 High Risk",
        high_risk
    )

    col3.metric(
        "🟡 Medium Risk",
        medium_risk
    )

    col4.metric(
        "🟢 Low Risk",
        low_risk
    )

    st.divider()

    # --------------------------------------------------
    # Reviewer Decisions
    # --------------------------------------------------

    st.subheader("👨‍💼 MDM Reviewer Decisions")

    decision_col1, decision_col2, decision_col3 = st.columns(3)

    duplicate_confirmed = len(
        df[df["review_decision"] == "Duplicate Confirmed"]
    )

    not_duplicate = len(
        df[df["review_decision"] == "Not a Duplicate"]
    )

    further_investigation = len(
        df[df["review_decision"] == "Further Investigation"]
    )

    decision_col1.metric(
        "✅ Duplicate Confirmed",
        duplicate_confirmed
    )

    decision_col2.metric(
        "❌ Not a Duplicate",
        not_duplicate
    )

    decision_col3.metric(
        "🔎 Further Investigation",
        further_investigation
    )

    st.divider()

    # ==================================================
    # DASHBOARD CHARTS
    # ==================================================

    st.subheader("📊 Duplicate Risk Distribution")

    risk_data = pd.DataFrame({
        "Risk Level": ["HIGH", "MEDIUM", "LOW"],
        "Reviews": [
            high_risk,
            medium_risk,
            low_risk
        ]
    })

    st.bar_chart(
        risk_data,
        x="Risk Level",
        y="Reviews"
    )

    st.divider()

    # --------------------------------------------------
    # Reviewer Decision Chart
    # --------------------------------------------------

    st.subheader("📊 Reviewer Decision Distribution")

    decision_data = pd.DataFrame({
        "Decision": [
            "Duplicate Confirmed",
            "Not a Duplicate",
            "Further Investigation"
        ],
        "Count": [
            duplicate_confirmed,
            not_duplicate,
            further_investigation
        ]
    })

    st.bar_chart(
        decision_data,
        x="Decision",
        y="Count"
    )

    st.divider()

    # --------------------------------------------------
    # Similarity Score Analysis
    # --------------------------------------------------

    st.subheader("📈 Similarity Score Analysis")

    if "similarity" in df.columns:

        similarity_df = df[
            ["customer_name", "similarity"]
        ].copy()

        similarity_df["similarity"] = pd.to_numeric(
            similarity_df["similarity"],
            errors="coerce"
        )

        similarity_df = similarity_df.dropna()

        if not similarity_df.empty:

            st.bar_chart(
                similarity_df,
                x="customer_name",
                y="similarity"
            )

        else:

            st.info(
                "No valid similarity score data available."
            )

    else:

        st.info(
            "Similarity score data is not available."
        )

    st.divider()

    # --------------------------------------------------
    # Recent Review Records
    # --------------------------------------------------

    st.subheader("📋 Recent Review Activity")

    st.dataframe(
        df.tail(10),
        use_container_width=True
    )