#!/bin/bash
# ULTRA FAST Matrix Effect - Optimized

matrix_ultra_fast() {
    local duration=${1:-30}
    
    trap 'tput cnorm; tput sgr0; clear; return' INT TERM EXIT
    
    tput civis
    tput setab 0
    clear
    
    local term_lines=$(tput lines)
    local term_cols=$(tput cols)
    
    timeout $duration bash << 'MATRIX'
while :; do 
    echo $LINES $COLUMNS $(( RANDOM % COLUMNS )) $(( RANDOM % 150 ))
    sleep 0.03
done | awk '{ 
    letters="ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()"; 
    c=$4; 
    letter=substr(letters,c,1);
    a[$3]=0;
    for (x in a) {
        o=a[x];
        a[x]=a[x]+1; 
        printf "\033[%s;%sH\033[2;32m%s",o,x,letter; 
        printf "\033[%s;%sH\033[1;37m%s\033[0;0H",a[x],x,letter;
        if (a[x] >= $1) { 
            a[x]=0; 
        } 
    }
}'
MATRIX
    
    tput cnorm
    tput sgr0
    clear
}

# Ultra smooth progress bar
ultra_progress() {
    local current=$1
    local total=$2
    local message=$3
    local width=60
    local percent=$((current * 100 / total))
    local filled=$((current * width / total))
    
    # Smooth gradient
    local colors=(196 202 208 214 220 226 190 154 118 82 46)
    
    printf "\r\033[38;5;51m▶\033[0m "
    
    for ((i=0; i<filled; i++)); do
        local ci=$((i * 11 / width))
        printf "\033[38;5;${colors[$ci]}m█\033[0m"
    done
    
    printf "\033[2m"
    printf "%$((width - filled))s" "" | tr ' ' '░'
    printf "\033[0m \033[1m%3d%%\033[0m \033[38;5;226m%s\033[0m" "$percent" "$message"
    
    if [ $current -eq $total ]; then
        echo -e " \033[38;5;46m✓\033[0m"
    fi
}

# Fast spinner
fast_spinner() {
    local message="$1"
    local chars='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    
    for i in {1..20}; do
        local c=${chars:$((i%10)):1}
        printf "\r\033[38;5;51m%s\033[0m \033[38;5;226m%s\033[0m" "$c" "$message"
        sleep 0.05
    done
    echo -e "\r\033[38;5;46m✓\033[0m $message"
}

echo "✨ Ultra-fast animations loaded!"
