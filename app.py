import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import string

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

# Likert calibration questions
likert_questions = {}
for cat in categories:
    likert_questions[cat] = [
        f"On a scale of 1-5, how important is {cat.lower()} to you in relationships?",
        f"How would you rate your current level in {cat.lower()}?",
        f"How often do you reflect on {cat.lower()}?"
    ]

# Assessment questions
assessment_questions = {}
for cat in categories:
    assessment_questions[cat] = [
        f"How often do you recognize patterns in {cat.lower()}?",
        f"How comfortable are you discussing {cat.lower()}?",
        f"How does {cat.lower()} impact your connections?"
    ]

# Session state initialization
if 'page' not in st.session_state:
    st.session_state.page = 'entry'
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
if 'consent_accepted' not in st.session_state:
    st.session_state.consent_accepted = False
if 'partner_code' not in st.session_state:
    st.session_state.partner_code = ''

# Function to generate unique invite code
def generate_invite_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Function to display logo on every page
def display_logo():
    st.markdown(f'<div class="logo">{logo_svg}</div>', unsafe_allow_html=True)

# Entry Screen (Unauthenticated)
def entry_page():
    display_logo()
    st.write("Private reflection. Shared only by choice.")
    if st.button("Create Profile"):
        st.session_state.page = 'create_profile'
    if st.button("Log In"):
        st.session_state.page = 'log_in'
    if st.button("Enter Invite Code"):
        st.session_state.page = 'partner_entry'

# Create Profile Screen
def create_profile_page():
    display_logo()
    st.header("Create your private profile")
    st.write("Your responses are encrypted and visible only to you unless you choose to share.")
    st.session_state.consent_accepted = st.checkbox("I understand that my reflections are private, encrypted, and can be deleted at any time.")
    st.write("No public profiles. No social exposure.")
    if st.session_state.consent_accepted and st.button("Continue"):
        st.session_state.logged_in = True
        st.session_state.page = 'home'

# Log In Screen
def log_in_page():
    display_logo()
    st.header("Welcome back")
    st.write("Your space for private relational clarity.")
    if st.button("Log In"):
        st.session_state.logged_in = True
        st.session_state.page = 'home'
    st.write("Access is limited to you and invited participants only.")

# Home Screen (Authenticated)
def home_page():
    display_logo()
    st.header("Your relationships deserve clarity—without pressure or performance.")
    if st.button("Create Invite"):
        st.session_state.invite_code = generate_invite_code()
        st.session_state.page = 'create_invite'
    st.write("Invitations are one-time use and expire automatically.")

# Create Invite Screen
def create_invite_page():
    display_logo()
    st.write("A unique invitation code has been created.")
    st.code(st.session_state.invite_code)
    st.write("Share this code privately with the person you trust.")
    st.write("Codes cannot be reused and do not expose your responses.")
    if st.button("Done"):
        st.session_state.page = 'home'

# Partner Entry Screen
def partner_entry_page():
    display_logo()
    st.header("Enter invitation code")
    st.write("This code connects you to a shared reflection space—nothing is visible without consent.")
    st.session_state.partner_code = st.text_input("Enter the code exactly as shared.")
    if st.button("Continue"):
        if st.session_state.partner_code == st.session_state.invite_code:
            st.session_state.partner_accepted = True
            st.session_state.page = 'invite_accepted'
        else:
            st.error("This invitation has expired. Ask the sender to generate a new one.")
            if st.button("Return to Home"):
                st.session_state.page = 'home'

# Invite Accepted
def invite_accepted_page():
    display_logo()
    st.write("Connection established.")
    st.write("You may begin reflection at your own pace.")
    if st.button("Start Reflection"):
        st.session_state.page = 'reflection_start'

# Reflection Start Screen
def reflection_start_page():
    display_logo()
    st.header("Begin when ready")
    st.write("There are no right or wrong answers.")
    st.write("You can pause, return, or withdraw at any time.")
    if st.button("Start Reflection"):
        st.session_state.page = 'likert'
    st.write("Progress is saved automatically.")

