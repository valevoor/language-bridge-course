"""
Interactive Kannada-English STEM Bridge Course Application.
A web-based learning app for students to master English STEM terminologies for native Kannada words.
"""

import os
import json
import random
import streamlit as st
from typing import List, Dict, Any

# Set Streamlit page config
st.set_page_config(
    page_title="Kannada-English STEM Bridge Course",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

TARGET_DIR = "/Users/vishwa/Dev/language-bridge-course/target"
DATA_FILE = os.path.join(TARGET_DIR, "stem_keywords_chapterwise.json")
FLASHCARDS_FILE = os.path.join(TARGET_DIR, "stem_flashcards.json")


@st.cache_data
def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_flashcards():
    if not os.path.exists(FLASHCARDS_FILE):
        return []
    with open(FLASHCARDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


data = load_data()

# Custom CSS for kid-friendly UI styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .card-box {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border: 2px solid #BAE6FD;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .flashcard-front {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 3px solid #3B82F6;
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.2);
    }
    .flashcard-back {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 3px solid #10B981;
        border-radius: 20px;
        padding: 40px 20px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.2);
    }
    .kannada-word {
        font-size: 2.6rem;
        font-weight: bold;
        color: #1E293B;
        margin-bottom: 8px;
    }
    .transliteration {
        font-size: 1.3rem;
        font-style: italic;
        color: #64748B;
        margin-bottom: 12px;
    }
    .english-word {
        font-size: 2.4rem;
        font-weight: 800;
        color: #047857;
        margin-bottom: 12px;
    }
    .tag {
        display: inline-block;
        background-color: #E2E8F0;
        color: #334155;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<div class='main-header'>🎓 Kannada ➔ English STEM Bridge Course</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Helping young minds transition from native Kannada medium to English STEM terminologies</div>", unsafe_allow_html=True)

if not data:
    st.error("⚠️ Extracted data not found! Please run the extraction pipeline first.")
    st.stop()

# Sidebar Navigation
st.sidebar.title("🧭 Navigation")
app_mode = st.sidebar.radio(
    "Choose Learning Mode:",
    [
        "📖 Chapter Explorer & Glossary",
        "🎴 Interactive Flashcards",
        "🎮 Quiz & Practice Challenge",
        "🧩 Term Matcher Game",
        "🔍 Bilingual Search Dictionary",
        "📊 Learning Analytics"
    ]
)

# Chapter filter in sidebar
chapters = data.get("chapters", [])
chapter_options = ["All Chapters"] + [f"Chapter {ch['chapter_num']}: {ch['chapter_title_kn']} ({ch['chapter_title_en']})" for ch in chapters]
selected_chapter_option = st.sidebar.selectbox("Filter by Chapter:", chapter_options)

# Helper to filter keywords
def get_filtered_keywords():
    if selected_chapter_option == "All Chapters":
        all_kws = []
        for ch in chapters:
            for kw in ch.get("keywords", []):
                item = dict(kw)
                item["chapter_num"] = ch["chapter_num"]
                item["chapter_title"] = ch["chapter_title_en"]
                all_kws.append(item)
        return all_kws
    else:
        ch_idx = chapter_options.index(selected_chapter_option) - 1
        ch = chapters[ch_idx]
        filtered = []
        for kw in ch.get("keywords", []):
            item = dict(kw)
            item["chapter_num"] = ch["chapter_num"]
            item["chapter_title"] = ch["chapter_title_en"]
            filtered.append(item)
        return filtered

# ==========================================
# MODE 1: CHAPTER EXPLORER & GLOSSARY
# ==========================================
if app_mode == "📖 Chapter Explorer & Glossary":
    st.header("📖 Chapter-wise STEM Glossary")
    st.write("Browse through foundational terms, read kid-friendly bilingual definitions, and master the English terms!")

    filtered_kws = get_filtered_keywords()
    st.info(f"Showing **{len(filtered_kws)}** STEM key words")

    for kw in filtered_kws:
        with st.container():
            st.markdown(f"""
            <div class='card-box'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <span class='kannada-word'>{kw['kannada_term']}</span>
                        <span class='transliteration'>({kw['transliteration']})</span>
                    </div>
                    <div>
                        <span class='tag'>🏷️ {kw['category']}</span>
                        <span class='tag' style='background-color:#FEF3C7; color:#92400E;'>📍 Chapter {kw.get('chapter_num', '')}</span>
                    </div>
                </div>
                <div style='margin-top: 12px;'>
                    <span style='font-size: 1.4rem; font-weight: 700; color: #0284C7;'>➔ English: {kw['english_term']}</span>
                </div>
                <hr style='margin: 12px 0; border: none; border-top: 1px solid #E2E8F0;'/>
                <p><b>📖 ಕನ್ನಡ ವಿವರಣೆ:</b> {kw['definition_kn']}</p>
                <p><b>📖 English Definition:</b> {kw['definition_en']}</p>
                <p><b>💡 Example:</b> <code style='background-color:#E0F2FE; padding: 2px 6px; border-radius: 4px;'>{kw['example_kn']}</code> ➔ <code style='background-color:#DCFCE7; padding: 2px 6px; border-radius: 4px;'>{kw['example_en']}</code></p>
                {"<p style='color: #4338CA;'><b>🧠 Bridge Memory Tip:</b> <i>" + kw['mnemonic_or_tip'] + "</i></p>" if kw.get('mnemonic_or_tip') else ""}
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# MODE 2: INTERACTIVE FLASHCARDS
# ==========================================
elif app_mode == "🎴 Interactive Flashcards":
    st.header("🎴 Interactive STEM Flashcards")
    st.write("Test your memory! Read the Kannada term, recall the English STEM term, and flip to verify.")

    flashcards = load_flashcards()
    if selected_chapter_option != "All Chapters":
        ch_idx = chapter_options.index(selected_chapter_option) - 1
        ch_num = chapters[ch_idx]["chapter_num"]
        flashcards = [fc for fc in flashcards if fc["chapter_num"] == ch_num]

    if not flashcards:
        st.warning("No flashcards found for this selection.")
    else:
        if "card_index" not in st.session_state:
            st.session_state.card_index = 0
        if "flipped" not in st.session_state:
            st.session_state.flipped = False

        if st.session_state.card_index >= len(flashcards):
            st.session_state.card_index = 0

        current_card = flashcards[st.session_state.card_index]

        col1, col2, col3 = st.columns([1, 4, 1])

        with col2:
            st.progress((st.session_state.card_index + 1) / len(flashcards))
            st.caption(f"Card {st.session_state.card_index + 1} of {len(flashcards)} (Chapter {current_card['chapter_num']}: {current_card['chapter_title']})")

            if not st.session_state.flipped:
                st.markdown(f"""
                <div class='flashcard-front'>
                    <span class='tag'>🏷️ {current_card['category']}</span>
                    <div style='height: 20px;'></div>
                    <div class='kannada-word'>{current_card['front_kannada']}</div>
                    <div class='transliteration'>Pronounced: "{current_card['transliteration']}"</div>
                    <div style='height: 20px;'></div>
                    <div style='color: #6B7280; font-size: 0.95rem;'>Can you recall the English STEM term?</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='flashcard-back'>
                    <span class='tag' style='background-color:#A7F3D0; color:#065F46;'>✅ English STEM Term</span>
                    <div style='height: 15px;'></div>
                    <div class='english-word'>{current_card['back_english']}</div>
                    <div style='color: #1F2937; margin-bottom: 10px;'><b>Native:</b> {current_card['front_kannada']} ({current_card['transliteration']})</div>
                    <div style='background: white; padding: 12px; border-radius: 10px; margin-top: 10px; text-align: left; border: 1px solid #A7F3D0;'>
                        <p style='margin:0; font-size: 0.95rem;'><b>Definition:</b> {current_card['definition_en']}</p>
                        <p style='margin:5px 0 0 0; font-size: 0.95rem;'><b>Example:</b> {current_card['example_en']}</p>
                        {"<p style='margin:5px 0 0 0; font-size: 0.9rem; color: #047857;'><b>💡 Tip:</b> " + current_card['hint'] + "</p>" if current_card.get('hint') else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                if st.button("⬅️ Previous", use_container_width=True):
                    st.session_state.card_index = (st.session_state.card_index - 1) % len(flashcards)
                    st.session_state.flipped = False
                    st.rerun()
            with btn_col2:
                flip_label = "🔄 Show Answer" if not st.session_state.flipped else "🔄 Show Kannada"
                if st.button(flip_label, use_container_width=True, type="primary"):
                    st.session_state.flipped = not st.session_state.flipped
                    st.rerun()
            with btn_col3:
                if st.button("➡️ Next", use_container_width=True):
                    st.session_state.card_index = (st.session_state.card_index + 1) % len(flashcards)
                    st.session_state.flipped = False
                    st.rerun()

# ==========================================
# MODE 3: QUIZ & PRACTICE CHALLENGE
# ==========================================
elif app_mode == "🎮 Quiz & Practice Challenge":
    st.header("🎮 STEM Bridge Quiz Challenge")
    st.write("Pick the correct English STEM terminology for each Kannada mathematical concept!")

    all_kws = get_filtered_keywords()
    if len(all_kws) < 4:
        st.warning("Need at least 4 keywords to generate a quiz.")
    else:
        if "quiz_index" not in st.session_state:
            st.session_state.quiz_index = 0
            st.session_state.score = 0
            st.session_state.quiz_answered = False
            st.session_state.selected_option = None

        total_questions = min(10, len(all_kws))
        
        if st.session_state.quiz_index < total_questions:
            q_target = all_kws[st.session_state.quiz_index]
            
            # Generate 4 options (1 correct, 3 distractors)
            if "options" not in st.session_state or st.session_state.get("last_q_idx") != st.session_state.quiz_index:
                correct = q_target["english_term"]
                distractors = [k["english_term"] for k in all_kws if k["english_term"] != correct]
                sample_distractors = random.sample(distractors, min(3, len(distractors)))
                options = sample_distractors + [correct]
                random.shuffle(options)
                st.session_state.options = options
                st.session_state.last_q_idx = st.session_state.quiz_index
                st.session_state.quiz_answered = False

            st.subheader(f"Question {st.session_state.quiz_index + 1} of {total_questions}")
            
            st.markdown(f"""
            <div style='background: #F8FAFC; border: 2px solid #CBD5E1; border-radius: 12px; padding: 20px; margin-bottom: 20px;'>
                <div style='font-size: 1.1rem; color: #64748B;'>What is the English STEM term for:</div>
                <div style='font-size: 2.2rem; font-weight: bold; color: #1E3A8A; margin: 10px 0;'>{q_target['kannada_term']} <span style='font-size: 1.2rem; font-weight: normal; color:#64748B;'>({q_target['transliteration']})</span></div>
                <div style='color: #334155;'><b>Context:</b> {q_target['definition_kn']}</div>
            </div>
            """, unsafe_allow_html=True)

            selected = st.radio("Select the correct English term:", st.session_state.options, index=None, key=f"q_{st.session_state.quiz_index}")

            if st.button("Submit Answer", type="primary", disabled=selected is None or st.session_state.quiz_answered):
                st.session_state.quiz_answered = True
                st.session_state.selected_option = selected
                if selected == q_target["english_term"]:
                    st.session_state.score += 1
                    st.balloons()
                st.rerun()

            if st.session_state.quiz_answered:
                if st.session_state.selected_option == q_target["english_term"]:
                    st.success(f"🎉 Correct! **{q_target['kannada_term']}** is **{q_target['english_term']}**.")
                else:
                    st.error(f"❌ Incorrect. The correct English term is **{q_target['english_term']}**.")
                
                st.info(f"💡 **English Definition:** {q_target['definition_en']}")

                if st.button("Next Question ➡️"):
                    st.session_state.quiz_index += 1
                    st.session_state.quiz_answered = False
                    st.rerun()
        else:
            st.success("🏁 Quiz Finished!")
            st.markdown(f"### Your Final Score: **{st.session_state.score} / {total_questions}** ({int(st.session_state.score / total_questions * 100)}%)")
            if st.button("Restart Quiz 🔄"):
                st.session_state.quiz_index = 0
                st.session_state.score = 0
                st.session_state.quiz_answered = False
                st.rerun()

# ==========================================
# MODE 4: TERM MATCHER GAME
# ==========================================
elif app_mode == "🧩 Term Matcher Game":
    st.header("🧩 Kannada-English Term Matcher")
    st.write("Match the Kannada words on the left with their correct English counterparts!")

    filtered = get_filtered_keywords()
    sample_size = min(5, len(filtered))
    sample_set = filtered[:sample_size]

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🇮🇳 Kannada Words")
        for item in sample_set:
            st.markdown(f"- **{item['kannada_term']}** *({item['transliteration']})*")
    with col_b:
        st.markdown("### 🇬🇧 English STEM Words")
        for item in sorted(sample_set, key=lambda x: x["english_term"]):
            st.markdown(f"- **{item['english_term']}** (`{item['category']}`)")

# ==========================================
# MODE 5: BILINGUAL SEARCH DICTIONARY
# ==========================================
elif app_mode == "🔍 Bilingual Search Dictionary":
    st.header("🔍 Bilingual STEM Dictionary & Search")
    st.write("Search for any word in Kannada script, English, or Roman transliteration.")

    query = st.text_input("Enter search keyword (e.g. 'ವರ್ಗ', 'square', 'diagonal', 'ಆಯತ'):", "").strip().lower()
    
    all_kws = get_filtered_keywords()
    
    if query:
        results = [
            k for k in all_kws
            if query in k["kannada_term"].lower()
            or query in k["english_term"].lower()
            or query in k["transliteration"].lower()
            or query in k["definition_kn"].lower()
            or query in k["definition_en"].lower()
        ]
        st.write(f"Found **{len(results)}** matches for *'{query}'*:")
        
        for kw in results:
            st.markdown(f"""
            <div class='card-box'>
                <h4>{kw['kannada_term']} ➔ <span style='color:#059669;'>{kw['english_term']}</span> <span style='color:#6B7280; font-size: 0.9rem;'>({kw['transliteration']})</span></h4>
                <p><b>Category:</b> {kw['category']} | <b>Chapter:</b> {kw.get('chapter_num', '')}</p>
                <p><b>Kannada:</b> {kw['definition_kn']}</p>
                <p><b>English:</b> {kw['definition_en']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Type above to search across all chapters and definitions.")

# ==========================================
# MODE 6: LEARNING ANALYTICS
# ==========================================
elif app_mode == "📊 Learning Analytics":
    st.header("📊 Learning Analytics & Curriculum Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Chapters", data.get("total_chapters", 7))
    with col2:
        st.metric("Total Keywords Extracted", data.get("total_keywords_extracted", 0))
    with col3:
        st.metric("Target Audience", "Grade 8 STEM (Kannada Medium)")

    st.markdown("### 📈 Keyword Distribution by Chapter")
    ch_stats = []
    for ch in chapters:
        ch_stats.append({
            "Chapter": f"Ch {ch['chapter_num']}: {ch['chapter_title_en']}",
            "Keywords Count": ch["total_keywords_count"]
        })
    st.table(ch_stats)
