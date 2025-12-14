from typing import List
from avatar_engine import Avatar

class Story:
    def __init__(self, user_id: int, content: str):
        self.user_id = user_id
        self.content = content

class SocialStories:
    def __init__(self):
        self.stories: List[Story] = []

    def post_story(self, avatar: Avatar, content: str):
        story = Story(user_id=avatar.user_id, content=content)
        self.stories.append(story)
        return f"Story posted by avatar {avatar.user_id}"

    def get_stories(self, limit: int = 10):
        return [s.content for s in self.stories[-limit:]]
