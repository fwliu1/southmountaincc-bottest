import streamlit as st
import google.generativeai as genai

# Initialize session state
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'context' not in st.session_state:
    st.session_state.context = ""

def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def get_gemini_response(model, question, user_type, context):
    user_type_prompts = {
        "Kid": "You are talking to a child. Use simple language and explanations suitable for children. Keep responses brief and engaging.",
        "Adult": "You are conversing with an adult. Provide detailed and comprehensive responses.",
        "Senior": "You are speaking with a senior citizen. Be respectful, patient, and use clear language. Consider potential health or technology-related concerns in your responses."
    }
    
    full_prompt = f"""
    {context}

    You are an AI assistant for South Mountain Community College Gaudalupe Center. Always be helpful, friendly, and informative. 
    {user_type_prompts.get(user_type, '')}
    
    If asked about information not provided in the context, politely state that you don't have that specific information 
    and offer to help with general inquiries or direct them to contact the center's staff for the most up-to-date information.

    Human: {question}
    AI Assistant:
    """
    response = model.generate_content(full_prompt)
    return response.text

# Streamlit app
st.title("Guadalupe Center Assistant")

# Sidebar for context input (for demo purposes, normally this would be pre-set)
#st.sidebar.title("Set Envision Center Information")
context_input = """
LOCATION: South Mountain Community College Guadalupe Center
ADDRESS: 9233 S. Avenida del Yaqui (Priest Drive)

CONTACT_INFORMATION:
- Hours: Monday-Thursday, 8:00 AM - 5:00 PM
- Email: extended.campuses@southmountaincc.edu
- Phone: 602-243-8217

FACILITY_DESCRIPTION:
- Type: Educational center
- Operating_history: 20+ years
- Service_areas: Tempe, Phoenix, Chandler, Ahwatukee, Guadalupe
- Schedule_focus: Afternoon and evening classes
- Target_audience: Working adults and general community

SERVICES:
1. Student Support:
   - Admissions assistance
   - Academic advising
   - Registration support
   - Financial aid/scholarship services
   - Transfer guidance to Arizona universities

2. Academic Resources:
   - Tutoring
   - Access to academic software
   - Workshops and seminars
   - Training programs

3. Specialized Services:
   - Veterans assistance
   - Pascua Yaqui Higher Education Assistance

COMMUNITY_FEATURES:
- Diverse cultural environment
- Regular community celebrations and events
- Partnership with Guadalupe community

KEY_BENEFITS:
- Convenient location
- Affordable education
- Support for first-time college students
- Transfer pathways to 4-year universities

COMMUNITY PARTNERS:
- IDIA, http://theidia.org
- If people ask questions about the hive, please look up the answers online about the hive or direct them to this link

If there is anything you don't know, please look it up online and tell the guest.
    """

#if st.sidebar.button("Update Center Information"):
st.session_state.context = context_input
#    st.sidebar.success("Envision Center information updated!")

# API key input
api_key = st.secrets["APIKEY"]
#st.text_input("Enter your Gemini API Key:", type="password")

if api_key:
    # Initialize the model
    model = initialize_gemini(api_key)

    # User type selection
    st.subheader("Select Your User Type:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Kid"):
            st.session_state.user_type = "Kid"
    with col2:
        if st.button("Adult"):
            st.session_state.user_type = "Adult"
    with col3:
        if st.button("Senior"):
            st.session_state.user_type = "Senior"

    # Display selected user type
    if st.session_state.user_type:
        st.write(f"Selected User Type: {st.session_state.user_type}")

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("How can I help you with at the Guadalupe Center?"):
        if st.session_state.user_type:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get and display Gemini response
            response = get_gemini_response(model, prompt, st.session_state.user_type, st.session_state.context)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)
        else:
            st.warning("Please select a user type before asking questions.")

else:
    st.warning("Please enter your Gemini API Key to start.")

# Instructions
st.sidebar.title("How to Use")
st.sidebar.markdown("""
1. Select your user type (Kid, Adult, or Senior).
2. Ask questions about Guadalupe Center in the chat interface.
3. The AI will provide information based on your user type and the center's details.

Quick Links:
* Guadalupe Center Website: https://www.southmountaincc.edu/about/locations/guadalupe-center

""")