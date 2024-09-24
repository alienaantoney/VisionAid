import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from config import TELEGRAM_TOKEN
from handlers.new_ticket import new_ticket, select_premise, capture_request_subject, capture_request_description, capture_request_media
from handlers.existing_ticket import existing_ticket, fetch_ticket_status
from api.find_user import get_user_info

# In-memory storage for contact numbers and button display state
contacts = {}
button_shown = {}

async def start(update: Update, context: CallbackContext) -> None:
    contact_button = KeyboardButton(text="Share Contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Please share your contact number with me.", reply_markup=reply_markup)

async def contact(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    contact_number = update.message.contact.phone_number

    contacts[user_id] = contact_number
    button_shown[user_id] = False  # Reset the button shown state

    try:
        user_name, reference_id = get_user_info(contact_number)
    except Exception as e:
        await update.message.reply_text(f"Sorry, there was an error retrieving your information: {e}")
        return

    if user_name == "User not found":
        await update.message.reply_text("User not found. Please make sure your contact number is correct.")
    else:
        await update.message.reply_text(f"Welcome, {user_name}")

        keyboard = [
            [InlineKeyboardButton("New Ticket", callback_data=f'new_ticket_{reference_id}')],
            [InlineKeyboardButton("Existing Ticket", callback_data='existing_ticket')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("What would you like to do?", reply_markup=reply_markup)

        button_shown[user_id] = True  # Set the button shown state to True

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data.startswith('new_ticket'):
        reference_id = query.data.split('_')[2]
        await new_ticket(query, context, reference_id)
    elif query.data.startswith('select_premise'):
        await select_premise(update, context)
    elif query.data == 'existing_ticket':
        await existing_ticket(query, context)

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id in contacts:
        contact_number = contacts[user_id]

        try:
            user_name, reference_id = get_user_info(contact_number)
        except Exception as e:
            await update.message.reply_text(f"Sorry, there was an error retrieving your information: {e}")
            return

        if user_name == "User not found":
            await update.message.reply_text("User not found. Please make sure your contact number is correct.")
        else:
            if not button_shown.get(user_id, False):  # Check if the button was already shown
                keyboard = [
                    [InlineKeyboardButton("New Ticket", callback_data=f'new_ticket_{reference_id}')],
                    [InlineKeyboardButton("Existing Ticket", callback_data='existing_ticket')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(f"Welcome back, {user_name}. What would you like to do?", reply_markup=reply_markup)
                button_shown[user_id] = True  # Set the button shown state to True
    else:
        await start(update, context)  # Trigger contact collection

    if 'conversation_state' in context.user_data:
        if context.user_data['conversation_state'] == 'WAITING_FOR_SUBJECT':
            await capture_request_subject(update, context)
        elif context.user_data['conversation_state'] == 'WAITING_FOR_DESCRIPTION':
            await capture_request_description(update, context)
        elif context.user_data['conversation_state'] == 'WAITING_FOR_MEDIA':
            await capture_request_media(update, context)
        elif context.user_data['conversation_state'] == 'WAITING_FOR_TICKETNUMBER':
            await fetch_ticket_status(update, context)
    else:
        None

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(MessageHandler(filters.CONTACT, contact))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()

