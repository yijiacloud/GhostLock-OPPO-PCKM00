.section .rodata
.balign 16

.global embedded_wallpaper_start
.type embedded_wallpaper_start, %object
embedded_wallpaper_start:
.incbin "assets/wallpaper.webp"

.global embedded_wallpaper_end
.type embedded_wallpaper_end, %object
embedded_wallpaper_end:
.byte 0
