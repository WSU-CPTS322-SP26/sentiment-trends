import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime, date

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(url, key)

#test query
response = supabase.table("users").select("*").limit(1).execute()


print("connection successful")
print(response.data)


positive = 0
negative = 0
neutral = 0


today = date.today().isoformat()
supabase.table("table").upsert(
    {
        "id": today,
        "positive_sentiment": positive,
        "negative_sentiment": negative,
        "neutral_sentiment": neutral
    },
    on_conflict="id"
).execute()
