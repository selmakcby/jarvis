# 🦾 Jarvis · v1

> **OpenClaw + Claude Code, ortak hafıza klasörüyle birleşmiş.**
> İki ajan, tek vault, paylaşılan Markdown notları.
> Discord'dan günlük işler, terminalden kod — aynı beyni okuyorlar.

Bu repo, [@selma.builds](https://youtube.com/@selma.builds) YouTube videosunda kurduğum **Jarvis v1**'in tüm dosyalarını içerir. Tony Stark Jarvis'i değil — kendi yaptığım, klasör adı **Jarvis** olan, çalışan, sade bir başlangıç. v2'de sesli kontrol, Telegram, otomatik routing gelecek.

```
   OpenClaw (Discord bot)  ─────►  ~/Jarvis/  ◄─────  Claude Code (Terminal)
                                    Markdown
                                  paylaşımlı vault
```

**Mesajlaşma protokolü = dosya sistemi.** OpenClaw `memory/`'ye yazar, Claude Code okur. Tek API: `cat memory/*.md`.

---

## 🎬 Video

YouTube: [@selma.builds](https://youtube.com/@selma.builds) · [video link buraya gelecek]

---

## ⚡ Ne yapıyor?

| Bileşen | Görev | Nerede çalışır |
|---|---|---|
| **OpenClaw** | Discord botu olarak arka planda çalışır, mesaj alır, notu hafızaya yazar | LaunchAgent (7/24) |
| **Claude Code** | Terminalden aynı klasörü okur, Jarvis kişiliğine bürünür | Sen `claude` deyince |
| **`~/Jarvis/`** | Hepsinin paylaştığı tek hafıza | Markdown dosyaları |
| **Obsidian** (opsiyonel) | Vault'u görsel grafik olarak gez | UI katmanı |

---

## 🚀 Hızlı kurulum (3 dakika)

### 1. Repoyu klonla

```bash
git clone https://github.com/selmakcby/jarvis.git ~/Jarvis
cd ~/Jarvis
```

### 2. Kişiliği özelleştir

`USER.md` dosyasını aç, kendin hakkında 4 satır yaz. İstersen `CLAUDE.md`, `IDENTITY.md` ve `SOUL.md`'yi de düzenle.

### 3. Claude Code ile uyandır

```bash
cd ~/Jarvis && claude
```

İlk soru: *"Merhaba, sen kimsin?"* — Claude Code, `CLAUDE.md` ve `USER.md`'yi okuyup cevap verir.

**Bu kadar.** Tek başına Claude Code tarafı çalışıyor — kişilikli, dosya farkında, hafıza yazabilen.

---

## 📞 OpenClaw + Discord ekleme

Telefondan/her yerden erişim için OpenClaw kur. **OpenAI API key gerekir** (~$5 aylar yeter).

> ⚠️ **Önemli:** Aynı makinede Claude Code varken **Anthropic API kullanma** — OpenClaw keychain'den Claude Pro kimliğini sessizce ele geçirir, kotanı tüketir. **OpenAI önerilir.**

```bash
# 1. OpenClaw kur
npm install -g openclaw
openclaw onboard
# → "QuickStart" seç, sağlayıcı: OpenAI, model: gpt-5-mini

# 2. OpenAI API key'i .env'e koy
mkdir -p ~/.openclaw
echo 'OPENAI_API_KEY=sk-proj-PASTE-HERE' > ~/.openclaw/secrets.env
chmod 600 ~/.openclaw/secrets.env

# 3. Key'i launchctl'e yükle (gateway daemon shell env görmez)
set -a; source ~/.openclaw/secrets.env; set +a
launchctl setenv OPENAI_API_KEY "$OPENAI_API_KEY"

# 4. Workspace'i Jarvis klasörüne yönlendir (her iki ajan aynı yeri kullansın)
openclaw config set agents.defaults.workspace $HOME/Jarvis

# 5. Discord botu oluştur, davet et, token'ı ekle
# (https://discord.com/developers/applications → New Application → Bot → Token)
echo 'DISCORD_BOT_TOKEN=PASTE-HERE' >> ~/.openclaw/secrets.env
set -a; source ~/.openclaw/secrets.env; set +a
launchctl setenv DISCORD_BOT_TOKEN "$DISCORD_BOT_TOKEN"
openclaw channels add --channel discord --token "$DISCORD_BOT_TOKEN"

# 6. Gateway'i yeniden başlat
pkill -9 -f openclaw-gateway && sleep 2 && openclaw gateway start
```

**Tam adım adım kılavuz:** [`docs/openclaw-kurulum.md`](docs/openclaw-kurulum.md)

---

## 🌐 Obsidian + Wiki Linkler (videoda gösterilen)

Vault'u Obsidian'da açtığında dosyalar arası grafik bağlantı görmek istiyorsan, Claude Code'a şu prompt'u ver:

```
Senin workspace olan ~/Jarvis klasörünün içindeki tüm Markdown dosyalarına
Obsidian-uyumlu [[wiki linkleri]] ekle. Her dosyanın içerisinde, ilgili olduğu
diğer dosyalara referans ver. Örneğin CLAUDE.md içerisinde IDENTITY,
USER, SOUL'a referans olsun. Dosyaların içeriğini değiştirme — sadece bağlantı ekle.
Sonra Obsidian Graph view'da yapıyı göster.
```

Tam prompt: [`docs/llm-wiki-prompt.md`](docs/llm-wiki-prompt.md)

Sonuç: Obsidian Graph view'da CLAUDE ↔ IDENTITY ↔ USER ↔ SOUL bağlı düğümler olarak görünüyor.

---

## 📁 Klasör yapısı

```
~/Jarvis/
├── CLAUDE.md            # Jarvis kişiliği (Claude Code okur)
├── IDENTITY.md          # Kim olduğu (OpenClaw okur)
├── USER.md              # Sen kimsin
├── SOUL.md              # Değerler + sınırlar
├── AGENTS.md, TOOLS.md  # Workspace dokümantasyonu
├── HEARTBEAT.md         # Periyodik görevler
├── memory/              # Günlük notlar (her iki ajan yazar/okur)
├── inbox/               # Gelen kutusu
├── tasks/               # Aktif görevler
├── people/              # Kişiler
├── calendar/            # Takvim notları
└── projects/            # Proje notları
```

---

## 🤖 Hangi modeli kullanmalı? (videodan dersler)

Videoda bizzat denedim, bunlar yaşandı:

| Model | Sonuç |
|---|---|
| **Yerel (Ollama, qwen2.5:7b)** | ✕ 16 GB RAM'de çok yavaş, prefill 30+ saniye |
| **Grok (xAI)** | ✕ Rate/auth limit problemi |
| **Anthropic (claude-haiku)** | ✕ Keychain hijack — Claude Pro kotamı çaldı |
| **OpenAI (gpt-5-mini)** | ✓ Çalıştı — ~$0.005/mesaj, hızlı |

**Öneri:** OpenClaw için **OpenAI gpt-5-mini**. Aylık ~$5-10, kişisel kullanım için bol. Detaylı karşılaştırma: `diagram/models.html` ve `diagram/local-models.html`.

---

## ⚠️ Bilmen gerekenler (canını yakmadan önce oku)

1. **OpenClaw "workspace" gerçek bir sandbox değil.** Sadece bellek operasyonlarını sınırlandırır. `coding` profili Bash erişimi verir → ajan istediği yeri okuyabilir.

2. **Aynı makinede Claude Code varken OpenClaw'a Anthropic API koyma.** Keychain'i ele geçirir → OpenAI veya başka sağlayıcı kullan.

3. **16 GB RAM yerel model için yetersiz.** OpenClaw'un 4K token system prompt'u küçük modelleri prefill'de kasıyor.

4. **Discord botuna kim mesaj atabilirse Jarvis'i kullanabilir.** Pairing approval kullan, sunucunda sadece güvendiğin kişileri tut.

---

## 🛣️ Jarvis v2 için yol haritası

- [ ] Telegram / WhatsApp entegrasyonu (telefondan)
- [ ] "Hey Jarvis" sesli kontrol (OpenWakeWord + Whisper)
- [ ] Otomatik routing — hangi ajana gitsin?
- [ ] iCloud Sync ile telefon-Mac uyumu
- [ ] Mobil iOS shortcut

---

## 🎨 Diyagramlar

Repoda `diagram/` klasöründe video B-roll için kullanılan terminal estetiğinde HTML görseller:

- `architecture.html` — sistem mimarisi şeması
- `models.html` — denenen modeller listesi (~6 saatlik savaş)
- `local-models.html` — yerel modeller RAM rehberi

Tarayıcıda aç, screenshot al.

---

## 📜 Lisans

MIT — kullan, fork'la, satabilirsin. Atıf hoş ama zorunlu değil.

---

## 🦾 Yapan

**Selma** — AI Engineer
[@selma.builds](https://youtube.com/@selma.builds) · [@selmaaii](https://x.com/selmaaii) · selma@selmaai.dev

OpenClaw ile **6 saat kavga ettim**, sonunda bu sade kuruluma ulaştım. Senin de aynı acıyı çekme diye yazdım.

---

## 🙏 Teşekkürler

- [OpenClaw](https://openclaw.ai) — Discord ajanı için
- [Anthropic Claude Code](https://claude.com/claude-code) — terminal ajanı için
- [Obsidian](https://obsidian.md) — vault görselleştirme için
- [OpenAI](https://openai.com) — gpt-5-mini için
