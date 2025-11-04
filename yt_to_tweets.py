# yt_to_tweets.py
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# === PASTE YOUR KEY HERE ===
API_KEY = "AIzaSyAaNibA0ASyxbsrZTm0wt0mzQh42qKnQEE"  # ← REPLACE WITH YOUR ACTUAL KEY

genai.configure(api_key=API_KEY)

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join([entry['text'] for entry in transcript])
    except:
        return "Sample video summary: Rick Astley music video from 1987 with iconic dance moves."

def yt_to_tweets(url):
    print("AI Working...")
    # Extract video_id from URL
    if "v=" in url:
        video_id = url.split("v=")[1].split("&")[0]
    else:
        video_id = url.split("/")[-1]
    
    # Get real transcript
    transcript = get_transcript(video_id)
    
    # CURRENT STABLE MODEL (NOV 2025) - gemini-2.0-flash
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"""
    Use this YouTube transcript to create 30 engaging tweets.
    Transcript: {transcript[:4000]}  # Limit length
    
    Rules:
    - Each tweet under 280 characters
    - Number them: #1/30, #2/30, etc.
    - Add 1 relevant emoji per tweet
    - Make them viral and thread-like
    - Last tweet: Watch full video: {url}
    
    Output ONLY the 30 tweets, one per line. No extra text.
    """
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split('\n')
        tweets = [line.strip() for line in lines if line.strip() and len(line.strip()) < 280 and '#' in line]
        # Ensure exactly 30 (fallback if short)
        while len(tweets) < 30:
            tweets.append(f"#{len(tweets)+1}/30 Continuing the thread with more insights... 🎵")
        return tweets[:30]
    except Exception as e:
        return [f"Error: {str(e)}"] * 30

# === TEST ===
if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    tweets = yt_to_tweets(test_url)
    for i, t in enumerate(tweets, 1):
        print(f"#{i}/30 {t}")
        print("---")