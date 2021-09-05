import pygame,sys,math,random,os,pickle ,pygame.midi
from pygame.locals import *

pygame.mixer.pre_init(frequency=7350,buffer=128)
pygame.init()


BLACK=pygame.color.THECOLORS["black"]
WHITE=pygame.color.THECOLORS["white"]
RED=pygame.color.THECOLORS["red"]
BLUE=pygame.color.THECOLORS["blue"]
YELLOW=pygame.color.THECOLORS["yellow"]
ORANGE=pygame.color.THECOLORS["orange"]
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
DISPLAY_SURFACE_WIDTH=320
DISPLAY_SURFACE_HEIGHT=240
SCALE=2
FLOOR_Y_POS=180


def get_palette(palette_file):
    with open(palette_path, 'r') as file:
         palette_data=file.read()
    palette_data=palette_data.split('\n')
    del(palette_data[len(palette_data)-1])

    #palette=image.get_palette()
    palette=[[0,0,0]for i in range(256)]

    for i in range(len(palette_data)):
            palette_data[i]=palette_data[i].split(' ')
            color=palette_data[i]
            for j in range(len(color)-1,-1,-1):
                    if color[j]=='':
                            del(color[j])
                    else:
                            color[j]=int(color[j])

            palette[i][0]=color[1]*4
            palette[i][1]=color[2]*4
            palette[i][2]=color[3]*4
    return palette


def Runlength_decompression(bytes_list):
    bytes_list2=bytes_list
    bytes_list=list(bytes_list)
    step=0
    index=0
    length=len(bytes_list)-1
    while index<length:
       #loop speed limitation
       #30 frames per second is enought
       #pygame.time.Clock().tick(30)
       if bytes_list[index+2]!=0:
          bytes_list[index+1]=int.from_bytes(
          bytes([bytes_list[index+1],bytes_list[index+2]]),sys.byteorder)
       step=bytes_list[index+1]+1
       bytes_list[index]=[0]*bytes_list[index]
       del(bytes_list[index+1])
       del(bytes_list[index+1])
       length=len(bytes_list)-1
       index+=step
    for i in range(len(bytes_list)-1,-1,-1):
        if type(bytes_list[i])==list:
           bytes_list[i:i+1]=bytes_list[i][:]
    return bytes(bytes_list)


def load_RE_2(RE,IDE,PALETTE):
    alpha_color=PALETTE[0]
    with open(IDE, 'r') as file:
         data=file.read()
    data=data.split('_the_end')
    images=data[0]
    sprites=data[1]
    collisions=data[2]
    images=images.split('\n')
    sprites=sprites.split('\n')
    collisions=collisions.split('\n')
    for i in range(len(images)-1,-1,-1):
        images[i]=images[i].split(' ')
        for j in range(len(images[i])-1,-1,-1):
            if images[i][j]=='':
               del(images[i][j])
        if len(images[i])!=4:
           del(images[i])

    for i in range(len(sprites)-1,-1,-1):
        sprites[i]=sprites[i].split(' ')
        for j in range(len(sprites[i])-1,-1,-1):
            if sprites[i][j]=='':
               del(sprites[i][j])
        if len(sprites[i])>5:
           sprites[i]=sprites[i][:5]
        if len(sprites[i])!=5:
           #print(sprites[i])
           del(sprites[i])

    for i in range(len(collisions)-1,-1,-1):
        collisions[i]=collisions[i].split(' ')
        for j in range(len(collisions[i])-1,-1,-1):
            if collisions[i][j]=='':
               del(collisions[i][j])
        if len(collisions[i])!=4:
           del(collisions[i])
        else:
           for j in range(len(collisions[i])):
               collisions[i][j]=int(collisions[i][j])
    #print(len(images),len(sprites),len(collisions))
    frames=[]
    len_sprites=len(sprites)
    with open(RE, 'rb') as file:
         for i in range(len(images)):
             image=images[i]
             image_size=(int(image[2]),int(image[3]))
             image_data=file.read(int(image[1]))
             image_data=Runlength_decompression(image_data)
             padding=(image_size[0]*image_size[1])-len(image_data)
             if padding<0:
                image_data=image_data[:padding]
             else:
                image_data+=b'\x00'*padding
             image_data=pygame.image.fromstring(image_data,image_size,'P')
             image_data.set_palette(PALETTE)
             image_data.set_colorkey(alpha_color)
             image_data.convert()
             if i< len_sprites:
                sprite=sprites[i]
                frame={'name':sprite[0],'x_axis_shift':int(sprite[2]),'y_axis_shift':int(sprite[3]),
                       'image':image_data,'collision_box':collisions[i]}
             frames.append(frame)
    return frames

def load_RE(RE,IDE,PALETTE):
    alpha_color=PALETTE[0]
    with open(IDE, 'r') as file:
         data=file.read()
    data=data.split('_the_end')
    images=data[0]
    sprites=data[1]
    collisions=data[2]
    images=images.split('\n')
    sprites=sprites.split('\n')
    collisions=collisions.split('\n')
    for i in range(len(images)-1,-1,-1):
        images[i]=images[i].split(' ')
        for j in range(len(images[i])-1,-1,-1):
            if images[i][j]=='':
               del(images[i][j])
        if len(images[i])!=4:
           del(images[i])

    for i in range(len(sprites)-1,-1,-1):
        sprites[i]=sprites[i].split(' ')
        for j in range(len(sprites[i])-1,-1,-1):
            if sprites[i][j]=='':
               del(sprites[i][j])
        #if len(sprites[i])>5:
           #sprites[i]=sprites[i][:5]
        if len(sprites[i])<5:
           #print(sprites[i])
           del(sprites[i])

    for i in range(len(collisions)-1,-1,-1):
        collisions[i]=collisions[i].split(' ')
        for j in range(len(collisions[i])-1,-1,-1):
            if collisions[i][j]=='':
               del(collisions[i][j])
        if len(collisions[i])!=4:
           del(collisions[i])
        else:
           for j in range(len(collisions[i])):
               collisions[i][j]=int(collisions[i][j])

    #print(len(images),len(sprites),len(collisions))
    with open(RE, 'rb') as file:
         for i in range(len(images)):
             image=images[i]
             image_size=(int(image[2]),int(image[3]))
             image_data=file.read(int(image[1]))
             image_data=Runlength_decompression(image_data)
             padding=(image_size[0]*image_size[1])-len(image_data)
             if padding<0:
                image_data=image_data[:padding]
             else:
                image_data+=b'\x00'*padding
             image_data=pygame.image.fromstring(image_data,image_size,'P')
             image_data.set_palette(PALETTE)
             image_data.set_colorkey(alpha_color)
             image_data.convert()
             image[1]=image_data

    frames=[]
    len_collisions=len(collisions)
    for i in range(len(sprites)):
        sprite=sprites[i]
        image=images[int(sprite[1])][1]
        second_image=None
        collision=[0,0,0,0]
        if i < len_collisions:
           collision=collisions[i]
           if collision[2]<collision[0]:
              collision[2],collision[0]=collision[0],collision[2]
           if collision[3]<collision[1]:
              collision[3],collision[1]=collision[1],collision[3]
           collision=[collision[0],collision[1],collision[2]-collision[0],collision[3]-collision[1]]
        else:
           pass
           #print('no collision box')
        if len(sprite)>5:
           second_image=images[int(sprite[4])][1]
           second_image={'name':sprite[0],'x_axis_shift':int(sprite[5]),'y_axis_shift':int(sprite[6]),
                          'image':second_image,'collision_box':collision,
                          'image_size':second_image.get_size()}

        frame={'name':sprite[0],'x_axis_shift':int(sprite[2]),'y_axis_shift':int(sprite[3]),
               'image':image,'collision_box':collision,'second_image':second_image,
               'image_size':image.get_size()}

        if second_image:
           x_axis_shift = min(frame['x_axis_shift'], second_image['x_axis_shift'])
           y_axis_shift = min(frame['y_axis_shift'], second_image['y_axis_shift'])
           width = max(frame['x_axis_shift'] + frame['image_size'][0],
                       second_image['x_axis_shift'] + second_image['image_size'][0]) - x_axis_shift
           height = max(frame['y_axis_shift'] + frame['image_size'][1],
                        second_image['y_axis_shift'] + second_image['image_size'][1]) - y_axis_shift     
           image = pygame.Surface((width, height)).convert()
           image.set_colorkey(image.get_at((0,0)))
           image.blit(frame['image'], (frame['x_axis_shift'] - x_axis_shift,
                                       frame['y_axis_shift'] - y_axis_shift))
           image.blit(second_image['image'], (second_image['x_axis_shift'] - x_axis_shift,
                                              second_image['y_axis_shift'] - y_axis_shift))
           frame['image'] = image
           frame['image_size'] = (width, height)
           if frame['collision_box'] != [0,0,0,0]:
              frame['collision_box'][0] += frame['x_axis_shift'] - x_axis_shift
              frame['collision_box'][1] += frame['y_axis_shift'] - y_axis_shift
           frame['x_axis_shift'] = x_axis_shift
           frame['y_axis_shift'] = y_axis_shift
        frames.append(frame)
    return frames


def load_SEQ(SEQ):
    with open(SEQ, 'r') as file:
         seq_data=file.read()
    seq_data=seq_data.split('\n')
    process='sequences_frames'
    split_index=None
    sequences={}
    sequences_frames={}
    for i in range(len(seq_data)-1,-1,-1):
        seq_data[i]=seq_data[i].split(' ')
        for j in range(len(seq_data[i])-1,-1,-1):
            if seq_data[i][j]=='':
               del(seq_data[i][j])
            else:
               if process=='sequences':
                  seq_data[i][j]=int(seq_data[i][j])
        if process=='sequences':
           if seq_data[i]!=[]:
              seq_data[i][-1],seq_data[i][-2]=seq_data[i][-2],seq_data[i][-1]
              if seq_data[i][-1]==253:
                 seq_data[i].append(seq_data[i][-3])
                 if len(seq_data[i])>5:
                    del(seq_data[i][-4])
              sequences[seq_data[i][0]]=seq_data[i][1:]
        if process=='sequences_frames':
           if len(seq_data[i])==5:
              seq_data[i][0]=int(seq_data[i][0])
              seq_data[i][1]=int(seq_data[i][1])
              seq_data[i][2]=int(seq_data[i][2])
              seq_data[i][3]=int(seq_data[i][3])
              if len(seq_data[i][4])==6:
                 #seq_data[i][4]=seq_data[i][4][:3]+'N'+seq_data[i][4][3:]
                 seq_data[i][4]="D00N0xx"
              seq_data[i].append(seq_data[i][4][0])
              seq_data[i].append(int(seq_data[i][4][1]))
              seq_data[i].append(int(seq_data[i][4][2]))
              seq_data[i].append(seq_data[i][4][3])
              seq_data[i].append(int(seq_data[i][4][4]))
              seq_data[i].append(seq_data[i][4][5])
              seq_data[i].append(seq_data[i][4][6])
              del(seq_data[i][4])
              sequences_frames[seq_data[i][0]]={'Image_number':seq_data[i][1],
                 'x_movement':seq_data[i][2], 'y_movement':seq_data[i][3],
                 'frame_type':seq_data[i][4], 'hit_damage':seq_data[i][5],
                 'hit_reaction':seq_data[i][6], 'frame_orientation':seq_data[i][7],
                 'cancel_mode':seq_data[i][8], 'attack_mode':seq_data[i][9],
                 'invincible':seq_data[i][10]}
        if seq_data[i]==['-1']:
           seq_data[i][0]=int(seq_data[i][0])
           split_index=i
           process='sequences'
        elif seq_data[i]==[]:
           del(seq_data[i])
    #sequences=seq_data[:split_index]
    #sequences_frames=seq_data[split_index+1:]
    for i in range(9):
        sequences[i].append("movement_sequence")
    return (sequences, sequences_frames)


def load_KEY(KEY):
    with open(KEY, 'r') as file:
         key_data=file.read()
    key_data=key_data.split('_end    -1  _end')
    #key_data=key_data.split('_end -1 _end')
    super_moves=key_data[0]
    throws=key_data[1]
    super_moves=super_moves.split('\n')
    throws=throws.split('\n')
    for i in range(len(super_moves)-1,-1,-1):
        super_moves[i]=super_moves[i].split(' ')
        for j in range(len(super_moves[i])-1,-1,-1):
            if super_moves[i][j]=='':
               del(super_moves[i][j])
        if super_moves[i]==[]:
           del(super_moves[i])
    close_range=int(super_moves[0][0])
    del(super_moves[0])
    for i in range(len(super_moves)):
        super_moves[i][1]=int(super_moves[i][1])
        reverse_string=''
        for j in range(len(super_moves[i][0])-1,-1,-1):
            reverse_string+=super_moves[i][0][j]
        super_moves[i][0]=reverse_string
        super_move={'inputs':super_moves[i][0],
                    'sequence':super_moves[i][1],
                    'sound':super_moves[i][2],
                    'inputs_lenth':len(super_moves[i][0])}
        if super_moves[i][2] != '_no_voice':
           super_move['sound'] = pygame.mixer.Sound(sfibm_path+super_moves[i][2])
        elif super_moves[i][2] == '_no_voice':
           super_move['sound'] = pygame.mixer.Sound(bytes(0))
        super_move['sound'].set_volume(0.3)   
        super_moves[i]=super_move
    for i in range(len(throws)-1,-1,-1):
        throws[i]=throws[i].split(' ')
        for j in range(len(throws[i])-1,-1,-1):
            if throws[i][j]=='':
               del(throws[i][j])
        if throws[i]==[]:
           del(throws[i])
    del(throws[-1])
    for i in range(len(throws)):
        throw_data=throws[i]
        if len(throw_data[0]) == 1:
           throw_data[0] = '4' + throw_data[0]
        throw={'damage':int(throw_data[0][0]),'throw_height':int(throw_data[0][1]),
               'direction_held':int(throw_data[1][0]),
               'button_held':int(throw_data[1][1]),
               'character_sequence':int(throw_data[2]),
               'opponent_sequence':int(throw_data[3]),
               'slam_direction':int(throw_data[4]),'sound':throw_data[5]}
        if throw_data[5] != '_no_voice':
           throw['sound'] = pygame.mixer.Sound(sfibm_path+throw_data[5])
        elif throw_data[5] == '_no_voice':
           throw['sound'] = pygame.mixer.Sound(bytes(0))
        throw['sound'].set_volume(0.3)   
        throws[i]=throw
    return super_moves,throws,close_range


def load_R(R,ID,PALETTE):
    alpha_color=PALETTE[0]
    with open(ID, 'r') as file:
         data=file.read()
    data=data.split('_the_end')
    images=data[0]
    images=images.split('\n')
    for i in range(len(images)-1,-1,-1):
        images[i]=images[i].split(' ')
        for j in range(len(images[i])-1,-1,-1):
            if images[i][j]=='':
               del(images[i][j])
        if len(images[i])!=3:
           del(images[i])
        else:
           images[i][1]=int(images[i][1])
           images[i][2]=int(images[i][2])
    with open(R, 'rb') as file:
         for i in range(len(images)):
             image=images[i]
             image_size=(image[1],image[2])
             data_size=image[1]*image[2]
             image_data=file.read(data_size)
             image_data=pygame.image.fromstring(image_data,image_size,'P')
             image_data.set_palette(PALETTE)
             image_data.set_colorkey(alpha_color)
             image_data.convert()
             images[i]={'image':image_data,'width':image[1],'height':image[2],'name':image[0]}
    return images


def load_background(image_path,palette):
    with open(image_path, 'rb') as file:
         image_data=file.read()
    image_width=520  #int(image_path.split('.')[1])
    image_height=int(len(image_data)/image_width)
    image_size=(image_width,image_height)
    image=pygame.image.fromstring(image_data,image_size,'P')
    image.set_palette(palette)
    image.convert()
    pos=[int(160-image_width/2),200-image_height]
    pos[1]+=pos[1]%2
    background={'image':image,'width':image_width,'height':image_height,'pos':pos}
    return background


def load_character(RE, IDE, SEQ, KEY, controls, side, palette):
   sprites=load_RE(RE,IDE,palette)
   sequences,sequences_frames=load_SEQ(SEQ)
   super_moves,throws,close_range=load_KEY(KEY)
   if side == 'left':
      pos = [90, FLOOR_Y_POS]
   elif side == 'right':
      pos = [230, FLOOR_Y_POS]
   return Character(sprites,sequences,sequences_frames,controls,super_moves,throws,close_range,pos,side)


def check_character(character):
    for i in range(len(character.super_moves)-1,-1,-1):
        super_move = character.super_moves[i]
        try:
            character.sequences[super_move['sequence']]
        except KeyError:
            del(character.super_moves[i])
            print('delted super move with sequence number ',super_move['sequence'])
    for i in range(len(character.throws)-1,-1,-1):
        throw = character.throws[i]
        try:
            character.sequences[throw['character_sequence']]
        except KeyError:
            del(character.throws[i])
            print('delted throw with sequence number ',throw['character_sequence'])


def load_sounds(sfibm_path):
    sounds = []
    for i in range(10):
        if i < 8:
           sound = pygame.mixer.Sound(sfibm_path+'D'+str(i)+'.VOC')
        else:
           sound = pygame.mixer.Sound(sfibm_path+'D0.VOC')
        sound.set_volume(0.3)   
        sounds.append(sound)
    sounds.append(pygame.mixer.Sound(sfibm_path+'DEFENCE.VOC'))
    sounds[10].set_volume(0.3)
    for i in range(11,41):
        sound = pygame.mixer.Sound(sfibm_path+'A'+str(i)+'.VOC')
        sound.set_volume(0.3)
        sounds.append(sound)
    sounds.append(pygame.mixer.Sound(sfibm_path+'WAVEFX.VOC'))
    sounds[41].set_volume(0.3)
    return sounds
    

