import pygame

pygame.init() #초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 480  #가로 크기
screen_height = 640 #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("HELLO Game") #게임 이름

#배경 이미지 불러오기
background = pygame.image.load("/Users/gwonminjeong/Desktop/game/background.png")

# 스프라이트(캐릭터) 불러오기
character = pygame.image.load("/Users/gwonminjeong/Desktop/game/character.png")
character_size = character.get_rect().size #이미지의 크기를 구해옴
character_width = character_size[0] #캐릭터 가로 크기
character_height = character_size[1] #캐릭터 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2) #화면 가로의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height #화면 세로 크기 가장 아래에 해당하는 곳에 위치

#이벤트 루프
running = True # 게임이 진행중인가? 를 확인
while running:
    for event in pygame.event.get():  # 어떤 이벤트가 발생하는 동안
        if event.type == pygame.QUIT:  #창이 닫힌다면
            running = False #게임 진행중이 아님

    # screen.fill((23, 60, 41)) -> 색으로 채우기
    screen.blit(background, (0, 0)) #가로 세로 왼쪽부터 0 배경 그림
    
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update() #게임 화면 다시 그리기

#게임 종료
pygame.quit()
