"""
dictionary with MONGO DB query template for different group_types
"""

TEMPLATE = {
    "month": {
        "group": {
            "year": {"$year": "$dt"},
            "month": {"$month": "$dt"}
        },
        "project": {
            "year": "$_id.year",
            "month": "$_id.month",
        },
        "sort": {
            "year": 1,
            "month": 1,
        },
    },

    "day": {
        "group": {
            "year": {"$year": "$dt"},
            "month": {"$month": "$dt"},
            "day": {"$dayOfMonth": "$dt"}
        },
        "project": {
            "year": "$_id.year",
            "month": "$_id.month",
            "day": "$_id.day",
        },
        "sort": {
            "year": 1,
            "month": 1,
            "day": 1,
        },
    },
    "hour": {
        "group": {
            "year": {"$year": "$dt"},
            "month": {"$month": "$dt"},
            "day": {"$dayOfMonth": "$dt"},
            "hour": {"$hour": "$dt"},
        },
        "project": {
            "year": "$_id.year",
            "month": "$_id.month",
            "day": "$_id.day",
            "hour": "$_id.hour",
        },
        "sort": {
            "year": 1,
            "month": 1,
            "day": 1,
            "hour": 1,
        },
        }
    }