palette_path="SFLIU220\\RGB.PAL"
sfibm_path="SFLIU220\\"
IDE=sfibm_path+"HYPRYU.IDE"
RE=sfibm_path+"HYPRYU.RE"
SEQ=sfibm_path+"HYPRYU.SEQ"
KEY=sfibm_path+"HYPRYU.KEY"
IDE2=sfibm_path+"HYPKEN.IDE"
RE2=sfibm_path+"HYPKEN.RE"
SEQ2=sfibm_path+"HYPKEN.SEQ"
KEY2=sfibm_path+"HYPKEN.KEY"
background_path=sfibm_path+"HYPKEN.BK"
R=sfibm_path+"FACEW.R"
ID=sfibm_path+"FACEW.ID"


def read_RE(RE,IDE):
    screen = pygame.display.set_mode((640, 480))#,0,8)
    clock=pygame.time.Clock()
    PALETTE=get_palette(palette_path)
    #pygame.display.set_palette(get_palette(PALETTE))
    font=pygame.font.SysFont('Arial', 20)
    frames=load_RE(RE,IDE,PALETTE)
    image=frames[0]['image']
    images_lenth=len(frames)-1
    change_image=True
    image_index=0
    image_axis_pos=[200,400]
    image_pos=[0,0]
    frame=frames[image_index]

    pygame.key.set_repeat(400, 30)

    while True:

        #loop speed limitation
        #30 frames per second is enought
        clock.tick(30)

        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                 image_index+=1
                 if image_index>images_lenth:
                    image_index=0
                 frame=frames[image_index]
                 change_image=True
                elif event.key == K_LEFT:
                 image_index-=1
                 if image_index<0:
                    image_index=images_lenth
                 frame=frames[image_index]
                 change_image=True

        if change_image:
           change_image=False
           image=frame['image']
           image_width=image.get_width()
           image_height=image.get_height()
           image_scaled_size=(image_width*SCALE,image_height*SCALE)
           image=pygame.transform.scale(image,image_scaled_size).convert()
           screen.fill((255,255,255))
           x_axis=frame['x_axis_shift']*SCALE
           y_axis=frame['y_axis_shift']*SCALE
           image_pos=[x_axis+image_axis_pos[0],y_axis+image_axis_pos[1]]
           screen.blit(image,image_pos)
           if frame['second_image']:
              old_axis=[x_axis,y_axis]
              image=frame['second_image']['image']
              image_width2=image.get_width()
              image_height2=image.get_height()
              image_scaled_size=(image_width2*SCALE,image_height2*SCALE)
              image=pygame.transform.scale(image,image_scaled_size).convert()
              x_axis=frame['second_image']['x_axis_shift']*SCALE
              y_axis=frame['second_image']['y_axis_shift']*SCALE
              image_pos2=[x_axis+image_axis_pos[0],y_axis+image_axis_pos[1]]
              screen.blit(image,image_pos2)

           temp_rect=frames[image_index]['collision_box']
           rect=[image_pos[0],image_pos[1],image_width*SCALE,image_height*SCALE]
           pygame.draw.rect(screen, (255,0,0), rect,5)
           rect=[image_pos[0]+temp_rect[0]*SCALE,image_pos[1]+temp_rect[1]*SCALE,
                 temp_rect[2]*SCALE,temp_rect[3]*SCALE]
           pygame.draw.rect(screen, (0,0,255), rect,5)
           #pygame.draw.circle(screen,(0,255,0),(image_axis_pos),10)

           pygame.draw.line(screen,(0,255,0),(image_axis_pos[0]-15,image_axis_pos[1]),
                            (image_axis_pos[0]+15,image_axis_pos[1]),5)
           pygame.draw.line(screen,(0,255,0),(image_axis_pos[0],image_axis_pos[1]-15),
                            (image_axis_pos[0],image_axis_pos[1]+15),5)
           text=font.render(str(image_index)+' '+'/'+str(images_lenth), True, (250,0,0))
           screen.blit(text,(420,320))
           text=font.render(frames[image_index]['name'], True, (250,0,0))
           screen.blit(text,(420,340))
           pygame.display.flip()

#read_RE(RE,IDE)


def read_SEQ(RE,IDE,SEQ):
    screen = pygame.display.set_mode((640, 480))#,0,8)
    clock=pygame.time.Clock()
    PALETTE=get_palette(palette_path)
    #pygame.display.set_palette(get_palette(PALETTE))
    font=pygame.font.SysFont('Arial', 20)
    frames=load_RE(RE,IDE,PALETTE)
    sequences, sequences_frames=load_SEQ(SEQ)
    sequences_numbers=[]
    for number in sequences:
        sequences_numbers.append(number)
    sequences_numbers_index=0
    sequences_numbers_lenth=len(sequences_numbers)-1
    sequence_number=sequences_numbers[sequences_numbers_index]
    sequence=sequences[sequence_number]
    sequence_index=0
    sequence_frame=sequences_frames[sequence[sequence_index]]
    frame=frames[sequence_frame['Image_number']]
    image=frame['image']
    anim_time=0
    max_anim_time=2
    image_axis_pos=[200,400]
    image_pos=[0,0]
    change_image=True

    #pygame.key.set_repeat(400, 30)

    while True:

        #loop speed limitation
        #30 frames per second is enought
        clock.tick(30)

        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                 sequences_numbers_index+=1
                 if sequences_numbers_index>sequences_numbers_lenth:
                    sequences_numbers_index=0
                 sequence_number=sequences_numbers[sequences_numbers_index]
                 sequence=sequences[sequence_number]
                 sequence_index=0
                 anim_time=max_anim_time
                 change_image=True
                elif event.key == K_LEFT:
                 sequences_numbers_index-=1
                 if sequences_numbers_index<0:
                    sequences_numbers_index=sequences_numbers_lenth
                 sequence_number=sequences_numbers[sequences_numbers_index]
                 sequence=sequences[sequence_number]
                 sequence_index=0
                 anim_time=max_anim_time
                 change_image=True

        anim_time+=1
        if anim_time>=max_anim_time:
           anim_time=0
           sequence_index+=1
           if sequence[sequence_index]==-1:
              #print(sequence[sequence_index+1])
              sequence=sequences[sequence[sequence_index+1]]
              sequence_index=0
           sequence_frame=sequences_frames[sequence[sequence_index]]
           frame=frames[sequence_frame['Image_number']]
           image=frame['image']
           change_image=True

        if change_image:
           change_image=False
           image_width=image.get_width()
           image_height=image.get_height()
           image_scaled_size=(image_width*SCALE,image_height*SCALE)
           scaled_image=pygame.transform.scale(image,image_scaled_size).convert()
           x_axis=frame['x_axis_shift']*SCALE
           y_axis=frame['y_axis_shift']*SCALE
           image_pos=[x_axis+image_axis_pos[0],y_axis+image_axis_pos[1]]
           screen.fill((255,255,255))
           screen.blit(scaled_image,image_pos)
           text=font.render(str(sequences_numbers_index)+' '+'/'+str(sequences_numbers_lenth), True, (250,0,0))
           screen.blit(text,(420,320))
           text=font.render(str(sequence_number)+' '+str(sequence[sequence_index]), True, (250,0,0))
           screen.blit(text,(420,340))
           text=font.render(frame['name'], True, (250,0,0))
           screen.blit(text,(420,360))
           pygame.display.flip()

#read_SEQ(RE,IDE,SEQ)


def read_R(R,ID):
    screen = pygame.display.set_mode((640, 480))#,0,8)
    clock=pygame.time.Clock()
    PALETTE=get_palette(palette_path)
    #pygame.display.set_palette(get_palette(PALETTE))
    font=pygame.font.SysFont('Arial', 20)
    images=load_R(R,ID,PALETTE)
    images_lenth=len(images)-1
    change_image=True
    image_index=0
    image=images[image_index]
    image_pos=[50,50]

    pygame.key.set_repeat(400, 30)

    while True:

        #loop speed limitation
        #30 frames per second is enought
        clock.tick(30)

        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                 image_index+=1
                 if image_index>images_lenth:
                    image_index=0
                 image=images[image_index]
                 change_image=True
                elif event.key == K_LEFT:
                 image_index-=1
                 if image_index<0:
                    image_index=images_lenth
                 image=images[image_index]
                 change_image=True

        if change_image:
           change_image=False
           image_scaled_size=(image['width']*SCALE,image['height']*SCALE)
           scaled_image=pygame.transform.scale(image['image'],image_scaled_size).convert()
           screen.fill((255,255,255))
           screen.blit(scaled_image,image_pos)

           #rect=[image_pos[0],image_pos[1],image['width']*SCALE,image['height']*SCALE]
           #pygame.draw.rect(screen, (255,0,0), rect,5)
           text=font.render(str(image_index)+' '+'/'+str(images_lenth), True, (250,0,0))
           screen.blit(text,(50,250))
           text=font.render(image['name'], True, (250,0,0))
           screen.blit(text,(50,270))
           pygame.display.flip()

#read_R(R,ID)


def sound_test():
    screen = pygame.display.set_mode((640, 480))
    clock=pygame.time.Clock()
    font=pygame.font.SysFont('Arial', 20)
    update = True
    sound_files = []
    sound_files_index = 0
    voc_length = 0
    mdi_length = 0
    message = font.render('Sound Test', True, RED)
    message_time = 50
    
    for file in os.listdir(sfibm_path):
        if file[-3:] in ('VOC','MDI'):
           sound_files.append(file)
           if file[-3:] == 'VOC':
              voc_length += 1
           elif file[-3:] == 'MDI':
              mdi_length += 1              
    sound_files_length = len(sound_files)-1
    
    pygame.key.set_repeat(400, 30)

    while True:

        #loop speed limitation
        #30 frames per second is enought
        clock.tick(30)
        
        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                  pygame.quit()
                  sys.exit()
               if event.key == K_RIGHT:
                  sound_files_index += 1
                  if sound_files_index > sound_files_length:
                     sound_files_index = 0
                  update = True   
               elif event.key == K_LEFT:
                  sound_files_index -= 1
                  if sound_files_index < 0:
                     sound_files_index = sound_files_length
                  update = True
               elif event.key == K_RETURN:
                  sound_file = sound_files[sound_files_index]
                  try:
                      if sound_file[-3:] == 'VOC':
                         pygame.mixer.stop()
                         pygame.mixer.music.stop()
                         sound = pygame.mixer.Sound(sfibm_path+sound_file)
                         sound.play()
                      elif sound_file[-3:] == 'MDI':
                          pygame.mixer.stop()
                          pygame.mixer.music.stop()
                          pygame.mixer.music.load(sfibm_path+sound_file)
                          pygame.mixer.music.play()
                  except pygame.error:
                      message = font.render(sound_file +'  Not Working', True, RED)
                      message_time = 50
                      update = True
               elif event.key == K_SPACE:
                  pygame.mixer.stop()
                  pygame.mixer.music.stop()

                  
        if update:
           update = False
           screen.fill(WHITE)
           text=font.render(str(voc_length)+' VOC', True, RED)
           screen.blit(text,(280,160))
           text=font.render(str(mdi_length)+' MDI', True, RED)
           screen.blit(text,(280,190))           
           text=font.render(str(sound_files_index)+' /'+str(sound_files_length), True, RED)
           screen.blit(text,(280,240))
           text=font.render(sound_files[sound_files_index], True, RED)
           screen.blit(text,(280,260))
           if message_time > 0:
              message_time -=1
              screen.blit(message,(280,300))
              update = True
           pygame.display.flip()

#sound_test()


