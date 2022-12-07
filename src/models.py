import uuid

from faker import Faker
from pydantic import BaseModel, Field


fake = Faker()


def create_id():
    return str(uuid.uuid4())


class Message(BaseModel):
    id: str = Field(name='id', default_factory=create_id)
    recipient: str = Field(name='recipient', default_factory=fake.ascii_email)
    message: str = Field(name='message', default_factory=fake.sentence)
