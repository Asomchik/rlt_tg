"""
Interaction with MongoDB
"""
import os

from dotenv import load_dotenv
import pymongo

from exceptions import DataBaseError
from query_template import TEMPLATE


def get_db_collection():
    """Creates db connection cursor"""
    load_dotenv()
    password = os.getenv('MONGO_PASSWORD')
    connection_str = f'mongodb+srv://asomchik:{password}@asomchik.de5m2qj.mongodb.net'
    try:
        client = pymongo.MongoClient(connection_str)
        db = client['sampleDB']
        collection = db['sample_collection']
        return collection
    except Exception as exc:
        raise DataBaseError from exc


async def make_aggregation_query(dt_from, dt_upto, group_type):
    """Makes query to DB for aggregate payment information using template"""

    try:
        query = {"dt": {"$gte": dt_from, "$lte": dt_upto}}

        pipeline = [
            {"$match": query},
            {"$group": {
                "_id": TEMPLATE[group_type]['group'],
                "total_value": {"$sum": "$value"}
            }
            },
            {"$project": {
                "_id": 0,
                **TEMPLATE[group_type]['project'],
                "total_value": 1
            }
            },
            {"$sort": TEMPLATE[group_type]['sort']},
        ]

        collection = get_db_collection()
        query_result = list(collection.aggregate(pipeline))
        return query_result
    except Exception as exc:
        raise DataBaseError from exc
