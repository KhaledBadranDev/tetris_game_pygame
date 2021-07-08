#######################
#AUTHOR: KHALED BADRAN
#######################

from util import *
import random
import time


def update_graphics(playing_field):
    #background and text
    DISPLAY_SCREEN.blit(background_img, (0, 0))
    pygame.draw.rect(DISPLAY_SCREEN , black, (off_set_x, off_set_y, playing_field_width, playing_field_height) )
    font = pygame.font.SysFont("comicsansms", 48)
    rendered_text = font.render("Tetris", 1, orange)
    DISPLAY_SCREEN.blit(rendered_text, (width/2-80, 10))

    #borders
    pygame.draw.line(DISPLAY_SCREEN , orange, (off_set_x-2, off_set_y-3), (playing_field_width+off_set_x+1, off_set_y-3), 4) # horizontal line top
    pygame.draw.line(DISPLAY_SCREEN , orange, (off_set_x-2, off_set_y+playing_field_height+1), (playing_field_width+off_set_x+1, off_set_y+playing_field_height+1), 4) # horizontal line bottom
    pygame.draw.line(DISPLAY_SCREEN , orange, (off_set_x-3, off_set_y-3), (off_set_x-3, off_set_y+playing_field_height+1), 4) # vertical line left
    pygame.draw.line(DISPLAY_SCREEN , orange, (playing_field_width+off_set_x+1, off_set_y-3), (playing_field_width+off_set_x+1, off_set_y+playing_field_height+1), 4) # vertical line right

    #grid
    current_y_horizontal_lines = off_set_y
    current_x_vertical_lines = off_set_x
    for i in range(19): #20 tile/square per row --> 19 horizontal lines
        current_y_horizontal_lines += 33
        pygame.draw.line(DISPLAY_SCREEN , white, (off_set_x, current_y_horizontal_lines), (playing_field_width+off_set_x-1, current_y_horizontal_lines)) # horizontal line top
    for j in range(9): #10 tile/square per col --> 9 vertical lines
        current_x_vertical_lines += 33        
        pygame.draw.line(DISPLAY_SCREEN , white, (current_x_vertical_lines-1, off_set_y), (current_x_vertical_lines-1, playing_field_height+off_set_y)) # horizontal line top

    pygame.display.update()


########################################


def start_game():    
    playing_field = PlayingField()

    while True:
        update_graphics(playing_field)        
        manage_events()

        pygame.display.update()


def manage_events():
     for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                pass
                #TODO


def introduction():
    button_width = 200
    button_height = 80
    #width/2-button_width/2
    play_button = Button(blue, orange, -400, height/2, button_width, button_height, 32, black, white, "PLAY")
    quit_button = Button(blue, orange, width+200, height/2+button_height+10, button_width,button_height, 32, black, white, "QUIT")
    
    font = pygame.font.SysFont("comicsansms", 48)
    rendered_text = font.render("Tetris", 1, orange)
    rendered_text_y = height

    #to draw the "Tetris" text in an animated way.
    while rendered_text_y > 10: 
        DISPLAY_SCREEN.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        rendered_text_y -= 1
        DISPLAY_SCREEN.blit(rendered_text, (width/2-80, rendered_text_y))
        pygame.display.update()
    
    #to draw the buttons in an animated way.
    while play_button.x < width/2-button_width/2 or quit_button.x > width/2-button_width/2:
        DISPLAY_SCREEN.blit(background_img, (0, 0))
        DISPLAY_SCREEN.blit(rendered_text, (width/2-80, rendered_text_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if play_button.x < width/2-button_width/2:
            play_button.x += 2
        if quit_button.x > width/2-button_width/2 :    
            quit_button.x -= 2

        play_button.blit(DISPLAY_SCREEN)
        quit_button.blit(DISPLAY_SCREEN)
        pygame.display.update()

    run = True
    while run:
        DISPLAY_SCREEN.blit(background_img, (0, 0))
        DISPLAY_SCREEN.blit(rendered_text, (width/2-80, rendered_text_y))

        mouse_position = pygame.mouse.get_pos() # get the position of the mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(mouse_position, event):
                    start_game()
                    run = True

                if quit_button.is_clicked(mouse_position, event):
                    pygame.quit()
                    sys.exit()
        
        if play_button.is_hovered_over(mouse_position):
            play_button.blit_hovered_over(DISPLAY_SCREEN)
        else:
            play_button.blit(DISPLAY_SCREEN, gray)
        if quit_button.is_hovered_over(mouse_position):
            quit_button.blit_hovered_over(DISPLAY_SCREEN)
        else:
            quit_button.blit(DISPLAY_SCREEN, gray)

        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__":
    introduction()
