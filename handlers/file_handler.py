from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import user_data_store
from services.parser import extract_text
from services.analyzer import compare_skills, classify_text
from services.resume_generator import generate_resume_pdf
import asyncio


# 🔄 CLEAN LOADER (FAST)
async def circular_loader(update):
    steps = [
        "Analyzing JD...",
        "Extracting skills...",
        "Matching resume...",
        "Preparing report..."
    ]

    message = await update.message.reply_text("🤖 Processing...")

    for step in steps:
        await message.edit_text(f"🔄 {step}")
        await asyncio.sleep(0.3)

    await message.edit_text("✅ Done!")


# 🤖 TEXT QUERY HANDLER
async def handle_query(update, context):
    user_id = update.message.chat_id

    if user_id not in user_data_store or "jd" not in user_data_store[user_id]:
        await update.message.reply_text("⚠️ Upload JD first")
        return

    await update.message.reply_text("🤖 Ask like:\n- important skills\n- what should I focus on")


# 📄 FILE HANDLER
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    file = update.message.document

    if file:
        new_file = await file.get_file()
        file_path = file.file_name

        await new_file.download_to_drive(file_path)

        if user_id not in user_data_store:
            user_data_store[user_id] = {}

        text = extract_text(file_path)

        if not text:
            await update.message.reply_text("⚠️ Could not extract text")
            return

        file_type = classify_text(text)

        # ✅ STORE FULL TEXT
        user_data_store[user_id][file_type] = text

        if file_type == "jd":
            await update.message.reply_text("📌 JD saved. Now upload Resume")
        else:
            await update.message.reply_text("✅ Resume saved")

        # 🔥 PROCESS WHEN BOTH AVAILABLE
        if "jd" in user_data_store[user_id] and "resume" in user_data_store[user_id]:

            jd_text = user_data_store[user_id]["jd"]
            resume_text = user_data_store[user_id]["resume"]

            await circular_loader(update)

            # 🔥 NEW ANALYSIS (DICT FORMAT)
            result = compare_skills(jd_text, resume_text)

            msg = "📊 SMART ANALYSIS REPORT\n"
            msg += "━━━━━━━━━━━━━━━\n\n"

            msg += f"🧠 JD Domain: {result['jd_domain']}\n"
            msg += f"🧠 Resume Domain: {result['resume_domain']}\n\n"

            msg += f"🎯 Score: {result['score']}/100\n\n"

            # 📌 JD NEEDS
            msg += "📌 JD Requires:\n"
            msg += "\n".join([f"• {s}" for s in result["jd_skills"]]) or "None"

            # ✅ YOUR SKILLS
            msg += "\n\n✅ Your Skills:\n"
            msg += "\n".join([f"✔ {s}" for s in result["resume_skills"]]) or "None"

            # 🟢 MATCHED
            msg += "\n\n🟢 Matching Skills:\n"
            msg += "\n".join([f"✔ {s}" for s in result["matched"]]) or "None"

            # ❌ MISSING
            msg += "\n\n❌ Missing Skills:\n"
            msg += "\n".join([f"✖ {s}" for s in result["missing"]]) or "None"

            # ⚠️ EXTRA
            msg += "\n\n⚠️ Extra Skills:\n"
            msg += "\n".join([f"• {s}" for s in result["extra"]]) or "None"

            # 💡 IMPROVEMENTS
            msg += "\n\n💡 Improvements:\n"
            msg += "\n".join([f"👉 {i}" for i in result["improvements"]])

            await update.message.reply_text(msg)

            # 📄 OPTIONAL PDF (you can improve later)
            pdf_file = generate_resume_pdf(result["jd_skills"], result["matched"], result["missing"])

            with open(pdf_file, "rb") as f:
                await update.message.reply_document(document=f)

            del user_data_store[user_id]