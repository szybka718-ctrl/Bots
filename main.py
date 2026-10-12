import discord
from discord.ext import commands
from discord.ui import Select, View

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

STYLES = {
    "minimal": {
        "name": "Minimalny",
        "channels": {
            "Główna": ["regulamin", "ogłoszenia", "chat"],
            "Firma": ["produkty", "wsparcie", "opinie"],
        },
    },
    "gaming": {
        "name": "Gamingowy",
        "channels": {
            "📌 INFORMACJE": ["📜│regulamin", "📢│ogłoszenia", "🎁│giveaways"],
            "💬 SPOŁECZNOŚĆ": ["💬│chat-ogólny", "🎮│setupy-klientów", "💡│pomysły"],
            "🛒 SKLEP": ["🛍│sklep", "🔧│wsparcie-techniczne", "⭐│opinie"],
        },
    },
}


class StyleSelect(Select):

  def __init__(self):
    options = [
        discord.SelectOption(
            label=data["name"],
            value=key,
            description=f"Styl {data['name']} dla serwera myszek",
        )
        for key, data in STYLES.items()
    ]
    super().__init__(
        placeholder="Wybierz styl kanałów...",
        min_values=1,
        max_values=1,
        options=options,
    )

  async def callback(self, interaction: discord.Interaction):
    guild = interaction.guild
    style = STYLES[self.values[0]]

    await interaction.response.send_message(
        f"Tworzę serwer w stylu **{style['name']}**...", ephemeral=True
    )

    for channel in guild.channels:
      if channel.name not in ["regulamin", "rules"]:
        try:
          await channel.delete()
        except:
          pass

    for category_name, channels in style["channels"].items():
      category = await guild.create_category(category_name)
      for ch_name in channels:
        await guild.create_text_channel(ch_name, category=category)


class StyleView(View):

  def __init__(self):
    super().__init__()
    self.add_item(StyleSelect())


@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
  view = StyleView()
  await ctx.send(
      "Wybierz styl kanałów dla serwera firmy z myszkami:", view=view
  )


bot.run("TWÓJ_TOKEN_BOTA")
