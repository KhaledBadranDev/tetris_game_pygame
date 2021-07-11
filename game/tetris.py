#######################
#AUTHOR: KHALED BADRAN
#######################

from util import *
import random
import time


def block_is_falling(block, playing_field):
    if can_fall(block, playing_field):
        for tile in block.tiles:
            tile.y += tile_length
        clock.get_rawtime()
        clock.tick(8)

def can_fall(current_block, playing_field):
    for tile in playing_field.occupied_tiles:
        for block_tile in current_block.tiles:
            if block_tile.y+tile_length == tile.y and block_tile.x == tile.x:
                return False         
    if current_block.tiles[0].y >= playing_field_height+tile_length:
        return False  

    return True

def update_graphics(block, playing_field):
    #background and text
    DISPLAY_SCREEN.blit(background_img, (0, 0))
    pygame.draw.rect(DISPLAY_SCREEN , black, (off_set_x, off_set_y, playing_field_width, playing_field_height) )
    font = pygame.font.SysFont("comicsansms", 48)
    rendered_text = font.render("Tetris", 1, orange)
    DISPLAY_SCREEN.blit(rendered_text, (width/2-80, 10))

    #tiles
    for tile in playing_field.occupied_tiles:
        pygame.draw.rect(DISPLAY_SCREEN , tile.color, (tile.x, tile.y, tile_length, tile_length) )

    #blocks
    for tile in block.tiles:
        if tile.y >= off_set_y:
            pygame.draw.rect(DISPLAY_SCREEN , tile.color, (tile.x, tile.y, tile_length, tile_length) )


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


def get_new_block(current_block, playing_field):
    if can_fall(current_block, playing_field): return (current_block, False)
    
    for block_tile in current_block.tiles: 
        found = False
        for row in playing_field.tiles:
            if not found:
                for tile in row:
                    if block_tile.x == tile.x and block_tile.y == tile.y:
                        tile.x = block_tile.x
                        tile.y = block_tile.y
                        tile.color = block_tile.color
                        tile.empty = False

                        playing_field.occupied_tiles.append(tile)
                        found = True
                        break

    rand_index1 = random.randint(0, 6)
    rand_index2 = random.randint(0, 6)
    
    clock.tick(2)
    new_block = Block(shapes[rand_index1], block_colors[rand_index2])
    
    return (new_block, True)

def is_game_over(current_block, playing_field):
    for tile in playing_field.occupied_tiles:
        if tile.y <= off_set_y:
            for tile in playing_field.occupied_tiles:
                pygame.draw.rect(DISPLAY_SCREEN , tile.color, (tile.x, tile.y, tile_length, tile_length) )
            pygame.display.update()
            print("Game Over")
            time.sleep(2)   
            start_game()

# for moving the tetris block
########################################
def move_left(block, playing_field):
    if can_move_left(block, playing_field):
        for tile in block.tiles:
            tile.x -= tile_length


def move_right(block, playing_field):
    if can_move_right(block, playing_field):
        for tile in block.tiles:
            tile.x += tile_length


def can_move_left(block, playing_field):
    # whether inside the playing field or not
    for tile in block.tiles:
        if tile.x <= off_set_x:
            return False
    # whether adjacent field_tiles are occupied or not
    for block_tile in block.tiles:
        for occupied_tile in playing_field.occupied_tiles:
            if block_tile.x - tile_length == occupied_tile.x and block_tile.y == occupied_tile.y:
                return False

    return True
    

def can_move_right(block, playing_field):
    # whether inside the playing field or not
    for tile in block.tiles:
        if tile.x + tile_length >= off_set_x+playing_field_width:
            return False
    # whether adjacent field_tiles are occupied or not
    for block_tile in block.tiles:
        for occupied_tile in playing_field.occupied_tiles:
            if block_tile.x + tile_length == occupied_tile.x and block_tile.y  == occupied_tile.y:
                return False

    return True


def rotate(block, playing_field):
    pass
    #TODO

#########################################


def start_game():    
    playing_field = PlayingField()
    rand_index = random.randint(0, 6)
    block = Block(shapes[rand_index], block_colors[rand_index])


    while True:
        (block, new) = get_new_block(block, playing_field)

        update_graphics(block, playing_field)        
        manage_events(block, playing_field)

        block_is_falling(block, playing_field)
        update_graphics(block, playing_field)

        is_game_over(block, playing_field)

        pygame.display.update()


def manage_events(block, playing_field):
     for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    #move the block to the left
                    move_left(block, playing_field)
                elif event.key == pygame.K_RIGHT:
                    #move the block to the right
                    move_right(block, playing_field)


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
