from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ConversationHandler
)
from django.conf import settings
from accounts.models import User
from services.models import Service, Client, Request

CHOOSING_SERVICE, FILLING_DYNAMIC = range(2)

async def start(update: Update, context):
    tg_username = update.effective_user.username or str(update.effective_user.id)
    user, _ = User.objects.get_or_create(username=tg_username)
    client, _ = Client.objects.get_or_create(user=user, telegram_username=tg_username)
    if not all([client.full_name, client.phone, client.address]):
        context.user_data['reg_client'] = client
        context.user_data['reg_fields'] = ['full_name', 'phone', 'address']
        await update.message.reply_text('Введите ФИО')
        return FILLING_DYNAMIC
    keyboard = [["Заказать услугу"], ["Поддержка"], ["История заказов"]]
    await update.message.reply_text("Выберите действие", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def dynamic_handler(update: Update, context):
    client = context.user_data.get('reg_client')
    if client:
        field = context.user_data['reg_fields'][0]
        setattr(client, field, update.message.text)
        context.user_data['reg_fields'].pop(0)
        if context.user_data['reg_fields']:
            prompts = {
                'full_name': 'Введите ФИО',
                'phone': 'Введите телефон',
                'address': 'Введите адрес',
            }
            await update.message.reply_text(prompts[context.user_data['reg_fields'][0]])
            return FILLING_DYNAMIC
        client.save()
        context.user_data.pop('reg_client')
        keyboard = [["Заказать услугу"], ["Поддержка"], ["История заказов"]]
        await update.message.reply_text("Выберите действие", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return ConversationHandler.END
    # ordering service
    questions = context.user_data['questions']
    idx = context.user_data.get('q_idx', 0)
    context.user_data.setdefault('answers', {})
    context.user_data['answers'][questions[idx]] = update.message.text
    idx += 1
    if idx < len(questions):
        context.user_data['q_idx'] = idx
        await update.message.reply_text(questions[idx])
        return FILLING_DYNAMIC
    # create request
    service = Service.objects.get(id=context.user_data['service_id'])
    client = Client.objects.get(user__username=update.effective_user.username)
    req = Request.objects.create(client=client, service=service, data=context.user_data['answers'])
    await update.message.reply_text(f"Спасибо, ваша заявка принята, ID №{req.id}.")
    context.user_data.clear()
    return ConversationHandler.END

async def choose_service(update: Update, context):
    services = Service.objects.all()
    keyboard = [[s.name] for s in services]
    await update.message.reply_text("Выберите услугу", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    return CHOOSING_SERVICE

async def service_chosen(update: Update, context):
    service = Service.objects.filter(name=update.message.text).first()
    if not service:
        await update.message.reply_text("Неизвестная услуга")
        return CHOOSING_SERVICE
    context.user_data['service_id'] = service.id
    questions = service.form_schema or []
    context.user_data['questions'] = questions
    if questions:
        await update.message.reply_text(questions[0])
        context.user_data['q_idx'] = 0
        return FILLING_DYNAMIC
    client = Client.objects.get(user__username=update.effective_user.username)
    req = Request.objects.create(client=client, service=service)
    await update.message.reply_text(f"Спасибо, ваша заявка принята, ID №{req.id}.")
    return ConversationHandler.END

async def history(update: Update, context):
    client = Client.objects.get(user__username=update.effective_user.username)
    requests = client.requests.all()
    text = "\n".join([f"#{r.id} — {r.service.name} — {r.status}" for r in requests]) or "История пуста"
    await update.message.reply_text(text)

async def support(update: Update, context):
    users = User.objects.filter(is_support=True)
    usernames = ", ".join([f"@{u.username}" for u in users]) or "нет"
    await update.message.reply_text(f"Наши менеджеры: {usernames}")

def run_bot():
    application = Application.builder().token(settings.TG_BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Заказать услугу$"), choose_service), CommandHandler('start', start)],
        states={
            CHOOSING_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, service_chosen)],
            FILLING_DYNAMIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, dynamic_handler)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    application.add_handler(conv)
    application.add_handler(MessageHandler(filters.Regex("^История заказов$"), history))
    application.add_handler(MessageHandler(filters.Regex("^Поддержка$"), support))
    application.run_polling()
