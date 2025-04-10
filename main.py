import pygame # type: ignore
import time

pygame.init()

# Screen
screen = pygame.display.set_mode((1200, 800))  # زيادة حجم الشاشة إلى 1200x800
pygame.display.set_caption("Player Training Projection")

# Colors
FIELD_GREEN = (4, 22, 4)  # اللون الأخضر للأرض
WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 102, 204)  # اللون الأزرق للاعب
BALL_COLOR = (255, 165, 0)  # اللون البرتقالي للكرة
GOAL_COLOR = (200, 200, 200)  # اللون الرمادي للمرمى
CORRECT_PATH_COLOR = (0, 0, 255)  # اللون الأزرق للمسار الصحيح
WRONG_PATH_COLOR = (255, 0, 0)  # اللون الأحمر للمسار الخطأ

# Font
font = pygame.font.SysFont(None, 32)

# Objects
player = pygame.Rect(100, 370, 40, 40)  # اللاعب
ball = pygame.Rect(100, 420, 20, 20)  # الكرة
goal = pygame.Rect(1100, 370, 60, 60)  # المرمى
correct_path = pygame.Rect(100, 370, 1000, 40)  # الخط الذي يحدد المسار الصحيح

# States
ball_shot = False
correction_shown = False
ball_target = pygame.Vector2(1100, 420)  # الهدف الخطأ (في مكان غير الهدف الصحيح)
score = 0
mistakes = 0
already_penalized = False

# Timing and additional analysis variables
time_taken = 0  # الوقت المستغرق
attempts = 0  # عدد المحاولات
successful_shots = 0  # التصويبات الصحيحة
path_deviation = 0  # الانحراف عن المسار الصحيح
shooting_speed = 0  # سرعة التصويب
correction_instructions = 0  # عدد التوجيهات التصحيحية
distance_travelled = 0  # المسافة المقطوعة
time_on_correct_path = 0  # الوقت في المسار الصحيح
start_time = 0  # وقت البداية للتوقيت

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(FIELD_GREEN)  # تعبئة الشاشة باللون الأخضر (أرض الملعب)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if not ball_shot:
        if keys[pygame.K_RIGHT]:
            player.x += 5
            ball.x += 5
            distance_travelled += 5  # حساب المسافة المقطوعة
        if keys[pygame.K_LEFT]:
            player.x -= 5
            ball.x -= 5
            distance_travelled += 5
        if keys[pygame.K_UP]:
            player.y -= 5
            ball.y -= 5
            distance_travelled += 5
        if keys[pygame.K_DOWN]:
            player.y += 5
            ball.y += 5
            distance_travelled += 5
        if keys[pygame.K_SPACE] and not ball_shot:
            ball_shot = True
            start_time = pygame.time.get_ticks()  # بدء العد التنازلي للوقت
            attempts += 1  # زيادة عدد المحاولات

            if goal.collidepoint(ball.center):
                successful_shots += 1  # التصويب الصحيح
                score += 20  # تصويب ناجح
            else:
                score -= 10  # تصويب خاطئ
                mistakes += 1  # الأخطاء

    # منطق تصويب الكرة
    if ball_shot and not correction_shown:
        ball_direction = pygame.Vector2(ball_target.x - ball.centerx, ball_target.y - ball.centery)
        
        # إذا كانت المسافة بين الكرة والهدف أقل من 5 بيتم إيقاف الكرة
        if ball_direction.length() > 5:
            ball_direction = ball_direction.normalize() * 5
            ball.x += int(ball_direction.x)
            ball.y += int(ball_direction.y)
        else:
            ball_shot = False  # الكرة وصلت للمكان الهدف
            correction_shown = True

    if correction_shown:
        pygame.draw.line(screen, (255, 0, 0), ball.center, goal.center, 3)  # رسم خط تصحيح المسار
        screen.blit(font.render("Wrong shot detected!", True, (255, 0, 0)), (ball.x - 40, ball.y + 40))
        screen.blit(font.render("Correct target shown in blue", True, (0, 255, 255)), (ball.x - 60, ball.y + 70))
        pygame.draw.circle(screen, (0, 255, 255), goal.center, 8)  # رسم الهدف الصحيح باللون الأزرق

    # رسم المسار الأزرق إذا كان اللاعب في المسار الصحيح
    if player.x > 100 and player.x < 1100 and player.y > 370 and player.y < 410:  # التحقق من كون اللاعب على المسار الصحيح
        pygame.draw.line(screen, CORRECT_PATH_COLOR, player.center, goal.center, 2)  # رسم المسار الأزرق من اللاعب إلى الهدف
        screen.blit(font.render("You're on the right path!", True, (0, 0, 255)), (player.x - 50, player.y + 50))
        score += 10  # إذا التزم اللاعب بالمسار الصحيح
    else:
        pygame.draw.line(screen, WRONG_PATH_COLOR, player.center, goal.center, 2)  # رسم المسار الأحمر إذا كان اللاعب في المسار الخطأ
        screen.blit(font.render("Wrong path! Get back on track!", True, (255, 0, 0)), (player.x - 80, player.y + 50))
        if not already_penalized:
            score -= 5  # نقص النقاط عند الخروج عن المسار الصحيح
            mistakes += 1  # الأخطاء
            path_deviation += 1  # زيادة الانحراف عن المسار
            already_penalized = True

    # رسم اللاعب
    pygame.draw.rect(screen, PLAYER_COLOR, player)

    # رسم الكرة
    pygame.draw.circle(screen, BALL_COLOR, ball.center, 10)

    # رسم المرمى
    pygame.draw.rect(screen, GOAL_COLOR, goal)

    # عرض النقاط والأخطاء في التيرمنال
    print(f"Score: {score}")
    print(f"Mistakes: {mistakes}")
    print(f"Attempts: {attempts}")
    if attempts > 0:
        print(f"Shooting accuracy: {successful_shots / attempts * 100:.2f}%")
    print(f"Path deviation: {path_deviation:.2f} meters")
    print(f"Distance travelled: {distance_travelled} meters")
    
    # وقت التحليل (تحليل الوقت المستغرق للتصويب)
    if ball_shot == False and correction_shown:
        time_taken = (pygame.time.get_ticks() - start_time) / 1000  # الوقت بالثواني
        print(f"Time taken for shot: {time_taken:.2f} seconds")
    
    if keys[pygame.K_r]:
        ball.x = player.x + 40  # إعادة الكرة إلى مكان اللاعب
        ball.y = player.y + 40
        ball_shot = False
        correction_shown = False
        mistakes = 0
        score = 0
        attempts = 0
        successful_shots = 0
        path_deviation = 0
        distance_travelled = 0
        print("\n--- Restarting Game ---")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
