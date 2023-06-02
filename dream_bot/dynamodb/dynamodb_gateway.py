import uuid
from datetime import datetime

from mypy_boto3_dynamodb.service_resource import Table

from .db_entities import DreamEntity
from .get_dynamodb_table import get_dynamodb_table


def add_dream(dream: dict) -> bool:
    """
    :param dream: A dream object
    :return: True if the dream was added successfully, False otherwise
    """
    dreams_table: Table = get_dynamodb_table("dreams")
    res = dreams_table.put_item(Item=dream)
    if res["ResponseMetadata"]["HTTPStatusCode"] == 200:
        print(f"Added dream |💾| {dream['dream_id']} - {dream.get('title')}")
        return True


def search_dreams_for_user(user_id: int, query: str = "") -> list[DreamEntity]:
    """
    :param user_id: The user id to search for
    :param query: The query to filter dreams by
    """
    dreams_table: Table = get_dynamodb_table("dreams")
    # Get by secondary index
    res = dreams_table.query(
        IndexName="user_id-index",
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": user_id},
    )
    assert res["ResponseMetadata"]["HTTPStatusCode"] == 200, f"Failed to get dreams for user {user_id} with error {res}"

    # Filter dreams by query if query is set
    filtered_dreams: list[dict] = [dream for dream in res["Items"]
                                   if query.lower() in dream["text"].lower()
                                   or query.lower() in dream["title"].lower()]

    user_dreams: list[DreamEntity] = []
    for item in filtered_dreams:
        dream = DreamEntity(
            dream_id=uuid.UUID(item["dream_id"]),
            date=datetime.fromisoformat(item["date"]),
            user_id=int(item["user_id"]),
            username=item["username"],
            title=item["title"],
            text=item["text"],
        )
        user_dreams.append(dream)
    return user_dreams
