import bisect
import time
from collections import deque
from dataclasses import dataclass
from typing import List, Dict
import os
from pathlib import Path

@dataclass
class CharacterProfile:
    name: str
    age: int
    occupation: str
    skills: List[str]
    relationships: Dict[str, str]

class Memory:
    def __init__(self, content, priority=0):
        self.content = content
        self.priority = priority
        self.timestamp = time.time()

class TriDeque:
    def __init__(self, maxlen):
        self.data = deque(maxlen=maxlen)

    def push(self, memory):
        # Insert memory in order of priority
        index = bisect.bisect([m.priority for m in self.data], memory.priority)
        self.data.insert(index, memory)

    def remove(self, content):
        # Remove a memory based on its content
        for memory in self.data:
            if memory.content == content:
                self.data.remove(memory)
                break

    def update_priority(self, content, new_priority):
        # Update the priority of a memory based on its content
        for memory in self.data:
            if memory.content == content:
                # Remove the memory
                self.data.remove(memory)
                # Update its priority
                memory.priority = new_priority
                # Re-insert it with the new priority
                self.push(memory)
                break

class CharacterMemory:
    MAX_PAST_ACTIONS = 1000  # Increase to 1000
    PAST_ACTIONS_FILE = os.path.join(os.path.dirname(__file__), 'datafiles', 'past_actions.txt')  # file to store older actions

    def __init__(self):
        self.attributes = {}
        self.past_actions = TriDeque(self.MAX_PAST_ACTIONS)  # Initialize a TriDeque with a size of MAX_PAST_ACTIONS
        self.color_code = "white"  # default color
        self.profile = CharacterProfile("John Doe", 40, "Detective", ["Investigation", "Hand-to-hand combat"], {"Sarah": "Wife", "Tom": "Partner"})
        self.thoughts_file = "thoughts.txt"

        # Check if the past actions file exists, and create it if it doesn't
        past_actions_path = Path(self.PAST_ACTIONS_FILE)
        past_actions_path.parent.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
        past_actions_path.touch(exist_ok=True)  # Create the file if it doesn't exist

        # Load past actions from the file
        with open(self.PAST_ACTIONS_FILE, 'r') as f:
            for line in f:
                action = line.strip()
                self.add_past_action(action)

    def update_attribute(self, attribute, value):
        self.attributes[attribute] = value
        if attribute == "mood":
            self.update_color_code(value)

    def update_color_code(self, mood):
        if mood == "happy":
            self.color_code = "yellow"
        elif mood == "sad":
            self.color_code = "blue"
        elif mood == "angry":
            self.color_code = "red"
        else:
            self.color_code = "white"

    def add_past_action(self, action, priority=0):
        memory = Memory(action, priority)
        self.past_actions.push(memory)

        # Write the action to the past actions file
        with open(self.PAST_ACTIONS_FILE, 'a') as f:
            f.write(f'{action}\n')

    def clear_past_actions(self):
        # Clear the past actions in memory
        self.past_actions = TriDeque(self.MAX_PAST_ACTIONS)

        # Clear the past actions file
        with open(self.PAST_ACTIONS_FILE, 'w') as f:
            pass

    def save_state(self, filename):
        # Save the bot's current state to a file
        with open(filename, 'w') as f:
            f.write(f'Color code: {self.color_code}\n')
            f.write(f'Attributes: {self.attributes}\n')
            f.write(f'Profile: {self.profile}\n')
            f.write('Past actions:\n')
            for memory in self.past_actions:
                f.write(f'  {memory.content}\n')

