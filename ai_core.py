import os
from mistralai.client import MistralClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL_NAME = "mistral-large-latest" # Using a more powerful model for creative tasks
client = MistralClient(api_key=API_KEY)

def generate_response(system_prompt, user_prompt):
    """A generic function to get a response from Mistral AI."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    try:
        chat_response = client.chat(model=MODEL_NAME, messages=messages, temperature=0.8)
        return chat_response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# --- Foundational Analysis Tools (Existing) ---

def generate_market_research(project_idea):
    """Generates market research report."""
    system_prompt = "You are a world-class market research analyst. Your analysis is sharp, concise, and formatted strictly in Markdown."
    user_prompt = f"""
    Based on the project idea "{project_idea}", produce a market research summary with these sections:
    - **Target Audience:** Describe primary and secondary customer segments.
    - **Market Size (TAM, SAM, SOM):** Provide a high-level estimate and justification.
    - **Key Trends & Opportunities:** Identify 3-5 major trends.
    - **Potential Risks & Challenges:** List the most significant hurdles.
    """
    return generate_response(system_prompt, user_prompt)

def generate_competitor_analysis(project_idea):
    """Generates competitor analysis."""
    system_prompt = "You are a competitive intelligence strategist. You excel at identifying and dissecting competitors. Format your output strictly in Markdown."
    user_prompt = f"""
    Given the project idea "{project_idea}", identify key competitors. Structure your output like this:
    - **Direct Competitors (Top 2):**
      - **Competitor 1:** [Name]
        - *What they do:* | *Key Strengths:* | *Key Weaknesses:*
      - **Competitor 2:** [Name]
        - *What they do:* | *Key Strengths:* | *Key Weaknesses:*
    - **Indirect Competitors / Alternatives (Top 2):**
      - **Competitor 1:** [Name]
        - *How they are an alternative:* | *Why a customer might choose them:*
    """
    return generate_response(system_prompt, user_prompt)

def generate_pitch_deck_slides(market_research, competitor_analysis, project_idea):
    """Generates text for key pitch deck slides."""
    system_prompt = "You are a startup co-founder and expert storyteller. Synthesize the provided information into compelling, concise text for a pitch deck. Use Markdown headings for slides."
    user_content = f"""
    Synthesize the following info into pitch deck slides (Problem, Solution, Market, Competition).

    **Project Idea:** {project_idea}
    **Market Research:** {market_research}
    **Competitor Analysis:** {competitor_analysis}
    """
    return generate_response(system_prompt, user_content)

# --- NEW: Interactive and Creative Tools ---

def generate_project_names(project_idea):
    """Generates potential project names, taglines, and brand identity."""
    system_prompt = """
    You are a world-class branding expert and creative director. You have a knack for creating memorable and fitting names for tech startups.
    You will generate a branding kit based on a project idea.
    Format your output strictly in Markdown.
    """
    user_prompt = f"""
    Project Idea: "{project_idea}"

    Based on this idea, generate the following:
    
    ### 🚀 Project Name Suggestions (5 options)
    Provide 5 creative, modern, and available-sounding names. For each name, give a brief rationale.
    
    ### 🏷️ Tagline Suggestions (3 options)
    Write 3 short, punchy taglines that capture the essence of the project.
    
    ### 🎨 Core Brand Identity
    - **Vibe:** (e.g., Energetic & Motivating, Calm & Trustworthy, Innovative & Futuristic)
    - **Keywords:** (List 5 keywords associated with the brand)
    """
    return generate_response(system_prompt, user_prompt)

def generate_outreach_email(project_idea, market_research):
    """Generates a cold outreach email template for user interviews."""
    system_prompt = """
    You are a growth marketer and startup founder, expert at writing concise and effective cold outreach emails to get user feedback.
    The goal is NOT to sell, but to learn. The email should be short, personal, and offer value to the recipient (the chance to shape a new product).
    """
    user_prompt = f"""
    Based on the project below, write a template for an outreach email to find potential users for interviews.
    Use placeholders like `[Prospect Name]`, `[Your Name]`, and `[Your Project Name]`.

    **Project Idea:**
    {project_idea}

    **Target Audience (from market research):**
    {market_research}

    ---
    Generate the email template now.
    """
    return generate_response(system_prompt, user_prompt)