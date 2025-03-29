from mongo_connection import find_many, test_connection


def verify_data():
    print("\nVerifying MongoDB Connection and Data...")

    # First test the connection
    if not test_connection():
        print("❌ Database connection failed!")
        return

    # Check each collection
    collections = {"companies": 3, "skills": 8, "job_postings": 3, "candidates": 2}

    for collection, expected_count in collections.items():
        try:
            cursor = find_many(collection)
            documents = list(cursor)
            count = len(documents)
            if count == expected_count:
                print(f"✅ {collection}: Found {count} documents as expected")
            else:
                print(
                    f"❌ {collection}: Expected {expected_count} documents, found {count}"
                )
        except Exception as e:
            print(f"❌ Error querying {collection}: {str(e)}")


if __name__ == "__main__":
    verify_data()
