# -*- coding: utf-8 -*-
import pygame,math
from pygame.locals import *
import random
import sys
import re

START, PLAY, GAMEOVER = (0, 1, 2) #ゲーム状態
SCR_RECT = Rect(0,0,800,600) # スクリーンサイズ（px指定）

class Game:
    #クラス化することで各メソッドで共通して使う変数にアクセスしやすくする。
    enemy_prob = 10 #敵の出現率
    def __init__(self):
        #各種読み込み
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("初めてのシューティング")
        #素材のロード
        self.load_images()
        #ゲームオブジェクトを初期化
        self.init_game()
        #メインループ開始
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def init_game(self):
        #ゲームオブジェクトを初期化

        #ゲーム状態
        self.game_state = START
        #スプライトグループを作成して登録
        self.all_sprite = pygame.sprite.RenderUpdates()
        self.pc = pygame.sprite.Group() # プレイヤーキャラクターグループ
        self.enemies = pygame.sprite.Group() #エネミーグループ
        self.shots = pygame.sprite.Group() # 弾グループ
        #デフォルトスプライトグループを登録
        Player.containers = self.all_sprite, self.pc
        Enemy.containers = self.all_sprite, self.enemies
        Shot.containers = self.all_sprite, self.shots
        #プレイヤーを作成
        self.player = Player()

    def update(self):
        #情報の更新と敵の出現管理
        if self.game_state == PLAY:
            # 0からenemy_probまでの乱数を出して，0が出たらエネミー出現
            #　enemy_probを大きくすると出現率が下がる
            if not random.randrange(self.enemy_prob):
                Enemy()
            self.all_sprite.update()
            self.collision_detection()

    def draw(self, screen):
        #描画
        screen.fill((0, 0, 0))
        if self.game_state == START:
            sysfont = pygame.font.SysFont(None, 80)
            sys = sysfont.render("PUSH SPACE TO START",False,(255,0,0))
            screen.blit(sys, ((SCR_RECT.width-sys.get_width())/2,270))

        if self.game_state == PLAY:
            self.all_sprite.draw(screen)

        if self.game_state == GAMEOVER:
            sysfont = pygame.font.SysFont(None, 80)
            sys = sysfont.render("GAMEOVER",False,(255,0,0))
            screen.blit(sys, ((SCR_RECT.width-sys.get_width())/2,270))


    def collision_detection(self):
        #プレイヤーとエネミー，レーザーとエネミーの衝突判定
        player_collided = pygame.sprite.groupcollide(self.enemies, self.pc, True, False)
        for enemy in player_collided.keys():
            #本当はゲームオーバー画面
            self.player.kill()
            self.player = Player()
            self.game_state = GAMEOVER

            #spriteを消すすごいやつ
            for sprite in self.enemies:
                if isinstance(sprite, Enemy):
                    sprite.kill()
        alien_collided = pygame.sprite.groupcollide(self.enemies, self.shots, True, True)

    def load_images(self):
        #各イメージの読み込み

        #スプライトの画像を登録
        Player.image = load_image("pc_img.png")
        Enemy.image = load_image("enemy_img.png")
        Shot.image = load_image("lazer.png")

    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    if self.game_state == START:
                        self.game_state = PLAY
                    elif self.game_state == GAMEOVER:
                        self.game_state = START

class Shot(pygame.sprite.Sprite):
    #弾
    speed = 9
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos # 中心座標をposに
    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:
            self.kill();
            del self



class Player(pygame.sprite.Sprite):
    #プレイヤークラス
    speed = 7 # 移動速度
    reload_time = 15

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCR_RECT.bottom # プレイヤーは画面の一番下からスタート
        self.rect.left = 400
        self.reload_timer = 0
    def update(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_key[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if pressed_key[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_key[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        #画面からはみ出さないようにする
        self.rect = self.rect.clamp(SCR_RECT)
        #弾を撃つ
        if self.reload_timer > 0:
            self.reload_timer -= 1
        if pressed_key[K_SPACE]:
            #リロード時間
            if not self.reload_timer > 0:
                Shot(self.rect.center)
                self.reload_timer = self.reload_time


class Enemy(pygame.sprite.Sprite):
    #エネミークラス
    speed = 3 # 移動速度

    def __init__(self):
        #初期化処理
        #敵は上からランダムに出てくる
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(SCR_RECT.width - self.rect.width)
        self.rect.bottom = SCR_RECT.top
    def update(self):
        #更新処理
        #ランダムに動き回る
        #上，右，下，左の順に設定
        mov_vec = [(-3 * self.speed, 0),(0, 5 * self.speed), (3 * self.speed, 0)]
        self.rect.move_ip(random.choice(mov_vec))

def load_image(filename, colorkey=None):
    # 画像をロード
    # colorkeyは背景色

    # 画像ファイルがpngかgifか判定するための正規表現
    filecase = re.compile(r'[a-zA-Z0-9_/]+¥.png|[a-zA-Z0-9_/]+¥.gif')

    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image: " + filename)
        raise SystemExit from message

    #画面の拡張子によって処理を振り分け
    is_match = filecase.match(filename)
    if is_match:
        image = image.convert_alpha()
    else:
        image = image.convert()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


if __name__ == '__main__':
    Game()
