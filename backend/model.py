import os
import psycopg2
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CareerAdvisorModel:
    def __init__(self):
        """
        Initialize PostgreSQL and Redis connections.
        """
        try:
            # Connect to PostgreSQL
            self.conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            self.cursor = self.conn.cursor()

            # Connect to Redis
            self.redis_client = redis.StrictRedis(
                host=os.getenv("REDIS_HOST", "localhost"),  
                port=int(os.getenv("REDIS_PORT", 6379)), 
                db=0, 
                decode_responses=True
            )
        except Exception as e:
            print(f"Database connection error: {e}")

    def suggest_careers(self, user_skills, user_interests):
        """
        Suggest careers based on skills and interests using PostgreSQL.
        Cache results in Redis for faster retrieval.
        """
        cache_key = f"career:{user_skills}:{user_interests}"
        cached_result = self.redis_client.get(cache_key)

        # If found in Redis, return cached result
        if cached_result:
            return cached_result.split(",")

        # Query PostgreSQL for career matches
        query = """
        SELECT career FROM careers 
        WHERE required_skills ILIKE %s OR typical_interests ILIKE %s
        """
        self.cursor.execute(query, (f"%{user_skills}%", f"%{user_interests}%"))
        results = self.cursor.fetchall()

        # Format response
        response = [row[0] for row in results] if results else ["No suitable careers found."]

        # Store result in Redis (cache expires in 1 hour)
        self.redis_client.set(cache_key, ",".join(response), ex=3600)
        
        return response