def test_character(RE,IDE,SEQ,KEY):
    screen = pygame.display.set_mode((640, 480))#,0,8)
    clock=pygame.time.Clock()
    PALETTE=get_palette(palette_path)
    #pygame.display.set_palette(get_palette(PALETTE))
    font=pygame.font.SysFont('Arial', 20)
    sprites=load_RE(RE,IDE,PALETTE)
    sequences, sequences_frames=load_SEQ(SEQ)
    super_moves,throws,close_range=load_KEY(KEY)
    sequences_numbers=[]
    for number in sequences:
        sequences_numbers.append(number)
    sequences_list_indexes={}
    for i in range(len(sequences_numbers)):
        sequences_list_indexes[sequences_numbers[i]]=i

    sequences_numbers_index=0
    sequences_numbers_lenth=len(sequences_numbers)-1
    sequence_number=sequences_numbers[sequences_numbers_index]
    current_sequence=sequences[sequence_number]
    sequence_index=0
    current_sequence_frame=sequences_frames[current_sequence[sequence_index]]
    current_sprite=sprites[current_sequence_frame['Image_number']]
    image=current_sprite['image']
    anim_time=0
    max_anim_time=2
    floor_y_pos=400
    axis_pos=[200,400]
    image_pos=[0,0]
    change_image=True

    up=False
    down=False
    forward=False
    backward=False
    punch1=False
    punch2=False
    punch3=False
    kick1=False
    kick2=False
    kick3=False
    FORWARD=K_RIGHT
    BACKWARD=K_LEFT
    UP=K_UP
    DOWN=K_DOWN
    PUNCH1=K_a
    PUNCH2=K_s
    PUNCH3=K_d
    KICK1=K_z
    KICK2=K_x
    KICK3=K_c
    SPECIAL=K_v

    state='stand'
    jump_sequence=None
    jump_sequence_frame=None
    jump_sequence_index=0
    jump_forward=False
    jump_back=False
    attack=False

    projectile_active=False
    projectile_axis_pos=[0,0]
    projectile_sequence=None
    projectile_sequence_index=0
    projectile_sequence_frame=None
    projectile_sprite=None
    projectile_image=None
    projectile_scaled_image=None
    projectile_image_pos=[0,0]

    command_buffer=''
    command_buffer_size=0
    command_buffer_max_size=50
    command_time=0
    command_max_time=5
    command_active=False

    #pygame.key.set_repeat(400, 30)

    while True:

        #loop speed limitation
        #30 frames per second is enought
        clock.tick(30)

        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
               if event.key == PUNCH1:
                  command_buffer+='1'
                  command_buffer_size+=1
                  command_time=0
                  command_active=True
                  if state=='stand':
                     if current_sequence_frame['cancel_mode']==7 \
                     or current_sequence_frame['cancel_mode']==2:
                        current_sequence=sequences[14]
                        attack=True
                        sequence_index=-1
                        anim_time=0
                        sequence_number=14
                  elif state=='crouch':
                     if current_sequence_frame['cancel_mode']==7 \
                     or current_sequence_frame['cancel_mode']==2:
                        current_sequence=sequences[38]
                        sequence_index=-1
                        anim_time=0
                        sequence_number=38
                  elif state=='jump':
                     if not jump_sequence:
                        if current_sequence_frame['cancel_mode']==7 \
                        or current_sequence_frame['cancel_mode']==2:
                           jump_sequence=sequences[26]
                           jump_sequence_index=0
                           if jump_forward or jump_back:
                              jump_sequence=sequences[32]

               elif event.key == PUNCH2:
                  command_buffer+='2'
                  command_buffer_size+=1
                  command_time=0
                  command_active=True
                  if state=='stand':
                     if current_sequence_frame['cancel_mode']==7 \
                     or current_sequence_frame['cancel_mode']==2:
                        current_sequence=sequences[15]
                        attack=True
                        sequence_index=-1
                        anim_time=0
                        sequence_number=15
                  elif state=='crouch':
                     if current_sequence_frame['cancel_mode']==7 \
                     or current_sequence_frame['cancel_mode']==2:
                        current_sequence=sequences[39]
                        sequence_index=-1
                        anim_time=0
                        sequence_number=39
                  elif state=='jump':
                     if not jump_sequence:
                        if current_sequence_frame['cancel_mode']==7 \
                        or current_sequence_frame['cancel_mode']==2:
                           jump_sequence=sequences[27]
                           jump_sequence_index=0
                           if jump_forward or jump_back:
                              jump_sequence=sequences[33]

               elif event.key == PUNCH3:
                  command_buffer+='3'
                  command_buffer_size+=1
                  command_time=0
                  command_active=True
                  if state=='stand':
                     if current_sequence_frame['cancel_mode']==7 \
                     or current_sequence_frame['cancel_mode']==2:
                        current_sequence=sequences[16]
                        attack=True
                        sequence_index=-1
                        anim_time=0
                        sequence_number=16
                  elif state=='crouch':
                     if current_sequence_frame['cancel_mode']==7 \
                     or current_sequence_frame['cancel_mode']==2:
                        current_sequence=sequences[40]
                        sequence_index=-1
                        anim_time=0
                        sequence_number=40
                  elif state=='jump':
                     if not jump_sequence:
                        if current_sequence_frame['cancel_mode']==7 \
                        or current_sequence_frame['cancel_mode']==2:
                           jump_sequence=sequences[28]
                           jump_sequence_index=0
                           if jump_forward or jump_back:
                              jump_sequence=sequences[34]

               elif event.key == KICK1:
                  command_buffer+='4'
                  command_buffer_size+=1
                  command_time=0
                  command_active=True
                  if state=='stand':
                     if current_sequence_frame['cancel_mode']==7 \
                     or current_sequence_frame['cancel_mode']==2:
                        current_sequence=sequences[11]
                        attack=True
                        sequence_index=-1
                        anim_time=0
                        sequence_number=11
                  elif state=='crouch':
                     if current_sequence_frame['cancel_mode']==7 \
                     or current_sequence_frame['cancel_mode']==2:
                        current_sequence=sequences[35]
                        sequence_index=-1
                        anim_time=0
                        sequence_number=35
                  elif state=='jump':
                     if not jump_sequence:
                        if current_sequence_frame['cancel_mode']==7 \
                        or current_sequence_frame['cancel_mode']==2:
                           jump_sequence=sequences[23]
                           jump_sequence_index=0
                           if jump_forward or jump_back:
                              jump_sequence=sequences[29]

               elif event.key == KICK2:
                  command_buffer+='5'
                  command_buffer_size+=1
                  command_time=0
                  command_active=True
                  if state=='stand':
                     if current_sequence_frame['cancel_mode']==7 \
                     or current_sequence_frame['cancel_mode']==2:
                        current_sequence=sequences[12]
                        attack=True
                        sequence_index=-1
                        anim_time=0
                        sequence_number=12
                  elif state=='crouch':
                     if current_sequence_frame['cancel_mode']==7 \
                     or current_sequence_frame['cancel_mode']==2:
                        current_sequence=sequences[36]
                        sequence_index=-1
                        anim_time=0
                        sequence_number=36
                  elif state=='jump':
                     if not jump_sequence:
                        if current_sequence_frame['cancel_mode']==7 \
                        or current_sequence_frame['cancel_mode']==2:
                           jump_sequence=sequences[24]
                           jump_sequence_index=0
                           if jump_forward or jump_back:
                              jump_sequence=sequences[30]

               elif event.key == KICK3:
                  command_buffer+='6'
                  command_buffer_size+=1
                  command_time=0
                  command_active=True
                  if state=='stand':
                     if current_sequence_frame['cancel_mode']==7 \
                     or current_sequence_frame['cancel_mode']==2:
                        current_sequence=sequences[13]
                        attack=True
                        sequence_index=-1
                        anim_time=0
                        sequence_number=12
                  elif state=='crouch':
                     if current_sequence_frame['cancel_mode']==7 \
                     or current_sequence_frame['cancel_mode']==2:
                        current_sequence=sequences[37]
                        sequence_index=-1
                        anim_time=0
                        sequence_number=37
                  elif state=='jump':
                     if not jump_sequence:
                        if current_sequence_frame['cancel_mode']==7 \
                        or current_sequence_frame['cancel_mode']==2:
                           jump_sequence=sequences[25]
                           jump_sequence_index=0
                           if jump_forward or jump_back:
                              jump_sequence=sequences[31]

               elif event.key == SPECIAL:
                    if state!='jump':
                       if current_sequence_frame['cancel_mode'] > 0 \
                       and current_sequence_frame['cancel_mode']< 8:
                          current_sequence=sequences[47]
                          attack=True
                          sequence_index=-1
                          anim_time=0
                          sequence_number=47


            if event.type == KEYUP:
                if event.key == FORWARD:
                   if forward:
                      forward=False
                      if current_sequence_frame['cancel_mode']==7:
                         current_sequence=sequences[0]
                         sequence_index=-1
                         anim_time=0
                         sequence_number=0
                         if state =='crouch':
                            current_sequence=sequences[2]
                            sequence_number=2
                elif event.key == BACKWARD:
                   if backward:
                      backward=False
                      if current_sequence_frame['cancel_mode']==7:
                         current_sequence=sequences[0]
                         sequence_index=-1
                         anim_time=0
                         sequence_number=0
                         if state =='crouch':
                            current_sequence=sequences[2]
                            sequence_number=2
                if event.key == UP:
                   if up:
                      up=False
                      if forward:
                         forward=False
                      elif backward:
                         backward=False
                elif event.key == DOWN:
                   if down:
                      down=False
                      if current_sequence_frame['cancel_mode']==7:
                         current_sequence=sequences[0]
                         state='stand'
                         sequence_index=-1
                         anim_time=0
                         sequence_number=0
                         if forward:
                            forward=False
                         elif backward:
                            backward=False



        #Movement controls
        keys = pygame.key.get_pressed()
        if keys[FORWARD]:
           if not (forward or backward or up):
              command_buffer+='f'
              command_buffer_size+=1
              command_time=0
              command_active=True
              #forward=True
              if current_sequence_frame['cancel_mode']==7:
                 forward=True
                 current_sequence=sequences[6]
                 sequence_index=-1
                 anim_time=0
                 sequence_number=6
                 if down:
                    current_sequence=sequences[8]
                    sequence_number=8
                    state='crouch'
        elif keys[BACKWARD]:
           if not (backward or forward or up):
              command_buffer+='b'
              command_buffer_size+=1
              command_time=0
              command_active=True
              if current_sequence_frame['cancel_mode']==7:
                 backward=True
                 current_sequence=sequences[3]
                 sequence_index=-1
                 anim_time=0
                 sequence_number=3
                 if down:
                    current_sequence=sequences[5]
                    sequence_number=5
                    state='crouch'
        if keys[UP]:
           if not(up or down):
              command_buffer+='u'
              command_buffer_size+=1
              command_time=0
              command_active=True
              if current_sequence_frame['cancel_mode']==7:
                 up=True
                 current_sequence=sequences[1]
                 state='jump'
                 sequence_index=-1
                 anim_time=max_anim_time#0
                 sequence_number=1
                 if forward:
                    current_sequence=sequences[7]
                    jump_forward=True
                    sequence_number=7
                 elif backward:
                    current_sequence=sequences[4]
                    jump_back=True
                    sequence_number=4
        elif keys[DOWN]:
           if not down:
              command_buffer+='d'
              command_buffer_size+=1
              command_time=0
              command_active=True
              if current_sequence_frame['cancel_mode']==7:
                 down=True
                 current_sequence=sequences[2]
                 state='crouch'
                 sequence_index=-1
                 anim_time=0
                 sequence_number=2
                 if backward:
                    current_sequence=sequences[5]
                    sequence_number=5
                 if forward:
                    current_sequence=sequences[8]
                    sequence_number=8


        if command_active:
           if (state!='jump' or sequence_index<1) and command_time==0:
              for move in super_moves:
                 if command_buffer[-move['inputs_lenth']:]==move['inputs']:
                    if current_sequence_frame['cancel_mode'] > 0 \
                    and current_sequence_frame['cancel_mode']< 8:
                        current_sequence=sequences[move['sequence']]
                        attack=True
                        jump_sequence=None
                        sequence_index=-1
                        anim_time=max_anim_time
                        sequence_number=move['sequence']
                        command_buffer=''
                        command_active=False
                        command_time=0
                        break
           #print(command_buffer)
           command_time+=1
           if command_time > command_max_time:
             command_buffer=''
             command_active=False
             command_time=0
           if command_buffer_size > command_buffer_max_size:
              command_buffer=''
              command_buffer_size=0



        anim_time+=1
        if anim_time>=max_anim_time:
           anim_time=0
           sequence_index+=1
           if current_sequence[sequence_index]==-1:
              current_sequence=sequences[current_sequence[sequence_index+1]]
              sequence_index=0
              if state=='jump':
                 state='stand'
                 jump_forward=False
                 jump_back=False
                 up=False
                 if jump_sequence:
                    jump_sequence=None
                    jump_sequence_frame=None
                    jump_sequence_index=0
              if axis_pos[1]!=floor_y_pos:
                 axis_pos[1]=floor_y_pos
              if attack:
                 attack=False
                 forward=False
                 backward=False
              if state=='crouch'  and not down:
                 if current_sequence_frame['cancel_mode']==7:
                    current_sequence=sequences[0]
                    state='stand'
                    sequence_index=-1
                    anim_time=0
                    sequence_number=0
           current_sequence_frame=sequences_frames[current_sequence[sequence_index]]
           axis_pos[0]+=current_sequence_frame['x_movement']*SCALE
           axis_pos[1]+=current_sequence_frame['y_movement']*SCALE
           current_sprite=sprites[current_sequence_frame['Image_number']]
           image=current_sprite['image']
           if projectile_active:
              projectile_sequence_index+=1
              if projectile_sequence[projectile_sequence_index]==-1:
                 if projectile_sequence[projectile_sequence_index+1]!=253:
                    projectile_sequence=sequences[projectile_sequence[projectile_sequence_index+1]]
                    projectile_sequence_index=0
                 else:
                    projectile_active=False
                    projectile_sequence_index-=1
              projectile_sequence_frame=sequences_frames[projectile_sequence[projectile_sequence_index]]
              projectile_sprite=sprites[projectile_sequence_frame['Image_number']]
              projectile_image=projectile_sprite['image']
              projectile_axis_pos[0]+=projectile_sequence_frame['x_movement']*SCALE
              projectile_axis_pos[1]+=projectile_sequence_frame['y_movement']*SCALE
              projectile_image_pos[0]=projectile_axis_pos[0]+projectile_sprite['x_axis_shift']*SCALE
              projectile_image_pos[1]=projectile_axis_pos[1]+projectile_sprite['y_axis_shift']*SCALE
              if projectile_image_pos[0]>640:
                 projectile_active=False
           if current_sequence_frame['frame_type']=='F':
              if current_sequence_frame['hit_damage']>3:
                 if not (projectile_active and projectile_sequence_frame['cancel_mode']==0):
                    projectile_active=True
                    projectile_sequence=sequences[current_sequence[sequence_index+1]]
                    projectile_sequence_index=0
                    projectile_sequence_frame=sequences_frames[projectile_sequence[projectile_sequence_index]]
                    projectile_sprite=sprites[projectile_sequence_frame['Image_number']]
                    projectile_image=projectile_sprite['image']
                    projectile_axis_pos[0]=axis_pos[0]+projectile_sequence_frame['x_movement']*SCALE
                    projectile_axis_pos[1]=axis_pos[1]+projectile_sequence_frame['y_movement']*SCALE
                    projectile_image_pos[0]=projectile_axis_pos[0]+projectile_sprite['x_axis_shift']*SCALE
                    projectile_image_pos[1]=projectile_axis_pos[1]+projectile_sprite['y_axis_shift']*SCALE
                 sequence_index+=1
           if jump_sequence:
              if jump_sequence[jump_sequence_index]==-1:
                 jump_sequence=None
                 jump_sequence_frame=None
                 jump_sequence_index=0
              else:
                 jump_sequence_frame=sequences_frames[jump_sequence[jump_sequence_index]]
                 current_sprite=sprites[jump_sequence_frame['Image_number']]
                 image=current_sprite['image']
                 jump_sequence_index+=1
           change_image=True

        if change_image:
           change_image=False
           image_width=image.get_width()
           image_height=image.get_height()
           image_scaled_size=(image_width*SCALE,image_height*SCALE)
           scaled_image=pygame.transform.scale(image,image_scaled_size)
           x_axis_shift=current_sprite['x_axis_shift']*SCALE
           y_axis_shift=current_sprite['y_axis_shift']*SCALE
           image_pos=[axis_pos[0]+x_axis_shift, axis_pos[1]+y_axis_shift]
           screen.fill((255,255,255))
           if current_sequence_frame['frame_orientation']=='N':
              screen.blit(scaled_image,image_pos)
           elif current_sequence_frame['frame_orientation']=='U':
              flipped_image=pygame.transform.flip(scaled_image, False, True)
              screen.blit(flipped_image,image_pos)
           elif current_sequence_frame['frame_orientation']=='F':
              flipped_image=pygame.transform.flip(scaled_image, True, False)
              screen.blit(flipped_image,image_pos)
           elif current_sequence_frame['frame_orientation']=='R':
              flipped_image=pygame.transform.flip(scaled_image, True, True)
              screen.blit(flipped_image,image_pos)
           if current_sprite['second_image']:
              image=current_sprite['second_image']['image']
              image_width=image.get_width()
              image_height=image.get_height()
              image_scaled_size=(image_width*SCALE,image_height*SCALE)
              image=pygame.transform.scale(image,image_scaled_size)
              x_axis_shift=current_sprite['second_image']['x_axis_shift']*SCALE
              y_axis_shift=current_sprite['second_image']['y_axis_shift']*SCALE
              image_pos=[axis_pos[0]+x_axis_shift, axis_pos[1]+y_axis_shift]
              screen.blit(image,image_pos)
           if projectile_active:
              image_width=projectile_image.get_width()
              image_height=projectile_image.get_height()
              image_scaled_size=(image_width*SCALE,image_height*SCALE)
              projectile_scaled_image=pygame.transform.scale(projectile_image,image_scaled_size).convert()
              if projectile_sequence_frame['frame_orientation']=='N':
                 screen.blit(projectile_scaled_image,projectile_image_pos)
              elif projectile_sequence_frame['frame_orientation']=='U':
                 flipped_image=pygame.transform.flip(projectile_scaled_image, False, True)
                 screen.blit(flipped_image,projectile_image_pos)
              elif projectile_sequence_frame['frame_orientation']=='F':
                 flipped_image=pygame.transform.flip(projectile_scaled_image, True, False)
                 screen.blit(flipped_image,projectile_image_pos)
              elif projectile_sequence_frame['frame_orientation']=='R':
                 flipped_image=pygame.transform.flip(projectile_scaled_image, True, True)
                 screen.blit(flipped_image,projectile_image_pos)
           text=font.render(str(sequences_list_indexes[sequence_number])+' '+'/'+str(sequences_numbers_lenth), True, (250,0,0))
           screen.blit(text,(420,320))
           text=font.render(str(sequence_number)+' '+str(current_sequence[sequence_index]), True, (250,0,0))
           screen.blit(text,(420,340))
           text=font.render(current_sprite['name'], True, (250,0,0))
           screen.blit(text,(420,360))
           pygame.display.flip()

#test_character(RE,IDE,SEQ,KEY)



