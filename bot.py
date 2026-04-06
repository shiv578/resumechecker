      from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
 from config import TOKEN
from handlers.start import start
from handlers.file_handler import handle_file, handle_query

# 🚀 Create App
app = ApplicationBuilder().token(TOKEN).build()

 # ✅ Start command
app.add_handler(CommandHandler("start", start))

# 📄 File handler (JD + Resume)
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

 # 💬 Text query handler (AI assistant)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query))

print("Bot is running...")
app.run_polling()
