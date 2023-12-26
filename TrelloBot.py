import discord
from discord.ext import commands
from trello import TrelloApi

#Need to finish building

# Discord Bot Token
DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

# Trello API Key and Token
TRELLO_API_KEY = 'YOUR_TRELLO_API_KEY'
TRELLO_API_TOKEN = 'YOUR_TRELLO_ACCESS_TOKEN'
TRELLO_BOARD_ID = 'YOUR_TRELLO_BOARD_ID'

# Create instances
bot = commands.Bot(command_prefix='!')
trello = TrelloApi(TRELLO_API_KEY, TRELLO_API_TOKEN)

# Bot event - on ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

# Command - Get Trello Cards in a List
@bot.command(name='getTrelloCards')
async def get_trello_cards(ctx, list_name):
    try:
        # Fetch Trello cards in the specified list
        cards = trello.lists.get_card(TRELLO_BOARD_ID, list_name)
        
        # Send cards to Discord
        if cards:
            response = f'Trello Cards in {list_name}:\n'
            for card in cards:
                response += f'- {card["name"]}\n'
        else:
            response = f'No cards found in {list_name}.'

        await ctx.send(response)

    except Exception as e:
        print(e)
        await ctx.send('Error fetching Trello cards.')

# Command - Set Trello Card Due Date
@bot.command(name='setDueDate')
async def set_due_date(ctx, card_name, due_date):
    try:
        # Find the Trello card
        card_id = None
        cards = trello.boards.get_card(TRELLO_BOARD_ID)
        for card in cards:
            if card['name'] == card_name:
                card_id = card['id']

        if card_id:
            # Update due date
            trello.cards.update_due_date(card_id, due_date)
            await ctx.send(f'Due date for {card_name} set to {due_date}.')
        else:
            await ctx.send(f'Card {card_name} not found.')

    except Exception as e:
        print(e)
        await ctx.send('Error updating due date.')

# Command - Assign Trello Card to User
@bot.command(name='assignTask')
async def assign_task(ctx, card_name, user_mention):
    try:
        # Find the Trello card
        card_id = None
        cards = trello.boards.get_card(TRELLO_BOARD_ID)
        for card in cards:
            if card['name'] == card_name:
                card_id = card['id']

        if card_id:
            # Assign the card to the mentioned user
            member_id = ctx.message.mentions[0].id
            trello.cards.assign(card_id, member_id)
            await ctx.send(f'Task {card_name} assigned to {user_mention}.')
        else:
            await ctx.send(f'Card {card_name} not found.')

    except Exception as e:
        print(e)
        await ctx.send('Error assigning task.')

# Command - Discuss Trello Card in Discord
@bot.command(name='discussTask')
async def discuss_task(ctx, card_name):
    try:
        # Find the Trello card
        card_id = None
        cards = trello.boards.get_card(TRELLO_BOARD_ID)
        for card in cards:
            if card['name'] == card_name:
                card_id = card['id']

        if card_id:
            # Fetch comments on the Trello card
            comments = trello.cards.get_comment(card_id)

            # Send comments to Discord
            if comments:
                response = f'Discussion for {card_name}:\n'
                for comment in comments:
                    response += f'- {comment["data"]["text"]}\n'
            else:
                response = 'No discussion found for this task.'

            await ctx.send(response)
        else:
            await ctx.send(f'Card {card_name} not found.')

    except Exception as e:
        print(e)
        await ctx.send('Error fetching task discussion.')

# Command - Custom Trello Command
@bot.command(name='customCommand')
async def custom_command(ctx, *args):
    # Implement your custom logic based on the command arguments
    # Example: !customCommand arg1 arg2
    response = f'Custom Command Executed with Args: {", ".join(args)}'
    await ctx.send(response)

# Command - Vote on Trello Card
@bot.command(name='voteTask')
async def vote_task(ctx, card_name):
    try:
        # Find the Trello card
        card_id = None
        cards = trello.boards.get_card(TRELLO_BOARD_ID)
        for card in cards:
            if card['name'] == card_name:
                card_id = card['id']

        if card_id:
            # Add a vote to the Trello card
            trello.cards.new_action_comment(card_id, '👍')  # Use emoji for voting
            await ctx.send(f'Vote added for {card_name}.')
        else:
            await ctx.send(f'Card {card_name} not found.')

    except Exception as e:
        print(e)
        await ctx.send('Error adding vote.')

# Run the bot
bot.run(DISCORD_TOKEN)