class Character:
    def __init__(self,sprites,sequences,sequences_frames,controls,super_moves,throws,close_range,axis_pos,side):
        self.sprites=sprites
        self.left_side_sprites=sprites
        self.right_side_sprites=self.get_right_side_sprites(sprites)
        self.sequences=sequences
        self.sequences_frames=sequences_frames
        self.left_side_sequences_frames=sequences_frames
        self.right_side_sequences_frames=self.get_right_side_sequences_frames(sequences_frames)
        self.side=side
        self.super_moves=super_moves
        self.throws=throws
        self.get_throws()
        self.close_range=close_range

        self.current_sequence=self.sequences[0]
        self.sequence_index=0
        self.current_sequence_frame=self.sequences_frames[self.current_sequence[self.sequence_index]]
        self.current_sprite=self.sprites[self.current_sequence_frame['Image_number']]
        self.image=self.current_sprite['image']
        self.image_orientation = self.current_sequence_frame['frame_orientation']
        self.anim_time=2
        self.max_anim_time=2
        self.axis_pos=axis_pos
        self.image_pos=[
        self.axis_pos[0]+self.current_sprite['x_axis_shift'],
        self.axis_pos[1]+self.current_sprite['y_axis_shift']]
        self.opponent = None
        self.ai = None

        self.up=False
        self.down=False
        self.forward=False
        self.backward=False
        self.punch1=False
        self.punch2=False
        self.punch3=False
        self.kick1=False
        self.kick2=False
        self.kick3=False
        self.speciale=self.super_moves[
        random.randint(0,len(super_moves)-1)]['sequence']
        self.FORWARD=controls['FORWARD']
        self.BACKWARD=controls['BACKWARD']
        self.UP=controls['UP']
        self.DOWN=controls['DOWN']
        self.PUNCH1=controls['PUNCH1']
        self.PUNCH2=controls['PUNCH2']
        self.PUNCH3=controls['PUNCH3']
        self.KICK1=controls['KICK1']
        self.KICK2=controls['KICK2']
        self.KICK3=controls['KICK3']
        self.SPECIAL=controls['SPECIAL']

        self.state='stand'
        self.jump_sequence=None
        self.jump_sequence_frame=None
        self.jump_sequence_index=0
        self.jump_forward=False
        self.jump_back=False
        self.move=False
        self.hitted=False
        self.guard=False
        self.guard_hitted = False
        self.health = 100
        self.updated_health = 100
        self.knocked_out=False
        self.victory=False
        self.get_jump_hit_reaction_pos()

        self.projectile_active=False
        self.projectile_collided=False
        self.projectile_axis_pos=[0,0]
        self.projectile_sequence=None
        self.projectile_sequence_index=0
        self.projectile_sequence_frame=None
        self.projectile_sprite=None
        self.projectile_image=None
        self.projectile_scaled_image=None
        self.projectile_image_pos=[0,0]

        self.command_buffer=''
        self.command_buffer_size=0
        self.command_buffer_max_size=16
        self.command_time=0
        self.command_max_time=10
        self.command_active=False

        if self.side=='right':
           self.side='left'
           self.switch_side()
           self.current_sprite=self.sprites[self.current_sequence_frame['Image_number']]
           self.image=self.current_sprite['image']
           #self.image_pos=[
           #self.axis_pos[0]+self.current_sprite['x_axis_shift'],
           #self.axis_pos[1]+self.current_sprite['y_axis_shift']]

    def get_right_side_sprites(self,sprites):
        left_side_sprites=[]
        for sprite in sprites:
            left_side_sprite={
            'name':sprite['name'],
            'x_axis_shift':-(sprite['image_size'][0]+sprite['x_axis_shift']),
            'y_axis_shift':sprite['y_axis_shift'],
            'image':pygame.transform.flip(sprite['image'], True, False),
            'collision_box':sprite['collision_box'],
            'second_image':sprite['second_image'],
            'image_size':sprite['image_size']}
            if sprite['collision_box']!=[0,0,0,0]:
               collision=sprite['collision_box']
               image_width=sprite['image_size'][0]
               left_side_collision=[image_width-(collision[0]+collision[2]),
                                    collision[1],collision[2],collision[3]]
               left_side_sprite['collision_box']=left_side_collision
            if sprite['second_image']:
               second_image={
               'name':sprite['second_image']['name'],
               'x_axis_shift':-(sprite['second_image']['image_size'][0]+sprite['second_image']['x_axis_shift']),
               'y_axis_shift':sprite['second_image']['y_axis_shift'],
               'image':pygame.transform.flip(sprite['second_image']['image'], True, False),
               'collision_box':sprite['second_image']['collision_box'],
               'image_size':sprite['second_image']['image_size']}
               left_side_sprite['second_image']=second_image
            left_side_sprites.append(left_side_sprite)
        return left_side_sprites

    def get_right_side_sequences_frames(self,sequences_frames):
        left_side_sequences_frames={}
        for sequence_frame in sequences_frames:
            seq_frame=sequences_frames[sequence_frame]
            left_side_sequences_frames[sequence_frame]={'Image_number':seq_frame['Image_number'],
                 'x_movement':-seq_frame['x_movement'], 'y_movement':seq_frame['y_movement'],
                 'frame_type':seq_frame['frame_type'], 'hit_damage':seq_frame['hit_damage'],
                 'hit_reaction':seq_frame['hit_reaction'], 'frame_orientation':seq_frame['frame_orientation'],
                 'cancel_mode':seq_frame['cancel_mode'], 'attack_mode':seq_frame['attack_mode'],
                 'invincible':seq_frame['invincible']}
        return left_side_sequences_frames

    def switch_side(self):
        if self.side=='left':
           self.side='right'
           self.sprites=self.right_side_sprites
           #self.current_sprite=self.sprites[self.current_sequence_frame['Image_number']]
           #self.image=self.current_sprite['image']
           self.sequences_frames=self.right_side_sequences_frames
           self.FORWARD,self.BACKWARD=self.BACKWARD,self.FORWARD
           self.forward = False
           self.backward = False
           if self.projectile_active:
              self.projectile_active=False
        elif self.side=='right':
           self.side='left'
           self.sprites=self.left_side_sprites
           #self.current_sprite=self.sprites[self.current_sequence_frame['Image_number']]
           #self.image=self.current_sprite['image']
           self.sequences_frames=self.left_side_sequences_frames
           self.FORWARD,self.BACKWARD=self.BACKWARD,self.FORWARD
           self.forward = False
           self.backward = False
           if self.projectile_active:
              self.projectile_active=False

    def get_throws(self):
        normal_throws={
        'punch1':[],'punch2':[],'punch3':[],
        'kick1':[],'kick2':[],'kick3':[]}
        jump_throws={
        'punch1':[],'punch2':[],'punch3':[],
        'kick1':[],'kick2':[],'kick3':[]}
        for throw in self.throws:
            if throw['throw_height']==1:
               if throw['button_held']==1:
                  normal_throws['kick1'].append(throw)
               elif throw['button_held']==2:
                  normal_throws['kick2'].append(throw)
               elif throw['button_held']==3:
                  normal_throws['kick3'].append(throw)
               elif throw['button_held']==4:
                  normal_throws['punch1'].append(throw)
               elif throw['button_held']==5:
                  normal_throws['punch2'].append(throw)
               elif throw['button_held']==6:
                  normal_throws['punch3'].append(throw)
            elif throw['throw_height']==2:
               if throw['button_held']==1:
                  jump_throws['kick1'].append(throw)
               elif throw['button_held']==2:
                  jump_throws['kick2'].append(throw)
               elif throw['button_held']==3:
                  jump_throws['kick3'].append(throw)
               elif throw['button_held']==4:
                  jump_throws['punch1'].append(throw)
               elif throw['button_held']==5:
                  jump_throws['punch2'].append(throw)
               elif throw['button_held']==6:
                  jump_throws['punch3'].append(throw)
        self.normal_throws=normal_throws
        self.jump_throws=jump_throws

    def handle_normal_throws(self,button_held):
        if self.opponent.current_sequence_frame['frame_type']=='M':
           for throw in self.normal_throws[button_held]:
               if self.side=='left':
                  if throw['direction_held']==3 and self.backward \
                  or throw['direction_held']== 6 and self.forward \
                  or throw['direction_held']== 0 \
                  or throw['direction_held']== 2 and self.down \
                  or throw['direction_held']== 1 and self.up \
                  or throw['direction_held']== 4 and (self.up and self.backward) \
                  or throw['direction_held']== 5 and (self.down and self.backward) \
                  or throw['direction_held']== 7 and (self.up and self.forward) \
                  or throw['direction_held']== 8 and (self.down and self.forward):
                     self.handle_throw_slam_direction(throw)
                     self.opponent.health-=health_damage[throw['damage']]
                     if self.opponent.health<0:
                        self.opponent.health=0
                        self.opponent.knocked_out=True
                        self.victory=True
                        pygame.mixer.stop()
                        self.opponent.ko_sound.play()
                     break
               elif self.side=='right':
                  if throw['direction_held']==3 and self.forward \
                  or throw['direction_held']== 6 and self.backward \
                  or throw['direction_held']== 0 \
                  or throw['direction_held']== 2 and self.down \
                  or throw['direction_held']== 1 and self.up \
                  or throw['direction_held']== 4 and (self.up and self.forward) \
                  or throw['direction_held']== 5 and (self.down and self.forward) \
                  or throw['direction_held']== 7 and (self.up and self.backward) \
                  or throw['direction_held']== 8 and (self.down and self.backward):
                     self.handle_throw_slam_direction(throw)
                     self.opponent.health-=health_damage[throw['damage']]
                     if self.opponent.health<0:
                        self.opponent.health=0
                        self.opponent.knocked_out=True
                        self.victory=True
                        pygame.mixer.stop()
                        self.opponent.ko_sound.play()
                     break

    def handle_jump_throws(self,button_held):
        if self.opponent.current_sequence_frame['frame_type']=='M':
           for throw in self.jump_throws[button_held]:
               if self.side=='left':
                  if throw['direction_held']==3 and self.backward \
                  or throw['direction_held']== 6 and self.forward \
                  or throw['direction_held']== 0 \
                  or throw['direction_held']== 2 and self.down \
                  or throw['direction_held']== 1 and self.up \
                  or throw['direction_held']== 4 and (self.up and self.backward) \
                  or throw['direction_held']== 5 and (self.down and self.backward) \
                  or throw['direction_held']== 7 and (self.up and self.forward) \
                  or throw['direction_held']== 8 and (self.down and self.forward):
                     self.axis_pos[1]=105
                     self.opponent.axis_pos[1]=105
                     self.handle_throw_slam_direction(throw)
                     self.opponent.health-=health_damage[throw['damage']]
                     if self.opponent.health<0:
                        self.opponent.health=0
                        self.opponent.knocked_out=True
                        self.victory=True
                        pygame.mixer.stop()
                        self.opponent.ko_sound.play()
                     break
               elif self.side=='right':
                  if throw['direction_held']==3 and self.forward \
                  or throw['direction_held']== 6 and self.backward \
                  or throw['direction_held']== 0 \
                  or throw['direction_held']== 2 and self.down \
                  or throw['direction_held']== 1 and self.up \
                  or throw['direction_held']== 4 and (self.up and self.forward) \
                  or throw['direction_held']== 5 and (self.down and self.forward) \
                  or throw['direction_held']== 7 and (self.up and self.backward) \
                  or throw['direction_held']== 8 and (self.down and self.backward):
                     self.axis_pos[1]=105
                     self.opponent.axis_pos[1]=105
                     self.handle_throw_slam_direction(throw)
                     self.opponent.health-=health_damage[throw['damage']]
                     if self.opponent.health<0:
                        self.opponent.health=0
                        self.opponent.knocked_out=True
                        self.victory=True
                        pygame.mixer.stop()
                        self.opponent.ko_sound.play()
                     break

    def handle_throw_slam_direction(self,throw):
        opponent=self.opponent
        if throw['slam_direction']==0:
           if opponent.side=='right':
              opponent.axis_pos[0]=self.axis_pos[0]+20
           elif opponent.side=='left':
              opponent.axis_pos[0]=self.axis_pos[0]-20
        elif throw['slam_direction']==1:
           if opponent.side=='right':
              opponent.axis_pos[0]=self.axis_pos[0]+20
           elif opponent.side=='left':
              self.axis_pos[0]=opponent.axis_pos[0]
              opponent.axis_pos[0]=self.axis_pos[0]+20
              self.switch_side()
              opponent.switch_side()
        elif throw['slam_direction']==2:
           if opponent.side=='right':
              self.axis_pos[0]=opponent.axis_pos[0]
              opponent.axis_pos[0]=self.axis_pos[0]-20
              self.switch_side()
              opponent.switch_side()
           elif opponent.side=='left':
              opponent.axis_pos[0]=self.axis_pos[0]-20
        elif throw['slam_direction']==3:
           if opponent.side=='right':
              opponent.axis_pos[0]=self.axis_pos[0]+20
              self.switch_side()
           elif opponent.side=='left':
              self.axis_pos[0]=opponent.axis_pos[0]
              opponent.axis_pos[0]=self.axis_pos[0]+20
              opponent.switch_side()
        elif throw['slam_direction']==4:
           if opponent.side=='right':
              self.axis_pos[0]=opponent.axis_pos[0]
              opponent.axis_pos[0]=self.axis_pos[0]-20
              opponent.switch_side()
           elif opponent.side=='left':
              opponent.axis_pos[0]=self.axis_pos[0]-20
              self.switch_side()
        self.current_sequence=self.sequences[throw['character_sequence']]
        self.current_sequence_frame=self.sequences_frames[self.current_sequence[0]]
        self.sequence_index=-1
        self.anim_time=self.max_anim_time
        opponent.current_sequence=opponent.sequences[throw['opponent_sequence']]
        opponent.current_sequence_frame=opponent.sequences_frames[opponent.current_sequence[0]]
        opponent.sequence_index=-1
        opponent.anim_time=self.anim_time
        opponent.jump_sequence = None
        opponent.hitted=True
        opponent.move=True
        throw['sound'].play()


    def handle_collision(self):
        opponent=self.opponent

        if self.current_sprite['collision_box']!=empty_box:
           temp_rect=self.current_sprite['collision_box']
           rect1=[self.image_pos[0]+temp_rect[0],
                  self.image_pos[1]+temp_rect[1],
                  temp_rect[2],temp_rect[3]]
        else:
           rect1=[self.image_pos[0],self.image_pos[1],
                  self.current_sprite['image_size'][0],
                  self.current_sprite['image_size'][1]]
        rect2=[opponent.image_pos[0],opponent.image_pos[1],
               opponent.current_sprite['image_size'][0],
               opponent.current_sprite['image_size'][1]]
        if opponent.state =='jump':
           rect2[3] -= int(rect2[3]/3)

        collision=0
        if rect1[0]+rect1[2]>=rect2[0] and rect1[0]<=rect2[0]+rect2[2] \
        and rect1[1]+rect1[3]>=rect2[1] and rect1[1]<=rect2[1]+rect2[3]:
            collision=1

        if collision:
           self_current_sequence_frame = self.current_sequence_frame
           opponent_current_sequence_frame = opponent.current_sequence_frame
           if self_current_sequence_frame['attack_mode'] in ('A','H','L'):
              if opponent_current_sequence_frame['invincible']!='A':
                 hit_reaction=self_current_sequence_frame['hit_reaction']+71
                 """if opponent_current_sequence_frame['frame_type']=='D':
                    if self_current_sequence_frame['attack_mode'] in ('A','L') \
                    and opponent_current_sequence_frame['invincible']=='H':
                        hit_reaction=67
                        opponent.guard_hitted = True
                    elif self_current_sequence_frame['attack_mode'] in ('A','H') \
                    and opponent_current_sequence_frame['invincible']=='L':
                        hit_reaction=68
                        opponent.guard_hitted = True"""
                 if opponent.guard:
                    if opponent.state=='stand' \
                    and self_current_sequence_frame['attack_mode'] in ('A','L'):
                       hit_reaction=67
                       opponent.guard_hitted = True
                       sounds[10].play()
                    elif opponent.state=='crouch' \
                    and self_current_sequence_frame['attack_mode'] in ('A','H'):
                       hit_reaction=68
                       opponent.guard_hitted = True
                       sounds[10].play()
                 else:
                    opponent.health-=health_damage[self_current_sequence_frame['hit_damage']]
                    sounds[self_current_sequence_frame['hit_damage']].play()
                    if opponent.health<0:
                       opponent.health=0
                       opponent.knocked_out=True
                       self.victory=True
                       hit_reaction=79
                       pygame.mixer.stop()
                       opponent.ko_sound.play()
                 if opponent.side == self.side:
                    opponent.switch_side()
                 opponent.current_sequence=opponent.sequences[hit_reaction]
                 opponent.current_sequence_frame=opponent.sequences_frames[opponent.current_sequence[0]]
                 opponent.sequence_index=-1
                 opponent.anim_time=self.anim_time
                 opponent.jump_sequence = None
                 opponent.hitted=True
                 opponent.move=True

                 opponent_hit_reaction_pos = opponent.axis_pos[1] + 30
                 opponent.axis_pos[1] = FLOOR_Y_POS
                 if opponent_hit_reaction_pos < FLOOR_Y_POS:
                    for i,pos in enumerate(opponent.jump_hit_reaction_pos):
                        if pos < opponent_hit_reaction_pos:
                           opponent.current_sequence = opponent.sequences[4]
                           opponent.sequence_index = i
                           opponent.axis_pos[1] = pos
                           opponent.jump_sequence=opponent.sequences[hit_reaction]
                           opponent.jump_sequence_index=0
                           opponent.state = 'jump'
                           break

           else:
              if opponent.current_sequence[-1] == 'movement_sequence':
                 rect1=[self.image_pos[0],self.image_pos[1],
                        self.current_sprite['image_size'][0],
                        self.current_sprite['image_size'][1]]
                 if rect1[0]+rect1[2]>rect2[0] and rect1[0]<rect2[0]+rect2[2] \
                 and rect1[1]+rect1[3]>rect2[1] and rect1[1]<rect2[1]+rect2[3]:
                    if attack_range<30 and self.side!=opponent.side \
                    and abs(self.axis_pos[1]-opponent.axis_pos[1])<30:
                          x_movement=opponent_current_sequence_frame['x_movement']
                          if self.side=='left' and x_movement<0 \
                          or self.side=='right' and x_movement>0:
                             self.axis_pos[0]+=x_movement
                             if self.axis_pos[0]<20 \
                             or self.axis_pos[0]>300:
                                self.axis_pos[0]-=x_movement
                                opponent.axis_pos[0]-=x_movement

                                background['pos'][0]-=x_movement
                                if background['pos'][0]>0 \
                                or background['pos'][0]+background['width']<DISPLAY_SURFACE_WIDTH:
                                   background['pos'][0]+=x_movement


        if self.projectile_active and not self.projectile_collided:
           if self.projectile_sequence_frame['attack_mode'] in ('A','H','L') \
           and opponent.current_sequence_frame['invincible']!='A':
              if self.projectile_sprite['collision_box']!=empty_box:
                 temp_rect=self.projectile_sprite['collision_box']
                 rect1=[self.projectile_image_pos[0]+temp_rect[0],
                        self.projectile_image_pos[1]+temp_rect[1],
                        temp_rect[2],temp_rect[3]]
              else:
                 rect1=[self.projectile_image_pos[0],self.projectile_image_pos[1],
                        self.projectile_sprite['image_size'][0],
                        self.projectile_sprite['image_size'][1]]
              if rect1[0]+rect1[2]>rect2[0] and rect1[0]<rect2[0]+rect2[2] \
              and rect1[1]+rect1[3]>rect2[1] and rect1[1]<rect2[1]+rect2[3]:
                 self.projectile_sequence=self.sequences[66]
                 self.projectile_sequence_index=-1
                 hit_reaction=self.projectile_sequence_frame['hit_reaction']+71
                 if opponent.guard:
                    if opponent.state=='stand' \
                    and self.projectile_sequence_frame['attack_mode'] in ('A','L'):
                       hit_reaction=67
                       sounds[10].play()
                    elif opponent.state=='crouch' \
                    and self.projectile_sequence_frame['attack_mode'] in ('A','H'):
                       hit_reaction=68
                       sounds[10].play()
                 else:
                    opponent.health-=health_damage[self.projectile_sequence_frame['hit_damage']]
                    sounds[self.projectile_sequence_frame['hit_damage']].play()
                    if opponent.health<0:
                       opponent.health=0
                       opponent.knocked_out=True
                       self.victory=True
                       hit_reaction=79
                       pygame.mixer.stop()
                       opponent.ko_sound.play()
                 if opponent.side == self.side:
                    opponent.switch_side()                       
                 opponent.current_sequence=opponent.sequences[hit_reaction]
                 opponent.current_sequence_frame=opponent.sequences_frames[opponent.current_sequence[0]]
                 opponent.sequence_index= -1
                 opponent.anim_time=self.anim_time
                 opponent.jump_sequence = None
                 opponent.hitted=True
                 opponent.move=True

                 opponent_hit_reaction_pos = opponent.axis_pos[1] + 30
                 opponent.axis_pos[1] = FLOOR_Y_POS
                 if opponent_hit_reaction_pos < FLOOR_Y_POS:
                    for i,pos in enumerate(opponent.jump_hit_reaction_pos):
                        if pos < opponent_hit_reaction_pos:
                           opponent.current_sequence = opponent.sequences[4]
                           opponent.sequence_index = i
                           opponent.axis_pos[1] = pos
                           opponent.jump_sequence=opponent.sequences[hit_reaction]
                           opponent.jump_sequence_index=0
                           opponent.state = 'jump'
                           break

              if opponent.projectile_active:
                 if opponent.projectile_sequence_frame['attack_mode'] in ('A','H','L'):
                     rect2=[opponent.projectile_image_pos[0],opponent.projectile_image_pos[1],
                            opponent.projectile_sprite['image_size'][0],
                            opponent.projectile_sprite['image_size'][1]]
                     if rect1[0]+rect1[2]>rect2[0] and rect1[0]<rect2[0]+rect2[2] \
                     and rect1[1]+rect1[3]>rect2[1] and rect1[1]<rect2[1]+rect2[3]:
                        self.projectile_sequence=self.sequences[66]
                        opponent.projectile_sequence=opponent.sequences[66]
                        self.projectile_sequence_index=-1
                        opponent.projectile_sequence_index=-1
                        opponent.anim_time=self.anim_time
                        self.projectile_collided=True
                        opponent.projectile_collided=True
                        sounds[41].play()
                        
                        
    def get_jump_hit_reaction_pos(self):
        floor_y_pos=FLOOR_Y_POS
        jump_hit_reaction_pos=[]
        for i in  range(len(self.sequences[4])):
            frame_index=self.sequences[4][i]
            if frame_index==-1:
               break
            y_movement=self.sequences_frames[frame_index]['y_movement']
            floor_y_pos+=y_movement
            jump_hit_reaction_pos.append(floor_y_pos)
        #del(jump_sequence_hit_reaction[-1])
        self.jump_hit_reaction_pos=jump_hit_reaction_pos
        #return jump_sequence_hit_reaction


    def handle_buttons_inputs(self,event):
        if event.key == self.PUNCH1:
           self.command_buffer+='1'
           self.command_buffer_size+=1
           self.command_time=0
           self.command_active=True
           if self.current_sequence_frame['cancel_mode']>1:
              if self.state=='stand':
                 self.move=True
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if attack_range<=self.close_range:
                    self.current_sequence=self.sequences[20]
                    sounds[20].play()
                    if self.opponent.axis_pos[1] == FLOOR_Y_POS:
                       self.handle_normal_throws('punch1')
                 else:
                    self.current_sequence=self.sequences[14]
                    sounds[14].play()
              elif self.state=='crouch':
                 self.current_sequence=self.sequences[38]
                 sounds[38].play()
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if attack_range<=self.close_range and self.opponent.axis_pos[1] == FLOOR_Y_POS:
                    self.handle_normal_throws('punch1')
              elif self.state=='jump':
                 if not self.jump_sequence:
                    if attack_range<=self.close_range \
                    and self.axis_pos[1]<120 and self.opponent.axis_pos[1]<120:
                        self.handle_jump_throws('punch1')
                    else:
                       self.jump_sequence=self.sequences[26]
                       sounds[26].play()
                       self.jump_sequence_index=0
                       self.anim_time=self.max_anim_time
                       if self.jump_forward or self.jump_back:
                          self.jump_sequence=self.sequences[32]
                          sounds[32].play()

        elif event.key == self.PUNCH2:
           self.command_buffer+='2'
           self.command_buffer_size+=1
           self.command_time=0
           self.command_active=True
           if self.current_sequence_frame['cancel_mode']>1:
              if self.state=='stand':
                 self.move=True
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if attack_range<=self.close_range:
                    self.current_sequence=self.sequences[21]
                    sounds[21].play()
                    if self.opponent.axis_pos[1] == FLOOR_Y_POS:
                       self.handle_normal_throws('punch2')
                 else:
                    self.current_sequence=self.sequences[15]
                    sounds[15].play()
              elif self.state=='crouch':
                 self.current_sequence=self.sequences[39]
                 sounds[39].play()
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if attack_range<=self.close_range and self.opponent.axis_pos[1] == FLOOR_Y_POS:
                    self.handle_normal_throws('punch2')
              elif self.state=='jump':
                 if not self.jump_sequence:
                    if attack_range<=self.close_range \
                    and self.axis_pos[1]<120 and self.opponent.axis_pos[1]<120:
                        self.handle_jump_throws('punch2')
                    else:
                       self.jump_sequence=self.sequences[27]
                       sounds[27].play()
                       self.jump_sequence_index=0
                       self.anim_time=self.max_anim_time
                       if self.jump_forward or self.jump_back:
                          self.jump_sequence=self.sequences[33]
                          sounds[33].play()

        elif event.key == self.PUNCH3:
           self.command_buffer+='3'
           self.command_buffer_size+=1
           self.command_time=0
           self.command_active=True
           if self.current_sequence_frame['cancel_mode']>1:
              if self.state=='stand':
                 self.move=True
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if attack_range<=self.close_range:
                    self.current_sequence=self.sequences[22]
                    sounds[22].play()
                    if self.opponent.axis_pos[1] == FLOOR_Y_POS:
                       self.handle_normal_throws('punch3')
                 else:
                    self.current_sequence=self.sequences[16]
                    sounds[16].play()
              elif self.state=='crouch':
                 self.current_sequence=self.sequences[40]
                 sounds[40].play()
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if attack_range<=self.close_range and self.opponent.axis_pos[1] == FLOOR_Y_POS:
                    self.handle_normal_throws('punch3')
              elif self.state=='jump':
                 if not self.jump_sequence:
                    if attack_range<=self.close_range \
                    and self.axis_pos[1]<120 and self.opponent.axis_pos[1]<120:
                        self.handle_jump_throws('punch3')
                    else:
                       self.jump_sequence=self.sequences[28]
                       sounds[28].play()
                       self.jump_sequence_index=0
                       self.anim_time=self.max_anim_time
                       if self.jump_forward or self.jump_back:
                          self.jump_sequence=self.sequences[34]
                          sounds[34].play()

        elif event.key == self.KICK1:
           self.command_buffer+='4'
           self.command_buffer_size+=1
           self.command_time=0
           self.command_active=True
           if self.current_sequence_frame['cancel_mode']>1:
              if self.state=='stand':
                 self.move=True
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if attack_range<=self.close_range:
                    self.current_sequence=self.sequences[17]
                    sounds[17].play()
                    if self.opponent.axis_pos[1] == FLOOR_Y_POS:
                       self.handle_normal_throws('kick1')
                 else:
                    self.current_sequence=self.sequences[11]
                    sounds[11].play()
              elif self.state=='crouch':
                    self.current_sequence=self.sequences[35]
                    sounds[35].play()
                    self.sequence_index=-1
                    self.anim_time=self.max_anim_time
                    if attack_range<=self.close_range and self.opponent.axis_pos[1] == FLOOR_Y_POS:
                       self.handle_normal_throws('kick1')
              elif self.state=='jump':
                 if not self.jump_sequence:
                    if attack_range<=self.close_range \
                    and self.axis_pos[1]<120 and self.opponent.axis_pos[1]<120:
                        self.handle_jump_throws('kick1')
                    else:
                       self.jump_sequence=self.sequences[23]
                       sounds[23].play()
                       self.jump_sequence_index=0
                       self.anim_time=self.max_anim_time
                       if self.jump_forward or self.jump_back:
                          self.jump_sequence=self.sequences[29]
                          sounds[29].play()

        elif event.key == self.KICK2:
           self.command_buffer+='5'
           self.command_buffer_size+=1
           self.command_time=0
           self.command_active=True
           if self.current_sequence_frame['cancel_mode']>1:
              if self.state=='stand':
                 self.move=True
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if attack_range<=self.close_range:
                    self.current_sequence=self.sequences[18]
                    sounds[18].play()
                    if self.opponent.axis_pos[1] == FLOOR_Y_POS:
                       self.handle_normal_throws('kick2')
                 else:
                    self.current_sequence=self.sequences[12]
                    sounds[12].play()
              elif self.state=='crouch':
                    self.current_sequence=self.sequences[36]
                    sounds[36].play()
                    self.sequence_index=-1
                    self.anim_time=self.max_anim_time
                    if attack_range<=self.close_range and self.opponent.axis_pos[1] == FLOOR_Y_POS:
                       self.handle_normal_throws('kick2')
              elif self.state=='jump':
                 if not self.jump_sequence:
                    if attack_range<=self.close_range \
                    and self.axis_pos[1]<120 and self.opponent.axis_pos[1]<120:
                        self.handle_jump_throws('kick2')
                    else:
                       self.jump_sequence=self.sequences[24]
                       sounds[24].play()
                       self.jump_sequence_index=0
                       self.anim_time=self.max_anim_time
                       if self.jump_forward or self.jump_back:
                          self.jump_sequence=self.sequences[30]
                          sounds[30].play()

        elif event.key == self.KICK3:
           self.command_buffer+='6'
           self.command_buffer_size+=1
           self.command_time=0
           self.command_active=True
           if self.current_sequence_frame['cancel_mode']>1:
              if self.state=='stand':
                 self.move=True
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if attack_range<=self.close_range:
                   self.current_sequence=self.sequences[19]
                   sounds[19].play()
                   if self.opponent.axis_pos[1] == FLOOR_Y_POS:
                      self.handle_normal_throws('kick3')
                 else:
                   self.current_sequence=self.sequences[13]
                   sounds[13].play()
              elif self.state=='crouch':
                    self.current_sequence=self.sequences[37]
                    sounds[37].play()
                    self.sequence_index=-1
                    self.anim_time=self.max_anim_time
                    if attack_range<=self.close_range and self.opponent.axis_pos[1] == FLOOR_Y_POS:
                       self.handle_normal_throws('kick3')
              elif self.state=='jump':
                 if not self.jump_sequence:
                    if attack_range<=self.close_range \
                    and self.axis_pos[1]<120 and self.opponent.axis_pos[1]<120:
                        self.handle_jump_throws('kick3')
                    else:
                       self.jump_sequence=self.sequences[25]
                       sounds[25].play()
                       self.jump_sequence_index=0
                       self.anim_time=self.max_anim_time
                       if self.jump_forward or self.jump_back:
                          self.jump_sequence=self.sequences[31]
                          sounds[31].play()

        elif event.key == self.SPECIAL:
             if self.state!='jump':
                if self.current_sequence_frame['cancel_mode'] > 0 :
                   self.current_sequence=self.sequences[self.speciale]
                   self.move=True
                   self.sequence_index=-1
                   self.anim_time=self.max_anim_time

        if event.key == self.FORWARD:
           self.command_buffer+='f'
           self.command_buffer_size+=1
           self.command_time=0
           self.command_active=True
        elif event.key == self.BACKWARD:
           self.command_buffer+='b'
           self.command_buffer_size+=1
           self.command_time=0
           self.command_active=True
        if event.key == self.UP:
           self.command_buffer+='u'
           self.command_buffer_size+=1
           self.command_time=0
           self.command_active=True
        elif event.key == self.DOWN:
           self.command_buffer+='d'
           self.command_buffer_size+=1
           self.command_time=0
           self.command_active=True


    def handle_stick_inputs(self,keys):
        if keys[self.FORWARD]:
           if not (self.forward or self.backward or self.up):
              if self.current_sequence_frame['cancel_mode']>3:
                 self.forward=True
                 self.current_sequence=self.sequences[6]
                 self.state='stand'
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if self.down:
                    self.current_sequence=self.sequences[8]
                    self.sequence_number=8
                    self.state='crouch'
        elif keys[self.BACKWARD]:
           if not (self.backward or self.forward or self.up):
              if self.current_sequence_frame['cancel_mode']>3:
                 self.backward=True
                 self.current_sequence=self.sequences[3]
                 self.state='stand'
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if self.down:
                    self.current_sequence=self.sequences[5]
                    self.sequence_number=5
                    self.state='crouch'

        if keys[self.UP]:
           if not(self.up or self.down):
              if self.current_sequence_frame['cancel_mode']>3:
                 self.up=True
                 self.current_sequence=self.sequences[1]
                 self.state='jump'
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if self.forward:
                    self.current_sequence=self.sequences[7]
                    self.jump_forward=True
                    self.sequence_number=7
                 elif self.backward:
                    self.current_sequence=self.sequences[4]
                    self.jump_back=True
                    self.sequence_number=4
        elif keys[self.DOWN]:
           if not self.down:
              if self.current_sequence_frame['cancel_mode']>3:
                 self.down=True
                 self.current_sequence=self.sequences[2]
                 self.state='crouch'
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if self.backward:
                    self.current_sequence=self.sequences[5]
                 if self.forward:
                    self.current_sequence=self.sequences[8]

    def handle_keyup_inputs(self,event):
        if event.key == self.FORWARD:
           if self.forward:
              self.forward=False
              if self.current_sequence_frame['cancel_mode']>3:
                 self.current_sequence=self.sequences[0]
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if self.state =='crouch':
                    self.current_sequence=self.sequences[2]
        elif event.key == self.BACKWARD:
           if self.backward:
              self.backward=False
              if self.current_sequence_frame['cancel_mode']>3:
                 self.current_sequence=self.sequences[0]
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if self.state =='crouch':
                    self.current_sequence=self.sequences[2]
        if event.key == self.UP:
           if self.up:
              self.up=False
              if self.forward:
                 self.forward=False
              elif self.backward:
                 self.backward=False
        elif event.key == self.DOWN:
           if self.down:
              self.down=False
              if self.current_sequence_frame['cancel_mode']>3:
                 self.current_sequence=self.sequences[0]
                 self.state='stand'
                 self.sequence_index=-1
                 self.anim_time=self.max_anim_time
                 if self.forward:
                    self.forward=False
                 elif self.backward:
                    self.backward=False

    def update_command_buffer(self):
        if self.command_active:
           if (self.state!='jump' or self.sequence_index<1) and self.command_time==0:
              for move in self.super_moves:
                 if self.command_buffer[-move['inputs_lenth']:]==move['inputs']:
                    if self.current_sequence_frame['cancel_mode'] > 0:
                        self.current_sequence=self.sequences[move['sequence']]
                        self.jump_sequence=None
                        self.sequence_index=-1
                        self.anim_time=self.max_anim_time
                        self.command_buffer=''
                        self.command_active=False
                        self.command_time=0
                        self.move=True
                        move['sound'].play()
                        break
           #print(self.command_buffer)
           self.command_time+=1
           if self.command_time > self.command_max_time:
              self.command_buffer=''
              self.command_active=False
              self.command_time=0
           if self.command_buffer_size > self.command_buffer_max_size:
              self.command_buffer=''
              self.command_buffer_size=0

    def update(self):
        self.anim_time+=1
        if self.anim_time>=self.max_anim_time:
           self.anim_time=0
           self.sequence_index+=1
           if self.current_sequence[self.sequence_index]==-1:
              self.current_sequence=self.sequences[self.current_sequence[self.sequence_index+1]]
              self.sequence_index=0
              if self.state=='jump':
                 self.state='stand'
                 self.jump_forward=False
                 self.jump_back=False
                 self.up=False
                 if self.jump_sequence:
                    self.jump_sequence=None
                    self.jump_sequence_frame=None
                    self.jump_sequence_index=0
              if self.axis_pos[1]!=FLOOR_Y_POS:
                 if self.current_sequence[-1] == 'movement_sequence': 
                    self.axis_pos[1]=FLOOR_Y_POS
              if self.move:
                 self.move=False
                 self.forward=False
                 self.backward=False
                 self.down=False
              if self.state=='crouch'  and not self.down:
                 if self.current_sequence_frame['cancel_mode']>3:
                    self.current_sequence=self.sequences[0]
                    self.state='stand'
                    self.sequence_index=0
                    self.anim_time=0
              self.hitted = False
              self.guard_hitted  = False
              if self.knocked_out:
                 #self.knocked_out=False
                 #self.victory=False
                 self.current_sequence=self.sequences[43]
              elif self.victory:
                 self.victory+=1
                 if self.victory > 5:
                    global fighting
                    fighting = False
                    #self.victory = False
                    return
                 if self.victory < 3:
                    self.current_sequence=self.sequences[41+random.randint(0,1)]
           if self.backward and not self.guard:
              if (attack_range < 130 and self.opponent.current_sequence_frame['frame_type']=='A') \
              or (self.opponent.projectile_active
              and self.opponent.projectile_sequence_frame['frame_type']=='A'
              and abs(self.axis_pos[0]-self.opponent.projectile_axis_pos[0]) < 130):
                 if self.current_sequence_frame['cancel_mode']>3:
                    if self.state=='stand':
                       self.current_sequence=self.sequences[9]
                       self.sequence_index=0
                       self.anim_time=0
                       self.guard=True
                    elif self.state=='crouch':
                       self.current_sequence=self.sequences[10]
                       self.sequence_index=0
                       self.anim_time=0
                       self.guard=True
           elif self.guard:
              if self.opponent.current_sequence_frame['frame_type']!='A' \
              and not (self.opponent.projectile_active
              and self.opponent.projectile_sequence_frame['frame_type']=='A') \
              or not self.backward:
                 if self.current_sequence_frame['cancel_mode']>3:
                    if self.state=='stand':
                       self.current_sequence=self.sequences[0]
                       self.sequence_index=0
                       self.anim_time=0
                       self.guard=False
                       self.forward=False
                       self.backward=False
                    elif self.state=='crouch':
                       self.current_sequence=self.sequences[2]
                       self.sequence_index=0
                       self.anim_time=0
                       self.guard=False
                       self.forward=False
                       self.backward=False
           if self.updated_health > self.health:
              self.updated_health -=1
           self.current_sequence_frame=self.sequences_frames[self.current_sequence[self.sequence_index]]
           if not self.opponent.guard_hitted:
              self.axis_pos[0]+=self.current_sequence_frame['x_movement']
           self.axis_pos[1]+=self.current_sequence_frame['y_movement']
           self.current_sprite=self.sprites[self.current_sequence_frame['Image_number']]
           self.image=self.current_sprite['image']
           self.image_orientation = self.current_sequence_frame['frame_orientation']
           if self.axis_pos[0] < 20 or self.axis_pos[0] > 300:
              #x_movement = self.current_sequence_frame['x_movement']
              if self.axis_pos[0] < 20:
                 x_movement=self.axis_pos[0]-20
              elif self.axis_pos[0] > 300:
                 x_movement=self.axis_pos[0]-300
              self.axis_pos[0]-=x_movement
              opponent_pos=self.opponent.axis_pos[0]-x_movement
              if opponent_pos>20 and opponent_pos<300:
                  background['pos'][0]-=x_movement
                  self.opponent.axis_pos[0]-=x_movement
                  if background['pos'][0]>0 \
                  or background['pos'][0]+background['width']<DISPLAY_SURFACE_WIDTH:
                     background['pos'][0]+=x_movement
                     self.opponent.axis_pos[0]+=x_movement
                     if self.hitted and attack_range<80: #<100:
                        self.opponent.axis_pos[0]-=x_movement
           if self.hitted:
              if self.state!='jump' and self.sequence_index==0 \
              or self.jump_sequence and self.jump_sequence_index==0:
                 global hit_freeze_time
                 hit_freeze_time = 5
                 if self.guard_hitted:
                    hit_freeze_time = 3
              if self.current_sequence_frame['invincible']!='A' \
              and self.state!='jump':
                 self.hitted=False
           if self.projectile_active:
              self.projectile_sequence_index+=1
              if self.projectile_sequence[self.projectile_sequence_index]==-1:
                 if self.projectile_sequence[self.projectile_sequence_index+1]!=253:
                    self.projectile_sequence=self.sequences[self.projectile_sequence[self.projectile_sequence_index+1]]
                    self.projectile_sequence_index=0
                 else:
                    self.projectile_active=False
                    self.projectile_sequence_index-=1
              self.projectile_sequence_frame=self.sequences_frames[self.projectile_sequence[self.projectile_sequence_index]]
              self.projectile_sprite=self.sprites[self.projectile_sequence_frame['Image_number']]
              self.projectile_image=self.projectile_sprite['image']
              self.projectile_axis_pos[0]+=self.projectile_sequence_frame['x_movement']
              self.projectile_axis_pos[1]+=self.projectile_sequence_frame['y_movement']
              self.projectile_image_pos[0]=self.projectile_axis_pos[0]+self.projectile_sprite['x_axis_shift']
              self.projectile_image_pos[1]=self.projectile_axis_pos[1]+self.projectile_sprite['y_axis_shift']
              if self.projectile_image_pos[0]>DISPLAY_SURFACE_WIDTH \
              or self.projectile_image_pos[0]+self.current_sprite['image_size'][0]<0:
                self. projectile_active=False
           if self.current_sequence_frame['frame_type']=='F':
              if self.current_sequence_frame['hit_damage']>3:
                 if not (self.projectile_active and self.projectile_sequence_frame['attack_mode'] in ('A','H','L')): 
                 #if not (self.projectile_active and self.projectile_sequence_frame['cancel_mode']==0
                         #and self.projectile_sequence_frame['frame_type']=='A'):
                    self.projectile_active=True
                    self.projectile_collided=False
                    self.projectile_sequence=self.sequences[self.current_sequence[self.sequence_index+1]]
                    self.projectile_sequence_index=0
                    self.projectile_sequence_frame=self.sequences_frames[self.projectile_sequence[self.projectile_sequence_index]]
                    self.projectile_sprite=self.sprites[self.projectile_sequence_frame['Image_number']]
                    self.projectile_image=self.projectile_sprite['image']
                    self.projectile_axis_pos[0]=self.axis_pos[0]+self.projectile_sequence_frame['x_movement']
                    self.projectile_axis_pos[1]=self.axis_pos[1]+self.projectile_sequence_frame['y_movement']
                    self.projectile_image_pos[0]=self.projectile_axis_pos[0]+self.projectile_sprite['x_axis_shift']
                    self.projectile_image_pos[1]=self.projectile_axis_pos[1]+self.projectile_sprite['y_axis_shift']
                 self.sequence_index+=1
           if self.jump_sequence:
              if self.jump_sequence[self.jump_sequence_index]==-1:
                 self.jump_sequence=None
                 #self.jump_sequence_frame=None
                 self.jump_sequece_index=0
              else:
                 self.current_sequence_frame=self.sequences_frames[self.jump_sequence[self.jump_sequence_index]]
                 self.current_sprite=self.sprites[self.current_sequence_frame['Image_number']]
                 self.image=self.current_sprite['image']
                 self.jump_sequence_index+=1
                 if self.current_sequence_frame['frame_type']=='F' \
                 and self.current_sequence_frame['hit_damage']>3:
                    self.jump_sequence_index+=1
           self.image_pos[0] = self.axis_pos[0] + self.current_sprite['x_axis_shift']
           self.image_pos[1] = self.axis_pos[1] + self.current_sprite['y_axis_shift']
           if self.current_sequence_frame['cancel_mode']>3:
              dx=self.axis_pos[0]-self.opponent.axis_pos[0]
              if self.side=='left':
                 if dx>0:
                    self.switch_side()
              elif self.side=='right':
                 if dx<0:
                    self.switch_side()

    def draw(self,surface):
        if self.image_orientation == 'N':
           surface.blit(self.image,self.image_pos)
        elif self.image_orientation == 'U':
           flipped_image=pygame.transform.flip(self.image, False, True)
           surface.blit(flipped_image,self.image_pos)
        elif self.image_orientation == 'F':
           flipped_image=pygame.transform.flip(self.image, True, False)
           surface.blit(flipped_image,self.image_pos)
        elif self.image_orientation == 'R':
           flipped_image=pygame.transform.flip(self.image, True, True)
           surface.blit(flipped_image,self.image_pos)

        """temp_rect=self.current_sprite['collision_box']
        image_width=self.current_sprite['image_size'][0]
        image_height=self.current_sprite['image_size'][1]
        rect=[self.image_pos[0],self.image_pos[1],image_width,image_height]
        pygame.draw.rect(surface, (255,0,0), rect,2)
        rect=[self.image_pos[0]+temp_rect[0],self.image_pos[1]+temp_rect[1],
        temp_rect[2],temp_rect[3]]
        pygame.draw.rect(surface, (0,0,255), rect,2)
        pygame.draw.line(surface,(0,255,0),(self.axis_pos[0]-15,self.axis_pos[1]),
                        (self.axis_pos[0]+15,self.axis_pos[1]),2)
        pygame.draw.line(surface,(0,255,0),(self.axis_pos[0],self.axis_pos[1]-15),
                        (self.axis_pos[0],self.axis_pos[1]+15),2)"""

        if self.projectile_active:
           if self.projectile_sequence_frame['frame_orientation']=='N':
              surface.blit(self.projectile_image,self.projectile_image_pos)
           elif self.projectile_sequence_frame['frame_orientation']=='U':
              flipped_image=pygame.transform.flip(self.projectile_image, False, True)
              surface.blit(flipped_image,self.projectile_image_pos)
           elif self.projectile_sequence_frame['frame_orientation']=='F':
              flipped_image=pygame.transform.flip(self.projectile_image, True, False)
              surface.blit(flipped_image,self.projectile_image_pos)
           elif self.projectile_sequence_frame['frame_orientation']=='R':
              flipped_image=pygame.transform.flip(self.projectile_image, True, True)
              surface.blit(flipped_image,self.projectile_image_pos)

        """if self.projectile_active:
            temp_rect=self.projectile_sprite['collision_box']
            image_width=self.projectile_sprite['image_size'][0]
            image_height=self.projectile_sprite['image_size'][1]
            rect=[self.projectile_image_pos[0],self.projectile_image_pos[1],image_width,image_height]
            pygame.draw.rect(surface, (255,0,0), rect,2)
            rect=[self.projectile_image_pos[0]+temp_rect[0],self.projectile_image_pos[1]+temp_rect[1],
            temp_rect[2],temp_rect[3]]
            pygame.draw.rect(surface, (0,0,255), rect,2)"""


