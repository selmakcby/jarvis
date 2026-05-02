#!/usr/bin/env bash
# Jarvis hızlı kurulum yardımcısı
# Kullanım: ./kurulum.sh

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🦾 Jarvis kurulum kontrolü${NC}"
echo

# 1. Klasörleri oluştur
echo -e "${YELLOW}[1/4]${NC} Klasör yapısı kuruluyor..."
mkdir -p memory inbox tasks people calendar projects
echo "  ✓ memory/, inbox/, tasks/, people/, calendar/, projects/"
echo

# 2. Bağımlılık kontrolü
echo -e "${YELLOW}[2/4]${NC} Bağımlılıklar kontrol ediliyor..."

check() {
  if command -v "$1" >/dev/null 2>&1; then
    echo -e "  ✓ $1 (${GREEN}var${NC})"
  else
    echo -e "  ✕ $1 (${RED}yok${NC}) — $2"
  fi
}

check git "brew install git"
check claude "claude.com/claude-code adresinden indir (zorunlu)"
check python3 "python.org veya brew install python3 (sesli kontrol için)"
check npm "brew install node (OpenClaw için, opsiyonel)"
check ollama "ollama.com (yerel model için, opsiyonel)"
echo

# 3. USER.md kontrol
echo -e "${YELLOW}[3/4]${NC} Kişiselleştirme kontrolü..."
if grep -q "İsim:$" USER.md 2>/dev/null; then
  echo -e "  ${YELLOW}!${NC} USER.md henüz doldurulmamış — bir editörle aç ve kendin hakkında 4 satır yaz"
else
  echo "  ✓ USER.md doldurulmuş"
fi
echo

# 4. Sıradaki adım
echo -e "${YELLOW}[4/4]${NC} Sıradaki adımlar:"
echo
echo "  1. USER.md'yi düzenle:    ${GREEN}open USER.md${NC}"
echo "  2. Jarvis'i uyandır:      ${GREEN}claude${NC}"
echo "  3. (Opsiyonel) Discord:   ${GREEN}cat docs/openclaw-kurulum.md${NC}"
echo "  4. (Opsiyonel) Sesli:     ${GREEN}cat voice/README.md${NC}"
echo
echo -e "${GREEN}Hazır.${NC} 🦾"
