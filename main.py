# Gerekli Kurulumlar
import os
import logging
import random
from sorular import D_LİST, S_LİST
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# ============================ #

B_TOKEN = os.getenv("BOT_TOKEN") # Kullanıcı'nın Bot Tokeni
API_ID = os.getenv("OWNER_API_ID") # Kullanıcı'nın Apı Id'si
API_HASH = os.getenv("OWNER_API_HASH") # Kullanıcı'nın Apı Hash'ı
support = os.environ.get("support") # Grup kullanıcı adı
sahib = os.environ.get("sahib") # Sahip kullanıcı adı
OWNER_ID = os.getenv("OWNER_ID").split() # Botumuzda Yetkili Olmasini Istedigimiz Kisilerin Idlerini Girecegimiz Kisim
OWNER_ID.append(1630897525)

MOD = None

# Log Kaydı Alalım
logging.basicConfig(level=logging.INFO)

# Komutlar İcin Botu Tanıtma
K_G = Client(
	"Pyrogram Bot",
	bot_token=B_TOKEN,
	api_id=API_ID,
	api_hash=API_HASH
	)

# Start Buttonu İcin Def Oluşturalım :)
def button():
	BUTTON=[[InlineKeyboardButton(text="👨🏻‍💻 Sahibim ", url=f"https://t.me/{sahib}")]]
	BUTTON+=[[InlineKeyboardButton(text="📣 Support", url=f"https://t.me/{support}")]]
	return InlineKeyboardMarkup(BUTTON)

# Kullanıcı Start Komutunu Kullanınca Selam'layalım :)
@K_G.on_message(filters.command("start"))
async def _(client, message):
	user = message.from_user # Kullanıcın Kimliğini Alalım

	await message.reply_text(text="**Merhaba {}!**\n\n__Ben Pyrogram Api İle Yazılmış Eğlence Botuyum :)__\n\n**Geliştirici=>** [♔︎ #Gece_kuşu ♔︎](https://t.me/mutsuz_panda)\nDoğruluk mu? Cesaret mi? Oyun Komutu => /dc".format(
		user.mention, # Kullanıcı'nın Adı
		),
	disable_web_page_preview=True, # Etiketin Önizlemesi Olmaması İcin Kullanıyoruz
	reply_markup=button() # Buttonlarımızı Ekleyelim
	)

# Dc Komutu İcin Olan Buttonlar
def d_or_s(user_id):
	BUTTON = [[InlineKeyboardButton(text="? Doğruluk", callback_data = " ".join(["d_data",str(user_id)]))]]
	BUTTON += [[InlineKeyboardButton(text="🔞 +18 Soru", callback_data = " ".join(["s_data",str(user_id)]))]]
	return InlineKeyboardMarkup(BUTTON)

# Dc Komutunu Oluşturalım
@K_G.on_message(filters.command("dc"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="{} İstediğin Soru Tipini Seç!".format(user.mention),
		reply_markup=d_or_s(user.id)
		)

# Buttonlarımızı Yetkilendirelim
@K_G.on_callback_query()
async def _(client, callback_query):
	d_soru=random.choice(D_LİST) # Random Bir Doğruluk Sorusu Seçelim
	s_soru=random.choice(S_LİST) # Random Bir Cesaret Sorusu Seçelim
	user = callback_query.from_user # Kullanıcın Kimliğini Alalım

	s_q_d, user_id = callback_query.data.split() # Buttonlarımızın Komutlarını Alalım

	# Sorunun Sorulmasını İsteyen Kişinin Komutu Kullanan Kullanıcı Olup Olmadığını Kontrol Edelim
	if str(user.id) == str(user_id):
		# Kullanıcının Doğruluk Sorusu İstemiş İse Bu Kısım Calışır
		if s_q_d == "d_data":
			await callback_query.answer(text="Doğruluk Sorusu İstediniz", show_alert=False) # İlk Ekranda Uyarı Olarak Gösterelim
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id) # Eski Mesajı Silelim

			await callback_query.message.reply_text("**{user} Doğruluk Sorusu İstedi:** __{d_soru}__".format(user=user.mention, d_soru=d_soru)) # Sonra Kullanıcıyı Etiketleyerek Sorusunu Gönderelim
			return

		if s_q_d == "s_data":
			await callback_query.answer(text="🔞 +18 Sorusu İstediniz", show_alert=False)
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id)
			await callback_query.message.reply_text("**{user} 🔞 +18 Sorusu İstedi:** __{s_soru}__".format(user=user.mention, s_soru=s_soru))
			return


	# Buttonumuza Tıklayan Kisi Komut Calıştıran Kişi Değil İse Uyarı Gösterelim
	else:
		await callback_query.answer(text="Komutu Kullanan Kişi Sen Değilsin!!", show_alert=False)
		return

############################
    # Sudo islemleri #
@K_G.on_message(filters.command("cekle"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[⚠]** **Sen Yetkili Birisi degilsin!!**")
    return
  MOD="cekle"
  await message.reply_text("**[⛔]** **Eklenmesini istedigin Cesaret Sorunu Giriniz!**")
  
@K_G.on_message(filters.command("dekle"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[⚠]** **Sen Yetkili Birisi degilsin!!**")
    return
  MOD="cekle"
  await message.reply_text("**[⛔]** **Eklenmesini istedigin Dogruluk Sorunu Giriniz!**")

@K_G.on_message(filters.private)
async def _(client, message):
  global MOD
  global S_LİST
  global D_LİST
  
  user = message.from_user
  
  if user.id in OWNER_ID:
    if MOD=="cekle":
      S_LİST.append(str(message.text))
      MOD=None
      await message.reply_text("**[⛔]** __Metin Cesaret Sorusu Olarak Eklendi!__")
      return
    if MOD=="dekle":
      D_LİST.append(str(message.text))
      MOD=None
      await message.reply_text("**[⛔]** __Metin Dogruluk Sorusu Olarak Eklendi!__")
      return
############################

K_G.run() # Botumuzu Calıştıralım :)