class AI:
    def __init__(self, character):
        self.character = character
        self.moves = [self.walk, self.jump, self.crouch,
                      self.strike, self.throw, self.special_move,
                      self.do_nothing]
        self.moves_length = len(self.moves)-1
        self.move = None
        self.move_time = 0
        self.moves_times = [20, 10, 20, 10, 10, 20, 3]
        self.punches =[(20,14,38,26,32), (21,15,39,27,33), (22,16,40,28,34)]
        self.kicks =[(17,11,35,23,29), (18,12,36,24,30), (19,13,37,25,31)]
        self.strikes = self.punches + self.kicks

    def update(self):
        #self.walk()
        #self.jump()
        #self.crouch()
        #self.guard()
        #self.punch()
        #self.kick()
        #self.strike()
        #self.throw()
        #self.special_move()
        self.random_move()
        #self.do_nothing()

    def walk(self):
        if not self.character.forward:
           character = self.character
           if character.current_sequence_frame['cancel_mode']>3:
              #walk = [6,3][random.randint(0,1)]
              character.current_sequence=character.sequences[6]
              character.state='stand'
              character.sequence_index=-1
              character.anim_time=character.max_anim_time
              character.forward=True

    def jump(self):
        character = self.character
        if character.current_sequence_frame['cancel_mode']>3:
           if not random.randint(0, 9): 
              #jump = [1,7,4][random.randint(0,2)]
              #if jump == 7:
              character.jump_forward=True
              #elif jump == 4:
                 #character.jump_backward=True
              character.current_sequence=character.sequences[7]
              character.state = 'jump'
              character.sequence_index=-1
              character.anim_time=character.max_anim_time

    def crouch(self):
        if not self.character.down:
           character = self.character
           if character.current_sequence_frame['cancel_mode']>3:
              character.current_sequence=character.sequences[2]
              character.state='crouch'
              character.sequence_index=-1
              character.anim_time=character.max_anim_time
              character.down = True

    def guard(self):
        if not self.character.guard:
           character = self.character
           if (attack_range < 130 and character.opponent.current_sequence_frame['frame_type']=='A'):
              if character.current_sequence_frame['cancel_mode']>3:
                 if character.state!='jump':
                    if character.opponent.current_sequence_frame['attack_mode'] in ('A','L'):
                       character.current_sequence=character.sequences[9]
                       character.current_sequence_frame=character.sequences_frames[character.current_sequence[0]]
                       character.sequence_index=-1
                       character.anim_time=character.max_anim_time
                       character.guard=True
                       character.backward = True
                    elif character.opponent.current_sequence_frame['attack_mode'] == 'H':
                       character.current_sequence=character.sequences[10]
                       character.current_sequence_frame=character.sequences_frames[character.current_sequence[0]]
                       character.sequence_index=-1
                       character.anim_time=character.max_anim_time
                       character.guard=True
                       character.backward = True
                       character.state = 'crouch'
           elif (character.opponent.projectile_active
           and character.opponent.projectile_sequence_frame['frame_type']=='A'
           and abs(character.axis_pos[0]-character.opponent.projectile_axis_pos[0]) < 130):
              if character.current_sequence_frame['cancel_mode']>3:
                 if character.state!='jump':
                    if character.opponent.projectile_sequence_frame['attack_mode'] in ('A','L'):
                       character.current_sequence=character.sequences[9]
                       character.current_sequence_frame=character.sequences_frames[character.current_sequence[0]]
                       character.sequence_index=-1
                       character.anim_time=character.max_anim_time
                       character.guard=True
                       character.backward = True
                    elif character.opponent.projectile_sequence_frame['attack_mode'] == 'H':
                       character.current_sequence=character.sequences[10]
                       character.current_sequence_frame=character.sequences_frames[character.current_sequence[0]]
                       character.sequence_index=-1
                       character.anim_time=character.max_anim_time
                       character.guard=True
                       character.backward = True
                       character.state = 'crouch'

    def punch(self):
        character = self.character
        if character.current_sequence_frame['cancel_mode']>1:
           punch = self.punches[random.randint(0,2)]
           if character.state=='stand':
              character.sequence_index=-1
              character.anim_time=character.max_anim_time
              if attack_range<=character.close_range:
                 character.current_sequence=character.sequences[punch[0]]
              else:
                 character.current_sequence=character.sequences[punch[1]]
           elif character.state=='crouch':
              character.current_sequence=character.sequences[punch[2]]
              character.sequence_index=-1
              character.anim_time=character.max_anim_time
           elif character.state=='jump':
              if not character.jump_sequence:
                 character.jump_sequence=character.sequences[punch[3]]
                 character.jump_sequence_index=0
                 character.anim_time=character.max_anim_time
                 if character.jump_forward or character.jump_back:
                    character.jump_sequence=character.sequences[punch[4]]

    def kick(self):
        character = self.character
        if character.current_sequence_frame['cancel_mode']>1:
           kick = self.kicks[random.randint(0,2)]
           if character.state=='stand':
              character.sequence_index=-1
              character.anim_time=character.max_anim_time
              if attack_range<=character.close_range:
                 character.current_sequence=character.sequences[kick[0]]
              else:
                 character.current_sequence=character.sequences[kick[1]]
           elif character.state=='crouch':
              character.current_sequence=character.sequences[kick[2]]
              character.sequence_index=-1
              character.anim_time=character.max_anim_time
           elif character.state=='jump':
              if not character.jump_sequence:
                 character.jump_sequence=character.sequences[kick[3]]
                 character.jump_sequence_index=0
                 character.anim_time=character.max_anim_time
                 if character.jump_forward or character.jump_back:
                    character.jump_sequence=character.sequences[kick[4]]

    def strike(self):
        character = self.character
        if character.current_sequence_frame['cancel_mode']>1:
           strike = self.strikes[random.randint(0,5)]
           if character.state=='stand':
              character.sequence_index=-1
              character.anim_time=character.max_anim_time
              if attack_range<=character.close_range:
                 character.current_sequence=character.sequences[strike[0]]
                 sounds[strike[0]].play()
              else:
                 character.current_sequence=character.sequences[strike[1]]
                 sounds[strike[1]].play()
           elif character.state=='crouch':
              character.current_sequence=character.sequences[strike[2]]
              sounds[strike[2]].play()
              character.sequence_index=-1
              character.anim_time=character.max_anim_time
           elif character.state=='jump':
              if not character.jump_sequence:
                 character.jump_sequence=character.sequences[strike[3]]
                 sounds[strike[3]].play()
                 character.jump_sequence_index=0
                 character.anim_time=character.max_anim_time
                 if character.jump_forward or character.jump_back:
                    character.jump_sequence=character.sequences[strike[4]]
                    sounds[strike[4]].play()

    def throw(self):
        character = self.character
        if character.current_sequence_frame['cancel_mode']>1 \
        and attack_range<=character.close_range and  character.opponent.side != character.side:
           if character.opponent.axis_pos[1] == FLOOR_Y_POS and character.axis_pos[1] == FLOOR_Y_POS:
              button_held = ('punch1','punch2','punch3','kick1','kick2','kick3')[random.randint(0,5)]
              if len(character.normal_throws[button_held]) > 0:
                 throw = character.normal_throws[button_held]
                 throw = throw[random.randint(0, len(throw)-1)]
              else:
                 return  
              character.handle_throw_slam_direction(throw)
              character.opponent.health-=health_damage[throw['damage']]
              character.move = True
              if character.opponent.health<0:
                 character.opponent.health=0
                 character.opponent.knocked_out=True
                 character.victory=True
           elif character.axis_pos[1]<120 and character.opponent.axis_pos[1]<120:
              button_held = ('punch1','punch2','punch3','kick1','kick2','kick3')[random.randint(0,5)]
              if len(character.jump_throws[button_held]) > 0:
                 throw = character.jump_throws[button_held]
                 throw = throw[random.randint(0, len(throw)-1)]
              else:
                 return
              character.axis_pos[1]=105
              character.opponent.axis_pos[1]=105
              character.handle_throw_slam_direction(throw)
              character.move = True
              character.opponent.health-=health_damage[throw['damage']]
              if character.opponent.health<0:
                 character.opponent.health=0
                 character.opponent.knocked_out=True
                 character.victory=True

    def special_move(self):
        character = self.character
        if character.axis_pos[1]==FLOOR_Y_POS and character.current_sequence_frame['cancel_mode'] > 0:
           move = character.super_moves[random.randint(0, len(character.super_moves)-1)]
           character.current_sequence=character.sequences[move['sequence']]
           character.jump_sequence=None
           character.sequence_index=-1
           character.anim_time=character.max_anim_time
           move['sound'].play()

    def random_move(self):
        if not self.character.victory:
           if self.move_time <= 0:
              move_choice = random.randint(0, self.moves_length)
              self.move = self.moves[move_choice]
              self.move_time = self.moves_times[move_choice]
              self.guard()
              self.move()
           else:
              self.move_time -= 1
              self.guard()
              self.move()
              if attack_range <= self.character.close_range:
                 self.move_time = 0

    def do_nothing(self):
        pass


