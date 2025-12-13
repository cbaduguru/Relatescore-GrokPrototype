import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Custom CSS for brand/visual system
st.markdown("""
<style>
    .main {
        max-width: 400px;
        margin: 0 auto;
        background-color: #F5F5F5;
        padding: 20px;
        font-family: 'Open Sans', sans-serif;
    }
    h1, h2 {
        font-family: 'Montserrat', sans-serif;
        color: #1A1A1A;
    }
    .stButton > button {
        background-color: #C6A667;
        color: #FFFFFF;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    .stSlider > div > div > div {
        background-color: #2E6AF3;
    }
    .insight-card {
        background-color: #FFFFFF;
        border: 1px solid #C6A667;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .logo {
        text-align: center;
        margin-bottom: 20px;
    }
    .rgi-big {
        font-size: 48px;
        font-weight: bold;
        color: #C6A667;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Logo SVG (simple circle with checkmark)
logo_svg = """
<svg width="50" height="50" viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">
    <circle cx="25" cy="25" r="20" stroke="#C6A667" stroke-width="4" fill="none"/>
    <path d="M15 25 L22 32 L35 19" stroke="#C6A667" stroke-width="4" fill="none"/>
</svg>
<h3 style="color: #1A1A1A; display: inline; margin-left: 10px;">RelateScore™</h3>
"""

# Categories from RQ Wheel doc
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

# Likert calibration questions (inferred from docs: personal perception scale for each category)
likert_questions = {}
for cat in categories:
    likert_questions[cat] = [
        f"On a scale of 1-5, how important is {cat.lower()} to you in relationships?",
        f"How would you rate your current level in {cat.lower()}?",
        f"How often do you reflect on {cat.lower()}?"
    ]

# Assessment questions (guided prompts, 1-5 Likert)
assessment_questions = {}
for cat in categories:
    assessment_questions[cat] = [
        f"How often do you recognize patterns in {cat.lower()}?",
        f"How comfortable are you discussing {cat.lower()}?",
        f"How does {cat.lower()} impact your connections?"
    ]

# Session state initialization
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'invite_code' not in st.session_state:
    st.session_state.invite_code = None
if 'partner_accepted' not in st.session_state:
    st.session_state.partner_accepted = False
if 'confirmed' not in st.session_state:
    st.session_state.confirmed = False
if 'likert_responses' not in st.session_state:
    st.session_state.likert_responses = {}
if 'assessment_responses' not in st.session_state:
    st.session_state.assessment_responses = {}
if 'scores' not in st.session_state:
    st.session_state.scores = None
if 'insights' not in st.session_state:
    st.session_state.insights = None
if 'use_mutual' not in st.session_state:
    st.session_state.use_mutual = False

# Function to display logo on every page
def display_logo():
    st.markdown(f'<div class="logo">{logo_svg}</div>', unsafe_allow_html=True)

# Login/Create Profile
def login_page():
    display_logo()
    st.title("RelateScore™")
    st.write("Relationship clarity without exposure.")
    if st.button("Create Profile / Log In"):
        st.session_state.logged_in = True
        st.session_state.page = 'home'

# Home Screen
def home_page():
    display_logo()
    st.header("Home")
    st.write("Your relationships deserve clarity and truth.")
    if st.button("Create Invite"):
        st.session_state.invite_code = "INVITE123"  # Simulated code
        st.session_state.page = 'invite'

# Create Invite
def invite_page():
    display_logo()
    st.header("Invite Partner")
    st.write("Share this code with your partner who has a RelateScore™ account.")
    st.code(st.session_state.invite_code)
    if st.checkbox("Simulate Partner Acceptance (for prototype)"):
        st.session_state.partner_accepted = True
        st.session_state.page = 'confirmation'

# Confirmation
def confirmation_page():
    display_logo()
    st.header("Confirm Connection")
    st.write("Your partner has accepted the invite.")
    if st.button("Confirm"):
        st.session_state.confirmed = True
        st.session_state.page = 'welcome'
    if st.button("Decline"):
        st.session_state.page = 'declined'

# Declined Edge Case
def declined_page():
    display_logo()
    st.header("Connection Not Created")
    st.write("No connection was created.")
    if st.button("Return to Home"):
        st.session_state.page = 'home'

# Welcome Screen
def welcome_page():
    display_logo()
    st.header("Welcome")
    st.write("Private relational clarity.")
    st.write("There are no right or wrong answers.")
    if st.button("Begin Reflection"):
        st.session_state.page = 'likert'

# Likert Calibration
def likert_page():
    display_logo()
    st.header("Personal Calibration")
    st.write("Answer with honesty – this sets your personal scale.")
    for cat in categories:
        st.subheader(cat)
        for q in likert_questions[cat]:
            st.session_state.likert_responses[q] = st.slider(q, 1, 5, 3)
    if st.button("Proceed to Preview"):
        st.session_state.page = 'preview'

# Preview (What You'll Get - Figure 2 inferred as outputs preview)
def preview_page():
    display_logo()
    st.header("What You'll Get")
    st.write("A private Relationship Growth Index (RGI).")
    st.write("Personalized RQ Wheel showing patterns.")
    st.write("Insights on strengths, blind spots, and growth areas.")
    st.write("No public scores, no comparisons – just your clarity.")
    if st.checkbox("Include simulated mutual reflection?"):
        st.session_state.use_mutual = True
    if st.button("Proceed to Assessment"):
        st.session_state.page = 'assessment'

# Assessment
def assessment_page():
    display_logo()
    st.header("Relational Assessment")
    st.write("Respond based on what feels true most of the time.")
    for cat in categories:
        st.subheader(cat)
        for q in assessment_questions[cat]:
            st.session_state.assessment_responses[q] = st.slider(q, 1, 5, 3)
    if st.button("Submit Assessment"):
        # Simulate toxicity filter
        if np.random.rand() < 0.1:
            st.error("Input blocked for toxicity. Please revise.")
        else:
            compute_scores()
            generate_insights()
            st.success("Assessment complete!")
            st.session_state.page = 'dashboard'

# Compute Scores (from engineering spec)
def compute_scores():
    cat_scores = {}
    for cat in categories:
        likert_vals = [st.session_state.likert_responses[q] for q in likert_questions[cat]]
        assess_vals = [st.session_state.assessment_responses[q] for q in assessment_questions[cat]]
        # Use Likert for normalization baseline
        baseline = np.mean(likert_vals) * 20  # 0-100
        raw = np.sum(assess_vals) / len(assess_vals) * 20
        score = (raw / baseline) * 50 if baseline > 0 else raw  # Relative to personal scale
        # Mutual simulation
        if st.session_state.use_mutual:
            mutual = np.random.uniform(40, 80)
            score = 0.4 * score + 0.6 * mutual  # Weight mutual heavier
        # Outlier dampening (clip)
        score = np.clip(score, 20, 90)
        cat_scores[cat] = score
    # RGI weighted sum (approx weights from doc)
    weights = np.array([0.15, 0.15, 0.15, 0.1, 0.15, 0.1, 0.1, 0.1])
    rgi = np.sum(np.array(list(cat_scores.values())) * weights)
    cat_scores['RGI'] = rgi
    st.session_state.scores = cat_scores

# Generate Insights (thresholds from spec)
def generate_insights():
    insights = []
    for cat, score in st.session_state.scores.items():
        if cat == 'RGI':
            continue
        if score > 70:
            type_ = "Strength"
            desc = "This is a strong foundation to build on."
        elif score < 40:
            type_ = "Blind Spot"
            desc = "This pattern may create misunderstandings."
        else:
            type_ = "Neutral"
            desc = "Balanced area with room for awareness."
        insights.append({"category": cat, "type": type_, "description": desc, "suggestion": "Consider experimenting with this new approach."})
    st.session_state.insights = insights

# Dashboard
def dashboard_page():
    display_logo()
    st.header("Your Relational Dashboard")
    st.write("Your relational clarity at a glance.")
    # Big bold RGI
    st.markdown(f'<div class="rgi-big">{st.session_state.scores["RGI"]:.1f}</div>', unsafe_allow_html=True)
    st.write("Relationship Growth Index")
    # RQ Wheel
    scores = st.session_state.scores
    labels = np.array(categories)
    values = np.array([scores[cat] for cat in categories])
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values = np.concatenate((values, [values[0]]))
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='#A6E3DA', alpha=0.25)
    ax.plot(angles, values, color='#C6A667', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12)
    st.pyplot(fig)
    # Key Insights
    st.header("Key Insights")
    for insight in st.session_state.insights:
        st.markdown(f"""
        <div class="insight-card">
            <h3>{insight['category']}: {insight['type']}</h3>
            <p>{insight['description']}</p>
            <p><i>Suggestion: {insight['suggestion']}</i></p>
        </div>
        """, unsafe_allow_html=True)
    # Daily Reflection
    st.header("Daily Reflection")
    st.write("Take a moment to reflect...")
    st.text_area("Your thoughts")
    if st.button("Save"):
        st.success("Saved.")
    # Withdraw & Reset
    if st.button("Withdraw & Reset"):
        st.session_state.scores = None
        st.session_state.insights = None
        st.session_state.page = 'home'
        st.warning("All data erased.")

# Page Router
pages = {
    'login': login_page,
    'home': home_page,
    'invite': invite_page,
    'confirmation': confirmation_page,
    'declined': declined_page,
    'welcome': welcome_page,
    'likert': likert_page,
    'preview': preview_page,
    'assessment': assessment_page,
    'dashboard': dashboard_page
}

if st.session_state.page in pages:
    pages[st.session_state.page]()
else:
    st.error("Invalid page.")
    st.session_state.page = 'login'