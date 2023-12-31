import asyncio
import openai
from typing import List
from fastapi import FastAPI
from .llm_game import LlmGame, CharacterMemory
from .llm_twitch_bot import LlmTwitchBot
from .models import Proposal, StoryEntry
from .story_generator import StoryGenerator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
background_task = None
image_url = None

origins = [
    "http://localhost:3000",  # React app is served from this URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
async def on_startup():
    global background_task, image_url

    # Create a CharacterMemory and StoryGenerator instance
    character_memory = CharacterMemory()
    generator = StoryGenerator(character_memory)

    # Generate a description of the current scene
    scene_description = await generator.generate_image_prompt()

    # Send this description to the DALL-E API
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: openai.Image.create(
        prompt=scene_description,
        n=1,
        size="512x512"
    ))

    # Store the generated image URL
    image_url = response['data'][0]['url']

    app.state.game = game = LlmGame()
    app.state.bot = bot = LlmTwitchBot(game)
    game.hooks = bot
    background_task = asyncio.create_task(bot.start())

@app.get('/proposals')
def get_proposals() -> List[Proposal]:
    game: LlmGame = app.state.game
    return game.proposals

@app.get('/story-history')
def get_story_history() -> List[StoryEntry]:
    game: LlmGame = app.state.game
    return game.generator.past_story_entries

@app.get('/vote-time-remaining')
def get_vote_time_remaining():
    game: LlmGame = app.state.game
    remaining_time = game.calculate_remaining_time()
    return {"remaining_time": remaining_time}

@app.get("/generate-image")
async def generate_image():
    # Return the generated image
    global image_url
    return {"image": image_url}