def character_select(player1_controls, player2_controls):
    clock=pygame.time.Clock()
    PALETTE=get_palette(palette_path)
    alpha_color=PALETTE[0]
    #pygame.display.set_palette(get_palette(PALETTE))
    font=pygame.font.SysFont('Arial', 25, bold = True)
    image_path = sfibm_path + "SELECT.SF2"
    with open(image_path, 'rb') as file:
         image_data1=file.read(195*93)
         image_data2=file.read(122*75)
    surface_size = ((26*6)+14, (30*2)+6)
    characters_faces = pygame.Surface(surface_size).convert()
    characters_images=load_R(sfibm_path+'SFACE.R',sfibm_path+'SFACE.ID',PALETTE)
    four_kings_images=load_R(sfibm_path+'4KING.R',sfibm_path+'4KING.ID',PALETTE)
    i = 0
    j = 8
    pygame.draw.rect(characters_faces, (243,211,32), [0, 0, (26*6)+14, (30*2)+6], 5)  #color=(146,81,32)
    pygame.draw.rect(characters_faces, (243,211,32), [0, 0, (26*6)+14, 33], 5)
    for y in range(2):
        for x in range(6):
            pygame.draw.rect(characters_faces, (243,211,32), [((x*26)+2*x+2), ((y*30)+2*y+2), 26, 30], 5)
            if y < 1 or x < 2:
               characters_faces.blit(characters_images[i]['image'],((x*26)+2*x+2,(y*30)+2*y+2))
               i += 1
            else:
               characters_faces.blit(four_kings_images[j]['image'],((x*26)+2*x+2,(y*30)+2*y+2))
               j += 1
    characters_faces_scaled_size=(characters_faces.get_width()*SCALE,characters_faces.get_height()*SCALE)
    characters_faces=pygame.transform.scale(characters_faces,characters_faces_scaled_size)
    characters_faces_pos=[int((640-characters_faces.get_width())/2), 280]
    world_map=pygame.image.fromstring(image_data1,(195,93),'P')
    world_map.set_palette(PALETTE)
    world_map.set_colorkey(alpha_color)
    world_map.convert()
    world_map_scaled_size=(world_map.get_width()*SCALE,world_map.get_height()*SCALE)
    world_map=pygame.transform.scale(world_map,world_map_scaled_size)
    world_map_pos=[int((640-world_map.get_width())/2), 50]
    images=load_R(sfibm_path+'FACEW.R',sfibm_path+'FACEW.ID',PALETTE)
    for image in images:
        image_scaled_size = (image['width']*SCALE, image['height']*SCALE)
        image['image'] = pygame.transform.scale(image['image'], image_scaled_size)
    for image in four_kings_images:
        image_scaled_size = (image['width']*SCALE, image['height']*SCALE)
        image['image'] = pygame.transform.scale(image['image'], image_scaled_size)
    player1_selection_box = images[11]['image']
    player1_selection_box_pos = [characters_faces_pos[0]-2, characters_faces_pos[1]-10]
    selection_box_x_move = 56
    selection_box_y_move = 64
    box1_flash_time = 0
    box2_flash_time = 0
    box_flash_surface = pygame.Surface((52, 60))
    box_flash_surface.fill(WHITE)
    box_flash_surface.set_alpha(100)
    player2_selection_box = images[13]['image']
    player2_selection_box_pos = [characters_faces_pos[0]-2, characters_faces_pos[1]-2+selection_box_y_move]
    characters = [[{'name':'RYU', 'portrait':images[0]['image'], 'RE':'HYPRYU.RE', 'IDE':'HYPRYU.IDE', 'SEQ':'HYPRYU.SEQ', 'KEY':'HYPRYU.KEY','background':'HYPRYU.BK','music':'RYU.MDI','KO_sound':'0L.VOC'},
                   {'name':'E.HONDA', 'portrait':images[1]['image'], 'RE':'HYPHONDA.RE', 'IDE':'HYPHONDA.IDE', 'SEQ':'HYPHONDA.SEQ', 'KEY':'HYPHONDA.KEY','background':'HYPHONDA.BK','music':'HONDA.MDI','KO_sound':'1L.VOC'},
                   {'name':'BLANKA', 'portrait':images[2]['image'], 'RE':'HYPBLANK.RE', 'IDE':'HYPBLANK.IDE', 'SEQ':'HYPBLANK.SEQ', 'KEY':'HYPBLANK.KEY','background':'HYPBLANK.BK','music':'BLANKA.MDI','KO_sound':'2L.VOC'},
                   {'name':'GUILE', 'portrait':images[3]['image'], 'RE':'HYPGUILE.RE', 'IDE':'HYPGUILE.IDE', 'SEQ':'HYPGUILE.SEQ', 'KEY':'HYPGUILE.KEY','background':'HYPGUILE.BK','music':'GUILE.MDI','KO_sound':'3L.VOC'},
                   {'name':'BALROG', 'portrait':images[4]['image'], 'RE':'HYPBAL.RE', 'IDE':'HYPBAL.IDE', 'SEQ':'HYPBAL.SEQ', 'KEY':'HYPBAL.KEY','background':'HYPBAL.BK','music':'BALOG.MDI','KO_sound':'4L.VOC'},
                   {'name':'VEGA', 'portrait':images[5]['image'], 'RE':'HYPVEGA.RE', 'IDE':'HYPVEGA.IDE', 'SEQ':'HYPVEGA.SEQ', 'KEY':'HYPVEGA.KEY','background':'HYPVEGA.BK','music':'VEGA.MDI','KO_sound':'5L.VOC'}],
                  [{'name':'KEN', 'portrait':images[6]['image'], 'RE':'HYPKEN.RE', 'IDE':'HYPKEN.IDE', 'SEQ':'HYPKEN.SEQ', 'KEY':'HYPKEN.KEY','background':'HYPKEN.BK','music':'KEN.MDI','KO_sound':'6L.VOC'},
                   {'name':'CHUN-LI', 'portrait':images[7]['image'], 'RE':'HYPCHUN.RE', 'IDE':'HYPCHUN.IDE', 'SEQ':'HYPCHUN.SEQ', 'KEY':'HYPCHUN.KEY','background':'HYPCHUN.BK','music':'CHUNLI.MDI','KO_sound':'7L.VOC'},
                   {'name':'ZANGIEF', 'portrait':four_kings_images[0]['image'], 'RE':'HYPZANG.RE', 'IDE':'HYPZANG.IDE', 'SEQ':'HYPZANG.SEQ', 'KEY':'HYPZANG.KEY','background':'HYPZANG.BK','music':'ZANGIEF.MDI','KO_sound':'8L.VOC'},
                   {'name':'DHALSIM', 'portrait':four_kings_images[1]['image'], 'RE':'HYPDHAL.RE', 'IDE':'HYPDHAL.IDE', 'SEQ':'HYPDHAL.SEQ', 'KEY':'HYPDHAL.KEY','background':'HYPDHAL.BK','music':'DALSIM.MDI','KO_sound':'9L.VOC'},
                   {'name':'SAGAT', 'portrait':four_kings_images[2]['image'], 'RE':'HYPSAGAT.RE', 'IDE':'HYPSAGAT.IDE', 'SEQ':'HYPSAGAT.SEQ', 'KEY':'HYPSAGAT.KEY','background':'HYPSAGAT.BK','music':'C-SF.MDI','KO_sound':'AL.VOC'},
                   {'name':'M.BISON', 'portrait':four_kings_images[3]['image'], 'RE':'HYPBISON.RE', 'IDE':'HYPBISON.IDE', 'SEQ':'HYPBISON.SEQ', 'KEY':'HYPBISON.KEY','background':'HYPBISON.BK','music':'C-SF.MDI','KO_sound':'BL.VOC'}]]
    player1_column_index = 0
    player1_row_index = 0
    player1_character = characters[player1_row_index][player1_column_index]
    player1_character_pos =[-30, 420-player1_character['portrait'].get_height()]
    player1_name = font.render(player1_character['name'], True, WHITE)
    player2_column_index = 0
    player2_row_index = 1
    player2_character = characters[player2_row_index][player2_column_index]
    player2_character_pos =[640-player2_character['portrait'].get_width()+30, 420-player2_character['portrait'].get_height()]
    player2_name = font.render(player2_character['name'], True, WHITE)
    player1_choice = None
    player2_choice = None
    character1 = None
    character2 = None
    background = None
    music = None
    ting_sound = pygame.mixer.Sound(sfibm_path+'TING.VOC')
    ting_sound.set_volume(0.3)
    select_sound = pygame.mixer.Sound(sfibm_path+'SELECT.VOC')
    select_sound.set_volume(0.3)    
    pygame.mixer.music.load(sfibm_path+'SELECT.MDI')
    pygame.mixer.music.play(-1)


    #pygame.key.set_repeat(400, 30)

    while True:
        
        #loop speed limitation
        #30 frames per second is enought
        clock.tick(30)

        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                  global mode
                  if mode == 'arcade':
                     mode = 'title screen'
                     return None, None, []
                  elif mode in ('versus', 'watch'):
                     mode = 'title screen'
                     return None, None, None, None, None
               if not character1:
                  if event.key == K_RIGHT:
                     ting_sound.play() 
                     player1_selection_box_pos[0] += selection_box_x_move
                     player1_column_index += 1
                     if player1_column_index >= len(characters[player1_row_index]):
                        player1_column_index = 0
                        player1_row_index += 1
                        if player1_row_index >= len(characters):
                           player1_row_index = 0
                        player1_selection_box_pos = [characters_faces_pos[0]-2,
                                                    (characters_faces_pos[1]-10)+(selection_box_y_move*player1_row_index)]
                     player1_character = characters[player1_row_index][player1_column_index]
                     player1_character_pos[1] = 420-player1_character['portrait'].get_height()
                     player1_name = font.render(player1_character['name'], True, WHITE)
                  elif event.key == K_LEFT:
                     ting_sound.play() 
                     player1_selection_box_pos[0] -= selection_box_x_move
                     player1_column_index -= 1
                     if player1_column_index < 0:
                        player1_column_index = len(characters[player1_row_index])-1
                        player1_row_index += 1
                        if player1_row_index >= len(characters):
                           player1_row_index = 0
                        player1_selection_box_pos = [characters_faces_pos[0]-2+(selection_box_x_move*(len(characters[player1_row_index])-1)),
                                                    (characters_faces_pos[1]-10)+(selection_box_y_move*player1_row_index)]
                     player1_character = characters[player1_row_index][player1_column_index]
                     player1_character_pos[1] = 420-player1_character['portrait'].get_height()
                     player1_name = font.render(player1_character['name'], True, WHITE)
                  elif event.key == K_UP:
                     ting_sound.play() 
                     player1_selection_box_pos[1] -= selection_box_y_move
                     player1_row_index -= 1
                     if player1_row_index < 0:
                        player1_row_index = len(characters)-1
                        player1_selection_box_pos[1] = (characters_faces_pos[1]-10)+(selection_box_y_move*player1_row_index)
                     player1_character = characters[player1_row_index][player1_column_index]
                     player1_character_pos[1] = 420-player1_character['portrait'].get_height()
                     player1_name = font.render(player1_character['name'], True, WHITE)
                  elif event.key == K_DOWN:
                     ting_sound.play() 
                     player1_selection_box_pos[1] += selection_box_y_move
                     player1_row_index += 1
                     if player1_row_index > len(characters)-1:
                        player1_row_index = 0
                        player1_selection_box_pos[1] = (characters_faces_pos[1]-10)+(selection_box_y_move*player1_row_index)
                     player1_character = characters[player1_row_index][player1_column_index]
                     player1_character_pos[1] = 420-player1_character['portrait'].get_height()
                     player1_name = font.render(player1_character['name'], True, WHITE)
                  if event.key in (K_a, K_s, K_d, K_z, K_x, K_c):
                     select_sound.play() 
                     RE=sfibm_path+player1_character['RE']
                     IDE=sfibm_path+player1_character['IDE']
                     SEQ=sfibm_path+player1_character['SEQ']
                     KEY=sfibm_path+player1_character['KEY']
                     background=sfibm_path+player1_character['background']
                     sprites=load_RE(RE,IDE,PALETTE)
                     sequences,sequences_frames=load_SEQ(SEQ)
                     super_moves,throws,close_range=load_KEY(KEY)
                     background=load_background(background,PALETTE)
                     character1=Character(sprites,sequences,sequences_frames,player1_controls,super_moves,throws,close_range,[90,FLOOR_Y_POS],'left')
                     character1.ko_sound = pygame.mixer.Sound(sfibm_path+player1_character['KO_sound'])
                     character1.ko_sound.set_volume(0.3)
                     character1.name = player1_character['name']
                     music = sfibm_path+player1_character['music']
                     
               if mode in ('versus', 'watch'):
                  if not character2:
                     if event.key == K_SEMICOLON:
                        ting_sound.play() 
                        player2_selection_box_pos[0] += selection_box_x_move
                        player2_column_index += 1
                        if player2_column_index >= len(characters[player2_row_index]):
                           player2_column_index = 0
                           player2_row_index += 1
                           if player2_row_index >= len(characters):
                              player2_row_index = 0
                           player2_selection_box_pos = [characters_faces_pos[0]-2,
                                                       (characters_faces_pos[1]-2)+(selection_box_y_move*player2_row_index)]
                        player2_character = characters[player2_row_index][player2_column_index]
                        player2_character_pos[1] = 420-player2_character['portrait'].get_height()
                        player2_name = font.render(player2_character['name'], True, WHITE)
                     elif event.key == K_l:
                        ting_sound.play() 
                        player2_selection_box_pos[0] -= selection_box_x_move
                        player2_column_index -= 1
                        if player2_column_index < 0:
                           player2_column_index = len(characters[player2_row_index])-1
                           player2_row_index += 1
                           if player2_row_index >= len(characters):
                              player2_row_index = 0
                           player2_selection_box_pos = [characters_faces_pos[0]-2+(selection_box_x_move*(len(characters[player2_row_index])-1)),
                                                       (characters_faces_pos[1]-2)+(selection_box_y_move*player2_row_index)]
                        player2_character = characters[player2_row_index][player2_column_index]
                        player2_character_pos[1] = 420-player2_character['portrait'].get_height()
                        player2_name = font.render(player2_character['name'], True, WHITE)
                     elif event.key == K_p:
                        ting_sound.play() 
                        player2_selection_box_pos[1] -= selection_box_y_move
                        player2_row_index -= 1
                        if player2_row_index < 0:
                           player2_row_index = len(characters)-1
                           player2_selection_box_pos[1] = (characters_faces_pos[1]-2)+(selection_box_y_move*player2_row_index)
                        player2_character = characters[player2_row_index][player2_column_index]
                        player2_character_pos[1] = 420-player2_character['portrait'].get_height()
                        player2_name = font.render(player2_character['name'], True, WHITE)
                     elif event.key == K_PERIOD:
                        ting_sound.play() 
                        player2_selection_box_pos[1] += selection_box_y_move
                        player2_row_index += 1
                        if player2_row_index > len(characters)-1:
                           player2_row_index = 0
                           player2_selection_box_pos[1] = (characters_faces_pos[1]-2)+(selection_box_y_move*player2_row_index)
                        player2_character = characters[player2_row_index][player2_column_index]
                        player2_character_pos[1] = 420-player2_character['portrait'].get_height()
                        player2_name = font.render(player2_character['name'], True, WHITE)
                     if event.key in (K_1, K_2, K_3, K_q, K_w, K_e):
                        select_sound.play() 
                        RE=sfibm_path+player2_character['RE']
                        IDE=sfibm_path+player2_character['IDE']
                        SEQ=sfibm_path+player2_character['SEQ']
                        KEY=sfibm_path+player2_character['KEY']
                        background=sfibm_path+player2_character['background']
                        sprites=load_RE(RE,IDE,PALETTE)
                        sequences,sequences_frames=load_SEQ(SEQ)
                        super_moves,throws,close_range=load_KEY(KEY)
                        background=load_background(background,PALETTE)
                        character2=Character(sprites,sequences,sequences_frames,player2_controls,super_moves,throws,close_range,[230,FLOOR_Y_POS],'right')
                        character2.ko_sound = pygame.mixer.Sound(sfibm_path+player2_character['KO_sound'])
                        character2.ko_sound.set_volume(0.3)
                        character2.name = player2_character['name']
                        music = sfibm_path+player2_character['music']

        if mode == 'arcade':
           if character1:
              versus_data = [player1_character, None, images[8]['image']]
              return character1, versus_data, characters[0] + characters[1]
         
        elif mode in ('versus', 'watch'):
           if character1 and character2:
              character1.opponent=character2
              character2.opponent=character1
              versus_data = [player1_character, player2_character, images[8]['image']]
              return character1, character2, background, versus_data, music

        screen.fill(BLUE)
        #text=font.render(str(image_index)+' '+'/'+str(images_lenth), True, (250,0,0))
        #screen.blit(text,(50,250))
        #text=font.render(image['name'], True, (250,0,0))
        #screen.blit(text,(50,270))
        screen.blit(world_map, world_map_pos)
        screen.blit(characters_faces, characters_faces_pos)
        if mode in ('versus', 'watch'):
           if character2:
              box2_flash_time += 1
              if box2_flash_time < 5 :
                 screen.blit(box_flash_surface, (player2_selection_box_pos[0]+6,player2_selection_box_pos[1]+6))
              elif box2_flash_time > 10 :
                 box2_flash_time = 0
              #screen.blit(player2_selection_box, player2_selection_box_pos)
           elif not character2:
              box2_flash_time += 1
              if box2_flash_time < 8 :
                 screen.blit(player2_selection_box, player2_selection_box_pos)
              elif box2_flash_time > 12 :
                 box2_flash_time = 0
           flipped_image = pygame.transform.flip(player2_character['portrait'], True, False)
           screen.blit(flipped_image, player2_character_pos)
           screen.blit(player2_name, (640-player2_name.get_width()-30,200))
        if character1:
           box1_flash_time += 1
           if box1_flash_time < 5 :
              screen.blit(box_flash_surface, (player1_selection_box_pos[0]+6,player1_selection_box_pos[1]+14))
           elif box1_flash_time > 10 :
              box1_flash_time = 0
           screen.blit(player1_selection_box, player1_selection_box_pos)
        elif not character1:
           box1_flash_time += 1
           if box1_flash_time < 8 :
              screen.blit(player1_selection_box, player1_selection_box_pos)
           elif box1_flash_time > 12 :
              box1_flash_time = 0
        screen.blit(player1_character['portrait'], player1_character_pos)
        screen.blit(player1_name, (30,200))
        pygame.display.flip()


