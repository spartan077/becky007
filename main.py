from discord_bot.discord_api import client,key
from keepalive import keep_alive
if '__name__'=='__main__':
  keep_alive()
  client.run(key)
  