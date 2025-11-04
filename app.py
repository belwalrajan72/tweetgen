# app.py
import streamlit as st
from yt_to_tweets import yt_to_tweets

st.set_page_config(page_title="YouTube → 30 Tweets", layout="centered")

st.title("YouTube → 30 Viral Tweets in 60 Sec")
st.markdown("**Paste any YouTube link → Get 30 ready-to-post tweets**")

url = st.text_input("YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Generate Thread"):
    if url:
        with st.spinner("AI generating tweets..."):
            tweets = yt_to_tweets(url)
        st.success("Done! 30 tweets ready.")
        
        # Show tweets
        for i, tweet in enumerate(tweets, 1):
            st.markdown(f"**#{i}/30** {tweet}")
        
        # Download button
        tweet_text = "\n\n".join(tweets)
        st.download_button(
            label="Download .txt",
            data=tweet_text,
            file_name="tweets.txt",
            mime="text/plain"
        )
    else:
        st.error("Please paste a YouTube link.")