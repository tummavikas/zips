import html
import os

import requests
import streamlit as st

# =====================================================
# CONFIG
# =====================================================

API_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")

REQUEST_TIMEOUT = 30
LLM_TIMEOUT = 120
FOIR_LIMIT = 50

st.set_page_config(
    page_title="Vehicle Loan Advisor",
    page_icon="🚗",
    layout="wide",
)

# =====================================================
# STYLE
# Palette: paper #F2F4EF, ink #172421, forest #0E4F47,
#          amber #F2B632, brick #A63A2B
# Needs Streamlit >= 1.39 (container keys -> .st-key-* classes)
# =====================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

:root{
    --paper:#F2F4EF;
    --panel:#FFFFFF;
    --ink:#172421;
    --muted:#5B6A65;
    --line:#D5DAD0;
    --forest:#0E4F47;
    --forest-soft:#E1EDE8;
    --amber:#F2B632;
    --brick:#A63A2B;
    --brick-soft:#F6E4E0;
}

.stApp{ background:var(--paper); color:var(--ink); }
.stApp, .stApp p, .stApp label, .stApp button,
.stApp input, .stApp textarea, .stApp li{
    font-family:'IBM Plex Sans', system-ui, sans-serif;
}
.stApp h1, .stApp h2, .stApp h3, .stApp h4{
    font-family:'Bricolage Grotesque', 'IBM Plex Sans', sans-serif;
    color:var(--ink);
    letter-spacing:-0.01em;
}

.block-container{ max-width:1180px; padding-top:2rem; padding-bottom:7rem; }

/* ---------- masthead ---------- */
.masthead{ border-bottom:2px solid var(--ink); padding-bottom:14px; margin-bottom:28px; }
.wordmark{
    font-family:'Bricolage Grotesque', sans-serif;
    font-weight:700; font-size:2.1rem; line-height:1.1; color:var(--ink);
}
.tagline{ color:var(--muted); margin-top:6px; max-width:60ch; }

/* ---------- form group titles ---------- */
.group-title{
    font-family:'Bricolage Grotesque', sans-serif;
    font-weight:700; font-size:1.05rem; margin:0 0 6px 0;
    padding-bottom:6px; border-bottom:1px solid var(--line);
}

/* ---------- verdict ---------- */
.verdict{
    display:flex; align-items:center; gap:22px;
    padding:20px 24px; border-radius:6px; margin:6px 0 18px 0;
}
.verdict.approved{ background:var(--forest-soft); border-left:8px solid var(--forest); }
.verdict.rejected{ background:var(--brick-soft); border-left:8px solid var(--brick); }
.verdict-num{
    font-family:'Bricolage Grotesque', sans-serif;
    font-weight:700; font-size:3.4rem; line-height:1;
}
.verdict.approved .verdict-num{ color:var(--forest); }
.verdict.rejected .verdict-num{ color:var(--brick); }
.verdict-title{ font-family:'Bricolage Grotesque', sans-serif; font-weight:700; font-size:1.35rem; }
.verdict-sub{ color:var(--muted); font-size:.92rem; }

.reason{
    background:var(--panel); border:1px solid var(--line);
    border-left:4px solid var(--brick); border-radius:4px;
    padding:10px 14px; margin-bottom:8px;
}

/* ---------- vehicle list ---------- */
.row-head{ color:var(--muted); font-size:.82rem; padding:4px 0; }
.row-line{ border:0; border-top:1px solid var(--line); margin:2px 0 6px 0; }

/* ---------- metrics ---------- */
div[data-testid="stMetric"]{
    background:var(--panel); border:1px solid var(--line);
    border-radius:6px; padding:12px 16px;
}

