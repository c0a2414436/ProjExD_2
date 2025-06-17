import os
import random
import sys
import time 
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向，縦方向の画面内外判定結果
    画面内ならTrue,画面外ならFalse
    """
    yoko,tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


import time  # ← ファイル冒頭に追加すること

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に,半透明の黒い画面上に「Game Over」と表示し,泣いているこうかとん画像を貼り付ける関数
    """
    blackout = pg.Surface((WIDTH, HEIGHT))
    blackout.set_alpha(180)  # 半透明
    blackout.fill((0, 0, 0))
    screen.blit(blackout, (0, 0))  # screen に貼り付け

    sad_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    sad_kk_rect_left = sad_kk_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
    sad_kk_rect_right = sad_kk_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))
    screen.blit(sad_kk_img, sad_kk_rect_left)   # 左側
    screen.blit(sad_kk_img, sad_kk_rect_right)  # 右側

    # Game Over
    font = pg.font.SysFont(None, 80)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]  # 加速度リスト

    for r in range(1, 11):  # r=1〜10
        size = 20 * r
        img = pg.Surface((size, size))
        pg.draw.circle(img, (255, 0, 0), (size // 2, size // 2), size // 2)
        img.set_colorkey((0, 0, 0))  # 透明に
        bb_imgs.append(img)

    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  
    bb_rct.centery = random.randint(0, HEIGHT) 
    vx, vy = +5, +5  
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # 衝突判定
            gameover(screen)
            return
        
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) 
        screen.blit(kk_img, kk_rct)

        # tmrに応じて爆弾のサイズ・加速度を変更
        level = (min(tmr // 500, 9))  
        bb_img = bb_imgs[level]
        avx = vx * bb_accs[level]
        avy = vy * bb_accs[level]
        center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = center
        bb_rct.move_ip(avx, avy)  # 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)  

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
