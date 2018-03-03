# -*- coding: utf-8 -*-
import pygame,math
from pygame.locals import *
import sys

SCR_RECT = Rect(0,0,800,600) # スクリーンサイズ（px指定）

#キャラクターのスプライト（クラス）を作る
class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = Rect(x, y, width, height)
        self.vx = vx
        self.vy = vy

    def update(self):
        #画面からはみ出さないようにする
        self.rect = self.rect.clamp(SCR_RECT)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

#プレイヤーのスプライト（クラス）を作る
class PCSprite(CharacterSprite):
    def move(self, press):
        if press[K_LEFT]:
            self.rect.move_ip(-self.vx, 0)
        if press[K_RIGHT]:
            self.rect.move_ip(self.vx, 0)
        if press[K_UP]:
            self.rect.move_ip(0, -self.vy)
        if press[K_DOWN]:
            self.rect.move_ip(0, self.vy)

if __name__ == '__main__':
    pygame.init()
    #SCREEN_SIZEの画面作成
    screen = pygame.display.set_mode(SCR_RECT.size)
    #タイトルバーの文字セット
    pygame.display.set_caption("初めてのシューティング")

    #スプライト作成
    MyPC = PCSprite("pc_img.png", 400, 500, 100, 100)

    #画面の更新時間を管理するオブジェクト
    fps = pygame.time.Clock()

    #ゲームイベントループ
    while True:
        screen.fill((0,0,0)) #画面を真っ青で塗りつぶす
        fps.tick(60)

        #スプライト更新
        MyPC.draw(screen)
        #スプライトを描画
        MyPC.draw(screen)

        pygame.display.update() #画面を更新

        #イベント処理
        for event in pygame.event.get():
            if event.type == QUIT: # 終了イベント
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                pressed_keys = pygame.key.get_pressed()
                MyPC.move(pressed_keys)
