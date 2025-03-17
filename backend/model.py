import os
import psycopg2
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CareerAdvisorModel:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.redis_client = None

        try:
            # Connect to PostgreSQL
            self.conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                connect_timeout=10  # Timeout for connection attempts
            )
            self.cursor = self.conn.cursor()
            print("✅ PostgreSQL connection established.")

            # Connect to Redis
            self.redis_client = redis.StrictRedis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                db=0,
                decode_responses=True
            )
            print("✅ Redis connection established.")
        except Exception as e:
            print(f"❌ Database connection error: {e}")

    def suggest_careers(self, user_skills: str, user_interests: str):
        """
        Suggest careers based on user skills and interests.
        Utilizes Redis caching to improve performance.
        """
        if not user_skills or not user_interests:
            return ["Error: Skills and interests cannot be empty."]

        cache_key = f"career:{user_skills.lower()}:{user_interests.lower()}"
        cached_result = self.redis_client.get(cache_key)

        if cached_result:
            print("🔹 Returning cached result from Redis.")
            return cached_result.split(",")

        try:
            query = """
            SELECT career FROM careers 
            WHERE required_skills ILIKE %s OR typical_interests ILIKE %s
            """
            self.cursor.execute(query, (f"%{user_skills}%", f"%{user_interests}%"))
            results = self.cursor.fetchall()

            if results:
                response = [row[0] for row in results]
                # Store in Redis cache (expires in 1 hour)
                self.redis_client.set(cache_key, ",".join(response), ex=3600)
                print("✅ Query successful. Result cached.")
                return response
            else:
                return ["No suitable careers found."]
        except psycopg2.Error as db_error:
            return [f"Database query error: {str(db_error)}"]
        except Exception as e:
            return [f"Unexpected error: {str(e)}"]

    def close_connections(self):
        """Close database and Redis connections."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("🔻 Database connection closed.")
