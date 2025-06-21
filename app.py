import streamlit as st
import time
from ai_core import (
    generate_market_research, 
    generate_competitor_analysis, 
    generate_pitch_deck_slides,
    generate_project_names,       # <-- Import new tool
    generate_outreach_email     # <-- Import new tool
)

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Archimedes AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. CUSTOM CSS ---
st.markdown("""
<style>
    body { font-family: 'Poppins', sans-serif; }
    .main .block-container { padding: 2rem 5rem; }
    [data-testid="stSidebar"] { background-color: #2d3748; border-right: 2px solid #4A5568; }
    .sidebar-title { font-size: 28px; font-weight: 700; color: #F97316; padding-bottom: 1rem; border-bottom: 2px solid #4A5568; text-align: center; }
    .stButton>button { border-radius: 12px; border: 2px solid #F97316; background-color: transparent; color: #F97316; padding: 10px 24px; font-weight: 600; transition: all 0.3s ease-in-out; }
    .stButton>button:hover { background-color: #F97316; color: white; border-color: #F97316; }
    .content-card { background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 20px; padding: 2rem; margin-top: 1rem; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1); }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE MANAGEMENT ---
if 'results' not in st.session_state:
    st.session_state.results = {}
if 'project_idea' not in st.session_state:
    st.session_state.project_idea = ""

# --- 4. THE AGENTIC WORKFLOW FUNCTION ---
def run_agentic_workflow(project_idea):
    """The core agent. Defines a plan and executes it step-by-step."""
    # The agent's plan, now including creative steps
    plan = [
        {"name": "Project Naming & Branding", "tool": generate_project_names, "args": [project_idea], "output_key": "branding"},
        {"name": "Market Research", "tool": generate_market_research, "args": [project_idea], "output_key": "market_research"},
        {"name": "Competitor Analysis", "tool": generate_competitor_analysis, "args": [project_idea], "output_key": "competitor_analysis"},
        {"name": "Drafting Outreach Email", "tool": generate_outreach_email, "args": [], "output_key": "outreach_email"},
        {"name": "Pitch Deck Generation", "tool": generate_pitch_deck_slides, "args": [], "output_key": "pitch_deck"}
    ]

    for step in plan:
        with st.status(f"🚀 Executing: {step['name']}...", expanded=True) as status:
            st.write(f"Agent starting task: **{step['name']}**")
            time.sleep(1)

            # Dynamically set arguments for steps that depend on previous outputs
            if step['name'] == "Pitch Deck Generation":
                step['args'] = [st.session_state.results['market_research'], st.session_state.results['competitor_analysis'], project_idea]
            elif step['name'] == "Drafting Outreach Email":
                step['args'] = [project_idea, st.session_state.results['market_research']]

            result = step['tool'](*step['args'])
            st.session_state.results[step['output_key']] = result
            
            st.markdown("---")
            st.write(f"**Output Preview for {step['name']}:**")
            st.markdown(result[:300] + "...")
            
            status.update(label=f"✅ {step['name']} Complete!", state="complete", expanded=False)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">🤖 Archimedes Agent</div>', unsafe_allow_html=True)
    st.markdown("Your end-to-end AI Co-founder.")
    st.divider()
    st.subheader("Your Big Idea")
    project_input = st.text_area("Describe your project idea:", height=150, placeholder="e.g., A mobile app that uses AI to create personalized workout plans...", value=st.session_state.project_idea)
    if project_input:
        st.session_state.project_idea = project_input
    st.divider()
    if st.button("Reset Analysis"):
        st.session_state.results = {}
        st.rerun()
    st.info("© 2024 Archimedes AI.")

# --- 6. MAIN PAGE ---
st.title("Agentic Co-Founder: From Idea to Outreach")
st.markdown("Provide your project idea and the AI agent will perform a full analysis, complete with creative branding and outreach tools.")

if not st.session_state.project_idea:
    st.info("Enter your project idea in the sidebar to activate the agent.")
    st.stop()

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("🚀 Launch Full Analysis", use_container_width=True):
        st.session_state.results = {}
        run_agentic_workflow(st.session_state.project_idea)

st.divider()

# --- 7. DISPLAY RESULTS ---
if st.session_state.results:
    st.header("Analysis Complete: Review Your Assets")

    # More tabs to display the new creative outputs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎨 Brand & Name", "📊 Market Research", "⚔️ Competitor Analysis", "📝 Pitch Deck", "💌 Outreach Tools"])

    with tab1:
        st.subheader("Project Branding & Naming")
        if "branding" in st.session_state.results:
            st.markdown(st.session_state.results["branding"])
        else:
            st.info("Branding has not been generated yet.")

    with tab2:
        st.subheader("Market Research")
        if "market_research" in st.session_state.results:
            st.markdown(st.session_state.results["market_research"])
    
    with tab3:
        st.subheader("Competitor Analysis")
        if "competitor_analysis" in st.session_state.results:
            st.markdown(st.session_state.results["competitor_analysis"])

    with tab4:
        st.subheader("Pitch Deck Content")
        if "pitch_deck" in st.session_state.results:
            st.markdown(st.session_state.results["pitch_deck"])
            st.download_button("⬇️ Download Pitch Deck", st.session_state.results["pitch_deck"], "pitch_deck.md")

    with tab5:
        st.subheader("Early Customer Outreach Email")
        if "outreach_email" in st.session_state.results:
            st.markdown(st.session_state.results["outreach_email"])
            st.download_button("⬇️ Download Email Template", st.session_state.results["outreach_email"], "outreach_email.txt")