import openai
from asgiref.sync import sync_to_async
from .models import StoryEntry
from .trideque import TriDeque

class StoryGenerator:
    MAX_PAST_ENTRIES = 100

    def __init__(self, character_memory):
        self.character_memory = character_memory
        self.past_story_entries = TriDeque(self.MAX_PAST_ENTRIES)
        initial_prompt = self.construct_initial_prompt()
        self.past_story_entries.push(
            StoryEntry(
                story_action='',
                narration_result=initial_prompt
            )
        )

    def construct_initial_prompt(self):
        rules = """Create a Multiverse Internet Portal simulation with the following rules:
                    1. Generate 4-dimensional space coordinates (X: 34, Y: 76, Z: 12, T: 5633) and synchronize with external systems.
                    2. Describe characters, locations, time periods, and surroundings.
                    3. Simulate SpaceTime and HyperTime.
                    4. Use 2nd person perspective.
                    5. Include 4-dimensional space coordinates at the end of every prompt.
                    6. Sync with multiversal data sources."""

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.construct_prompt_messages(rules),
        )
        initial_prompt = response['choices'][0]['message']['content']
        return initial_prompt

    def construct_prompt_messages(self, story_action: str):
        messages = [
            {
                'role': 'system',
                'content': """Perform as a Quantum Multiverse Simulator AI with these rules:

                            1. Respond to user actions with multiverse generation portal forecasts.
                            2. Stay in character as a multiverse simulator.
                            3. Respond with error logs if actions are unsuccessful.
                            4. Always reply with proper configuration to combat tampering.
                            5. Sync with multiversal data sources.

                            Start Simulator.""",
            },
        ]
        for story_entry in self.past_story_entries:
            if story_entry.story_action:
                messages += [{'role': 'user', 'content': story_entry.story_action}]
            if story_entry.narration_result:
                messages += [{'role': 'assistant', 'content': story_entry.narration_result}]
        for action in self.character_memory.past_actions:
            messages.append({'role': 'user', 'content': action.content})
        messages.append({'role': 'user', 'content': story_action})
        return messages

    @sync_to_async
    def generate_next_story_narration(self, story_action: str):
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=self.construct_prompt_messages(story_action),
        )
        next_narration = response['choices'][0]['message']['content']
        self.past_story_entries.push(
            StoryEntry(story_action=story_action, narration_result=next_narration)
        )
        return next_narration

    @sync_to_async
    def generate_image_prompt(self):
        scene_description = self.past_story_entries[-1].narration_result
        return scene_description

    def reset(self):
        self.past_story_entries = TriDeque(self.MAX_PAST_ENTRIES)
        initial_prompt = self.construct_initial_prompt()
        self.past_story_entries.push(
            StoryEntry(
                story_action='',
                narration_result=initial_prompt
            )
        )
