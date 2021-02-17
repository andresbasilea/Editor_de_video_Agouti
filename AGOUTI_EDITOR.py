# EDITOR DE VIDEOS PYTHON PARA AGOUTI


# ESTE EDITOR CONCATENA LOS VIDEOS SELECCIONADOS EN EL ORDEN SELECCIONADO. 
# LA EDICIÓN CONSISTE EN QUITAR 2 SEGUNDOS AL PRINCIPIO DE CADA CLIP Y 2 SEGUNDOS AL FINAL DE CADA CLIP.


from moviepy.editor import *
from tkinter import filedialog
from tkinter import *
import PyPDF2
import os
from PIL import Image, ImageTk
import shutil
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import numpy as np
import math

lista_videos = []

root = Tk()
root.iconbitmap("C:\\Users\\andre\\Desktop\\AGOUTI_EDITOR\\favicon3.ico")
alto = 390
ancho = 580
root.title("Editor de Video Agouti")

w = Canvas(root,width = ancho, height = alto, background = "white")
image = PhotoImage(file = "C:\\Users\\andre\\Desktop\\AGOUTI_EDITOR\\AGOUTI_I.png")
background_label = Label(root, image=image)
#background_label.bind('<Configure>',cambiarTamanio)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
w.pack()

s = Button(root, text = "Selecc. videos", font = 'Serif', foreground = 'black')
s.config(background = 'white')
s.pack()
s.place(relheight = 0.1, relwidth = 0.22, relx = 0.1 , rely = 0.2)

u = Button(root, text = "¡Editar!", font = 'Serif', foreground = 'black')
u.config(background = 'white')
u.pack()
u.place(relheight = 0.1, relwidth = 0.1, relx = 0.75, rely = 0.2)


def buscar_videos():
    global lista_videos
    archivo =  filedialog.askopenfilenames(parent=root, initialdir = "/",title = "Selecciona los videos",filetypes = (("Video files","*.mp4"),("all files","*.*")))
    lista_videos = list(archivo)
    print("\n\n\n ###############################\n\n\n")
    print(lista_videos)
    print("\n\n\n################################\n\n\n")



def editar_videos():

    global lista_videos
    lista_videos_editados = []
    

    fps = 44100.0   # CONSTANTE DE FRECUENCIA A LA QUE SE TOMA EL AUDIO
    nueve_segundos = 396900
    
    x = 0
    for i in lista_videos:
        x += 1
        clip = VideoFileClip(i)
        arr = clip.audio.to_soundarray()
        #print("\n\n\n",arr) # EL VIDEO CONVERTIDO EN UNICAMENTE EL AUDIO
        print("longitud del video en frames de audio: ", len(arr))
        duracion = 1.0 * len(arr) / fps    # COMO FUNCIONA LA DURACION

        lista_audio = arr.tolist()

        # with open("audio", "w") as audio_txt:
        #     for fila in arr:
        #         np.savetxt(audio_txt,fila)

        corte_inicio = 0

        for t in range(0, nueve_segundos): # 9 segundos, verificar si hay input de voz
            if lista_audio[t][0] <= 0.1:
                pass
            else:
                corte_inicio = t
                break

        corte_final = 0

        for t in range(int(duracion*fps), int(duracion*fps - nueve_segundos), -1):
            if lista_audio[t-1][0] <= 0.1:
                pass
            else:
                corte_final = t
                break

        if corte_inicio == 0:
            # hacer corte despues de 6 segundos
            ffmpeg_extract_subclip(i, nueve_segundos, duracion, targetname="recorte"+str(x)+".mp4")

        if corte_final == 0:
            # hacer corte en los ultimos 6 segundos
            ffmpeg_extract_subclip(i, nueve_segundos, duracion-2.5, targetname="recorte"+str(x)+".mp4")
           

        print("Corte inicio y final: ", corte_inicio, corte_final)


        if corte_inicio != 0 or corte_final != 0: 
            ffmpeg_extract_subclip(i, corte_inicio//fps - 1, corte_final//fps + 2.7, targetname="recorte" + str(x) + ".mp4")
        
        clip = VideoFileClip("recorte" + str(x) + ".mp4")
        # clip.write_videofile("test" + str(x) + ".mp4")




    for i in range(len(lista_videos)):
        lista_videos_editados.append("C:\\Users\\andre\\Desktop\\AGOUTI_EDITOR\\recorte" + str(i+1) + ".mp4")

    #print(lista_videos_editados)

    clips = []

    for i in lista_videos_editados:

        clips.append(VideoFileClip(i))

    video_editado = concatenate_videoclips(clips)
    video_editado.write_videofile("video_editado.mp4")




    

u.config(command = editar_videos)
s.config(command = buscar_videos)

mainloop()




# arr = clip.audio.to_soundarray()

        # with open("audio", "w") as audio_txt:
        #     for fila in arr:
        #         np.savetxt(audio_txt,fila)
        # print(arr)
