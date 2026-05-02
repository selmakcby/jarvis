# LLM Wiki Prompt — Obsidian uyumlu wiki linkleri ekle

Videoda Claude Code'a verdiğim prompt. Vault'undaki Markdown dosyaları arasında `[[wiki link]]` bağlantıları kurar. Sonuç: Obsidian Graph view'da bağlı düğümlerle güzel bir görsel.

## Kullanım

1. Vault'unda Claude Code başlat:
   ```bash
   cd ~/Jarvis && claude
   ```
2. Aşağıdaki prompt'u kopyala, Claude'a yapıştır.
3. Claude tüm dosyaları okur, anlamlı bağlantılar ekler.
4. Obsidian'da vault'u aç → sol alt **Graph view** → güzel görsel.

---

## Prompt

```
Bu workspace ~/Jarvis bir Obsidian vault'u olacak. İçindeki tüm Markdown
dosyalarına Obsidian-uyumlu [[wiki linkleri]] ekle.

Kurallar:

1. Her dosyada, ilgili olduğu diğer dosyalara [[Dosya]] formatında referans ver.
   Örneğin:
   - CLAUDE.md → [[IDENTITY]], [[USER]], [[SOUL]], [[AGENTS]], [[TOOLS]]'a referans
   - IDENTITY.md → [[USER]], [[SOUL]], [[CLAUDE]]'a
   - USER.md → [[IDENTITY|Jarvis]], [[memory/2026-04-30]] gibi günlük notlara
   - SOUL.md → [[IDENTITY|Jarvis]], [[USER]], [[CLAUDE]]'a

2. Dosyaların içeriğini değiştirme — sadece doğal yerlerde [[link]] formatında bağlantı ekle.
   Mesela "Selma'nın hayat asistanı" yerine "[[USER|Selma]]'nın hayat asistanı".

3. Görüntüleme adı farklıysa pipe kullan: [[USER|Selma]] → görsel olarak "Selma" gösterir
   ama USER.md dosyasına bağlanır.

4. memory/, inbox/, tasks/ klasörlerindeki dosyalara da referans verirken
   tam yolu kullan: [[memory/2026-05-01]], [[tasks/active]], [[people/README]]

5. Hiç değiştirilmemesi gereken dosyalar: HEARTBEAT.md (sadece yorum içeriyor)

Tamamla, sonra hangi dosyalara hangi linkleri eklediğini özet olarak söyle.
```

---

## Sonuç

Obsidian Graph view'da yapı şöyle görünür:

```
            CLAUDE ─── IDENTITY
              │           │
              │           │
            SOUL ─────  USER
              │           │
            TOOLS    memory/2026-05-01
                          │
                       tasks/active
```

Bağlı düğümler — vault'u gezmek ve dosyalar arası context kurmak çok kolay.

## Bonus

Prompt'u biraz değiştirip "Obsidian dataview-friendly frontmatter ekle" diyebilirsin → her dosyaya `tags`, `created`, `category` gibi metadata ekleyip Obsidian'da daha güçlü query'ler kurabilirsin. Bir sonraki video için sakla.
