#!/usr/bin/env python3
"""
بوت حياتنا الزوجية 🤍
تذكيرات منزلية تلقائية
"""

import os
import logging
from datetime import datetime, time
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ===== الإعدادات =====
TOKEN   = os.environ["BOT_TOKEN"]   # من BotFather
CHAT_ID = int(os.environ["CHAT_ID"]) # ID المجموعة الزوجية
TZ      = pytz.timezone("Asia/Riyadh")

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO
)

# ===== رسائل التذكيرات =====
MSGS = {
    "morning":     "🌅 *صباح الخير يا حبايب!*\nلا تنسون ترتيب غرفة النوم والصالة وتعطيرها اليوم 🕌",
    "incense":     "🪔 وقت البخور والترتيب العام للبيت ✨",
    "laundry":     "🧺 *الأربعاء — يوم الغسيل والكي!*\nلا تنسون الملابس المتسخة 👕",
    "restaurant":  "🍽️ *يوم المطعم هذا الأسبوع!*\nالخميس ولا السبت؟ وأي مطعم تبغون؟ 😋",
    "family":      "👨‍👩‍👧 *يوم الجمعة* — زيارة الأهل بعد صلاة الجمعة 🤍",
    "cleaning":    "🧹 *التنظيف الأسبوعي*\nمسح الأرضيات والبلاط والتلميع ✨",
    "workout":     "🏃 *وقت التمرين!*\nتمارين خفيفة في البيت — ولو 20 دقيقة تكفي 💪",
    "groceries":   "🛒 *وقت قائمة المقاضي!*\nنكتب سوا احتياجات الطبخ للأسبوعين الجايين 📝",
    "mall":        "🛍️ *أول الشهر — وقت المول!*\nنتفق على الميزانية والوقت المناسب 🗓️",
    "deep_clean":  "🧼 *التنظيف العميق الشهري*\nتعقيم + مبيد حشري + غسيل عميق 🏠",
    "online_shop": "📦 *وقت مراجعة الطلبيات الأونلاين*\nفيه شيء محتاجينه؟ نرتبها سوا 🛒",
}

# ===== دالة الإرسال =====
async def send(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=MSGS[context.job.data],
        parse_mode="Markdown"
    )

# ===== فحص شهري — يشتغل كل يوم ويتحقق من التاريخ =====
async def monthly_check(context: ContextTypes.DEFAULT_TYPE):
    now  = datetime.now(TZ)
    day  = now.day
    month = now.month

    # أول الشهر — المول
    if day == 1:
        await context.bot.send_message(chat_id=CHAT_ID, text=MSGS["mall"], parse_mode="Markdown")

    # منتصف الشهر — تنظيف عميق
    if day == 15:
        await context.bot.send_message(chat_id=CHAT_ID, text=MSGS["deep_clean"], parse_mode="Markdown")

    # كل شهرين (الأشهر الفردية) — تسوق أونلاين
    if day == 1 and month % 2 == 1:
        await context.bot.send_message(chat_id=CHAT_ID, text=MSGS["online_shop"], parse_mode="Markdown")

# ===== فحص كل أسبوعين — المقاضي =====
async def biweekly_groceries(context: ContextTypes.DEFAULT_TYPE):
    week_number = datetime.now(TZ).isocalendar()[1]
    if week_number % 2 == 0:  # الأسابيع الزوجية فقط
        await context.bot.send_message(chat_id=CHAT_ID, text=MSGS["groceries"], parse_mode="Markdown")

# ===== أوامر البوت =====
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(
        f"🤍 *بوت حياتنا الزوجية شغال!*\n\n"
        f"📌 ID هذه المجموعة: `{chat_id}`\n\n"
        f"الأوامر:\n"
        f"/reminders — عرض كل التذكيرات\n"
        f"/test — تجربة البوت\n"
        f"/help — مساعدة",
        parse_mode="Markdown"
    )

async def cmd_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 *التذكيرات النشطة:*\n\n"
        "🔁 *يومياً* 8:00 ص — ترتيب البيت وتعطيره\n"
        "🔁 *الاثنين والخميس* 8:00 م — بخور\n\n"
        "📅 *الأربعاء* 9:00 ص — غسيل وكي\n"
        "📅 *الأربعاء* 6:00 م — اختيار مطعم الأسبوع\n"
        "📅 *الجمعة* 9:00 ص — تنظيف أسبوعي\n"
        "📅 *الجمعة* 11:00 ص — زيارة الأهل\n"
        "📅 *الأحد والثلاثاء* 7:00 م — تمرين في البيت\n\n"
        "📆 *كل أسبوعين (سبت)* — قائمة المقاضي\n"
        "📆 *1 كل شهر* — رحلة المول\n"
        "📆 *15 كل شهر* — تنظيف عميق\n"
        "📆 *كل شهرين* — تسوق أونلاين",
        parse_mode="Markdown"
    )

async def cmd_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت شغال وتذكيراتك نشطة 🤍")

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *مساعدة البوت*\n\n"
        "/start — تشغيل البوت وعرض ID المجموعة\n"
        "/reminders — عرض جدول التذكيرات\n"
        "/test — التأكد إن البوت شغال\n"
        "/help — هذه الرسالة",
        parse_mode="Markdown"
    )

# ===== الإعداد الرئيسي =====
def main():
    app = Application.builder().token(TOKEN).build()
    jq  = app.job_queue

    # ── يومياً ──────────────────────────────────────────
    # كل يوم 8 صباحاً — ترتيب البيت
    jq.run_daily(send, time=time(8, 0, tzinfo=TZ), data="morning")

    # ── كل يومين ────────────────────────────────────────
    # الاثنين(0) والخميس(3) 8 مساءً — بخور
    jq.run_daily(send, time=time(20, 0, tzinfo=TZ), days=(0, 3), data="incense")

    # ── أسبوعي ──────────────────────────────────────────
    # الأربعاء(2) 9 صباحاً — غسيل وكي
    jq.run_daily(send, time=time(9, 0, tzinfo=TZ), days=(2,), data="laundry")
    # الأربعاء(2) 6 مساءً — اختيار مطعم
    jq.run_daily(send, time=time(18, 0, tzinfo=TZ), days=(2,), data="restaurant")
    # الجمعة(4) 9 صباحاً — تنظيف أسبوعي
    jq.run_daily(send, time=time(9, 0, tzinfo=TZ), days=(4,), data="cleaning")
    # الجمعة(4) 11 صباحاً — زيارة الأهل
    jq.run_daily(send, time=time(11, 0, tzinfo=TZ), days=(4,), data="family")
    # الأحد(6) والثلاثاء(1) 7 مساءً — تمرين
    jq.run_daily(send, time=time(19, 0, tzinfo=TZ), days=(6, 1), data="workout")

    # ── كل أسبوعين ──────────────────────────────────────
    # السبت(5) 10 صباحاً — مقاضي (الأسابيع الزوجية فقط)
    jq.run_daily(biweekly_groceries, time=time(10, 0, tzinfo=TZ), days=(5,))

    # ── شهري وكل شهرين ──────────────────────────────────
    # فحص يومي الساعة 9 صباحاً
    jq.run_daily(monthly_check, time=time(9, 0, tzinfo=TZ))

    # ── أوامر ────────────────────────────────────────────
    app.add_handler(CommandHandler("start",     cmd_start))
    app.add_handler(CommandHandler("reminders", cmd_reminders))
    app.add_handler(CommandHandler("test",      cmd_test))
    app.add_handler(CommandHandler("help",      cmd_help))

    print("🤍 البوت شغال! اضغط Ctrl+C للإيقاف")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
