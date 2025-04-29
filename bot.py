import logging
import random
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with the main menu when the command /start is issued."""
    keyboard = [
        [
            InlineKeyboardButton("📖 How to Play", callback_data='how_to_play'),
        ],
        [
            InlineKeyboardButton("🎮 Start Game", callback_data='start_game'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to HvesmarFlippaBot! 🪙\n\n"
        "I'm your decision-making companion. When you're unsure about something, "
        "I can help you make a choice by flipping a coin.\n\n"
        "Choose an option below to get started!",
        reply_markup=reply_markup
    )

async def how_to_play(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show how to play instructions."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("🎮 Start Game", callback_data='start_game'),
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="🎮 *How to Play HvesmarFlippaBot* 🎮\n\n"
        "1. Click the 'Start Game' button to begin\n"
        "2. I'll flip a coin for you\n"
        "3. The result will show either Heads or Tails\n"
        "4. Use this result to help make your decision\n"
        "5. You can flip again as many times as you need\n\n"
        "Remember: This is just for fun and to help with simple decisions!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Return to the main menu."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("📖 How to Play", callback_data='how_to_play'),
        ],
        [
            InlineKeyboardButton("🎮 Start Game", callback_data='start_game'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="Welcome to HvesmarFlippaBot! 🪙\n\n"
        "I'm your decision-making companion. When you're unsure about something, "
        "I can help you make a choice by flipping a coin.\n\n"
        "Choose an option below to get started!",
        reply_markup=reply_markup
    )

async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start the coin flip game."""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("🪙 Flip Coin", callback_data='flip'),
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text="Ready to make a decision? 🪙\n\n"
        "Click the button below to flip the coin!",
        reply_markup=reply_markup
    )

async def flip_coin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the coin flip button press."""
    query = update.callback_query
    await query.answer()

    # Flip the coin
    result = random.choice(['Heads', 'Tails'])
    
    # Create new keyboard for another flip
    keyboard = [
        [
            InlineKeyboardButton("🪙 Flip Again", callback_data='flip'),
        ],
        [
            InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send the result with emoji
    emoji = "🪙" if result == "Heads" else "🪙"
    await query.edit_message_text(
        text=f"The coin landed on: {result} {emoji}\n\n"
        f"Need another flip? Or want to go back to the menu?",
        reply_markup=reply_markup
    )

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(how_to_play, pattern='^how_to_play$'))
    application.add_handler(CallbackQueryHandler(start_game, pattern='^start_game$'))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern='^back_to_menu$'))
    application.add_handler(CallbackQueryHandler(flip_coin, pattern='^flip$'))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 