/* ---------- buttons ---------- */
.stButton > button, .stFormSubmitButton > button{
    border-radius:6px; font-weight:600; min-height:2.6rem;
    border:1.5px solid var(--forest); background:var(--panel); color:var(--forest);
}
.stButton > button:hover, .stFormSubmitButton > button:hover{
    background:var(--forest-soft); color:var(--forest); border-color:var(--forest);
}
.stButton > button[kind="primary"]{
    background:var(--forest); color:#fff; width:100%; min-height:3rem;
}
.stButton > button[kind="primary"]:hover{ background:#0A3B35; color:#fff; }

/* =====================================================
   PERMANENT ASSISTANT (floating button + popup panel)
   ===================================================== */
.st-key-assistant_dock{
    position:fixed; right:24px; bottom:24px;
    z-index:999990; width:auto !important;
}
.st-key-assistant_dock [data-testid="stPopover"] > button,
.st-key-assistant_dock button{
    background:var(--ink); color:#fff;
    border:2px solid var(--amber); border-radius:999px;
    padding:.65rem 1.25rem; min-height:3rem;
    font-weight:600; box-shadow:0 8px 24px rgba(23,36,33,.28);
}
.st-key-assistant_dock button:hover{ background:#0B1613; color:#fff; border-color:var(--amber); }

div[data-testid="stPopoverBody"]{
    width:min(430px, 92vw);
    border:1px solid var(--line);
    border-top:4px solid var(--amber);
    border-radius:8px;
    background:var(--paper);
}
.assistant-title{ font-family:'Bricolage Grotesque', sans-serif; font-weight:700; font-size:1.2rem; }
.assistant-sub{ color:var(--muted); font-size:.85rem; margin-bottom:8px; }

@media (max-width:640px){
    .st-key-assistant_dock{ right:12px; bottom:12px; }
    .verdict{ flex-direction:column; align-items:flex-start; gap:8px; }
}
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# API FUNCTIONS (unchanged contract with the backend)
# =====================================================


def predict(applicant):
    response = requests.post(
        f"{API_URL}/predict", json=applicant, timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def get_loan_amount(applicant, decision):
    response = requests.post(
        f"{API_URL}/loan-amount",
        json={"applicant": applicant, "decision": decision},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def get_vehicles(budget):
    response = requests.post(
        f"{API_URL}/vehicles", json={"budget": budget}, timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def get_vehicle_detail(vehicle_id):
    response = requests.get(
        f"{API_URL}/vehicles/{vehicle_id}", timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def ask_policy(question):
    response = requests.post(
        f"{API_URL}/explain", json={"question": question}, timeout=LLM_TIMEOUT
    )
    response.raise_for_status()
    return response.json()


# =====================================================
# HELPERS
# =====================================================


def money(value):
    try:
        return f"₹{float(value):,.0f}"
    except (TypeError, ValueError):
        return "N/A"


def pretty(key):
    return str(key).replace("_", " ").capitalize()


def credit_band(score):
    if score >= 750:
        return "success", "Excellent credit profile"
    if score >= 700:
        return "info", "Good credit profile"
    if score >= 650:
        return "warning", "Average credit profile"
    return "error", "High-risk credit profile"


def open_vehicle(vehicle_id):
    st.session_state.selected_vehicle = vehicle_id


def close_vehicle():
    st.session_state.selected_vehicle = None


def clear_chat():
    st.session_state.messages = []


# =====================================================
# SESSION STATE
# =====================================================

DEFAULTS = {
    "messages": [],
    "applicant": None,
    "decision": None,
    "amount": None,
    "vehicles": None,
    "vehicles_error": None,
    "selected_vehicle": None,
    "vehicle_details": {},
    "foir": 0.0,
}
for _key, _value in DEFAULTS.items():
    if _key not in st.session_state:
        st.session_state[_key] = _value

# =====================================================
# MASTHEAD
# =====================================================

st.markdown(
    """
<div class="masthead">
  <div class="wordmark">Vehicle Loan Advisor</div>
  <div class="tagline">
    Check your loan eligibility, see how much you can borrow,
    and find vehicles that fit your budget.
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# =====================================================
# APPLICANT FORM
# =====================================================

col_a, col_b, col_c = st.columns(3, gap="large")

with col_a:
    st.markdown('<div class="group-title">Income and credit</div>', unsafe_allow_html=True)
    monthly_income = st.number_input(
        "Monthly income (₹)", min_value=1000, value=85000, step=1000
    )
    existing_emis = st.number_input("Existing EMIs (₹ per month)", min_value=0, value=10000)
    credit_score = st.slider("Credit score", 300, 900, 750)

with col_b:
    st.markdown('<div class="group-title">About you</div>', unsafe_allow_html=True)
    age = st.number_input("Age", min_value=18, max_value=75, value=30)
    employment_type = st.selectbox(
        "Employment type",
        ["salaried", "self_employed"],
        format_func=pretty,
    )
    employment_years = st.number_input(
        "Years of experience", min_value=0.0, value=5.0, step=0.5
    )

with col_c:
    st.markdown('<div class="group-title">The loan</div>', unsafe_allow_html=True)
    requested_loan_amount = st.number_input(
        "Requested loan amount (₹)", min_value=10000, value=800000, step=10000
    )
    down_payment = st.number_input(
        "Down payment (₹)", min_value=0, value=150000, step=10000
    )
    requested_tenure_months = st.select_slider(
        "Tenure (months)", options=[12, 24, 36, 48, 60, 72, 84], value=60
    )

# ---------- live readout ----------

foir = existing_emis / monthly_income * 100 if monthly_income > 0 else 0

r1, r2, r3 = st.columns([1, 1.4, 1.6], gap="large")
with r1:
    st.metric("Current FOIR", f"{foir:.1f}%")
with r2:
    if foir <= FOIR_LIMIT:
        st.success(f"Within the {FOIR_LIMIT}% policy limit")
    else:
        st.error(f"Above the {FOIR_LIMIT}% policy limit")
with r3:
    kind, text = credit_band(credit_score)
    getattr(st, kind)(text)

evaluate = st.button("Check eligibility", type="primary")

# =====================================================
# EVALUATE
# =====================================================

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
        "age": age,
    }

    for key, value in DEFAULTS.items():
        if key != "messages":
            st.session_state[key] = value

    try:
        with st.spinner("Checking your application..."):
            decision = predict(applicant)
            st.session_state.applicant = applicant
            st.session_state.decision = decision
            st.session_state.foir = foir

            if decision.get("decision") == "Approved":
                amount = get_loan_amount(applicant, "Approved")
                st.session_state.amount = amount
                try:
                    st.session_state.vehicles = get_vehicles(
                        amount["total_vehicle_budget"]
                    )
                except Exception as exc:
                    st.session_state.vehicles_error = str(exc)
    except Exception as exc:
        st.session_state.decision = None
        st.error(
            f"We couldn't check eligibility. Make sure the API is running at "
            f"{API_URL} and try again. Details: {exc}"
        )

# =====================================================
# RESULT
# =====================================================

decision = st.session_state.decision

if decision:
    snapshot = st.session_state.applicant
    probability = float(decision.get("model_probability", 0) or 0)
    approved = decision.get("decision") == "Approved"

    st.markdown("---")

    st.markdown(
        f"""
<div class="verdict {'approved' if approved else 'rejected'}">
  <div class="verdict-num">{probability:.0%}</div>
  <div>
    <div class="verdict-title">{'Loan approved' if approved else 'Loan not approved'}</div>
    <div class="verdict-sub">Approval probability from the credit model</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Credit score", snapshot["credit_score"])
    m2.metric("FOIR at evaluation", f"{st.session_state.foir:.1f}%")
    m3.metric("Monthly income", money(snapshot["monthly_income"]))

    # ---------------- approved ----------------
    amount = st.session_state.amount
    if approved and amount:
        st.subheader("Your loan")

        a1, a2, a3 = st.columns(3)
        a1.metric("Sanctioned amount", money(amount.get("sanctioned_amount")))
        a2.metric("Monthly EMI", money(amount.get("estimated_monthly_emi")))
        a3.metric("Vehicle budget", money(amount.get("total_vehicle_budget")))

        calc = amount.get("calculation", [])
        if isinstance(calc, list) and calc:
            with st.expander("How this was calculated"):
                for item in calc:
                    st.write("•", item)

        st.subheader("Vehicles within your budget")

        vehicles = st.session_state.vehicles
        if st.session_state.vehicles_error:
            st.error(
                "We couldn't load vehicles right now. "
                f"Details: {st.session_state.vehicles_error}"
            )
        elif vehicles:
            widths = [3, 1.5, 1.4, 1.7, 1.7, 1.2]
            head = st.columns(widths)
            for col, title in zip(
                head, ["Vehicle", "Type", "Fuel", "On-road price", "Monthly EMI", ""]
            ):
                col.markdown(f'<div class="row-head">{title}</div>', unsafe_allow_html=True)
            st.markdown('<hr class="row-line">', unsafe_allow_html=True)

            for vehicle in vehicles:
                row = st.columns(widths, vertical_alignment="center")
                row[0].markdown(f"**{vehicle.get('name', 'Unnamed vehicle')}**")
                row[1].write(vehicle.get("category", "N/A"))
                row[2].write(vehicle.get("fuel_type", "N/A"))
                row[3].write(money(vehicle.get("on_road_price")))
                row[4].write(money(vehicle.get("estimated_emi")))
                row[5].button(
                    "Details",
                    key=f"vehicle_{vehicle['id']}",
                    on_click=open_vehicle,
                    args=(vehicle["id"],),
                )
                st.markdown('<hr class="row-line">', unsafe_allow_html=True)
        else:
            st.info(
                "No vehicles match this budget yet. "
                "A larger down payment or a longer tenure can raise it."
            )

        selected = st.session_state.selected_vehicle
        if selected is not None:
            details = st.session_state.vehicle_details
            if selected not in details:
                try:
                    with st.spinner("Loading vehicle details..."):
                        details[selected] = get_vehicle_detail(selected)
                except Exception as exc:
                    details[selected] = {"error": f"Could not load details: {exc}"}

            detail = details[selected]
            with st.container(border=True):
                head_l, head_r = st.columns([5, 1], vertical_alignment="center")
                head_l.markdown(f"### {detail.get('name', 'Vehicle details')}")
                head_r.button("Close", key="close_vehicle", on_click=close_vehicle)

                scalars = {
                    k: v
                    for k, v in detail.items()
                    if not isinstance(v, (dict, list)) and k not in ("id", "name")
                }
                nested = {
                    k: v for k, v in detail.items() if isinstance(v, (dict, list))
                }

                left, right = st.columns(2)
                for i, (k, v) in enumerate(scalars.items()):
                    (left if i % 2 == 0 else right).markdown(f"**{pretty(k)}**  \n{v}")
                for k, v in nested.items():
                    with st.expander(pretty(k)):
                        st.json(v)

    # ---------------- rejected ----------------
    elif not approved:
        st.subheader("Why it was not approved")
        reasons = decision.get("reasons", [])
        if reasons:
            for reason in reasons:
                st.markdown(
                    f'<div class="reason">{html.escape(str(reason))}</div>',
                    unsafe_allow_html=True,
                )
        st.caption(
            "Try changing your income, EMIs, down payment or tenure above, "
            "then check eligibility again."
        )

# =====================================================
# PERMANENT ASSISTANT
# Floating button, bottom-right, on every screen.
# =====================================================

SUGGESTIONS = [
    "What FOIR limit applies to me?",
    "How is my EMI calculated?",
    "What credit score do I need?",
]

with st.container(key="assistant_dock"):
    with st.popover("💬 Ask the policy assistant"):
        top_l, top_r = st.columns([3, 1], vertical_alignment="center")
        with top_l:
            st.markdown(
                '<div class="assistant-title">Policy assistant</div>'
                '<div class="assistant-sub">Answers come from your loan policy documents.</div>',
                unsafe_allow_html=True,
            )
        with top_r:
            st.button("Clear", key="clear_chat", on_click=clear_chat)

        history = st.container(height=340, border=True)

        question = None

        if not st.session_state.messages:
            for i, suggestion in enumerate(SUGGESTIONS):
                if st.button(suggestion, key=f"suggest_{i}"):
                    question = suggestion

        with st.form("assistant_form", clear_on_submit=True):
            typed = st.text_input(
                "Your question",
                placeholder="Ask about FOIR, EMI, credit score or eligibility",
                label_visibility="collapsed",
            )
            sent = st.form_submit_button("Send")

        if sent and typed.strip():
            question = typed.strip()

        if question:
            st.session_state.messages.append({"role": "user", "content": question})
            try:
                with st.spinner("Searching policy documents..."):
                    result = ask_policy(question)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result.get("answer", "No answer returned."),
                        "sources": result.get("sources", []),
                    }
                )
            except Exception:
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": (
                            "I couldn't reach the policy service. "
                            f"Check that the API is running at {API_URL} and ask again."
                        ),
                        "sources": [],
                    }
                )

        with history:
            if not st.session_state.messages:
                st.caption("No messages yet. Pick a question below or type your own.")
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    if msg.get("sources"):
                        with st.expander("Sources"):
                            for src in msg["sources"]:
                                st.markdown(
                                    f"**{src.get('document', 'N/A')}**  \n"
                                    f"Section: {src.get('section', 'N/A')}  \n"
                                    f"Relevance: {float(src.get('score', 0)):.2f}"
                                )