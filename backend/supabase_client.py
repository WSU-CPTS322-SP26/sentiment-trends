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

#test insertions
supabase.table("users").insert({
    "name": "Test User",
    "email": "sentimentTrendsTest@example.com"
}).execute()


supabase.table("users").insert({
    "name": "Im Dylan!",
    "email": "dylan@example.com"
}).execute()


supabase.table("users").insert({
    "name": "Im Dylan hale!",
    "email": "dylanhale@example.com"
}).execute()