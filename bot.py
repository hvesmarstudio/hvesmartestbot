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
    """Send a message with inline buttons when the command /start is issued."""
    keyboard = [
        [
            InlineKeyboardButton("Flip Coin", callback_data='flip'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to HvesmarFlippaBot! 🪙\n\n"
        "I can help you make decisions by flipping a coin.\n"
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
            InlineKeyboardButton("Flip Again", callback_data='flip'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send the result with emoji
    emoji = "🪙" if result == "Heads" else "🪙"
    await query.edit_message_text(
        text=f"The coin landed on: {result} {emoji}\n\nWant to flip again?",
        reply_markup=reply_markup
    )

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(flip_coin, pattern='^flip$'))

    # Start the Bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 