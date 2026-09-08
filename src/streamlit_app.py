import streamlit as st
import pandas as pd
import os

from validation import validate_customer
from duplicate import find_similar_customers
from llm import analyze_duplicate
from data_loader import load_customer_master
from audit_logger import save_review_decision


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Master Data AI",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "validation_result" not in st.session_state:
    st.session_state.validation_result = None

if "similar_customers" not in st.session_state:
    st.session_state.similar_customers = []

if "ai_analysis" not in st.session_state:
    st.session_state.ai_analysis = None

if "review_decision" not in st.session_state:
    st.session_state.review_decision = None


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🤖 Customer Master Data AI Assistant")

st.write(
    "Validate customer master data, detect potential duplicates, "
    "and generate an AI-assisted review recommendation."
)


# --------------------------------------------------
# Customer Information
# --------------------------------------------------

st.subheader("Customer Information")

customer_name = st.text_input(
    "Customer Name",
    value="ABC Distribution LLC"
)

country = st.text_input(
    "Country",
    value="USA"
)

city = st.text_input(
    "City",
    value="Chicago"
)

postal_code = st.text_input(
    "Postal Code",
    value="60601"
)

customer_type = st.selectbox(
    "Customer Type",
    [
        "Distributor",
        "Retailer",
        "Wholesaler"
    ]
)

sales_organization = st.text_input(
    "Sales Organization",
    value="US01"
)


# --------------------------------------------------
# Existing Customer Master Data
# --------------------------------------------------

existing_customers = load_customer_master()


# --------------------------------------------------
# Build Customer Record
# --------------------------------------------------

customer = {
    "customer_name": customer_name,
    "country": country,
    "city": city,
    "postal_code": postal_code,
    "customer_type": customer_type,
    "sales_organization": sales_organization
}


# --------------------------------------------------
# Validate Customer
# --------------------------------------------------

if st.button("🔍 Validate Customer"):

    # Clear previous results
    st.session_state.validation_result = None
    st.session_state.similar_customers = []
    st.session_state.ai_analysis = None
    st.session_state.review_decision = None

    # ----------------------------------------------
    # Step 1: Data Validation
    # ----------------------------------------------

    validation_result = validate_customer(customer)

    # Save result
    st.session_state.validation_result = validation_result

    # ----------------------------------------------
    # Step 2: Duplicate Detection
    # ----------------------------------------------

    if validation_result["status"] == "PASSED":

        similar_customers = find_similar_customers(
            customer,
            existing_customers
        )

        # Save duplicate results
        st.session_state.similar_customers = similar_customers

        # ------------------------------------------
        # Step 3: AI Analysis
        # ------------------------------------------

        if similar_customers:

            with st.spinner(
                "Qwen is analyzing the potential duplicate..."
            ):

                ai_analysis = analyze_duplicate(
                    customer,
                    similar_customers
                )

            # Save AI result
            st.session_state.ai_analysis = ai_analysis


# ==================================================
# DISPLAY RESULTS
# ==================================================

