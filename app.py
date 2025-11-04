import streamlit as st
from yt_to_tweets import yt_to_tweets_vibe

st.set_page_config(page_title="Vibe Code Your Thread", page_icon="")

# Session state for streaks
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'total_threads' not in st.session_state:
    st.session_state.total_threads = 0

st.title("Vibe Code Your YouTube Thread")
st.markdown("**Describe the vibe** + paste URL → Get 30 **custom viral tweets** in 60 sec")

col1, col2 = st.columns(2)
with col1:
    vibe = st.text_input("Vibe Description", placeholder="E.g., 'Funny 80s nostalgia'")
with col2:
    url = st.text_input("YouTube URL", placeholder="https://youtu.be/...")

if st.button("Vibe Generate Thread", type="primary"):
    if vibe and url:
        with st.spinner("AI is vibing your thread..."):
            tweets = yt_to_tweets_vibe(url, vibe)
        
        st.session_state.streak += 1
        st.session_state.total_threads += 1
        
        st.success(f"VIBE CODED! 30 tweets ready. Streak: {st.session_state.streak} days")
        
        for i, tweet in enumerate(tweets, 1):
            st.markdown(f"**#{i}/30** {tweet}")
        
        tweet_text = "\n\n".join(tweets)
        st.download_button(
            "Download .txt",
            tweet_text,
            f"vibe-tweets-{vibe[:10]}.txt",
            "text/plain"
        )
        
        # Badge unlock
        if st.session_state.streak == 7:
            st.balloons()
            st.success("7-DAY STREAK UNLOCKED: THREAD WARRIOR BADGE!")
        
        # Refine loop
        feedback = st.text_input("Refine vibe? (e.g., 'Make it funnier')")
        if st.button("Refine Thread") and feedback:
            with st.spinner("Refining..."):
                refined_tweets = yt_to_tweets_vibe(url, vibe + " " + feedback)
            st.rerun()
    else:
        st.error("Add vibe + URL")

# Stats
st.sidebar.metric("Your Streak", f"{st.session_state.streak} days")
st.sidebar.metric("Threads Created", st.session_state.total_threads)