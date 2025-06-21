import streamlit as st
from ai_core import generate_market_research, generate_competitor_analysis, generate_pitch_deck_slides

# --- Page Configuration ---
st.set_page_config(
    page_title="Archimedes AI Co-Founder",
    page_icon="🚀",
    layout="wide"
)

# --- State Management ---
# Using session_state to hold data across reruns
if 'project_idea' not in st.session_state:
    st.session_state.project_idea = ""
if 'market_research' not in st.session_state:
    st.session_state.market_research = ""
if 'competitor_analysis' not in st.session_state:
    st.session_state.competitor_analysis = ""
if 'pitch_deck' not in st.session_state:
    st.session_state.pitch_deck = ""

# --- UI Rendering ---
st.title("🚀 Archimedes: Your AI Co-Founder")
st.markdown("Automate the boring parts of launching your project. Let's build something great together.")

st.divider()

# --- STEP 1: Get Project Idea ---
st.subheader("1. Define Your Project")
project_input = st.text_input(
    "Enter your project idea in one sentence:",
    placeholder="e.g., A mobile app that uses AI to create personalized workout plans for busy professionals.",
    value=st.session_state.project_idea
)

if project_input:
    st.session_state.project_idea = project_input

# --- STEP 2: Main Dashboard (only shows if there's a project idea) ---
if st.session_state.project_idea:
    st.divider()
    st.subheader("2. Founder's Dashboard")
    
    # Create tabs for each module
    tab1, tab2, tab3 = st.tabs(["📊 Market Research", "⚔️ Competitor Analysis", "📝 Pitch Deck"])

    # --- Market Research Tab ---
    with tab1:
        st.header("Market Research")
        if st.button("Generate Market Research Report"):
            with st.spinner("Archimedes is analyzing the market..."):
                st.session_state.market_research = generate_market_research(st.session_state.project_idea)
        
        if st.session_state.market_research:
            st.markdown(st.session_state.market_research)

    # --- Competitor Analysis Tab ---
    with tab2:
        st.header("Competitor Analysis")
        if st.button("Generate Competitor Analysis"):
            with st.spinner("Archimedes is investigating the competition..."):
                st.session_state.competitor_analysis = generate_competitor_analysis(st.session_state.project_idea)
        
        if st.session_state.competitor_analysis:
            st.markdown(st.session_state.competitor_analysis)

    # --- Pitch Deck Tab ---
    with tab3:
        st.header("Pitch Deck Content")
        st.info("This module uses the results from the other tabs to generate your pitch.")
        
        # Check if prerequisites are met
        if not st.session_state.market_research or not st.session_state.competitor_analysis:
            st.warning("Please generate the Market Research and Competitor Analysis reports first.")
        else:
            if st.button("Generate Pitch Deck Content"):
                with st.spinner("Archimedes is drafting your story..."):
                    st.session_state.pitch_deck = generate_pitch_deck_slides(
                        st.session_state.market_research,
                        st.session_state.competitor_analysis,
                        st.session_state.project_idea
                    )
            
            if st.session_state.pitch_deck:
                st.markdown(st.session_state.pitch_deck)
                st.download_button(
                    "Download Pitch Deck Text",
                    st.session_state.pitch_deck,
                    file_name="pitch_deck_content.md"
                )