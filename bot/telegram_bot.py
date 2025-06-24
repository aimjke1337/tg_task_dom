"""Simple Telegram bot to handle service requests."""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ConversationHandler
)

from django.conf import settings
from services.models import Service, ServiceRequest


CHOOSING_SERVICE, FILLING_NAME, FILLING_ADDRESS, FILLING_PHONE = range(4)


async def start(update: Update, context):
    keyboard = [["Заказать услугу"], ["Поддержка"], ["История заказов"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите действие", reply_markup=markup)


async def choose_service(update: Update, context):
    services = Service.objects.all()
    keyboard = [[s.name] for s in services]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите услугу", reply_markup=markup)
    return CHOOSING_SERVICE


async def service_chosen(update: Update, context):
    service_name = update.message.text
    service = Service.objects.filter(name=service_name).first()
    if not service:
        await update.message.reply_text("Неизвестная услуга")
        return CHOOSING_SERVICE
    context.user_data["service_id"] = service.id
    await update.message.reply_text("Введите ФИО")
    return FILLING_NAME


async def fill_name(update: Update, context):
    context.user_data["full_name"] = update.message.text
    await update.message.reply_text("Введите адрес")
    return FILLING_ADDRESS


async def fill_address(update: Update, context):
    context.user_data["address"] = update.message.text
    await update.message.reply_text("Введите телефон")
    return FILLING_PHONE


async def fill_phone(update: Update, context):
    context.user_data["phone"] = update.message.text
    service = Service.objects.get(id=context.user_data["service_id"])
    ServiceRequest.objects.create(
        service=service,
        full_name=context.user_data["full_name"],
        address=context.user_data["address"],
        phone=context.user_data["phone"],
    )
    await update.message.reply_text("Ваше обращение принято в работу")
    return ConversationHandler.END


def run_bot():
    application = Application.builder().token(settings.TG_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Заказать услугу$"), choose_service)],
        states={
            CHOOSING_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, service_chosen)],
            FILLING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, fill_name)],
            FILLING_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, fill_address)],
            FILLING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, fill_phone)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.run_polling()

