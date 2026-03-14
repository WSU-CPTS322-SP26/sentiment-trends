import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(url, key)

#test query
response = supabase.table("users").select("*").limit(1).execute()


print("connection successful")
print(response.data)


supabase.table("table").insert({
    "positive_sentiment": 0.0,
    "negative_sentiment": 0.0,
    "neutral_sentiment": 0.0

}).execute()