if st.session_state.validation_result is not None:

    st.divider()

    # ----------------------------------------------
    # Step 1: Data Validation
    # ----------------------------------------------

    st.subheader("1. Data Validation")

    validation_result = st.session_state.validation_result

    if validation_result["status"] == "PASSED":

        st.success("Validation PASSED")

    else:

        st.error("Validation FAILED")

        for error in validation_result["errors"]:
            st.write(f"❌ {error}")


    # ----------------------------------------------
    # Continue only if validation passed
    # ----------------------------------------------

    if validation_result["status"] == "PASSED":

        # ------------------------------------------
        # Step 2: Duplicate Detection
        # ------------------------------------------

        st.subheader("2. Duplicate Detection")

        similar_customers = st.session_state.similar_customers

        if similar_customers:

            for match in similar_customers:

                st.warning(
                    f"Potential duplicate: "
                    f"{match['customer_name']} "
                    f"({match['similarity']}% similarity)"
                )

                # ------------------------------------------
                # Risk, Confidence and Recommendation
                # ------------------------------------------

                risk = match["risk"]

                confidence = match.get(
                    "confidence",
                    match["similarity"]
                )

                if risk == "HIGH":

                    recommendation = (
                        "Likely Duplicate – Manual Review Required"
                    )

                elif risk == "MEDIUM":

                    recommendation = (
                        "Possible Duplicate – Further Investigation Recommended"
                    )

                else:

                    recommendation = (
                        "Low Duplicate Probability – Likely New Customer"
                    )

                # ------------------------------------------
                # Display Risk and Confidence
                # ------------------------------------------

                metric1, metric2 = st.columns(2)

                metric1.metric(
                    "Risk Level",
                    risk
                )

                metric2.metric(
                    "Duplicate Detection Confidence",
                    f"{confidence}%"
                )

                # ------------------------------------------
                # AI Recommendation
                # ------------------------------------------

                st.write("### 🤖 AI Recommendation")

                if risk == "HIGH":

                    st.error(
                        f"🔴 {recommendation}"
                    )

                elif risk == "MEDIUM":

                    st.warning(
                        f"🟡 {recommendation}"
                    )

                else:

                    st.success(
                        f"🟢 {recommendation}"
                    )

                # ------------------------------------------
                # Match Evidence
                # ------------------------------------------

                st.write("### Match Evidence")

                st.write(
                    f"- Name similarity: "
                    f"{match['name_similarity']}%"
                )

                st.write(
                    f"- City match: "
                    f"{'Yes' if match['city_match'] else 'No'}"
                )

                st.write(
                    f"- Country match: "
                    f"{'Yes' if match['country_match'] else 'No'}"
                )

                st.write(
                    f"- Postal code match: "
                    f"{'Yes' if match['postal_match'] else 'No'}"
                )

                st.write(
                    f"- Customer type match: "
                    f"{'Yes' if match['customer_type_match'] else 'No'}"
                )

                st.write(
                    f"- Sales organization match: "
                    f"{'Yes' if match['sales_org_match'] else 'No'}"
                )


            # --------------------------------------
            # Step 3: AI Duplicate Analysis
            # --------------------------------------

            st.subheader("3. AI Duplicate Analysis")

            if st.session_state.ai_analysis:

                st.info(
                    st.session_state.ai_analysis
                )


            # --------------------------------------
            # Step 4: MDM Reviewer Decision
            # --------------------------------------

            st.subheader("4. MDM Reviewer Decision")

            st.write(
                "The AI recommendation is advisory. "
                "The Master Data reviewer makes the final decision."
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                if st.button(
                    "✅ Confirm Duplicate",
                    key="confirm_duplicate"
                ):

                    st.session_state.review_decision = (
                        "Duplicate Confirmed"
                    )

                    save_review_decision(
                        customer,
                        similar_customers[0],
                        "Duplicate Confirmed"
                    )

            
            
            with col2:

                if st.button(
                    "❌ Not a Duplicate",
                    key="not_duplicate"
                ):

                    st.session_state.review_decision = (
                        "Not a Duplicate"
                    )

                    save_review_decision(
                        customer,
                        similar_customers[0],
                        "Not a Duplicate"
                    )
            with col3:

                if st.button(
                    "🔎 Further Investigation",
                    key="further_investigation"
                ):

                    st.session_state.review_decision = (
                        "Further Investigation"
                    )

                    save_review_decision(
                        customer,
                        similar_customers[0],
                        "Further Investigation"
                    )   

            # --------------------------------------
            # Display Reviewer Decision
            # --------------------------------------

            if st.session_state.review_decision:

                decision = st.session_state.review_decision

                if decision == "Duplicate Confirmed":

                    st.error(
                        "🔴 Review Decision: "
                        "Duplicate Confirmed"
                    )

                elif decision == "Not a Duplicate":

                    st.success(
                        "🟢 Review Decision: "
                        "Not a Duplicate"
                    )

                elif decision == "Further Investigation":

                    st.warning(
                        "🟡 Review Decision: "
                        "Further Investigation"
                    )


        else:

            st.success(
                "No potential duplicate customers found."
            )
