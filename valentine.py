import streamlit as st
import random

# Configure page
st.set_page_config(
    page_title="Valentine's Adventure ❤️",
    page_icon="❤️",
    layout="centered"
)

# Initialize all session state variables
if 'stage' not in st.session_state:
    st.session_state.stage = 'name_input'
if 'q_number' not in st.session_state:
    st.session_state.q_number = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'no_count' not in st.session_state:
    st.session_state.no_count = 0
if 'accepted' not in st.session_state:
    st.session_state.accepted = False
if 'previous_stages' not in st.session_state:
    st.session_state.previous_stages = []
if 'partner_name' not in st.session_state:
    st.session_state.partner_name = ""

# Add floating hearts
for _ in range(15):
    st.markdown(f'<div style="position: fixed; left: {random.randint(0, 100)}%; \
                top: {random.randint(0, 100)}%; font-size: 2em; opacity: 0.7;">❤️</div>', 
                unsafe_allow_html=True)

# Navigation function
def go_back():
    if st.session_state.previous_stages:
        previous_stage = st.session_state.previous_stages.pop()
        st.session_state.stage = previous_stage
        st.rerun()

# Show back button when appropriate
if len(st.session_state.previous_stages) > 0 and st.session_state.stage not in ['name_input', 'proposal']:
    if st.button("⬅️"):
        go_back()

# Name input page
if st.session_state.stage == 'name_input':
    st.title("💖 Valentine's Adventure 💖")
    
    partner_name = st.text_input("Enter your name:")
    
    if st.button("Continue ❤️") and partner_name.strip():
        st.session_state.partner_name = partner_name
        st.session_state.previous_stages.append('name_input')
        st.session_state.stage = 'questions'
        st.rerun()

# Questions database
questions = [
    {
        "q": "What's your perfect date? 🌹",
        "options": ["Netflix and chill 🍿", "Fancy dinner 🍷", "Adventure hiking 🥾", "Pajama party 🛌"]
    },
    {
        "q": "What's my best feature? 👀",
        "options": ["Your smile 😁", "Your eyes 👁️", "Your humor 🤣", "Your hugs 🤗"]
    },
    {
        "q": "What would you rather have? 🎁",
        "options": ["Eternal snacks 🍕", "Kisses 🐶", "Free massages 💆", "All of the above(Don be greedy ,chuz one) "]
    }
]

# Questions page
if st.session_state.stage == 'questions':
    st.title("Valentine's Quiz Time! ❤️")
    st.markdown(f"### Hey {st.session_state.partner_name}, answer 3 questions! ")
    
    if st.session_state.q_number < len(questions):
        current_q = questions[st.session_state.q_number]
        
        st.subheader(f"Question {st.session_state.q_number + 1}:")
        st.markdown(f"### {current_q['q']}")

        cols = st.columns(2)
        for i, option in enumerate(current_q['options']):
            if cols[i % 2].button(option, key=f"q{st.session_state.q_number}_opt{i}"):
                st.session_state.answers[st.session_state.q_number] = option
                st.session_state.q_number += 1
                st.rerun()
        
        st.progress((st.session_state.q_number) / 3)
    else:
        st.balloons()
        st.subheader("Quiz Complete! 🎉")
        st.markdown("**Your answers:**")
        for i, answer in st.session_state.answers.items():
            st.markdown(f"{i+1}. {answer}")
        
        if st.button("Reveal My Surprise! 🎁"):
            st.session_state.previous_stages.append('questions')
            st.session_state.stage = 'reveal_confirm'
            st.rerun()

# Reveal confirmation page
if st.session_state.stage == 'reveal_confirm':
    st.title("💌 Special Message Alert! 💌")
    st.markdown(f"### {st.session_state.partner_name}, ready for your surprise?")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif", width=300)
    
    if st.button("Show Me the Love! ❤️"):
        st.session_state.previous_stages.append('reveal_confirm')
        st.session_state.stage = 'proposal'
        st.rerun()

# Proposal page
# Proposal page
if st.session_state.stage == 'proposal':
    if st.session_state.accepted:
        st.balloons()
        st.title(" Wagwan!🎉")
        st.markdown(f"## {st.session_state.partner_name},You've made me the happiest!, I can't wait to celebrate with you! 💖")
    else:
        st.title("🌸 Valentine's Day Special 🌸")
        st.markdown(f"### My Dearest {st.session_state.partner_name},")
        
        st.markdown("## Will you be my Valentine? 💌")

        cols = st.columns(5)
        button_pos = random.randint(0, 4) if st.session_state.no_count > 0 else 2

        # Yes button
        if cols[2].button("YES! 💖", key="yes"):
            st.session_state.accepted = True
            st.rerun()

        # No button
        no_button = cols[button_pos].button(
            "No... 😢" if st.session_state.no_count == 0 else 
            f"No... ({st.session_state.no_count}x) 😭",
            key=f"no_{button_pos}"
        )

        if no_button:
            st.session_state.no_count += 1
            st.error(" 🚨 Alert! Cutest partner detected! Please reconsider! 🥺")
            st.rerun()

        responses = [
            "I'll keep asking until you say yes! 💘",
            "My heart is breaking... 💔",
            "Is that your final answer? 🥺",
            "Pretty please with a cherry on top? 🍒",
            "I'll love you forever! 💑"
        ]
        
        if st.session_state.no_count > 0:
            response_index = min(st.session_state.no_count-1, len(responses)-1)
            st.warning(responses[response_index])