def title_screen():
    clock=pygame.time.Clock()
    PALETTE=get_palette(palette_path)
    alpha_color=PALETTE[0]
    #pygame.display.set_palette(get_palette(PALETTE))
    font=pygame.font.SysFont('Arial', 22)
    text=font.render("Hit Any Key to Play", True, YELLOW)
    text_pos=[320-int(text.get_width()/2), 380]
    text_flash_time = 0
    show_menu = False
    menu = ['arcade', 'versus', 'watch']
    menu_length = len(menu)
    menu_index = 0

    image_path = sfibm_path + "HYPTL.229"
    with open(image_path, 'rb') as file:
         image_data=file.read(229*131) #(320*120)
    title = pygame.image.fromstring(image_data,(229,131),'P')
    title.set_palette(PALETTE)
    title.set_colorkey(alpha_color)
    title.convert()
    title_scaled_size = (title.get_width()*SCALE,title.get_height()*SCALE)
    title = pygame.transform.scale(title,title_scaled_size)
    title_pos = [int((320-(title.get_width())/2)), 80]
    ting_sound = pygame.mixer.Sound(sfibm_path+'TING.VOC')
    ting_sound.set_volume(0.3)
    pygame.mixer.music.load(sfibm_path+'SF2TTL.MDI')
    pygame.mixer.music.play()
    

    #pygame.key.set_repeat(400, 30)

    while True:

        #loop speed limitation
        #30 frames per second is enought
        clock.tick(30)

        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                  pygame.quit()
                  sys.exit()
               if show_menu:
                  if event.key == K_UP:
                     ting_sound.play() 
                     texts[menu_index] = font.render(menu[menu_index].upper(), True, ORANGE)
                     menu_index -= 1
                     if menu_index < 0:
                        menu_index = menu_length-1
                     texts[menu_index] = font.render(menu[menu_index].upper(), True, YELLOW)   
                  elif event.key == K_DOWN:
                     ting_sound.play() 
                     texts[menu_index] = font.render(menu[menu_index].upper(), True, ORANGE) 
                     menu_index += 1
                     if menu_index > menu_length-1:
                        menu_index = 0
                     texts[menu_index] = font.render(menu[menu_index].upper(), True, YELLOW)
                  elif event.key in (K_a, K_s, K_d, K_z, K_x, K_c, K_RETURN):
                     return menu[menu_index]
               elif not show_menu:
                  show_menu = True
                  font=pygame.font.SysFont('Arial', 19)
                  texts = [font.render("ARCADE", True, ORANGE),
                           font.render("VERSUS", True, ORANGE),
                           font.render("WATCH", True, ORANGE)]
                  texts[menu_index] = font.render(menu[menu_index].upper(), True, YELLOW)
                  texts_pos = [[320-int(texts[0].get_width()/2), 360],
                               [320-int(texts[1].get_width()/2), 385],
                               [320-int(texts[2].get_width()/2), 410]]
                  
        screen.fill((0,0,200))
        screen.blit(title,title_pos)
        if show_menu:
           for i in range(menu_length):
               screen.blit(texts[i],texts_pos[i])
        elif not show_menu:
           text_flash_time += 1
           if text_flash_time < 10:
              screen.blit(text,text_pos)
           elif text_flash_time > 20:
              text_flash_time = 0
        pygame.display.flip()


