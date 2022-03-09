import pygame

###############################################################
# 기본 초기화 (반드시 해야하는 것들)
pygame.init()  # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 640  # 가로 크기
screen_height = 480  # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("HELLO Game")  # 게임 이름

# FPS
clock = pygame.time.Clock()
###############################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)

# 배경 이미지 불러오기
background = pygame.image.load(
    "/Users/gwonminjeong/Desktop/game/pygame_project/images/background.png")

# 스프라이트(캐릭터) 불러오기
character = pygame.image.load(
    "/Users/gwonminjeong/Desktop/game/pygame_project/images/character3.png")
character_size = character.get_rect().size  # 이미지의 크기를 구해옴
character_width = character_size[0]  # 캐릭터 가로 크기
character_height = character_size[1]  # 캐릭터 세로 크기
character_x_pos = (screen_width / 2) - \
    (character_width / 2)  # 화면 가로의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height  # 화면 세로 크기 가장 아래에 해당하는 곳에 위치

# 이동할 좌표
to_x = 0
to_y = 0

# 이동 속도
character_speed = 0.4

# 무기 만들기
weapon = pygame.image.load(
    "/Users/gwonminjeong/Desktop/game/pygame_project/images/weapon2.png")
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 4

# 적 캐릭터
enemy_images = [
    pygame.image.load(
        "/Users/gwonminjeong/Desktop/game/pygame_project/images/enemy2.png"),
    pygame.image.load(
        "/Users/gwonminjeong/Desktop/game/pygame_project/images/enemy3.png"),
    pygame.image.load(
        "/Users/gwonminjeong/Desktop/game/pygame_project/images/enemy4.png"),
    pygame.image.load("/Users/gwonminjeong/Desktop/game/pygame_project/images/enemy5.png")]

# 공 크기에 따른 최초 스피드
enemy_speed_y = [-16, -13, -10, -7]  # index 0, 1, 2, 3 에 해당하는 값

# 공들
enemys = []

# 최초 발생하는 큰 공 추가
enemys.append({
    "pos_x": 50,  # 공의 x 좌표
    "pos_y": 50,  # 공의 y 좌표
    "img_idx": 0,  # 공의 이미지 인덱스
    "to_x": 3,  # x축 이동방향 -3이면 왼쪽, 3이면 오른쪽
    "to_y": -6,  # y축 이동방향,
    "init_spd_y": enemy_speed_y[0]})  # y최초 속도


# enemy_size = enemy_images.get_rect().size #이미지의 크기를 구해옴
# enemy_width = enemy_size[0] #캐릭터 가로 크기
# enemy_height = enemy_size[1] #캐릭터 세로 크기
# enemy_x_pos = (screen_width / 2) - (enemy_width / 2) #화면 가로의 절반 크기에 해당하는 곳에 위치
# enemy_y_pos = (screen_height /2) - (enemy_height / 2)  #화면 세로 크기 가장 아래에 해당하는 곳에 위치

# #폰트 정의
game_font = pygame.font.Font(None, 40)  # 폰트 객체 생성(폰트, 크기)

# 총 시간
total_time = 50

# 시작 시간 정보
start_ticks = pygame.time.get_ticks()  # 시작 tick을 받아옴

###############################################################

# 2. 이벤트 처리 루프 ( 키보드, 마우스 등)
running = True  # 게임이 진행중인가? 를 확인
while running:
    dt = clock.tick(60)  # 게임화면의 초당 프레임 수를 설정

    # print("fps : " + str(clock.get_fps()))

    for event in pygame.event.get():  # 어떤 이벤트가 발생하는 동안
        if event.type == pygame.QUIT:  # 창이 닫힌다면
            running = False  # 게임 진행중이 아님

        if event.type == pygame.KEYDOWN:  # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT:  # 캐릭터 왼쪽으로
                to_x -= character_speed  # to_x = to_x - 5
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_SPACE:  # 무기 발사
                weapon_x_pos = character_x_pos + \
                    (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = screen_height - character_height - character_height
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:  # 방향키 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0


###############################################################

    # 3. 게임 캐릭터의 위치 정의
    character_x_pos += to_x * dt

    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    # 100, 200 -> y 좌표가 180, 160, 140 만큼 줄어들음
    # 500, 200 - > 180, 160, 140, ...
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]  # 무기 위치를 위로 변경

    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]  # 0은 x좌표, 1은 y 좌표

    # 공 위치 정의
    for enemy_idx, enemy_val in enumerate(enemys):
        enemy_pos_x = enemy_val["pos_x"]
        enemy_pos_y = enemy_val["pos_y"]
        enemy_img_idx = enemy_val["img_idx"]

        enemy_size = enemy_images[enemy_img_idx].get_rect().size
        enemy_width = enemy_size[0]
        enemy_height = enemy_size[1]

        # 가로벽에 닿았을 때 공 이동 위치 변경 (튕겨 나오는 효과)
        if enemy_pos_x < 0 or enemy_pos_x > screen_width - enemy_width:
            enemy_val["to_x"] = enemy_val["to_x"] * -1

        # 세로 위치
        if enemy_pos_y >= screen_height - enemy_height - 30:
            enemy_val["to_y"] = enemy_val["init_spd_y"]
        else:  # 그 외 모든 경우에는 속도를 증가
            enemy_val["to_y"] += 0.5

        enemy_val["pos_x"] += enemy_val["to_x"]
        enemy_val["pos_y"] += enemy_val["to_y"]

###############################################################

# 4. 충돌 처리


###############################################################
# . 5 화면에 그리기

    # screen.fill((23, 60, 41)) -> 색으로 채우기
    screen.blit(background, (0, 0))  # 가로 세로 왼쪽부터 0 배경 그림

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(enemys):
        enemy_pos_x = val["pos_x"]
        enemy_pos_y = val["pos_y"]
        enemy_img_idx = val["img_idx"]
        screen.blit(enemy_images[enemy_img_idx], (enemy_pos_x, enemy_pos_y))

    screen.blit(character, (character_x_pos, character_y_pos))

    # 타이머 넣기, 경과시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    # 경과 시간을(ms) 1000으로 나누어서 초 단위로 표시

    timer = game_font.render(
        str(int(total_time - elapsed_time)), True, (255, 255, 255))
    # 출력할 글자, True, 글자 색상
    screen.blit(timer, (600, 10))

    # 만약 시간이 0 이하이면 게임 종료
    if total_time - elapsed_time <= 0:
        print("시간 종료")
        running = False

    pygame.display.update()  # 게임 화면 다시 그리기


# 잠시 대기
pygame.time.delay(2000)  # 2초 정도 대기

# 게임 종료
pygame.quit()
