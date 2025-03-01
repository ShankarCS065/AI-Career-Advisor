import os
import psycopg2
import redis
from dotenv import load_dotenv

load_dotenv()

class CareerAdvisorModel:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        self.cursor = self.conn.cursor()

        # Get Redis Host & Port from environment variables
        redis_host = os.getenv("REDIS_HOST", "redis")
        redis_port = int(os.getenv("REDIS_PORT", 6379))

        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)

    def suggest_careers(self, user_skills, user_interests):
        cache_key = f"{user_skills}_{user_interests}"
        cached_result = self.redis_client.get(cache_key)
        
        if cached_result:
            return cached_result.split(",")

        query = """
        SELECT career FROM careers 
        WHERE required_skills ILIKE %s OR typical_interests ILIKE %s
        """
        self.cursor.execute(query, (f"%{user_skills}%", f"%{user_interests}%"))
        results = self.cursor.fetchall()
        response = [row[0] for row in results] if results else ["No suitable careers found."]

        self.redis_client.set(cache_key, ",".join(response), ex=3600)
        return response
