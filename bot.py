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
TOKEN   = os.environ["BOT_TOKEN"]
CHAT_ID = int(os.environ["CHAT_ID"])
# أضف في Railway: MEMBERS=123456789,987654321 (IDs مفصولة بفاصلة)
MEMBERS = [m.strip() for m in os.environ.get("MEMBERS", "").split(",") if m.strip()]
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
 
# ===== بناء المنشنات =====
def build_mentions() -> str:
    """يبني منشن لكل عضو مسجّل"""
    if not MEMBERS:
        return ""
    return " ".join(f"[‌](tg://user?id={uid})" for uid in MEMBERS)
 
# ===== دالة الإرسال العادي =====
async def send(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=MSGS[context.job.data],
        parse_mode="Markdown"
    )
 
# ===== رسالة الصباح اليومية (10 ص) =====
async def send_morning(context: ContextTypes.DEFAULT_TYPE):
    mentions = build_mentions()
    now      = datetime.now(TZ)
    days_ar  = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
    day_name = days_ar[now.weekday()]
 
    text = (
        f"☀️ *صباحكم خير وسعادة* {mentions}\n\n"
        f"📅 اليوم: *{day_name} {now.day}/{now.month}*\n\n"
        f"🤍 يوم جميل بإذن الله"
    )
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        parse_mode="Markdown"
    )
 
# ===== فحص شهري =====
async def monthly_check(context: ContextTypes.DEFAULT_TYPE):
    now   = datetime.now(TZ)
    day   = now.day
    month = now.month
 
    if day == 1:
        await context.bot.send_message(chat_id=CHAT_ID, text=MSGS["mall"], parse_mode="Markdown")
    if day == 15:
        await context.bot.send_message(chat_id=CHAT_ID, text=MSGS["deep_clean"], parse_mode="Markdown")
    if day == 1 and month % 2 == 1:
        await context.bot.send_message(chat_id=CHAT_ID, text=MSGS["online_shop"], parse_mode="Markdown")
 
# ===== فحص كل أسبوعين =====
async def biweekly_groceries(context: ContextTypes.DEFAULT_TYPE):
    week_number = datetime.now(TZ).isocalendar()[1]
    if week_number % 2 == 0:
        await context.bot.send_message(chat_id=CHAT_ID, text=MSGS["groceries"], parse_mode="Markdown")
 
# ===== أوامر البوت =====
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    await update.message.reply_text(
        f"🤍 *بوت حياتنا الزوجية شغال!*\n\n"
        f"📌 ID المجموعة: `{chat_id}`\n"
        f"👤 ID حسابك: `{user_id}`\n\n"
        f"الأوامر:\n"
        f"/reminders — جدول التذكيرات\n"
        f"/myid — اعرف ID حسابك\n"
        f"/test — تجربة البوت\n"
        f"/goodmorning — تجربة رسالة الصباح",
        parse_mode="Markdown"
    )
 
async def cmd_myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر للحصول على user ID"""
    user = update.effective_user
    await update.message.reply_text(
        f"👤 *معلوماتك:*\n\n"
        f"الاسم: {user.full_name}\n"
        f"ID: `{user.id}`\n\n"
        f"📋 انسخ هذا الـ ID وأضفه في Railway Variables تحت `MEMBERS`",
        parse_mode="Markdown"
    )
 
async def cmd_goodmorning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تجربة رسالة الصباح"""
    await send_morning(context)
 
async def cmd_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 *التذكيرات النشطة:*\n\n"
        "☀️ *يومياً* 10:00 ص — صباح الخير للجميع\n"
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
    members_status = f"✅ {len(MEMBERS)} عضو مسجّل" if MEMBERS else "⚠️ ما في أعضاء مسجّلين بعد — استخدم /myid"
    await update.message.reply_text(
        f"✅ *البوت شغال* 🤍\n\n"
        f"👥 الأعضاء: {members_status}\n"
        f"🕐 الوقت الحالي: {datetime.now(TZ).strftime('%I:%M %p')}",
        parse_mode="Markdown"
    )
 
# ===== الإعداد الرئيسي =====
def main():
    app = Application.builder().token(TOKEN).build()
    jq  = app.job_queue
 
    # ── صباح يومي ───────────────────────────────────────
    # كل يوم 10:00 ص — صباح الخير + منشن
    jq.run_daily(send_morning, time=time(10, 0, tzinfo=TZ))
 
    # ── يومياً ──────────────────────────────────────────
    jq.run_daily(send, time=time(8, 0, tzinfo=TZ), data="morning")
 
    # ── كل يومين ────────────────────────────────────────
    jq.run_daily(send, time=time(20, 0, tzinfo=TZ), days=(0, 3), data="incense")
 
    # ── أسبوعي ──────────────────────────────────────────
    jq.run_daily(send, time=time(9, 0, tzinfo=TZ),  days=(2,), data="laundry")
    jq.run_daily(send, time=time(18, 0, tzinfo=TZ), days=(2,), data="restaurant")
    jq.run_daily(send, time=time(9, 0, tzinfo=TZ),  days=(4,), data="cleaning")
    jq.run_daily(send, time=time(11, 0, tzinfo=TZ), days=(4,), data="family")
    jq.run_daily(send, time=time(19, 0, tzinfo=TZ), days=(6, 1), data="workout")
 
    # ── كل أسبوعين ──────────────────────────────────────
    jq.run_daily(biweekly_groceries, time=time(10, 0, tzinfo=TZ), days=(5,))
 
    # ── شهري ────────────────────────────────────────────
    jq.run_daily(monthly_check, time=time(9, 0, tzinfo=TZ))
 
    # ── أوامر ────────────────────────────────────────────
    app.add_handler(CommandHandler("start",      cmd_start))
    app.add_handler(CommandHandler("myid",       cmd_myid))
    app.add_handler(CommandHandler("reminders",  cmd_reminders))
    app.add_handler(CommandHandler("test",       cmd_test))
    app.add_handler(CommandHandler("goodmorning", cmd_goodmorning))
 
    print("🤍 البوت شغال!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
 
if __name__ == "__main__":
    main()
 
