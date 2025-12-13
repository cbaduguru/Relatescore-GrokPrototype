import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import string

# -----------------------------
# App config
# -----------------------------
st.set_page_config(page_title="RelateScore™", page_icon="✅", layout="centered")

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
        .block-container { max-width: 520px; padding-top: 24px; }
        h1, h2, h3 { color: #1A1A1A; font-family: sans-serif; }
        .stButton > button {
            background-color: #C6A667 !important;
            color: #FFFFFF !important;
            border-radius: 10px !important;
            border: none !important;
            padding: 10px 18px !important;
            width: 100% !important;
        }
        .insight-card {
            background-color: #FFFFFF;
            border: 1px solid #C6A667;
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 10px;
        }
        .logo { text-align:center; margin-bottom: 10px; }
        .tagline { text-align:center; color:#3A3A3A; margin-bottom: 18px; }
        .rgi-big { font-size: 54px; font-weight: 800; color: #C6A667; text-align: center; line-height: 1.0; }
        .small-muted { color:#666; font-size: 0.92rem; }
    </style>
    """,
    unsafe_allow_html=True
)

logo_svg = """
<div class="logo">
<svg width="56" height="56" viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">
    <circle cx="25" cy="25" r="20" stroke="#C6A667" stroke-width="4" fill="none"/>
    <path d="M15 25 L22 32 L35 19" stroke="#C6A667" stroke-width="4" fill="none"/>
</svg>
<div style="font-size: 22px; font-weight: 700; margin-top: 6px;">RelateScore™</div>
</div>
"""

def display_logo():
    st.markdown(logo_svg, unsafe_allow_html=True)

# -----------------------------
# Rerun compatibility (Streamlit Cloud safe)
# -----------------------------
def _rerun():
    # Streamlit Cloud may be on an older version where st.rerun() doesn't exist
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

def nav(to_page: str):
    st.session_state.page = to_page
    _rerun()

# -----------------------------
# Data
# -----------------------------
categories = [
    "Emotional Awareness",
    "Communication Style",
    "Conflict Tendencies",
    "Attachment Patterns",
    "Empathy & Responsiveness",
    "Self-Insight",
    "Trust & Boundaries",
    "Stability & Consistency"
]

likert_questions = {
    cat: [
        f"On a scale of 1–5, how important is {cat.lower()} to you in relationships?",
        f"How would you rate your current level in {cat.lower()}?",
        f"How often do you reflect on {cat.lower()}?"
    ]
    for cat in categories
}

assessment_questions = {
    cat: [
        f"How often do you recognize patterns in {cat.lower()}?",
        f"How comfortable are you discussing {cat.lower()}?",
        f"How does {cat.lower()} impact your connections?"
    ]
    for cat in categories
}

# -----------------------------
# Session state init
# -----------------------------
def init_state():
    defaults = {
        "page": "entry",
        "logged_in": False,
        "invite_code": None,
        "partner_code": "",
        "partner_accepted": False,
        "use_mutual": False,
        "consent_accepted": False,
        "likert_responses": {},
        "assessment_responses": {},
        "scores": None,
        "insights": None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_state(keep_invite=False):
    invite = st.session_state.get("invite_code")
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    init_state()
    if keep_invite:
        st.session_state.invite_code = invite

init_state()

# -----------------------------
# Helpers
# -----------------------------
def generate_invite_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def compute_scores():
    cat_scores = {}
    for cat in categories:
        likert_vals = [st.session_state.likert_responses[q] for q in likert_questions[cat]]
        assess_vals = [st.session_state.assessment_responses[q] for q in assessment_questions[cat]]

        baseline = float(np.mean(likert_vals)) * 20.0
        raw = float(np.mean(assess_vals)) * 20.0

        score = (raw / baseline) * 50.0 if baseline > 0 else raw

        if st.session_state.use_mutual:
            mutual = float(np.random.uniform(40, 80))
            score = 0.4 * score + 0.6 * mutual

        score = float(np.clip(score, 20, 90))
        cat_scores[cat] = score

    weights = np.array([0.15, 0.15, 0.15, 0.10, 0.15, 0.10, 0.10, 0.10], dtype=float)
    rgi = float(np.sum(np.array([cat_scores[c] for c in categories], dtype=float) * weights))
    cat_scores["RGI"] = rgi
    st.session_state.scores = cat_scores

def generate_insights():
    insights = []
    for cat in categories:
        score = st.session_state.scores.get(cat, 0)
        if score > 70:
            type_ = "Strength"
            desc = "This is a strong foundation to build on."
        elif score < 40:
            type_ = "Blind Spot"
            desc = "This pattern may create misunderstandings."
        else:
            type_ = "Neutral"
            desc = "Balanced area with room for awareness."
        insights.append({
            "category": cat,
            "type": type_,
            "description": desc,
            "suggestion": "Consider a small experiment this week to shift this pattern by 1%."
        })
    st.session_state.insights = insights

# -----------------------------
# Pages
# -----------------------------
def entry_page():
    display_logo()
    st.markdown('<div class="tagline">Private reflection. Shared only by choice.</div>', unsafe_allow_html=True)

    if st.button("Create Profile", key="entry_create"):
        nav("create_profile")

    if st.button("Log In", key="entry_login"):
        nav("log_in")

    if st.button("Enter Invite Code", key="entry_invite"):
        nav("partner_entry")

    st.markdown("<div class='small-muted'>Tip: If you're joining via code, the sender must generate one first.</div>", unsafe_allow_html=True)

def create_profile_page():
    display_logo()
    st.header("Create your private profile")
    st.write("Your responses are encrypted and visible only to you unless you choose to share.")

    st.session_state.consent_accepted = st.checkbox(
        "I understand that my reflections are private, encrypted, and can be deleted at any time.",
        value=st.session_state.consent_accepted,
        key="consent_checkbox"
    )

    st.write("No public profiles. No social exposure.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back", key="create_back"):
            nav("entry")
    with c2:
        if st.button("Continue", key="create_continue", disabled=not st.session_state.consent_accepted):
            st.session_state.logged_in = True
            nav("home")

def log_in_page():
    display_logo()
    st.header("Welcome back")
    st.write("Your space for private relational clarity.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back", key="login_back"):
            nav("entry")
    with c2:
        if st.button("Log In", key="login_go"):
            st.session_state.logged_in = True
            nav("home")

    st.markdown("<div class='small-muted'>Access is limited to you and invited participants only.</div>", unsafe_allow_html=True)

def home_page():
    display_logo()
    st.header("Home")
    st.write("Your relationships deserve clarity—without pressure or performance.")

    if not st.session_state.logged_in:
        st.warning("You must be logged in to access Home.")
        if st.button("Return to Entry", key="home_return_entry"):
            nav("entry")
        return

    if st.button("Create Invite", key="home_create_invite"):
        st.session_state.invite_code = generate_invite_code()
        nav("create_invite")

    if st.button("Withdraw & Reset", key="home_reset"):
        reset_state(keep_invite=False)
        nav("entry")

    st.markdown("<div class='small-muted'>Invitations are one-time use and expire automatically.</div>", unsafe_allow_html=True)

def create_invite_page():
    display_logo()
    st.header("Invite")
    st.write("A unique invitation code has been created:")

    if not st.session_state.invite_code:
        st.session_state.invite_code = generate_invite_code()

    st.code(st.session_state.invite_code)
    st.write("Share this code privately with the person you trust.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back to Home", key="invite_back_home"):
            nav("home")
    with c2:
        if st.button("Done", key="invite_done"):
            nav("home")

def partner_entry_page():
    display_logo()
    st.header("Enter invitation code")
    st.write("This code connects you to a shared reflection space—nothing is visible without consent.")

    # If no invite exists in this session, don't claim "expired".
    if st.session_state.invite_code is None:
        st.info("No active invite exists in this session yet. Ask the sender to generate a code (Home → Create Invite) and share it with you.")
        if st.button("Return to Entry", key="partner_no_invite_back"):
            nav("entry")
        return

    st.session_state.partner_code = st.text_input(
        "Enter the code exactly as shared.",
        value=st.session_state.partner_code,
        key="partner_code_input"
    ).strip().upper()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back", key="partner_back"):
            nav("entry")
    with c2:
        if st.button("Continue", key="partner_continue"):
            if st.session_state.partner_code == st.session_state.invite_code:
                st.session_state.partner_accepted = True
                nav("invite_accepted")
            else:
                st.error("Code not recognized. Ask the sender to generate a new code and share it again.")

def invite_accepted_page():
    display_logo()
    st.success("Connection established.")
    st.write("You may begin reflection at your own pace.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back", key="accepted_back"):
            nav("partner_entry")
    with c2:
        if st.button("Start Reflection", key="accepted_start"):
            nav("reflection_start")

def reflection_start_page():
    display_logo()
    st.header("Begin when ready")
    st.write("There are no right or wrong answers.")
    st.write("You can pause, return, or withdraw at any time.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back", key="refstart_back"):
            nav("invite_accepted")
    with c2:
        if st.button("Start Reflection", key="refstart_go"):
            nav("likert")

    st.markdown("<div class='small-muted'>Progress is saved automatically.</div>", unsafe_allow_html=True)

def likert_page():
    display_logo()
    st.header("Personal Calibration")
    st.write("Answer with honesty – this sets your personal scale.")

    # Deterministic keys (no hash)
    for cat_i, cat in enumerate(categories):
        st.subheader(cat)
        for q_i, q in enumerate(likert_questions[cat]):
            st.session_state.likert_responses[q] = st.slider(
                q, 1, 5, 3, key=f"likert_{cat_i}_{q_i}"
            )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back", key="likert_back"):
            nav("reflection_start")
    with c2:
        if st.button("Proceed to Preview", key="likert_next"):
            nav("preview")

def preview_page():
    display_logo()
    st.header("What You'll Get")
    st.write("A private Relationship Growth Index (RGI).")
    st.write("Personalized RQ Wheel showing patterns.")
    st.write("Insights on strengths, blind spots, and growth areas.")
    st.write("No public scores, no comparisons – just your clarity.")

    st.session_state.use_mutual = st.checkbox(
        "Include simulated mutual reflection?",
        value=st.session_state.use_mutual,
        key="mutual_checkbox"
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back", key="preview_back"):
            nav("likert")
    with c2:
        if st.button("Proceed to Assessment", key="preview_next"):
            nav("assessment")

def assessment_page():
    display_logo()
    st.header("Relational Assessment")
    st.write("Respond based on what feels true most of the time.")

    # Deterministic keys (no hash)
    for cat_i, cat in enumerate(categories):
        st.subheader(cat)
        for q_i, q in enumerate(assessment_questions[cat]):
            st.session_state.assessment_responses[q] = st.slider(
                q, 1, 5, 3, key=f"assess_{cat_i}_{q_i}"
            )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Back", key="assess_back"):
            nav("preview")
    with c2:
        if st.button("Submit Assessment", key="assess_submit"):
            # Keep simulated gate
            if np.random.rand() < 0.1:
                st.error("Input blocked for toxicity. Please revise.")
            else:
                compute_scores()
                generate_insights()
                nav("dashboard")

def dashboard_page():
    display_logo()
    st.header("Your Relational Dashboard")
    st.write("Your relational clarity at a glance.")

    if not st.session_state.scores:
        st.warning("No assessment results found yet. Please complete the assessment.")
        if st.button("Go to Assessment", key="dash_go_assessment"):
            nav("assessment")
        return

    st.markdown(f"<div class='rgi-big'>{st.session_state.scores['RGI']:.1f}</div>", unsafe_allow_html=True)
    st.caption("Relationship Growth Index")

    scores = st.session_state.scores
    labels = np.array(categories)
    values = np.array([scores[cat] for cat in categories], dtype=float)

    # Radar chart
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values_loop = np.concatenate((values, [values[0]]))
    angles_loop = angles + angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles_loop, values_loop, alpha=0.25)
    ax.plot(angles_loop, values_loop, linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=10)
    st.pyplot(fig)

    st.subheader("Key Insights")
    for insight in (st.session_state.insights or []):
        st.markdown(
            f"""
            <div class="insight-card">
                <div style="font-weight:700;">{insight['category']}: {insight['type']}</div>
                <div>{insight['description']}</div>
                <div><i>Suggestion: {insight['suggestion']}</i></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("Daily Reflection")
    reflection_text = st.text_area("Your thoughts", key="reflection_text")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Save", key="reflect_save"):
            st.success("Reflection saved. Carry this insight forward.")
    with c2:
        if st.button("Generate Insight", key="reflect_gen"):
            if "emotion" in (reflection_text or "").lower():
                insight = "Your reflection highlights growth in Emotional Awareness."
            elif "communication" in (reflection_text or "").lower():
                insight = "This ties to your Communication Style patterns."
            else:
                insight = "Balanced reflection – patterns evolve as you grow."
            st.info(insight)
    with c3:
        if st.button("Withdraw & Reset", key="dash_reset"):
            reset_state(keep_invite=False)
            nav("entry")

    if st.button("Return to Home", key="dash_home"):
        nav("home")

# -----------------------------
# Router
# -----------------------------
PAGES = {
    "entry": entry_page,
    "create_profile": create_profile_page,
    "log_in": log_in_page,
    "home": home_page,
    "create_invite": create_invite_page,
    "partner_entry": partner_entry_page,
    "invite_accepted": invite_accepted_page,
    "reflection_start": reflection_start_page,
    "likert": likert_page,
    "preview": preview_page,
    "assessment": assessment_page,
    "dashboard": dashboard_page,
}

page = st.session_state.get("page", "entry")
PAGES.get(page, entry_page)()
