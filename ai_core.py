import os
from mistralai.client import MistralClient
# from mistralai.models.chat_completion import ChatMessage # <-- REMOVED THIS LINE
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL_NAME = "mistral-small-latest" # or "mistral-large-latest" for higher quality

# --- Initialize Mistral Client ---
try:
    client = MistralClient(api_key=API_KEY)
except Exception as e:
    print(f"Error initializing Mistral client: {e}")
    client = None

def generate_response(system_prompt, user_prompt):
    """
    A generic function to get a response from Mistral AI.
    """
    if not client:
        return "Error: Mistral client is not initialized. Please check your API key."
    
    # --- THIS IS THE MAIN CHANGE ---
    # Instead of using the ChatMessage class, we now use a simple list of dictionaries.
    # This is the modern, recommended way.
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        chat_response = client.chat(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
        )
        return chat_response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while communicating with the API: {e}"

# --- Specific Generation Functions (No changes needed below this line) ---

def generate_market_research(project_idea):
    """Generates market research report."""
    system_prompt = """
    You are a world-class market research analyst for a top venture capital firm. 
    Your analysis is sharp, concise, and backed by logical reasoning.
    You will be given a project idea and you must produce a market research summary.
    Format your output strictly in Markdown with the following sections:
    - **Target Audience:** Describe the primary and secondary customer segments.
    - **Market Size (TAM, SAM, SOM):** Provide a high-level estimate and justification for the Total Addressable Market, Serviceable Addressable Market, and Serviceable Obtainable Market.
    - **Key Trends & Opportunities:** Identify 3-5 major trends in this market.
    - **Potential Risks & Challenges:** List the most significant hurdles this project might face.
    """
    return generate_response(system_prompt, f"Project Idea: {project_idea}")

def generate_competitor_analysis(project_idea):
    """Generates competitor analysis."""
    system_prompt = """
    You are a competitive intelligence strategist. You excel at identifying and dissecting competitors.
    Given a project idea, you must identify key competitors and analyze them.
    Format your output strictly in Markdown with the following structure:
    - **Direct Competitors (Top 2):**
      - **Competitor 1:** [Name]
        - *What they do:*
        - *Key Strengths:*
        - *Key Weaknesses:*
      - **Competitor 2:** [Name]
        - *What they do:*
        - *Key Strengths:*
        - *Key Weaknesses:*
    - **Indirect Competitors / Alternatives (Top 2):**
      - **Competitor 1:** [Name]
        - *How they are an alternative:*
        - *Why a customer might choose them:*
    """
    return generate_response(system_prompt, f"Project Idea: {project_idea}")

def generate_pitch_deck_slides(market_research, competitor_analysis, project_idea):
    """Generates text for key pitch deck slides."""
    system_prompt = """
    You are a startup co-founder and expert storyteller tasked with writing the content for a pitch deck.
    You will be given a project idea, market research, and competitor analysis.
    Your job is to synthesize this information into compelling, concise text for the key slides of a pitch deck.
    Generate content for the following slides using Markdown headings:

    ### Slide 2: The Problem
    (Describe the core pain point in 1-2 powerful sentences.)

    ### Slide 3: The Solution
    (Introduce your project as the clear solution. Start with "We are building [Your Project Name], which...")

    ### Slide 4: Market Opportunity
    (Summarize the most exciting parts of the market research.)

    ### Slide 5: The Competition
    (Briefly summarize the competitive landscape and state your unique advantage.)
    """
    user_content = f"""
    Here is all the information for the pitch deck.

    **Project Idea:**
    {project_idea}

    ---

    **Market Research Document:**
    {market_research}

    ---

    **Competitor Analysis Document:**
    {competitor_analysis}
    """
    return generate_response(system_prompt, user_content)