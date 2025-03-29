from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import logging
from typing import Dict, List, Optional, Union
import os
from urllib.parse import quote_plus
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# MongoDB connection configuration
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "fasthire")
MONGO_USER = os.getenv("MONGO_USER", "")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "")

print("\n=== MongoDB Connection Settings ===")
print(f"Host: {MONGO_HOST}")
print(f"Port: {MONGO_PORT}")
print(f"Database: {MONGO_DB}")
print(f"Username configured: {'Yes' if MONGO_USER else 'No'}")
print("=====================================\n")

# Construct connection URL based on whether authentication is provided
if MONGO_USER and MONGO_PASSWORD:
    MONGO_URL = f"mongodb://{quote_plus(MONGO_USER)}:{quote_plus(MONGO_PASSWORD)}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
else:
    MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"

print(f"Attempting to connect to MongoDB using URL: {MONGO_URL.replace(MONGO_PASSWORD, '****') if MONGO_PASSWORD else MONGO_URL}")

# Maximum number of connection attempts
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


def connect_with_retry():
    for attempt in range(MAX_RETRIES):
        try:
            print(f"\nConnection attempt {attempt + 1} of {MAX_RETRIES}...")
            client = MongoClient(
                MONGO_URL,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,
                retryWrites=True,
                connectTimeoutMS=5000,
                socketTimeoutMS=10000,
            )
            # Test connection
            print("Testing connection with ping command...")
            client.admin.command("ping")
            print(f"✅ Successfully connected to MongoDB on {MONGO_HOST}:{MONGO_PORT}")
            logger.info(f"Successfully connected to MongoDB on {MONGO_HOST}:{MONGO_PORT}")
            return client
        except Exception as e:
            print(f"❌ Connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < MAX_RETRIES - 1:
                print(f"Waiting {RETRY_DELAY} seconds before next attempt...")
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}. Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                error_msg = (f"Failed to connect to MongoDB after {MAX_RETRIES} attempts: {e}")
                print(f"❌ {error_msg}")
                logger.error(error_msg)
                raise


try:
    # Initialize the client with retry logic
    print("\nInitializing MongoDB connection...")
    client = connect_with_retry()
except Exception as e:
    error_msg = f"Failed to establish MongoDB connection: {e}"
    print(f"❌ {error_msg}")
    logger.error(error_msg)
    raise


def test_connection() -> bool:
    try:
        print("\nTesting MongoDB connection...")
        # Ping the server to verify connection is alive
        client.admin.command("ping")
        success_msg = "✅ Successfully connected to MongoDB"
        print(success_msg)
        logger.info(success_msg)
        return True
    except ConnectionFailure as e:
        error_msg = f"MongoDB connection error: {e}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        return False
    except OperationFailure as e:
        error_msg = f"MongoDB authentication error: {e}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        return False
    except Exception as e:
        error_msg = f"Unexpected MongoDB error: {e}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        return False


def get_mongo_db(db_name: Optional[str] = None):
    try:
        db_name = db_name or "fasthire"
        return client[db_name]
    except Exception as e:
        logger.error(f"Error getting MongoDB database: {e}")
        raise


def get_collection(collection_name: str, db_name: Optional[str] = None):
    try:
        db = get_mongo_db(db_name)
        return db[collection_name]
    except Exception as e:
        logger.error(f"Error getting collection {collection_name}: {e}")
        raise


def insert_data(collection_name: str, data: Union[Dict, List[Dict]], db_name: Optional[str] = None):
    try:
        collection = get_collection(collection_name, db_name)

        # Check if data is a list (multiple documents) or dict (single document)
        if isinstance(data, list):
            result = collection.insert_many(data)
            logger.info(f"Successfully inserted {len(result.inserted_ids)} documents into {collection_name}")
            return result
        else:
            result = collection.insert_one(data)
            logger.info(f"Successfully inserted document with ID: {result.inserted_id} into {collection_name}")
            return result
    except Exception as e:
        logger.error(f"Error inserting data into {collection_name}: {e}")
        raise


def update_one(collection_name: str,filter_query: Dict,update_data: Dict,db_name: Optional[str] = None,):
    try:
        collection = get_collection(collection_name, db_name)
        result = collection.update_one(filter_query, update_data)
        logger.info(f"Updated {result.modified_count} document in {collection_name}")
        return result
    except Exception as e:
        logger.error(f"Error updating document in {collection_name}: {e}")
        raise


def update_many(collection_name: str,filter_query: Dict,update_data: Dict,db_name: Optional[str] = None,):
    try:
        collection = get_collection(collection_name, db_name)
        result = collection.update_many(filter_query, update_data)
        logger.info(f"Updated {result.modified_count} documents in {collection_name}")
        return result
    except Exception as e:
        logger.error(f"Error updating documents in {collection_name}: {e}")
        raise


def delete_one(collection_name: str, filter_query: Dict, db_name: Optional[str] = None):
    try:
        collection = get_collection(collection_name, db_name)
        result = collection.delete_one(filter_query)
        logger.info(f"Deleted {result.deleted_count} document from {collection_name}")
        return result
    except Exception as e:
        logger.error(f"Error deleting document from {collection_name}: {e}")
        raise


def delete_many(collection_name: str, filter_query: Dict, db_name: Optional[str] = None):
    try:
        collection = get_collection(collection_name, db_name)
        result = collection.delete_many(filter_query)
        logger.info(f"Deleted {result.deleted_count} documents from {collection_name}")
        return result
    except Exception as e:
        logger.error(f"Error deleting documents from {collection_name}: {e}")
        raise


def find_one(collection_name: str, query: Dict, db_name: Optional[str] = None):
    try:
        collection = get_collection(collection_name, db_name)
        return collection.find_one(query)
    except Exception as e:
        logger.error(f"Error finding document in {collection_name}: {e}")
        raise


def find_many(collection_name: str,query: Dict = {},sort_by: Optional[List[tuple]] = None,limit: Optional[int] = None,skip: Optional[int] = None,db_name: Optional[str] = None,):
    try:
        collection = get_collection(collection_name, db_name)
        cursor = collection.find(query)

        # Apply sorting if specified
        if sort_by:
            cursor = cursor.sort(sort_by)

        # Apply pagination if specified
        if skip is not None:
            cursor = cursor.skip(skip)
        if limit is not None:
            cursor = cursor.limit(limit)

        return cursor
    except Exception as e:
        logger.error(f"Error finding documents in {collection_name}: {e}")
        raise


def count_documents(collection_name: str, query: Dict = {}, db_name: Optional[str] = None) -> int:
    try:
        collection = get_collection(collection_name, db_name)
        return collection.count_documents(query)
    except Exception as e:
        logger.error(f"Error counting documents in {collection_name}: {e}")
        raise


def aggregate(collection_name: str, pipeline: List[Dict], db_name: Optional[str] = None):
    try:
        collection = get_collection(collection_name, db_name)
        return collection.aggregate(pipeline)
    except Exception as e:
        logger.error(f"Error performing aggregation on {collection_name}: {e}")
        raise


def create_index(collection_name: str,keys: List[tuple],unique: bool = False,db_name: Optional[str] = None,):
    try:
        collection = get_collection(collection_name, db_name)
        result = collection.create_index(keys, unique=unique)
        logger.info(f"Created index {result} on collection {collection_name}")
        return result
    except Exception as e:
        logger.error(f"Error creating index on {collection_name}: {e}")
        raise


# Test the connection on module import
if not test_connection():
    logger.warning("Failed to establish initial MongoDB connection")
