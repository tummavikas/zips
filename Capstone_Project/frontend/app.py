import os
import requests
import streamlit as st

# =====================================================
# CONFIG
# =====================================================

API_URL = os.getenv(
    "API_BASE_URL",
    "http://localhost:8000"
).rstrip("/")

REQUEST_TIMEOUT = 30
LLM_TIMEOUT = 120

st.set_page_config(
    page_title="Vehicle Loan Advisor",
    page_icon="🚗",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.main{
    background:#f6f8fc;
}

.block-container{
    padding-top:1rem;
    max-width:1600px;
}

.hero-card{
    background:linear-gradient(135deg,#2563eb,#1e40af);
    color:white;
    padding:24px;
    border-radius:18px;
    margin-bottom:20px;
}

.form-card{
    background:white;
    padding:20px;
    border-radius:18px;
    border:1px solid #e5e7eb;
    margin-bottom:20px;
}

.vehicle-card{
    background:white;
    border-radius:18px;
    padding:18px;
    border:1px solid #e5e7eb;
    box-shadow:0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom:15px;
}

.approved{
    background:#ecfdf5;
    border-left:6px solid #10b981;
    padding:16px;
    border-radius:12px;
}

.rejected{
    background:#fef2f2;
    border-left:6px solid #ef4444;
    padding:16px;
    border-radius:12px;
}

.ai-panel{
    background:white;
    border-radius:18px;
    padding:15px;
    border:1px solid #e5e7eb;
}

div[data-testid="stMetric"]{
    background:white;
    border-radius:15px;
    padding:15px;
    box-shadow:0 2px 8px rgba(0,0,0,.05);
}

.stButton > button{
    width:100%;
    height:3rem;
    border-radius:12px;
    border:none;
    background:#2563eb;
    color:white;
    font-weight:600;
}

.stButton > button:hover{
    background:#1d4ed8;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# API FUNCTIONS
# =====================================================

def predict(applicant):
    response = requests.post(
        f"{API_URL}/predict",
        json=applicant,
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def get_loan_amount(applicant, decision):
    response = requests.post(
        f"{API_URL}/loan-amount",
        json={
            "applicant": applicant,
            "decision": decision
        },
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def get_vehicles(budget):
    response = requests.post(
        f"{API_URL}/vehicles",
        json={"budget": budget},
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def get_vehicle_detail(vehicle_id):
    response = requests.get(
        f"{API_URL}/vehicles/{vehicle_id}",
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def ask_policy(question):
    response = requests.post(
        f"{API_URL}/explain",
        json={"question": question},
        timeout=LLM_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="hero-card">
<h1>🚗 Intelligent Vehicle Loan Advisor</h1>
<p>
AI-powered loan eligibility assessment, vehicle recommendations,
policy search, and decision intelligence platform.
</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# LAYOUT
# =====================================================

left_col, right_col = st.columns([2.3, 1])

# =====================================================
# LEFT SIDE
# =====================================================

with left_col:

    st.markdown("## 👤 Applicant Information")

    with st.container():

        c1, c2 = st.columns(2)

        with c1:

            monthly_income = st.number_input(
                "Monthly Income (₹)",
                min_value=1000,
                value=85000,
                step=1000
            )

            credit_score = st.slider(
                "Credit Score",
                300,
                900,
                750
            )

            age = st.number_input(
                "Age",
                min_value=18,
                max_value=75,
                value=30
            )

            employment_type = st.selectbox(
                "Employment Type",
                [
                    "salaried",
                    "self_employed"
                ]
            )

        with c2:

            employment_years = st.number_input(
                "Employment Experience",
                min_value=0.0,
                value=5.0,
                step=0.5
            )

            existing_emis = st.number_input(
                "Existing EMI (₹)",
                min_value=0,
                value=10000
            )

            requested_loan_amount = st.number_input(
                "Requested Loan Amount (₹)",
                min_value=10000,
                value=800000,
                step=10000
            )

            down_payment = st.number_input(
                "Down Payment (₹)",
                min_value=0,
                value=150000,
                step=10000
            )

    requested_tenure_months = st.select_slider(
        "Loan Tenure (Months)",
        options=[12, 24, 36, 48, 60, 72, 84],
        value=60
    )

    # =================================================
    # LIVE INDICATORS
    # =================================================

    foir = (
        existing_emis / monthly_income * 100
        if monthly_income > 0
        else 0
    )

    m1, m2 = st.columns(2)

    with m1:

        st.metric(
            "Current FOIR",
            f"{foir:.1f}%"
        )

        if foir <= 50:
            st.success("✅ Within Policy Limit")
        else:
            st.error("❌ Above FOIR Limit")

    with m2:

        if credit_score >= 750:
            st.success("🟢 Excellent Credit Profile")

        elif credit_score >= 700:
            st.info("🔵 Good Credit Profile")

        elif credit_score >= 650:
            st.warning("🟠 Average Credit Profile")

        else:
            st.error("🔴 High Risk Profile")

    evaluate = st.button(
        "🚀 Evaluate Eligibility",
        use_container_width=True
    )

    # =================================================
    # PREDICT
    # =================================================

    if evaluate:

        applicant = {
            "monthly_income": monthly_income,
            "credit_score": credit_score,
            "employment_years": employment_years,
            "employment_type": employment_type,
            "existing_emis": existing_emis,
            "requested_tenure_months": requested_tenure_months,
            "requested_loan_amount": requested_loan_amount,
            "down_payment": down_payment,
            "age": age
        }

        try:

            with st.spinner("Analyzing application..."):

                decision = predict(applicant)

                st.session_state["applicant"] = applicant
                st.session_state["decision"] = decision

                if decision["decision"] == "Approved":

                    amount = get_loan_amount(
                        applicant,
                        "Approved"
                    )

                    st.session_state["amount"] = amount

        except Exception as e:
            st.error(f"Prediction failed: {e}")

    # =================================================
    # RESULT DASHBOARD
    # =================================================

    if "decision" in st.session_state:

        decision = st.session_state["decision"]

        probability = float(
            decision.get(
                "model_probability",
                0
            )
        )

        st.markdown("---")
        st.markdown("## 📊 Decision Dashboard")

        if decision["decision"] == "Approved":

            st.markdown(
                f"""
                <div class="approved">
                <h3>✅ Loan Approved</h3>
                Approval Probability:
                <b>{probability:.1%}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="rejected">
                <h3>❌ Loan Rejected</h3>
                Approval Probability:
                <b>{probability:.1%}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.progress(probability)

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Approval",
            f"{probability:.0%}"
        )

        c2.metric(
            "Credit Score",
            st.session_state["applicant"]["credit_score"]
        )

        c3.metric(
            "FOIR",
            f"{foir:.1f}%"
        )

        c4.metric(
            "Income",
            f"₹{monthly_income:,.0f}"
        )

        # =============================================
        # APPROVED
        # =============================================

        if (
            decision["decision"] == "Approved"
            and "amount" in st.session_state
        ):

            amount = st.session_state["amount"]

            st.markdown("## 💰 Loan Summary")

            a1, a2, a3 = st.columns(3)

            a1.metric(
                "Sanction Amount",
                f"₹{amount['sanctioned_amount']:,.0f}"
            )

            a2.metric(
                "Monthly EMI",
                f"₹{amount['estimated_monthly_emi']:,.0f}"
            )

            a3.metric(
                "Vehicle Budget",
                f"₹{amount['total_vehicle_budget']:,.0f}"
            )

            with st.expander(
                "📖 Calculation Details"
            ):
                calc = amount.get(
                    "calculation",
                    []
                )

                if isinstance(calc, list):
                    for item in calc:
                        st.write("•", item)

            # =========================================
            # VEHICLES
            # =========================================

            st.markdown("## 🚘 Recommended Vehicles")

            try:

                vehicles = get_vehicles(
                    amount["total_vehicle_budget"]
                )

                if vehicles:

                    cols = st.columns(3)

                    for i, vehicle in enumerate(vehicles):

                        with cols[i % 3]:

                            st.markdown(
                                f"""
                                <div class="vehicle-card">
                                <h4>{vehicle['name']}</h4>
                                🚘 {vehicle.get('category','N/A')}<br>
                                ⛽ {vehicle.get('fuel_type','N/A')}<br>
                                💰 ₹{vehicle.get('on_road_price',0):,.0f}<br>
                                📅 EMI ₹{vehicle.get('estimated_emi',0):,.0f}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            if st.button(
                                "View Details",
                                key=f"vehicle_{vehicle['id']}"
                            ):

                                detail = get_vehicle_detail(
                                    vehicle["id"]
                                )

                                st.json(detail)

                else:
                    st.info(
                        "No vehicles found."
                    )

            except Exception as e:
                st.error(
                    f"Vehicle error: {e}"
                )

        else:

            st.markdown("## ❌ Rejection Reasons")

            reasons = decision.get(
                "reasons",
                []
            )

            if reasons:

                for reason in reasons:
                    st.error(reason)

# =====================================================
# RIGHT SIDE
# =====================================================

with right_col:

    st.markdown("## 🤖 AI Policy Assistant")

    st.info(
        "Ask about FOIR, EMI, credit score, policies, eligibility, or vehicles."
    )

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.markdown(
                msg["content"]
            )

    prompt = st.chat_input(
        "Ask a question..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            try:

                with st.spinner(
                    "Searching documents..."
                ):

                    result = ask_policy(
                        prompt
                    )

                answer = result.get(
                    "answer",
                    "No answer returned."
                )

                sources = result.get(
                    "sources",
                    []
                )

                st.markdown(answer)

                if sources:

                    with st.expander(
                        "📚 Sources"
                    ):

                        for src in sources:

                            st.markdown(
                                f"""
**Document:** {src.get('document','N/A')}

**Section:** {src.get('section','N/A')}

**Score:** {src.get('score',0):.2f}
"""
                            )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"Assistant error: {e}"
                )