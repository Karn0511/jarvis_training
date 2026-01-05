#!/bin/bash
# ============================================================
# JARVIS - Ultra Modern Animated Loading System
# ============================================================

# Enhanced color palette
NEON_GREEN='\033[38;5;46m'
NEON_BLUE='\033[38;5;51m'
NEON_PINK='\033[38;5;201m'
NEON_YELLOW='\033[38;5;226m'
NEON_PURPLE='\033[38;5;129m'
NEON_CYAN='\033[38;5;87m'
GRAD1='\033[38;5;27m'
GRAD2='\033[38;5;33m'
GRAD3='\033[38;5;39m'
GRAD4='\033[38;5;45m'
GRAD5='\033[38;5;51m'

# Modern spinner with emojis
modern_spinner() {
    local pid=$1
    local message=$2
    local spinners=('⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏')
    local emojis=('🔄' '⚡' '🚀' '💫' '✨' '🔮' '⭐' '🌟' '💥' '🔥')
    local i=0
    
    while kill -0 $pid 2>/dev/null; do
        local spinner="${spinners[$((i % 10))]}"
        local emoji="${emojis[$((i % 10))]}"
        printf "\r${NEON_CYAN}${spinner}${NC} ${emoji} ${NEON_YELLOW}${message}${NC} "
        sleep 0.1
        i=$((i + 1))
    done
    printf "\r${NEON_GREEN}✓${NC} ${emoji} ${message} ${NEON_GREEN}Complete!${NC}\n"
}

# Rainbow progress bar
rainbow_progress() {
    local current=$1
    local total=$2
    local message=$3
    local width=50
    local percent=$((current * 100 / total))
    local filled=$((current * width / total))
    
    # Rainbow gradient colors
    local colors=('\033[38;5;196m' '\033[38;5;202m' '\033[38;5;226m' '\033[38;5;46m' '\033[38;5;51m' '\033[38;5;93m')
    local color_index=$((filled * 6 / width))
    local color="${colors[$color_index]}"
    
    printf "\r${NEON_CYAN}▶${NC} ${color}["
    
    # Gradient fill
    for ((i=0; i<filled; i++)); do
        local ci=$((i * 6 / width))
        echo -n -e "${colors[$ci]}█${NC}"
    done
    
    printf "${DIM}"
    printf "%$((width - filled))s" "" | tr ' ' '░'
    printf "${NC}${color}]${NC} ${BOLD}%3d%%${NC} ${NEON_YELLOW}%s${NC}" "$percent" "$message"
    
    if [ $current -eq $total ]; then
        echo -e " ${NEON_GREEN}✓${NC}"
    fi
}

# Glowing text effect
glow_text() {
    local text="$1"
    echo -e "${NEON_CYAN}${BOLD}╔$(printf '═%.0s' $(seq 1 ${#text}))═╗${NC}"
    echo -e "${NEON_CYAN}${BOLD}║${NC} ${NEON_PINK}${BLINK}${text}${NC} ${NEON_CYAN}${BOLD}║${NC}"
    echo -e "${NEON_CYAN}${BOLD}╚$(printf '═%.0s' $(seq 1 ${#text}))═╝${NC}"
}

# Pulsing dots loader
pulse_loader() {
    local message="$1"
    local duration=${2:-5}
    
    for ((i=0; i<duration*4; i++)); do
        local dots=$((i % 4))
        printf "\r${NEON_PURPLE}⟳${NC} ${NEON_YELLOW}${message}${NC}$(printf '.%.0s' $(seq 1 $dots))   "
        sleep 0.25
    done
    echo -e "\r${NEON_GREEN}✓${NC} ${message} ${NEON_GREEN}Done!${NC}     "
}

# DNA/Helix loader with emojis
dna_loader() {
    local message="$1"
    echo -e "${NEON_BLUE}${message}${NC}"
    
    for i in {1..10}; do
        local pos=$((i % 8))
        printf "  "
        printf "%${pos}s" ""
        echo -e "${NEON_GREEN}🧬${NEON_CYAN}━━━${NEON_BLUE}🧬${NC}"
        sleep 0.1
    done
    echo -e "${NEON_GREEN}  ✓ Analysis complete${NC}\n"
}

# Matrix-style data stream
matrix_stream() {
    local lines=5
    echo -e "${NEON_GREEN}Scanning neural pathways...${NC}"
    
    for i in {1..10}; do
        for line in $(seq 1 $lines); do
            echo -n "${NEON_GREEN}"
            for col in {1..60}; do
                echo -n $((RANDOM % 2))
            done
            echo -e "${NC}"
        done
        sleep 0.05
        tput cuu $lines
    done
    tput cud $lines
    echo -e "${NEON_GREEN}✓ Neural scan complete${NC}\n"
}

# Cyber box with gradient
cyber_box() {
    local title="$1"
    local content="$2"
    
    echo -e "${GRAD1}╔═══════════════════════════════════════════════╗${NC}"
    echo -e "${GRAD2}║${NC} ${NEON_PINK}${BOLD}${title}${NC}$(printf ' %.0s' $(seq 1 $((43 - ${#title}))))${GRAD2}║${NC}"
    echo -e "${GRAD3}╠═══════════════════════════════════════════════╣${NC}"
    echo -e "${GRAD4}║${NC} ${NEON_YELLOW}${content}${NC}$(printf ' %.0s' $(seq 1 $((43 - ${#content}))))${GRAD4}║${NC}"
    echo -e "${GRAD5}╚═══════════════════════════════════════════════╝${NC}"
}

# Emoji status with animation
emoji_status() {
    local status="$1"
    local message="$2"
    
    case $status in
        "loading")
            echo -e "${NEON_BLUE}⏳${NC} ${message}"
            ;;
        "success")
            echo -e "${NEON_GREEN}✅${NC} ${message}"
            ;;
        "error")
            echo -e "${NEON_PINK}❌${NC} ${message}"
            ;;
        "warning")
            echo -e "${NEON_YELLOW}⚠️${NC} ${message}"
            ;;
        "rocket")
            echo -e "${NEON_CYAN}🚀${NC} ${message}"
            ;;
        "sparkle")
            echo -e "${NEON_YELLOW}✨${NC} ${message}"
            ;;
        "fire")
            echo -e "${NEON_PINK}🔥${NC} ${message}"
            ;;
    esac
}

# Wave animation
wave_animation() {
    local message="$1"
    echo -e "${NEON_CYAN}${message}${NC}"
    
    for i in {1..20}; do
        printf "  "
        for j in {1..40}; do
            local wave=$(echo "scale=2; s((($i+$j)/3))*2" | bc -l 2>/dev/null || echo "0")
            if (( $(echo "$wave > 0" | bc -l 2>/dev/null || echo "0") )); then
                echo -n "${NEON_BLUE}~${NC}"
            else
                echo -n "${NEON_CYAN}~${NC}"
            fi
        done
        echo ""
        sleep 0.05
        tput cuu 1
    done
    tput cud 1
    echo -e "${NEON_GREEN}  ✓ Wave complete${NC}\n"
}

echo "Modern animations library loaded! ✨"
