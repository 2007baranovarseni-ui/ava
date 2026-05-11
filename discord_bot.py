import discord
from discord.ext import commands

TOKEN = "MTUwMzE5NDQ1MDI4Mzk5MTI1Mw.GiOTv_.Jl8TLFA4Lb_ZgRNFWZqu6jzKqqIMOKL3pOJVIE"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

bot.remove_command("help")

# =====================
# ДАННЫЕ
# =====================

sulfur_total = 0
items_total = 0

map_83_count = 0
map_84_count = 0

players = 0

MAP_83_PRICE = 12200000
MAP_84_PRICE = 24000000


# =====================
# НАЧАТЬ (СБРОС)
# =====================

@bot.command(name="начать")
async def start(ctx):
    global sulfur_total, items_total, map_83_count, map_84_count, players

    sulfur_total = 0
    items_total = 0
    map_83_count = 0
    map_84_count = 0
    players = 0

    await ctx.send("бурмалда(сброс всего)")


# =====================
# ЛЮДИ
# =====================

@bot.command(name="люди")
async def people(ctx, count: int):
    global players
    players = count

    await ctx.send(f"Участников: {players} (лутер входит)")


# =====================
# СЕРА (мешки)
# =====================

@bot.command(name="сера")
async def sulfur(ctx, *bags):
    global sulfur_total

    try:
        total_bags = sum(int(x) for x in bags)
        sulfur_total += total_bags * 10000

        await ctx.send(
            f"считал.\n"
            f"Сера: {sulfur_total:,}"
            .replace(",", " ")
        )

    except ValueError:
        await ctx.send("Ошибка: вводи числа")


# =====================
# ШМОТ
# =====================

@bot.command(name="шмот")
async def items(ctx, value: int):
    global items_total

    items_total += value

    await ctx.send(
        f"шмот добавлен: {items_total:,}"
        .replace(",", " ")
    )


# =====================
# КАРТА
# =====================

@bot.command(name="карта")
async def card(ctx, card_type: str, count: int):
    global map_83_count, map_84_count

    if card_type == "8.3":
        map_83_count += count
        await ctx.send(f"8.3 карт: {map_83_count}")

    elif card_type == "8.4":
        map_84_count += count
        await ctx.send(f"8.4 карт: {map_84_count}")

    else:
        await ctx.send("Используй: !карта 8.3 / !карта 8.4")


@bot.command(name="итог")
async def total(ctx):
    global sulfur_total, items_total, players

    if players == 0:
        await ctx.send("Сначала !люди N")
        return

    # =====================
    # КАРТЫ
    # =====================

    map_cost = (
        map_83_count * MAP_83_PRICE +
        map_84_count * MAP_84_PRICE
    )

    sulfur_after_cards = sulfur_total - map_cost

    # =====================
    # КАЗНА / ЛУТЕР
    # =====================

    treasury = int(sulfur_after_cards * 0.05)
    looter = int(sulfur_after_cards * 0.02)

    sulfur_pool = sulfur_after_cards - treasury - looter

    # =====================
    # ШМОТ
    # =====================

    loot_pool = items_total

    # =====================
    # ОБЩИЙ ЛУТ
    # =====================

    total_loot_after = sulfur_pool + loot_pool

    # =====================
    # НА 1 ЧЕЛОВЕКА
    # =====================

    per_sulfur = sulfur_pool // players
    per_loot = loot_pool // players

    await ctx.send(
        f"===== ИТОГ =====\n\n"

        f"Людей: {players}\n\n"

        f"СЕРА: {sulfur_total:,}\n"
        f"ШМОТ: {items_total:,}\n\n"

        f"КАЗНА (5%): {treasury:,}\n"
        f"ЛУТЕР (2%): {looter:,}\n"
        f"ВЫПЛАТА ЗА КАРТЫ: {map_cost:,}\n\n"

        f"Лут в целом (с вычетом карт и казны): {total_loot_after:,}\n\n"

        f"НА РАСПИЛ: {sulfur_pool + loot_pool:,}\n\n"

        f"НА 1 ЧЕЛОВЕКА (сера): {per_sulfur:,}\n"
        f"НА 1 ЧЕЛОВЕКА (шмот): {per_loot:,}"
        .replace(",", " ")
    )

bot.run(TOKEN)