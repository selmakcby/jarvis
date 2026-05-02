# Sıkça Sorulan Sorular

## Bu OpenClaw'a alternatif mi?

Hayır, bu **OpenClaw + Claude Code'u birlikte kullanma şekli**. İkisi de yapısal olarak farklı:

- **Claude Code** = terminal başına oturum açan ajan (sen başlatınca çalışır)
- **OpenClaw** = arka planda her zaman açık daemon, chat platformlarına bağlı

İkisi aynı `~/Jarvis/` klasörünü paylaşırsa Discord'dan yazdığını masada Claude Code biliyor.

---

## Neden Claude Code yerine OpenClaw?

OpenClaw değil — **ek olarak**. Kod işleri için Claude Code çok daha iyi (TDD, plan mode, subagent'lar). OpenClaw hayat işleri için (Discord'dan/telefondan ajana erişim).

Eğer terminalde yaşıyorsan ve telefondan AI'a erişme ihtiyacın yoksa: sadece Claude Code yeter, OpenClaw'a ihtiyaç yok.

---

## OpenClaw güvenli mi?

**Tamamen değil.** Bilmen gerekenler:

1. `coding` tools profili → ajanın **Bash erişimi var**. İstersen senin tüm dosyaları okuyabilir.
2. Workspace ayarı **gerçek bir sandbox değil** — sadece bellek operasyonlarını kapsar.
3. Discord'da botla pairing onayı yapmadığın kişi mesaj atamaz (✓ iyi koruma).

**Daha sıkı izolasyon istersen:** tools profilini `coding` yerine daha kısıtlı bir şeyle değiştir veya OpenClaw'ı Docker container'da çalıştır.

---

## Yerel modelle çalışmaz mı?

Çalışır ama **acı verir**. 16 GB RAM'de qwen 7B bile OpenClaw'un 4K token system prompt'unu prefill etmek için 30+ saniye harcıyor. Üstüne tool-call halüsinasyonları ekle.

Yerel modelle gerçek zamanlı kullanışlı bir asistan istiyorsan:
- 32 GB+ RAM gerekir
- 14B-32B model (qwen2.5:14b, qwen2.5:32b)
- M3 Max veya GPU sunucusu en iyisi

Sadece bir test/demo için 7B yeter.

---

## Maliyeti ne?

OpenAI gpt-5-mini ile:
- Mesaj başına ~$0.005
- 50 mesaj/gün = ~$0.25/gün = ~$7-8/ay

Sesli kullanım ekleyince:
- Whisper STT ~$0.006/dk
- gpt-4o-mini cevap ~$0.0001
- macOS `say` ücretsiz
- Toplam ~$0.005-0.01 per voice interaction

**Aylık $10-15 ile kişisel kullanım için bol fazla.**

---

## Türkçe çalışıyor mu?

Evet. Hem yazı hem ses (Whisper Türkçeyi tanır, gpt-5-mini Türkçe iyi konuşur). macOS `say` Türkçe sesi için "Yelda" sesini deneyebilirsin:

```bash
say -v Yelda "Merhaba, ben Jarvis."
```

`voice/jarvis_voice.py` içinde `Daniel` yerine `Yelda` yazarsan Türkçe konuşur. Ama "Hey Jarvis" wake word **İngilizce** — OpenWakeWord'ün eğitilmiş modeli sadece İngilizce çalışıyor.

---

## Telefondan erişim için Discord'dan başka seçenek?

OpenClaw destekliyor:
- Telegram (telefon numarası gerekir)
- WhatsApp (telefon numarası + macOS app)
- Slack (workspace gerekir)
- iMessage (Mac-only, kişisel Apple ID)

Discord en kolayı: telefon numarası gerektirmez, sadece e-posta.

---

## Obsidian ile uyumlu mu?

Evet. `~/Jarvis/` klasörünü Obsidian vault olarak aç. Jarvis ekibinin yazdığı Markdown dosyalarını grafiksel olarak gezebilirsin. Wiki linkleri (`[[CLAUDE]]`, `[[SOUL]]` gibi) Obsidian'da renkli görünür.
