import streamlit as st
import time
from ai_core import *

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Archimedes AI Agent", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# --- 2. CSS ---
st.markdown("""<style>body { font-family: 'Poppins', sans-serif; } .main .block-container { padding: 2rem 5rem; } [data-testid="stSidebar"] { background-color: #2d3748; } .sidebar-title { font-size: 28px; font-weight: 700; color: #F97316; padding-bottom: 1rem; border-bottom: 2px solid #4A5568; text-align: center; } .stButton>button { border-radius: 12px; border: 2px solid #F97316; background-color: transparent; color: #F97316; padding: 10px 24px; font-weight: 600; } .stButton>button:hover { background-color: #F97316; color: white; } .content-card { background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 20px; padding: 2rem; margin-top: 1rem; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }</style>""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'results' not in st.session_state: st.session_state.results = {}
if 'project_idea' not in st.session_state: st.session_state.project_idea = ""
# Add state for new user inputs
if 'price_point' not in st.session_state: st.session_state.price_point = 50.0
if 'cost_per_user' not in st.session_state: st.session_state.cost_per_user = 10.0

# --- 4. AGENTIC WORKFLOW ---
def run_agentic_workflow(project_idea, price_point, cost_per_user):
    plan = [
        {"name": "Project Naming & Branding", "tool": generate_project_names, "args": [project_idea], "output_key": "branding"},
        {"name": "Market Research (with Web Search)", "tool": generate_market_research_with_web, "args": [project_idea], "output_key": "market_research"},
        {"name": "Competitor Analysis", "tool": generate_competitor_analysis, "args": [project_idea], "output_key": "competitor_analysis"},
        {"name": "Technical Stack Recommendation", "tool": recommend_tech_stack, "args": [project_idea], "output_key": "tech_stack"},
        {"name": "Financial Projections", "tool": generate_financial_projections, "args": [], "output_key": "financials"},
        {"name": "Drafting Outreach Email", "tool": generate_outreach_email, "args": [], "output_key": "outreach_email"},
        {"name": "Pitch Deck Generation", "tool": generate_pitch_deck_slides, "args": [], "output_key": "pitch_deck"}
    ]
    for step in plan:
        with st.status(f"🚀 Executing: {step['name']}...", expanded=True) as status:
            st.write(f"Agent starting task: **{step['name']}**")
            time.sleep(1)
            # Dynamically set arguments for dependent steps
            if step['name'] == "Financial Projections": step['args'] = [st.session_state.results['market_research'], price_point, cost_per_user]
            elif step['name'] == "Drafting Outreach Email": step['args'] = [project_idea, st.session_state.results['market_research']]
            elif step['name'] == "Pitch Deck Generation": step['args'] = [st.session_state.results['market_research'], st.session_state.results['competitor_analysis'], project_idea, st.session_state.results['financials'], st.session_state.results['tech_stack']]

            result = step['tool'](*step['args'])
            st.session_state.results[step['output_key']] = result
            st.markdown(f"**Output Preview:**\n\n{result[:250]}...")
            status.update(label=f"✅ {step['name']} Complete!", state="complete", expanded=False)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">🤖 Archimedes Agent</div>', unsafe_allow_html=True)
    st.markdown("Your end-to-end AI Co-founder with live web access.")
    st.divider()
    st.subheader("Your Big Idea")
    project_input = st.text_area("Describe your project idea:", height=120, placeholder="e.g., A mobile app that uses AI to create personalized workout plans...", value=st.session_state.project_idea, key="project_idea_input")
    
    st.subheader("Financial Inputs")
    price_input = st.number_input("Price per User/Year ($)", min_value=0.0, value=st.session_state.price_point, step=5.0, key="price_point_input")
    cost_input = st.number_input("Est. Cost per User/Year ($)", min_value=0.0, value=st.session_state.cost_per_user, step=1.0, key="cost_per_user_input")
    
    st.session_state.project_idea = project_input
    st.session_state.price_point = price_input
    st.session_state.cost_per_user = cost_input

    st.divider()
    if st.button("Reset Analysis"):
        st.session_state.results = {}
        st.rerun()
    st.info("© 2024 Archimedes AI.")

# --- 6. MAIN PAGE ---
st.title("Autonomous Co-Founder Agent")
st.markdown("Provide your idea and financial assumptions. The agent will perform a full, web-augmented analysis.")
if not st.session_state.project_idea:
    st.info("Enter your project idea and financial inputs in the sidebar to activate the agent.")
    st.stop()

if st.button("🚀 Launch Full Autonomous Analysis", use_container_width=True):
    st.session_state.results = {}
    run_agentic_workflow(st.session_state.project_idea, st.session_state.price_point, st.session_state.cost_per_user)

st.divider()

# --- 7. DISPLAY RESULTS ---
if st.session_state.results:
    st.header("Analysis Complete: Review Your Assets")
    tabs = st.tabs(["🎨 Brand", "📊 Market", "⚔️ Competitors", "🛠️ Tech", "💰 Financials", "📝 Pitch Deck", "💌 Outreach"])
    
    with tabs[0]: st.markdown(st.session_state.results.get("branding", "Not generated."))
    with tabs[1]: st.markdown(st.session_state.results.get("market_research", "Not generated."))
    with tabs[2]: st.markdown(st.session_state.results.get("competitor_analysis", "Not generated."))
    with tabs[3]: st.markdown(st.session_state.results.get("tech_stack", "Not generated."))
    with tabs[4]: st.markdown(st.session_state.results.get("financials", "Not generated."))
    with tabs[5]: 
        st.markdown(st.session_state.results.get("pitch_deck", "Not generated."))
        if "pitch_deck" in st.session_state.results:
            st.download_button("⬇️ Download Pitch Deck", st.session_state.results["pitch_deck"], "pitch_deck.md")
    with tabs[6]: 
        st.markdown(st.session_state.results.get("outreach_email", "Not generated."))
        if "outreach_email" in st.session_state.results:
            st.download_button("⬇️ Download Email", st.session_state.results["outreach_email"], "outreach_email.txt")