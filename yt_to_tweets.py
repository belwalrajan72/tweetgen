# yt_to_tweets.py
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai


API_KEY = "AIzaSyAaNibA0ASyxbsrZTm0wt0mzQh42qKnQEE" 

genai.configure(api_key=API_KEY)

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join([entry['text'] for entry in transcript])
    except:
        return "Sample video summary: Rick Astley music video from 1987 with iconic dance moves."

def yt_to_tweets(url):
    print("AI Working...")
    
    if "v=" in url:
        video_id = url.split("v=")[1].split("&")[0]
    else:
        video_id = url.split("/")[-1]
    
    
    transcript = get_transcript(video_id)

    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt =prompt = f"""
You are a viral X/Twitter ghostwriter with 1M followers. Your threads get 10K+ likes by hooking fast, telling stories, dropping lessons, and sparking replies.

From this YouTube transcript, create a 30-tweet thread that repurposes the video into engaging, skimmable content for creators/coaches/founders.

Transcript: {transcript[:3800]}  # Full video content

STRICT RULES:
- EXACTLY 30 tweets, numbered #1/30 to #30/30
- Each < 280 chars (count them)
- 1 emoji per tweet (relevant, not overkill)
- Structure: 
  - Tweets 1–3: HOOK (question/confession/stat from transcript to grab attention)
  - Tweets 4–15: STORY (narrative flow from transcript — facts, examples, build tension)
  - Tweets 16–27: LESSONS (3–5 actionable takeaways, bold key phrases)
  - Tweets 28–29: BUILD EXCITEMENT (tease benefits, prediction)
  - Tweet 30: CTA ("Watch full: {url} | Reply: What's your biggest repurposing struggle? 👇")
- Make it conversational, in creator's voice: punchy, relatable, no fluff
- Add virality: 1 question every 5 tweets, 1 stat/confession per 10, end with share prompt
- Output ONLY the 30 tweets, one per line. No intro/outro/extras.

EXAMPLE HOOK TWEET: #1/30 Ever spent 3 hours turning 1 video into tweets? I did — until this hack saved me 20h/week 😩 Thread → 

Start with a killer hook from the transcript.
"""
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split('\n')
        tweets = [line.strip() for line in lines if line.strip() and len(line.strip()) < 280 and '#' in line]
        
        while len(tweets) < 30:
            tweets.append(f"#{len(tweets)+1}/30 Continuing the thread with more insights... 🎵")
        return tweets[:30]
    except Exception as e:
        return [f"Error: {str(e)}"] * 30


if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    tweets = yt_to_tweets(test_url)
    for i, t in enumerate(tweets, 1):
        print(f"#{i}/30 {t}")
        print("---")