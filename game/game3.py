# -*- coding: utf-8 -*-
import pygame,math
from pygame.locals import *
import random
import sys
import re

SCR_RECT = Rect(0,0,800,600) # スクリーンサイズ（px指定）

class Game:
    #クラス化することで各メソッドで共通して使う変数にアクセスしやすくする。
    enemy_prob = 12 #敵の出現率
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

        #スプライトグループを作成して登録
        self.all_sprite = pygame.sprite.RenderUpdates()
        self.pc = pygame.sprite.Group() # プレイヤーキャラクターグループ
        self.enemies = pygame.sprite.Group() #エネミーグループ
        #デフォルトスプライトグループを登録
        Player.containers = self.all_sprite, self.pc
        Enemy.containers = self.all_sprite, self.enemies
        #プレイヤーを作成
        self.player = Player()

    def update(self):
        #情報の更新と敵の出現管理
        # 0からenemy_probまでの乱数を出して，0が出たらエネミー出現
        #　enemy_probを大きくすると出現率が下がる
        if not random.randrange(self.enemy_prob):
            Enemy()
        self.all_sprite.update()
        self.collision_detection()

    def draw(self, screen):
        #描画
        screen.fill((0, 0, 0))
        self.all_sprite.draw(screen)

    def collision_detection(self):
        #プレイヤーとエネミー，レーザーとエネミーの衝突判定
        player_collided = pygame.sprite.groupcollide(self.enemies, self.pc, True, True)
        for enemy in player_collided.keys():
            #本当はゲームオーバー画面
            pygame.quit()
            sys.exit()

    def load_images(self):
        #各イメージの読み込み

        #スプライトの画像を登録
        Player.image = load_image("pc_img.png")
        Enemy.image = load_image("enemy_img.png")

    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()





class Player(pygame.sprite.Sprite):
    #プレイヤークラス
    speed = 3 # 移動速度

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.bottom = SCR_RECT.bottom # プレイヤーは画面の一番下からスタート
        self.rect.left = 400
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
        mov_vec = [(-self.speed, 0), (0, self.speed), (self.speed, 0), (0, -self.speed)]
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
