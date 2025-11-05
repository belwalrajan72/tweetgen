from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import streamlit as st

API_KEY = "AIzaSyAaNibA0ASyxbsrZTm0wt0mzQh42qKnQEE"

genai.configure(api_key=API_KEY)

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join([entry['text'] for entry in transcript])
    except:
        return "Sample transcript: A video about content creation and growth."

def yt_to_tweets_vibe(url, vibe):
    if "v=" in url:
        video_id = url.split("v=")[1].split("&")[0]
    else:
        video_id = url.split("/")[-1]
    
    transcript = get_transcript(video_id)
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    meta_prompt = f"""
    You are a viral X/Twitter ghostwriter with 1M followers.
    User vibe: '{vibe}'
    From transcript: {transcript[:3800]}

    Create a 30-tweet thread in {vibe} tone. Structure:
    - #1–3: HOOK (question/confession/stat from transcript)
    - #4–15: STORY (narrative flow, {vibe} spin)
    - #16–27: LESSONS (3–5 takeaways, bold keys)
    - #28–29: EXCITEMENT (benefits/prediction)
    - #30: CTA ("Watch full: {url} | Reply: What's your take on [vibe-related]? 👇")

    Rules:
    - <280 chars per tweet
    - #1/30 format
    - 1 emoji per tweet
    - Conversational, no fluff
    - Output ONLY 30 tweets, one per line
    """
    
    try:
        response = model.generate_content(meta_prompt)
        lines = [line.strip() for line in response.text.split('\n') if line.strip() and len(line.strip()) < 280 and '#' in line]
        while len(lines) < 30:
            lines.append(f"#{len(lines)+1}/30 {vibe} continuation... Keep going!")
        return lines[:30]
    except Exception as e:
        return [f"Error: {str(e)}"] * 30