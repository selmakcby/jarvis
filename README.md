# 🦾 Jarvis

> **İki AI ajanı, tek klasör, ortak hafıza.**
> Telefondan Discord ile konuş, masada Claude Code ile devam et.
> "Hey Jarvis" deyip sesli komut ver.

Kişisel AI asistanın için ihtiyacın olan tek şey **bir klasör + iki CLI**. Karmaşık orchestrator yok, propriyetary protokol yok, bulut yok. Sadece Markdown dosyaları.

```
   OpenClaw (Discord)  ─────►  ~/Jarvis/  ◄─────  Claude Code (Terminal)
                                    ▲
                                    │
                              Voice (mic)
```

---

## 🎬 Video

YouTube: [@selma.builds](https://youtube.com/@selma.builds)

---

## ⚡ Ne yapıyor?

| Bileşen | Görevi |
|---|---|
| **OpenClaw** | Discord botu olarak arka planda çalışır, telefondan/her yerden mesaj alır |
| **Claude Code** | Terminalden aynı klasörü okur, Jarvis kişiliğine bürünür |
| **Voice daemon** | "Hey Jarvis" wake word + Whisper STT + macOS `say` ile sesli yanıt |
| **`~/Jarvis/`** | Hepsinin paylaştığı tek hafıza — Markdown dosyaları |

**Mesajlaşma protokolü = dosya sistemi.** OpenClaw `memory/`'ye yazar, Claude Code okur. `cat memory/*.md` API'nin ta kendisi.

---

## 🚀 Hızlı kurulum (3 dakika)

### 1. Repoyu klonla

```bash
git clone https://github.com/<kullanici>/jarvis.git ~/Jarvis
cd ~/Jarvis
```

### 2. Kişiliği özelleştir

`USER.md` dosyasını aç, kendin hakkında 4 satır yaz. İstersen `CLAUDE.md` ve `SOUL.md`'yi de kendi tarzına göre düzenle.

### 3. Claude Code ile uyandır

```bash
cd ~/Jarvis && claude
```

İlk soru: *"Merhaba, sen kimsin?"* — Jarvis cevap verir.

**Bitti.** Bu kadar. Tek başına Claude Code Jarvis tarafı çalışıyor.

---

## 📞 Discord botunu ekle (opsiyonel ama eğlenceli)

Discord botu sayesinde telefondan/her yerden Jarvis'e yazabilirsin. OpenAI API key gerekir (~$5 aylar yeter).

```bash
# 1. OpenClaw kur
npm install -g openclaw
openclaw onboard
# → "QuickStart" seç, sağlayıcı: OpenAI, model: gpt-5-mini

# 2. Discord bot tokeni ekle
# https://discord.com/developers/applications → New Application → Bot → Token

# 3. Workspace'i Jarvis'e yönlendir
openclaw config set agents.defaults.workspace $HOME/Jarvis

# 4. Discord kanalını ekle
openclaw channels add --channel discord --token "<DISCORD_BOT_TOKEN>"

# 5. Botu kendi sunucuna davet et, kendine DM at
# Bot ilk mesajda "pairing code" verir, terminalde onayla:
openclaw pairing approve discord <PAIRING_CODE>
```

Detaylı kılavuz: `docs/openclaw-kurulum.md`

---

## 🎤 Sesli kontrol (opsiyonel)

"Hey Jarvis" deyince mikrofondan dinleyip cevap veren Python daemon.

```bash
# 1. Bağımlılıklar
pip install openwakeword sounddevice openai numpy onnxruntime

# 2. OpenAI key'ini .env'e ekle
echo 'OPENAI_API_KEY=sk-proj-...' > ~/Jarvis/voice/.env

# 3. Çalıştır
~/Jarvis/voice/run.sh
```

İlk çalıştırmada macOS mikrofon izni isteyecek → İzin Ver. Sonra **"Hey Jarvis, bugün ne var?"** de.

---

## 📁 Klasör yapısı

```
~/Jarvis/
├── CLAUDE.md            # Jarvis kişiliği (Claude Code okur)
├── IDENTITY.md          # Jarvis kim (OpenClaw okur)
├── USER.md              # Sen kimsin
├── SOUL.md              # Değerler + sınırlar
├── AGENTS.md, TOOLS.md  # Workspace dokümantasyonu
├── memory/              # Günlük notlar (her iki ajan yazar/okur)
├── inbox/               # Gelen kutusu
├── tasks/               # Aktif görevler
├── people/              # Kişiler
├── calendar/            # Takvim notları
├── projects/            # Proje notları
├── voice/               # Sesli daemon (jarvis_voice.py)
└── diagram/             # Mimari şemaları (HTML, screenshot için)
```

---

## 🤖 Hangi modeli kullanmalı?

**Yerel modeller (16 GB MacBook'ta):**
- `qwen2.5:7b-instruct` → tatlı nokta, en iyi tool-caller
- `llama3.1:8b` → genel sohbet için
- `gemma2:9b` → Türkçe nispeten güçlü
- 14B → sıkışık, sadece tek başına çalışırken
- 32B+ → unutmak en iyisi

**Bulut modelleri:**
- `gpt-5-mini` (OpenAI) → ✅ önerilen, ~$0.005/mesaj, hızlı
- `claude-haiku-4-5` (Anthropic) → ⚠️ keychain hijack riski
- `groq/*` → ücretsiz tier rate limit dar (1 req/dk)

Detaylı karşılaştırma: `diagram/local-models.html` ve `diagram/models.html`

---

## ⚠️ Önemli notlar (canını yakmadan önce oku)

1. **OpenClaw "workspace" gerçek bir sandbox değil.** Sadece bellek operasyonlarını sınırlandırır. `coding` profili Bash erişimi verir → ajan istediği yeri okuyabilir. Gerçek izolasyon için tools profilini değiştir.

2. **Aynı makinede Claude Code varken OpenClaw'a Anthropic API koyma.** Keychain'den Claude Pro kimliğini sessizce alır → Pro kotanı tüketir. **OpenAI veya başka sağlayıcı kullan.**

3. **16 GB RAM'de yerel model çalıştıracaksan 7-9B sınıfı yeterli.** OpenClaw 4K token system prompt yolluyor, daha küçük modeller bile prefill'de yavaşlıyor.

4. **Discord botuna kim mesaj atabilirse Jarvis'i kullanabilir.** Pairing approval kullan, sunucunda sadece güvendiğin kişileri tut.

---

## 🛣️ Yol haritası

- [x] OpenClaw + Claude Code ortak klasör
- [x] Discord bot
- [x] "Hey Jarvis" sesli kontrol
- [ ] Telegram/WhatsApp opsiyonu
- [ ] Otomatik routing (hangi ajana gitsin?)
- [ ] iOS Shortcut ile sesli komut
- [ ] Obsidian sync ile telefon-Mac iCloud paylaşım

---

## 📜 Lisans

MIT — kullan, fork'la, satabilirsin. Atıf hoş ama zorunlu değil.

---

## 🦾 Yapan

**Selma** — AI Engineer
[@selma.builds](https://youtube.com/@selma.builds) · [@selmaaii](https://x.com/selmaaii)

OpenClaw ile **6 saat kavga ettim**, sonunda bu kuruluma ulaştım. Senin de aynı acıyı çekme diye yazdım.

---

## 🙏 Teşekkürler

- [OpenClaw](https://openclaw.ai) — Discord ajanı için
- [Anthropic Claude Code](https://claude.com/claude-code) — terminal ajanı için
- [OpenWakeWord](https://github.com/dscripka/openWakeWord) — açık kaynak wake word için
- [OpenAI](https://openai.com) — Whisper + gpt-5-mini için