# Declined Edge Case
def declined_page():
    display_logo()
    st.header("The invitation was declined.")
    st.write("No data was shared.")
    if st.button("Return to Home"):
        st.session_state.page = 'home'

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

# Preview
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
        if np.random.rand() < 0.1:
            st.error("Input blocked for toxicity. Please revise.")
        else:
            compute_scores()
            generate_insights()
            st.success("Assessment complete!")
            st.session_state.page = 'dashboard'

# Compute Scores
def compute_scores():
    cat_scores = {}
    for cat in categories:
        likert_vals = [st.session_state.likert_responses[q] for q in likert_questions[cat]]
        assess_vals = [st.session_state.assessment_responses[q] for q in assessment_questions[cat]]
        baseline = np.mean(likert_vals) * 20
        raw = np.mean(assess_vals) * 20
        score = (raw / baseline) * 50 if baseline > 0 else raw
        if st.session_state.use_mutual:
            mutual = np.random.uniform(40, 80)
            score = 0.4 * score + 0.6 * mutual
        score = np.clip(score, 20, 90)
        cat_scores[cat] = score
    weights = np.array([0.15, 0.15, 0.15, 0.1, 0.15, 0.1, 0.1, 0.1])
    rgi = np.sum(np.array(list(cat_scores.values())) * weights)
    cat_scores['RGI'] = rgi
    st.session_state.scores = cat_scores

# Generate Insights
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
    st.markdown(f'<div class="rgi-big">{st.session_state.scores["RGI"]:.1f}</div>', unsafe_allow_html=True)
    st.write("Relationship Growth Index")
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
    st.header("Key Insights")
    for insight in st.session_state.insights:
        st.markdown(f"""
        <div class="insight-card">
            <h3>{insight['category']}: {insight['type']}</h3>
            <p>{insight['description']}</p>
            <p><i>Suggestion: {insight['suggestion']}</i></p>
        </div>
        """, unsafe_allow_html=True)
    st.header("Daily Reflection")
    st.write("Take a moment to reflect...")
    reflection_text = st.text_area("Your thoughts")
    if st.button("Save"):
        st.success("Reflection saved. Carry this insight forward.")
        if st.button("Generate Insight"):
            # Simulated AI insight
            if 'emotion' in reflection_text.lower():
                insight = "Your reflection highlights growth in Emotional Awareness."
            elif 'communication' in reflection_text.lower():
                insight = "This ties to your Communication Style patterns."
            else:
                insight = "Balanced reflection – patterns evolve as you grow."
            st.info(insight)
            st.success("Insight generated. Patterns evolve as you grow.")
            if st.button("Explore Further"):
                st.write("Would you like to explore this further?")
                additional_text = st.text_area("Add more details")
                if st.button("Refine Insight"):
                    refined_insight = f"Refined: {insight} based on additional input."
                    st.info(refined_insight)
            if st.button("Return to Dashboard"):
                st.experimental_rerun()
    if st.button("Withdraw & Reset"):
        st.session_state.scores = None
        st.session_state.insights = None
        st.session_state.page = 'home'
        st.warning("Connection ended. All shared access has been revoked.")

# Page Router
pages = {
    'entry': entry_page,
    'create_profile': create_profile_page,
    'log_in': log_in_page,
    'home': home_page,
    'create_invite': create_invite_page,
    'partner_entry': partner_entry_page,
    'invite_accepted': invite_accepted_page,
    'reflection_start': reflection_start_page,
    'likert': likert_page,
    'preview': preview_page,
    'assessment': assessment_page,
    'dashboard': dashboard_page,
    'declined': declined_page
}

if st.session_state.page in pages:
    pages[st.session_state.page]()
else:
    st.error("Invalid page.")
    st.session_state.page = 'entry'