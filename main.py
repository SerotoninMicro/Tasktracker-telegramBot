import random
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

NEW_TASKLIST, ADD_TASKS, VIEW_TASKS = range(3)

def start(update, context):
    update.message.reply_text(
        "Welcome to Task Bot! Here's what I can do:\n\n"
        "1. /newtasklist - Start a new task list\n"
        "2. /viewtasks - View your saved tasks\n"
        "3. /cleartasks - Clear your saved tasks\n"
        "4. /randomtask - Get a random task from your list\n"
        "5. /restart - Restart the bot session\n"
        "Feel free to explore these options!"
    )

def restart(update, context):
    update.message.reply_text("Bot session restarted. Use /start to begin.")
    return ConversationHandler.END

def newtasklist(update, context):
    keyboard = [
        [KeyboardButton("📝 Add Tasks"), KeyboardButton("🔍 View Tasks")]
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text("Choose an option:", reply_markup=markup)
    return NEW_TASKLIST

def addtasks(update, context):
    update.message.reply_text("Enter your tasks separated by commas:")
    return ADD_TASKS

def viewtasks(update, context):
    tasks = context.user_data.get('tasks', [])
    if tasks:
        task_list = "\n".join(tasks)
        update.message.reply_text("Your tasks:\n" + task_list)
    else:
        update.message.reply_text("You haven't added any tasks yet.")

def cleartasks(update, context):
    context.user_data['tasks'] = []
    update.message.reply_text("Your task list has been cleared.")

def randomtask(update, context):
    tasks = context.user_data.get('tasks', [])
    if tasks:
        random_task = random.choice(tasks)
        update.message.reply_text("Your random task is: " + random_task)
    else:
        update.message.reply_text("You haven't added any tasks yet.")

def tasks_input(update, context):
    user_input = update.message.text

    new_tasks = user_input.split(',')

    new_tasks = [task.strip() for task in new_tasks if task.strip()]

    if not new_tasks:
        update.message.reply_text("No tasks provided. Please enter at least one task.")
        return ADD_TASKS

    tasks = context.user_data.get('tasks', [])
    
    tasks.extend(new_tasks)

    context.user_data['tasks'] = tasks

    update.message.reply_text("Tasks added successfully!")
    return ConversationHandler.END

def main():
    updater = Updater("MY_API_IS_HERE", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('restart', restart))
    dispatcher.add_handler(CommandHandler('viewtasks', viewtasks))
    dispatcher.add_handler(CommandHandler('cleartasks', cleartasks))
    dispatcher.add_handler(CommandHandler('randomtask', randomtask))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('newtasklist', newtasklist)],
        states={
            NEW_TASKLIST: [
                MessageHandler(Filters.regex('^📝 Add Tasks$'), addtasks),
                MessageHandler(Filters.regex('^🔍 View Tasks$'), viewtasks),
            ],
            ADD_TASKS: [MessageHandler(Filters.text & ~Filters.command, tasks_input)],
        },
        fallbacks=[]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
