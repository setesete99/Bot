import logging
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = "7977593128:AAHzwfhgfKxc-FOZv04zoMcmeBBNoJG-f7A"
suporte = "@Skarlet7771"

usuarios = {}
saldos = {}
pontos = {}
giftcodes = {}

estoque = {
    "485464": [
        "4854647167981478|06|2026|789",
        "4854645152577434|06|2026|789",
        "4854645152574241|06|2026|789",
        "4854645152580354|06|2027|789"
    ],
    "498407": [],
    "498408": []
}

precos = {
    "485464": 4,
    "498407": 4,
    "498408": 4
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nome = update.effective_user.first_name
    usuarios[user_id] = nome
    saldos.setdefault(user_id, 0)
    pontos.setdefault(user_id, 0)

    texto = f"👋 Olá {nome}, bem-vindo! A melhor Store Do 7\n\n💰 Saldo: R${saldos[user_id]}\n⭐ Pontos: {pontos[user_id]}\n🆔 ID: {user_id}\nCanal: https://t.me/Mentespensantes777"

    with open("banner.jpeg", "rb") as f:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=f,
            caption=texto,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Adicionar saldo", callback_data="saldo"),
                    InlineKeyboardButton("GGS 💳", callback_data="produtos")
                ],
                [
                    InlineKeyboardButton("Resgatar Gift Code", callback_data="resgatar"),
                    InlineKeyboardButton("Suporte", url=f"https://t.me/{suporte.lstrip('@')}")
                ]
            ])
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except:
        pass

    if query.data == "saldo":
        with open("banner.jpeg", "rb") as f:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=f,
                caption=f"Pix Automático OFF. Adicione saldo via suporte {suporte}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
                ])
            )

    elif query.data == "produtos":
        produtos = list(estoque.keys())
        botoes_produtos = [[InlineKeyboardButton(f"💳 {p} - R${precos.get(p, 0)}", callback_data=f"comprar_{p}")] for p in produtos]
        botoes_produtos.append([InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")])
        with open("banner.jpeg", "rb") as f:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=f,
                caption="Escolha um produto abaixo:",
                reply_markup=InlineKeyboardMarkup(botoes_produtos)
            )

    elif query.data == "resgatar":
        with open("banner.jpeg", "rb") as f:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=f,
                caption="Envie o código para resgate:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
                ])
            )

    elif query.data == "voltar":
        await start(update, context)

    elif query.data.startswith("comprar_"):
        produto = query.data.split("_")[1]
        if produto not in estoque:
            with open("banner.jpeg", "rb") as f:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=f,
                    caption="❌ Produto inválido.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
                    ])
                )
            return

        if not estoque[produto]:
            with open("banner.jpeg", "rb") as f:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=f,
                    caption="❌ Sem estoque no momento.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
                    ])
                )
            return

        preco = precos.get(produto, 0)
        if saldos.get(user_id, 0) < preco:
            with open("banner.jpeg", "rb") as f:
                await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=f,
                    caption=f"❌ Saldo insuficiente. Produto custa R${preco}",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
                    ])
                )
            return

        card = estoque[produto].pop(0)
        saldos[user_id] -= preco
        pontos[user_id] += 1
        numero, mes, ano, cvv = card.split("|")
        bandeira = "Visa"
        banco = "Banco do Brasil"
        nome_falso = "João da Silva"
        cpf_falso = "123.456.789-00"
        pais = "BR"

        texto = f"""✅ Compra Efetuada!
💳 Cartão: {card}
🔹 Formato: |MM|AAAA|CVV|BANDEIRA|BANCO|
📦 Entrega: {card}|{bandeira.upper()}|{banco.upper()}
👤 Nome: {nome_falso}
🧾 CPF: {cpf_falso}
🌍 País: {pais}
🏦 Banco: {banco}
💳 Bandeira: {bandeira}
💰 Novo saldo: R${saldos[user_id]}
⭐ Pontos: {pontos[user_id]}"""

        with open("banner.jpeg", "rb") as f:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=f,
                caption=texto,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
                ])
            )

async def gerar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != 1956193181:
        await update.message.reply_text("❌ Apenas o admin pode usar este comando.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Use: /gerar VALOR")
        return
    try:
        valor = int(context.args[0])
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        giftcodes[codigo] = valor
        await update.message.reply_text(f"Gift code criado: {codigo}\nValor: R${valor}", parse_mode="Markdown")
    except:
        await update.message.reply_text("Erro ao gerar gift code. Use um valor numérico.")

async def mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
    except:
        pass

    texto = update.message.text.strip().upper()
    if texto in giftcodes:
        valor = giftcodes.pop(texto)
        saldos[user_id] = saldos.get(user_id, 0) + valor
        with open("banner.jpeg", "rb") as f:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=f,
                caption=f"✅ Gift code resgatado com sucesso!\n\n💰 Novo saldo: R${saldos[user_id]}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬅️ Voltar", callback_data="voltar")]
                ])
            )
    else:
        await update.message.reply_text("❌ Gift code inválido ou já utilizado.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gerar", gerar))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem))
    print("BOT RODANDO...")
    app.run_polling()