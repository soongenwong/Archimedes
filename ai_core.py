import os
import requests
import json
from mistralai.client import MistralClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
MODEL_NAME = "mistral-large-latest"
client = MistralClient(api_key=MISTRAL_API_KEY)

# --- Helper Function for Web Search ---
def web_search_tool(query: str):
    """Performs a live Google search using Serper API."""
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {'X-API-KEY': SERPER_API_KEY, 'Content-Type': 'application/json'}
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status() # Raise an exception for bad status codes
        return json.dumps(response.json())
    except requests.exceptions.RequestException as e:
        return f"Error during web search: {e}"

# --- Core Tool Functions ---
def generate_response(system_prompt, user_prompt):
    """Generic Mistral AI call."""
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
    try:
        chat_response = client.chat(model=MODEL_NAME, messages=messages, temperature=0.7)
        return chat_response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# --- MODIFIED: Foundational Tool with Web Research ---
def generate_market_research_with_web(project_idea):
    """Generates market research report using live web data."""
    system_prompt = """
    You are a world-class market research analyst. You will be given a project idea and a set of LIVE web search results.
    You MUST use the provided web results to inform your analysis, especially for Market Size and Key Trends.
    Cite your sources by mentioning the website (e.g., 'According to TechCrunch...').
    Format your output strictly in Markdown.
    """
    # Agent Step 1: Perform a web search
    search_query = f"market size, trends, and target audience for a product like '{project_idea}'"
    search_results = web_search_tool(search_query)
    
    # Agent Step 2: Analyze the results
    user_prompt = f"""
    Please generate a market research report based on the following information.

    **Project Idea:**
    {project_idea}

    **Live Web Search Results:**
    {search_results}

    ---
    Produce the report with these sections:
    - **Target Audience:**
    - **Market Size (TAM, SAM, SOM):**
    - **Key Trends & Opportunities:**
    - **Potential Risks & Challenges:**
    """
    return generate_response(system_prompt, user_prompt)

# --- UNCHANGED TOOLS ---
def generate_competitor_analysis(project_idea):
    """(Unchanged) Generates competitor analysis."""
    # This could also be upgraded with web search to find competitors, but we'll keep it simple for now.
    system_prompt = "You are a competitive intelligence strategist. Format your output strictly in Markdown."
    user_prompt = f"""Given the project idea "{project_idea}", identify key competitors. Structure your output as a clear list."""
    return generate_response(system_prompt, user_prompt)

def generate_project_names(project_idea):
    """(Unchanged) Generates potential project names, taglines, and brand identity."""
    system_prompt = "You are a world-class branding expert. Format your output strictly in Markdown."
    user_prompt = f"""Project Idea: "{project_idea}". Generate 5 project name suggestions, 3 taglines, and a core brand identity (vibe, keywords)."""
    return generate_response(system_prompt, user_prompt)

def generate_outreach_email(project_idea, market_research):
    """(Unchanged) Generates a cold outreach email template."""
    system_prompt = "You are a growth marketer, expert at writing concise and effective cold outreach emails to get user feedback."
    user_prompt = f"Based on the project idea '{project_idea}' and target audience from the market research '{market_research}', write a personalized email template to find users for interviews."
    return generate_response(system_prompt, user_prompt)
    
# --- NEW: Advanced Tools ---
def recommend_tech_stack(project_idea):
    """Recommends a technology stack for the project."""
    system_prompt = """
    You are a veteran Chief Technology Officer (CTO). Your job is to recommend a robust and scalable technology stack for a new project.
    Provide clear recommendations for each category and a brief, strong justification for your choice.
    Format the output as a clean Markdown list.
    """
    user_prompt = f"""
    Based on the project idea "{project_idea}", please recommend a full technology stack. Include the following categories:
    - **Frontend:** (e.g., Web Framework, Mobile Framework)
    - **Backend:** (e.g., Language, Framework)
    - **Database:** (e.g., SQL, NoSQL)
    - **Cloud & Deployment:** (e.g., Hosting Provider, CI/CD)
    - **AI/ML Services:** (If applicable)
    """
    return generate_response(system_prompt, user_prompt)

def generate_financial_projections(market_research, price_point, cost_per_user):
    """Generates a simple 3-year financial projection."""
    system_prompt = """
    You are a financial analyst for a Venture Capital firm. You specialize in creating simple, back-of-the-napkin financial models for early-stage startups.
    You will be given market research data, a price point, and a cost per user.
    - Use the SOM (Serviceable Obtainable Market) as the maximum number of users you can capture.
    - Assume a realistic market penetration growth rate over 3 years (e.g., Year 1: 1%, Year 2: 3%, Year 3: 7% of SOM).
    - Calculate Revenue, Costs, and Profit.
    - Present the output as a clean, formatted Markdown table.
    """
    user_prompt = f"""
    Please generate a 3-year financial projection based on the following data:

    **Market Research Data (for SOM):**
    {market_research}

    **User Inputs:**
    - Price per user (per year): ${price_point}
    - Cost per user (per year): ${cost_per_user}
    
    ---
    Generate the 3-year projection now. Include your assumptions about market penetration.
    """
    return generate_response(system_prompt, user_prompt)

def generate_pitch_deck_slides(market_research, competitor_analysis, project_idea, financial_projections, tech_stack):
    """(Upgraded) Generates pitch deck slides, now including financial and tech info."""
    system_prompt = "You are a startup co-founder and expert storyteller. Synthesize the provided information into compelling, concise text for a pitch deck. Use Markdown headings for slides."
    user_content = f"""
    Synthesize all the following info into key pitch deck slides.

    **Project Idea:** {project_idea}
    **Market Research:** {market_research}
    **Competitor Analysis:** {competitor_analysis}
    **Financial Projections:** {financial_projections}
    **Technology:** {tech_stack}

    ---
    Generate content for these slides:
    ### The Problem
    ### The Solution
    ### The Market Opportunity
    ### The Competition
    ### Business Model & Financials
    ### Our Technology
    """
    return generate_response(system_prompt, user_content)