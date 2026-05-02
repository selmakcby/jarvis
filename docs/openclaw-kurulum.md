# OpenClaw kurulumu — Discord botu olarak Jarvis

OpenClaw, Jarvis'in Discord'dan (veya diğer chat platformlarından) erişilebilir olmasını sağlayan **arka plan daemon**. Telefondan veya kanepedeyken Jarvis'e yazabilmen için gereken tek şey bu.

---

## Önce şunları kabul et

- **OpenClaw 6+ saat çuvallayabilir.** Bu repoyu yazan kişi (Selma) tam olarak bunu yaşadı. Aşağıdaki kurulum onun deneyiminden damıtıldı, en az kaybeden yol.
- **Anthropic API + Claude Code aynı makinedeyse OpenClaw keychain'i çalar.** Bu yüzden **OpenAI API key kullanacağız.** Claude Code'unu çıkarman gerekmez.
- **Ücretsiz olmayacak.** OpenAI gpt-5-mini ile mesaj başına ~$0.005. Aylık $5 kredisi haftalar yeter.

---

## Adım 1 — OpenAI API key al

1. https://platform.openai.com/api-keys → sign up (ChatGPT'den ayrı bir hesap)
2. Settings → Billing → **$5 kredi ekle**
3. API Keys → Create new → kopyala (`sk-proj-...`)

---

## Adım 2 — OpenClaw'ı kur

```bash
npm install -g openclaw
openclaw onboard
```

Onboard wizard'ında:

| Soru | Cevap |
|---|---|
| Setup mode | **QuickStart** |
| Provider | **OpenAI** |
| Model | `gpt-5-mini` (manuel gir) |
| Channel | **Skip for now** (Discord'u sonra ekleyeceğiz) |
| Web search | Skip for now |
| Hooks | Skip for now |

---

## Adım 3 — API key'i OpenClaw'a göster

OpenClaw'ın gateway'i bir LaunchAgent olarak arka planda çalışır. Shell env değişkenlerini görmez. `launchctl setenv` kullan:

```bash
# Anahtarı dosyaya kaydet (chmod 600 ile sadece sen okuyabilirsin)
mkdir -p ~/.openclaw
echo 'OPENAI_API_KEY=sk-proj-PASTE-HERE' > ~/.openclaw/secrets.env
chmod 600 ~/.openclaw/secrets.env

# Shell'e + launchctl'e yükle
set -a; source ~/.openclaw/secrets.env; set +a
launchctl setenv OPENAI_API_KEY "$OPENAI_API_KEY"

# Doğrula (sadece ilk 12 karakter, güvenli)
launchctl getenv OPENAI_API_KEY | cut -c1-12

# Gateway'i yeniden başlat
pkill -9 -f openclaw-gateway || true
sleep 2
openclaw gateway start
```

---

## Adım 4 — Workspace'i Jarvis'e yönlendir

OpenClaw varsayılan olarak `~/.openclaw/workspace` kullanır. Jarvis ile aynı klasörü paylaşmak için:

```bash
openclaw config set agents.defaults.workspace $HOME/Jarvis
```

Şimdi OpenClaw ve Claude Code aynı `~/Jarvis/` klasörünü okur/yazar.

---

## Adım 5 — Discord botu oluştur

1. https://discord.com/developers/applications → **New Application** → "Jarvis"
2. Sol menü → **Bot** → **Reset Token** → kopyala (`MTIz...`)
3. Aynı sayfada → **Privileged Gateway Intents** → ✅ MESSAGE CONTENT INTENT → Save
4. Sol menü → **OAuth2** → **URL Generator**:
   - Scopes: ✅ `bot`
   - Bot Permissions: ✅ Send Messages, Read Message History, View Channels
5. URL'yi kopyala, tarayıcıda aç → kendi Discord sunucuna davet et

---

## Adım 6 — Token'ı OpenClaw'a ekle

```bash
# Tokenı secrets dosyasına ekle
echo 'DISCORD_BOT_TOKEN=PASTE-DISCORD-TOKEN' >> ~/.openclaw/secrets.env

# Shell ve launchctl'e yükle
set -a; source ~/.openclaw/secrets.env; set +a
launchctl setenv DISCORD_BOT_TOKEN "$DISCORD_BOT_TOKEN"

# Discord kanalını OpenClaw'a kaydet
openclaw channels add --channel discord --token "$DISCORD_BOT_TOKEN"

# Gateway'i yeniden başlat
pkill -9 -f openclaw-gateway
sleep 2
openclaw gateway start
sleep 4

# Doğrula
openclaw channels status
```

`Discord default: enabled, configured, running, connected, bot:@jarvis` görmelisin.

---

## Adım 7 — Pairing approval

Botuna Discord'da DM at: `merhaba`

Bot şöyle cevap verecek:
```
OpenClaw: access not configured.
Your Discord user id: 1234567890
Pairing code: ABC123
Ask the bot owner to approve with:
openclaw pairing approve discord ABC123
```

Terminalde:
```bash
openclaw pairing approve discord ABC123
```

**Onaylandıktan sonra** botu tekrar yaz: `merhaba` → bu sefer Jarvis cevap verir.

---

## Test

Discord'dan:
```
Hatırla, yarın saat 15:00'te Maria ile kahvem var.
```

Jarvis cevap verecek + `~/Jarvis/memory/2026-XX-XX.md` veya benzer bir dosyaya yazacak.

Sonra masaya geç:
```bash
cd ~/Jarvis && claude
```

Sor: *"Yarın programımda ne var?"*

Claude Code aynı `memory/` dosyasını okuyup Maria'nın kahvesini söyleyecek. **Tek beyin, iki yüzey.**

---

## Hata ayıklama

| Sorun | Çözüm |
|---|---|
| Bot DM'leri görmüyor | Discord developer portal → Bot → MESSAGE CONTENT INTENT açık mı kontrol et |
| Cevap çok yavaş (10s+) | `launchctl getenv OPENAI_API_KEY` boş dönüyorsa → key launchctl'e yüklenmemiş |
| "harness not registered" | `openclaw config get agents.defaults.agentRuntime` — varsa `unset` et, default Pi runtime kullansın |
| "out of usage" | Anthropic kotanı tüketmişsin, OpenAI'a geç (Adım 1-3 tekrar) |
| Discord bot offline | Gateway çalışıyor mu? `pgrep -fl openclaw-gateway` |

---

## Maliyet kontrolü

```bash
# OpenAI dashboard → Usage → günlük takip
open https://platform.openai.com/usage
```

Her mesaj ~$0.005. 100 mesaj/gün = ~$0.50/gün = ~$15/ay. Üst sınır koymak istersen platform.openai.com → Billing → Usage limits.