def versus_screen(versus_data):
    clock=pygame.time.Clock()
    font=pygame.font.SysFont('Arial', 24, bold = True)
    character1_name = font.render(versus_data[0]['name'], True, WHITE)
    character2_name = font.render(versus_data[1]['name'], True, WHITE)
    character1_portrait = versus_data[0]['portrait']
    character2_portrait = pygame.transform.flip(versus_data[1]['portrait'], True, False)
    versus_image = versus_data[2]
    versus_image_pos = [320-int(versus_image.get_width()/2), 240-int(versus_image.get_height()/2)]
    x_offset = int(((640-versus_image.get_width())/2 - character1_portrait.get_width())/2)
    y_offset = 350
    character1_portrait_pos =  [x_offset, y_offset-character1_portrait.get_height()]
    character2_portrait_pos =  [640-x_offset-character2_portrait.get_width(), y_offset-character2_portrait.get_height()]
    character1_name_pos = [int(character1_portrait_pos[0]+character1_portrait.get_width()/2-character1_name.get_width()/2), 90]
    character2_name_pos = [int(character2_portrait_pos[0]+character2_portrait.get_width()/2-character2_name.get_width()/2), 90]
    pygame.mixer.music.load(sfibm_path+'VS.MDI')
    pygame.mixer.music.play()
    
    #pygame.key.set_repeat(400, 30)
    t1=pygame.time.get_ticks()
    while True:
        
        #loop speed limitation
        #30 frames per second is enought
        clock.tick(30)

        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                return

        t2=pygame.time.get_ticks()
        if(t2-t1)/1000>3:
           break


        screen.fill(BLUE)
        screen.blit(character1_portrait,character1_portrait_pos)
        screen.blit(character2_portrait,character2_portrait_pos)
        screen.blit(versus_image,versus_image_pos)
        screen.blit(character1_name,character1_name_pos)
        screen.blit(character2_name,character2_name_pos)
        pygame.display.flip()


def round_start(character1, character2, round_number):
    clock=pygame.time.Clock()
    display_surface=pygame.Surface((320, 240)).convert()
    font1=pygame.font.SysFont('Arial', 25, bold = True)
    font2=pygame.font.SysFont('Arial', 11, bold = True)
    health_bar=pygame.Surface((102,12)).convert()
    health_bar.fill((255,0,0))
    pygame.draw.rect(health_bar, (255,255,255), [0,0,102,12],1)
    text1 = font1.render('ROUND '+str(round_number), True, YELLOW)
    text2 = font1.render('ROUND '+str(round_number), True, RED)
    text_pos = [320-int(text1.get_width()/2), 200]
    text_flash_time = 1
    timer = 0
    character1.opponent = character2
    character2.opponent = character1
    character1_shadow_y_pos = FLOOR_Y_POS + character1.sprites[0]['y_axis_shift'] + 2
    character2_shadow_y_pos = FLOOR_Y_POS + character2.sprites[0]['y_axis_shift'] + 2    
    character1_name = font2.render(character1.name, True, WHITE)
    character2_name = font2.render(character2.name, True, WHITE)
    character1_name_pos = [20+2, 5]
    character2_name_pos = [(198+102)-(character2_name.get_width()+2), 5]    
    round_start_sound = pygame.mixer.Sound(sfibm_path+'R1.VOC')
    round_start_sound.set_volume(0.3)
    round_start_sound.play()
    #pygame.key.set_repeat(400, 30)

    while True:
        
        #loop speed limitation
        #30 frames per second is enought
        clock.tick(30)

        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
               pygame.quit()
               sys.exit()

            if event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                  pygame.quit()
                  sys.exit()
                  
        character1.update()
        character2.update()
        timer += 1
        if timer == 25:
           text1 = font1.render('FIGHT !', True, YELLOW)
           text2 = font1.render('FIGHT !', True, RED)
           text_pos = [320-int(text1.get_width()/2), 200]
        elif timer == 55:
           return
           
        display_surface.fill((0,0,0))
        display_surface.blit(background['image'],background['pos'])
        shadow_pos=[character1.axis_pos[0]+character1.sprites[0]['x_axis_shift'],character1_shadow_y_pos]
        display_surface.blit(character1.sprites[0]['image'],shadow_pos)
        shadow_pos=[character2.axis_pos[0]+character2.sprites[0]['x_axis_shift'],character2_shadow_y_pos]
        display_surface.blit(character2.sprites[0]['image'],shadow_pos)
        character1.draw(display_surface)
        character2.draw(display_surface)
        display_surface.blit(health_bar,(20,18))
        display_surface.blit(health_bar,(198,18))
        if character1.updated_health>0:
           pygame.draw.rect(display_surface, (255,255,0), [120,19,-character1.updated_health+2,10])
        if character2.updated_health>0:
           pygame.draw.rect(display_surface, (255,255,0), [199,19,character2.updated_health,10])
        display_surface.blit(character1_name,character1_name_pos)
        display_surface.blit(character2_name,character2_name_pos)
        scaled_display_surface=pygame.transform.scale(display_surface,(640,480))
        screen.blit(scaled_display_surface,(0,0))
        text_flash_time += 1
        if text_flash_time < 6:
           screen.blit(text1,text_pos)
        elif text_flash_time < 12:
           screen.blit(text2,text_pos)
        elif text_flash_time > 12:
           text_flash_time = 0
        pygame.display.flip()


def fight(character1, character2, mode):
    global fighting, attack_range, hit_freeze_time, empty_box, health_damage
    clock=pygame.time.Clock()
    display_surface=pygame.Surface((320, 240)).convert()
    font=pygame.font.SysFont('Arial', 11, bold = True)
    attack_range=0
    hit_freeze_time = 0
    empty_box=[0,0,0,0]
    health_damage=[2,5,10,12,15,18,20,22,2,2]
    health_bar=pygame.Surface((102,12)).convert()
    health_bar.fill((255,0,0))
    pygame.draw.rect(health_bar, (255,255,255), [0,0,102,12],1)
    character1.opponent = character2
    character2.opponent = character1
    character1_shadow_y_pos = FLOOR_Y_POS + character1.sprites[0]['y_axis_shift'] + 2
    character2_shadow_y_pos = FLOOR_Y_POS + character2.sprites[0]['y_axis_shift'] + 2
    character1_name = font.render(character1.name, True, WHITE)
    character2_name = font.render(character2.name, True, WHITE)
    character1_name_pos = [20+2, 5]
    character2_name_pos = [(198+102)-(character2_name.get_width()+2), 5]
    

    fighting = True
   
    #pygame.key.set_repeat(400, 30)
   
    if mode == "versus":

       while fighting:

           #loop speed limitation
           #30 frames per second is enought
           clock.tick(30)

           for event in pygame.event.get():    #wait for events
               if event.type == QUIT:
                 pygame.quit()
                 sys.exit()

               if event.type == KEYDOWN:
                 character1.handle_buttons_inputs(event)
                 character2.handle_buttons_inputs(event)
               if event.type == KEYUP:
                 character1.handle_keyup_inputs(event)
                 character2.handle_keyup_inputs(event)


           #Movement controls
           keys = pygame.key.get_pressed()
           character1.handle_stick_inputs(keys)
           character2.handle_stick_inputs(keys)


           if hit_freeze_time < 1:
              attack_range=abs(character1.axis_pos[0]-character2.axis_pos[0])

              character1.update_command_buffer()
              character2.update_command_buffer()
              character1.update()
              character2.update()
              if not (character1.hitted or character2.hitted):
                 character1.handle_collision()
                 character2.handle_collision()

           else:
              hit_freeze_time -= 1


           display_surface.fill((0,0,0))
           display_surface.blit(background['image'],background['pos'])
           shadow_pos=[character1.axis_pos[0]+character1.sprites[0]['x_axis_shift'],character1_shadow_y_pos]
           display_surface.blit(character1.sprites[0]['image'],shadow_pos)
           shadow_pos=[character2.axis_pos[0]+character2.sprites[0]['x_axis_shift'],character2_shadow_y_pos]
           display_surface.blit(character2.sprites[0]['image'],shadow_pos)
           if character1.current_sequence_frame['frame_type']=='A': #or character2.hitted:
              character2.draw(display_surface)
              character1.draw(display_surface)
           else:
              character1.draw(display_surface)
              character2.draw(display_surface)
           display_surface.blit(health_bar,(20,18))
           display_surface.blit(health_bar,(198,18))
           if character1.updated_health>0:
              pygame.draw.rect(display_surface, (255,255,0), [120,19,-character1.updated_health+2,10])
           if character2.updated_health>0:
              pygame.draw.rect(display_surface, (255,255,0), [199,19,character2.updated_health,10])
           display_surface.blit(character1_name,character1_name_pos)
           display_surface.blit(character2_name,character2_name_pos)
           scaled_display_surface=pygame.transform.scale(display_surface,(640,480))
           screen.blit(scaled_display_surface,(0,0))
           #text=font.render(str(character1.axis_pos[0])+' '+str(character2.axis_pos[0]), True, (250,0,0))
           #screen.blit(text,(420,20))
           #text=font.render(str(character1.axis_pos[1])+' '+str(character2.axis_pos[1]), True, (250,0,0))
           #screen.blit(text,(420,40))
           pygame.display.flip()

         
    elif mode == "arcade":
       character2.ai = AI(character2)   #;character1.ai = AI(character1)
      
       while fighting:
           
           #loop speed limitation
           #30 frames per second is enought
           clock.tick(30)

           for event in pygame.event.get():    #wait for events
               if event.type == QUIT:
                 pygame.quit()
                 sys.exit()

               if event.type == KEYDOWN:
                 character1.handle_buttons_inputs(event)
               if event.type == KEYUP:
                 character1.handle_keyup_inputs(event)


           #Movement controls
           keys = pygame.key.get_pressed()
           character1.handle_stick_inputs(keys)


           if hit_freeze_time < 1:
              attack_range=abs(character1.axis_pos[0]-character2.axis_pos[0])

              character1.update_command_buffer()
              character1.update()
              character2.update()
              character2.ai.update()   #;character1.ai.update()
              if not (character1.hitted or character2.hitted):
                 character1.handle_collision()
                 character2.handle_collision()

           else:
              hit_freeze_time -= 1


           display_surface.fill((0,0,0))
           display_surface.blit(background['image'],background['pos'])
           shadow_pos=[character1.axis_pos[0]+character1.sprites[0]['x_axis_shift'],character1_shadow_y_pos]
           display_surface.blit(character1.sprites[0]['image'],shadow_pos)
           shadow_pos=[character2.axis_pos[0]+character2.sprites[0]['x_axis_shift'],character2_shadow_y_pos]
           display_surface.blit(character2.sprites[0]['image'],shadow_pos)
           if character1.current_sequence_frame['frame_type']=='A': #or character2.hitted:
              character2.draw(display_surface)
              character1.draw(display_surface)
           else:
              character1.draw(display_surface)
              character2.draw(display_surface)
           display_surface.blit(health_bar,(20,18))
           display_surface.blit(health_bar,(198,18))
           if character1.updated_health>0:
              pygame.draw.rect(display_surface, (255,255,0), [120,19,-character1.updated_health+2,10])
           if character2.updated_health>0:
              pygame.draw.rect(display_surface, (255,255,0), [199,19,character2.updated_health,10])
           display_surface.blit(character1_name,character1_name_pos)
           display_surface.blit(character2_name,character2_name_pos)              
           scaled_display_surface=pygame.transform.scale(display_surface,(640,480))
           screen.blit(scaled_display_surface,(0,0))
           pygame.display.flip()

         
    elif mode == "watch":
       character1.ai = AI(character1)
       character2.ai = AI(character2)
       
       while fighting:
           
           #loop speed limitation
           #30 frames per second is enought
           clock.tick(30)

           for event in pygame.event.get():    #wait for events
               if event.type == QUIT:
                 pygame.quit()
                 sys.exit()

           if hit_freeze_time < 1:
              attack_range=abs(character1.axis_pos[0]-character2.axis_pos[0])
              character1.update()
              character2.update()
              character1.ai.update()
              character2.ai.update()
              if not (character1.hitted or character2.hitted):
                 character1.handle_collision()
                 character2.handle_collision()

           else:
              hit_freeze_time -= 1


           display_surface.fill((0,0,0))
           display_surface.blit(background['image'],background['pos'])
           shadow_pos=[character1.axis_pos[0]+character1.sprites[0]['x_axis_shift'],character1_shadow_y_pos]
           display_surface.blit(character1.sprites[0]['image'],shadow_pos)
           shadow_pos=[character2.axis_pos[0]+character2.sprites[0]['x_axis_shift'],character2_shadow_y_pos]
           display_surface.blit(character2.sprites[0]['image'],shadow_pos)
           if character1.current_sequence_frame['frame_type']=='A': #or character2.hitted:
              character2.draw(display_surface)
              character1.draw(display_surface)
           else:
              character1.draw(display_surface)
              character2.draw(display_surface)
           display_surface.blit(health_bar,(20,18))
           display_surface.blit(health_bar,(198,18))
           if character1.updated_health>0:
              pygame.draw.rect(display_surface, (255,255,0), [120,19,-character1.updated_health+2,10])
           if character2.updated_health>0:
              pygame.draw.rect(display_surface, (255,255,0), [199,19,character2.updated_health,10])
           display_surface.blit(character1_name,character1_name_pos)
           display_surface.blit(character2_name,character2_name_pos)              
           scaled_display_surface=pygame.transform.scale(display_surface,(640,480))
           screen.blit(scaled_display_surface,(0,0))
           pygame.display.flip()


def main():
    global screen, background, mode, sounds
    screen = pygame.display.set_mode((640, 480))
    #Title
    pygame.display.set_caption("SFGE")
    #icon
    icone = pygame.image.load("SFGE.bmp")
    pygame.display.set_icon(icone)    
    clock=pygame.time.Clock()
    PALETTE=get_palette(palette_path)
    sounds = load_sounds(sfibm_path)
    mode ='title screen'
    character1 = None
    character2 = None
    versus_data = None
    music = None
    pygame.mixer.music.set_volume(0.5)

    controls1={ 'FORWARD':K_RIGHT,
                'BACKWARD':K_LEFT,
                'UP':K_UP,
                'DOWN':K_DOWN,
                'PUNCH1':K_a,
                'PUNCH2':K_s,
                'PUNCH3':K_d,
                'KICK1':K_z,
                'KICK2':K_x,
                'KICK3':K_c,
                'SPECIAL':K_v }

    controls2={ 'FORWARD':K_SEMICOLON,
                'BACKWARD':K_l,
                'UP':K_p,
                'DOWN':K_PERIOD,
                'PUNCH1':K_1,
                'PUNCH2':K_2,
                'PUNCH3':K_3,
                'KICK1':K_q,
                'KICK2':K_w,
                'KICK3':K_e,
                'SPECIAL':K_r }

    """character1 = load_character(RE, IDE, SEQ, KEY, controls1, 'left', PALETTE)
    character2 = load_character(RE2, IDE2, SEQ2, KEY2, controls2, 'right', PALETTE)
    background=load_background(sfibm_path+'RBK.BKG',PALETTE)"""

        
    while True:
        
        #loop speed limitation
        #30 frames per second is enought
        clock.tick(30)
        
        for event in pygame.event.get():    #wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()        

        if mode == 'title screen':
           mode = title_screen()
        if mode == 'arcade':
           if character1:
              del(opponents[opponent_index])
              if len(opponents) > 0 and not character1.knocked_out:
                 data = versus_data[0]
                 RE = sfibm_path + data['RE']
                 IDE = sfibm_path + data['IDE']
                 SEQ = sfibm_path + data['SEQ']
                 KEY = sfibm_path + data['KEY']
                 character1 = load_character(RE, IDE, SEQ, KEY, controls1, 'left', PALETTE)
                 character1.name = data['name']
                 character1.ko_sound = pygame.mixer.Sound(sfibm_path+data['KO_sound'])
                 character1.ko_sound.set_volume(0.3)
                 opponent_index = random.randint(0,len(opponents)-1)
                 character2 = opponents[opponent_index]
                 music = sfibm_path+character2['music']
                 versus_data[1] = character2
                 background=sfibm_path+character2['background']
                 background=load_background(background,PALETTE)
                 RE = sfibm_path + character2['RE']
                 IDE = sfibm_path + character2['IDE']
                 SEQ = sfibm_path + character2['SEQ']
                 KEY = sfibm_path + character2['KEY']                 
                 character2 = load_character(RE, IDE, SEQ, KEY, controls2, 'right', PALETTE)
                 character2.name = opponents[opponent_index]['name']
                 character2.ko_sound = pygame.mixer.Sound(sfibm_path+opponents[opponent_index]['KO_sound'])
                 character2.ko_sound.set_volume(0.3)
              else:
                 mode ='title screen'
                 character1 = None
                 character2 = None
                 versus_data = None
           elif not character1:
              character1, versus_data , opponents = character_select(controls1, controls2)
              if character1 != None:
                 opponent_index = random.randint(0,len(opponents)-1)
                 character2 = opponents[opponent_index]
                 music = sfibm_path+character2['music']
                 versus_data[1] = character2
                 background=sfibm_path+character2['background']
                 background=load_background(background,PALETTE)
                 RE = sfibm_path + character2['RE']
                 IDE = sfibm_path + character2['IDE']
                 SEQ = sfibm_path + character2['SEQ']
                 KEY = sfibm_path + character2['KEY']                 
                 character2 = load_character(RE, IDE, SEQ, KEY, controls2, 'right', PALETTE)
                 character2.name = opponents[opponent_index]['name']
                 character2.ko_sound = pygame.mixer.Sound(sfibm_path+opponents[opponent_index]['KO_sound'])
                 character2.ko_sound.set_volume(0.3)
        elif mode in ('versus', 'watch'):
           character1, character2, background, versus_data, music = character_select(controls1, controls2)
        if versus_data:
           versus_screen(versus_data)
        if character1 and character2:
           pygame.mixer.music.load(music)
           pygame.mixer.music.play(-1)
           round_start(character1, character2, 1)
           fight(character1, character2, mode)
           pygame.mixer.music.stop()

     
if __name__ == "__main__":
    main()
