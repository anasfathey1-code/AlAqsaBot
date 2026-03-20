import requests
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- بياناتك ---
TELEGRAM_TOKEN = "8723613057:AAEe6IuB46Sd6tSDTeXaLgoo9kBjnMYURh4"
GROQ_API_KEY = "ضع_مفتاح_جروك_الجديد_هنا"

# وظيفة قراءة ملف الأحياء
def get_manhaj_content():
    # تأكد أن اسم الملف هنا مطابق تماماً لاسم ملفك في Pydroid 3
    file_name = "Ahyaa.txt" 
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()
    else:
        return "عذراً، لم يتم العثور على ملف المنهج (Ahyaa.txt)."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    manhaj = get_manhaj_content()
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY.strip()}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile", 
        "messages": [
            {
                "role": "system", 
                "content": f"""أنت 'مساعد مدرسة الأقصى الذكي' والمتخصص في مادة الأحياء.
                مهمتك: مساعدة الطلاب في فهم مادة الأحياء بناءً على المنهج المرفق فقط:
                --- منهج الأحياء المرفوع ---
                {manhaj}
                -----------------------
                تعليماتك:
                1. التزم بالمعلومات الموجودة في النص أعلاه.
                2. اشرح المصطلحات المعقدة (مثل الانقسام الميتوزي، الوراثة، إلخ) بأسلوب مبسط ولهجة يمنية محببة.
                3. إذا سألك الطالب عن موضوع غير موجود في ملف 'Ahyaa.txt'، قل له: 'يا بطل، هذا الموضوع مش في منهجنا الحالي، ركز في دروسك'.
                """
            },
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.4 
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if response.status_code == 200:
            ai_reply = result['choices'][0]['message']['content']
            await update.message.reply_text(ai_reply)
        else:
            await update.message.reply_text("عذراً، واجهت مشكلة في الوصول لعقل البوت.")
    except Exception as e:
        await update.message.reply_text("تأكد من تشغيل الإنترنت.")

if __name__ == '__main__':
    print("--- البوت يقرأ الآن من ملف Ahyaa.txt ---")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
