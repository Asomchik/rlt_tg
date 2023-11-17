"""
Parsing users input. Generate request to DB. Format output.
"""
# import asyncio
import json
from datetime import datetime, timedelta

from database import make_aggregation_query
from query_template import TEMPLATE

from exceptions import UnsupportedSchema, DataError, DataBaseError


def parse_user_input(input_string):
    """Parses user input to get expected dictionary"""
    try:
        parsed_data = json.loads(input_string)
        if all(key in parsed_data for key in ["dt_from", "dt_upto", "group_type"]):
            return {
                "dt_from": parsed_data["dt_from"],
                "dt_upto": parsed_data["dt_upto"],
                "group_type": parsed_data["group_type"]
            }
        raise UnsupportedSchema
    except (json.JSONDecodeError, TypeError, KeyError) as exc:
        raise UnsupportedSchema from exc


def generate_query_data(input_dict):
    """Converts strings to datetime and checks validity for querying the DB."""
    try:
        dt_from = datetime.fromisoformat(input_dict["dt_from"])
        dt_upto = datetime.fromisoformat(input_dict["dt_upto"])
        if dt_upto < dt_from:
            raise DataError
        group_type = input_dict["group_type"]
        if group_type not in TEMPLATE:
            raise DataError
        return dt_from, dt_upto, group_type
    except ValueError as exc:
        raise DataError from exc


def transform_raw_output(query_result):
    """Reformat MongoDB response for further processing"""
    output = {}
    for dict_ in query_result:
        total_value = dict_['total_value']

        year = dict_['year']
        month = dict_.get('month', 1)
        day = dict_.get('day', 1)
        hour = dict_.get('hour', 0)
        time_iso_str = f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:00:00"
        output[time_iso_str] = total_value
    return output


def format_query_results(query_data, raw_query_result):
    """Transforms query result to the needed format."""
    query_result = transform_raw_output(raw_query_result)
    current_date, end_date, step = query_data
    dataset = []
    labels = []
    while current_date <= end_date:
        current_date_str = current_date.strftime('%Y-%m-%dT%H:%M:%S')
        dataset.append(query_result.get(current_date_str, 0))
        labels.append(current_date_str)

        if step == 'hour':
            current_date += timedelta(hours=1)
        elif step == 'day':
            current_date += timedelta(days=1)
        elif step == 'month':
            current_date = (
                    current_date.replace(day=1) + timedelta(days=32)
            ).replace(day=1)
        else:
            raise ValueError("Invalid step. Use 'hour', 'day', or 'month'")

    return {'dataset': dataset, 'labels': labels}


async def aggregate_payments(input_text):
    """Main handler for input validation and generating response."""
    try:
        safe_input = parse_user_input(input_text)
    except UnsupportedSchema as exc:
        return f"{exc}"

    try:
        query_data = generate_query_data(safe_input)
    except DataError as exc:
        return f"{exc}"

    try:
        raw_query_result = await make_aggregation_query(*query_data)
    except DataBaseError as exc:
        return f"{exc}"

    final_result = format_query_results(query_data, raw_query_result)

    return str(final_result)
