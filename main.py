# Libreries
from tkinter import *
import cv2
import numpy as np
from PIL import Image, ImageTk
import imutils
import mediapipe as mp
import math
import os
import face_recognition as fr
from tkinter import Tk, Entry, font
# Face Code
def Code_Face(images):
    listacod = []

    # Iteramos
    for img in images:
        # Correccion de color
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Codificamos la imagen
        cod = fr.face_encodings(img)[0]
        # Almacenamos
        listacod.append(cod)

    return listacod

# Close Windows LogBiometric
def Close_Windows():
    global step, conteo
    # Reset Variables
    conteo = 0
    step = 0
    pantalla2.destroy()

# Close Windows SignBiometric
def Close_Windows2():
    global step, conteo
    # Reset Variables
    conteo = 0
    step = 0
    pantalla3.destroy()

# Profile
def Profile():
    global step, conteo, UserName, OutFolderPathUser
    # Reset Variables
    conteo = 0
    step = 0

    pantalla4 = Toplevel(pantalla)
    pantalla4.title("BIOMETRIC SIGN")
    pantalla4.geometry("1280x720")

    back = Label(pantalla4, image=imagenB, text="Back")
    back.place(x=0, y=0, relwidth=1, relheight=1)

    # Archivo
    UserFile = open(f"{OutFolderPathUser}/{UserName}.txt", 'r')
    InfoUser = UserFile.read().split(',')
    Name = InfoUser[0]
    User = InfoUser[1]
    Pass = InfoUser[2]
    UserFile.close()

    # Check
    if User in clases:
        # Interfaz
        texto1 = Label(pantalla4, text=f"Bienvenido {Name}", fg="Black", bg="lightgray", font=("Arial", 12, "bold"))
        texto1.place(x=580, y=50)
        # Label
        # Video
        lblImgUser = Label(pantalla4)
        lblImgUser.place(x=450, y=80)

        # Imagen
        PosUserImg = clases.index(User)
        UserImg = images[PosUserImg]

        ImgUser = Image.fromarray(UserImg)
        #
        ImgUser = cv2.imread(f"{OutFolderPathFace}/{User}.png")
        ImgUser = cv2.cvtColor(ImgUser, cv2.COLOR_RGB2BGR)
        ImgUser = Image.fromarray(ImgUser)
        # Ajustar tamaño
        desired_size = (420, 420)  # Ajusta a las dimensiones
        ImgUser = ImgUser.resize(desired_size,Image.Resampling.LANCZOS) # Usa Image.Resampling.LANCZOS en lugar de Image.ANTIALIAS

        #
        IMG = ImageTk.PhotoImage(image=ImgUser)

        lblImgUser.configure(image=IMG)
        lblImgUser.image = IMG


# Register Biometric
def Log_Biometric():
    global pantalla, pantalla2, conteo, parpadeo, img_info, step

    # Leemos la videocaptura
    if cap is not None:
        ret, frame = cap.read()

        # Frame Save
        frameSave = frame.copy()

        # RGB
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Show
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Si es correcta
        if ret == True:

            # Inference
            res = FaceMesh.process(frameRGB)

            # List Results
            px = []
            py = []
            lista = []
            r = 5
            t = 3

            # Resultados
            if res.multi_face_landmarks:
                # Iteramos
                for rostros in res.multi_face_landmarks:

                    # Draw Face Mesh
                    mpDraw.draw_landmarks(frame, rostros, FacemeshObject.FACEMESH_CONTOURS, ConfigDraw, ConfigDraw)

                    # Extract KeyPoints
                    for id, puntos in enumerate(rostros.landmark):

                        # Info IMG
                        al, an, c = frame.shape
                        x, y = int(puntos.x * an), int(puntos.y * al)
                        px.append(x)
                        py.append(y)
                        lista.append([id, x, y])

                        # 468 KeyPoints
                        if len(lista) == 468:
                            # Ojo derecho
                            x1, y1 = lista[145][1:]
                            x2, y2 = lista[159][1:]
                            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                            longitud1 = math.hypot(x2 - x1, y2 - y1)
                            #print(longitud1)

                            # Ojo Izquierdo
                            x3, y3 = lista[374][1:]
                            x4, y4 = lista[386][1:]
                            cx2, cy2 = (x3 + x4) // 2, (y3 + y4) // 2
                            longitud2 = math.hypot(x4 - x3, y4 - y3)
                            #print(longitud2)

                            # Parietal Derecho
                            x5, y5 = lista[139][1:]
                            # Parietal Izquierdo
                            x6, y6 = lista[368][1:]

                            # Ceja Derecha
                            x7, y7 = lista[70][1:]
                            # Ceja Izquierda
                            x8, y8 = lista[300][1:]

                            #cv2.circle(frame, (x5, y5), 2, (255, 0, 0), cv2.FILLED)
                            #cv2.circle(frame, (x6, y6), 2, (0, 0, 0), cv2.FILLED)
                            #cv2.circle(frame, (x7, y7), 2, (0, 255, 0), cv2.FILLED)
                            #cv2.circle(frame, (x8, y8), 2, (0, 255, 0), cv2.FILLED)

                            # Face Detect
                            faces = detector.process(frameRGB)

                            if faces.detections is not None:
                                for face in faces.detections:

                                    # bboxInfo - "id","bbox","score","center"
                                    score = face.score
                                    score = score[0]
                                    bbox = face.location_data.relative_bounding_box

                                    # Threshold
                                    if score > confThreshold:
                                        # Info IMG
                                        alimg, animg, c = frame.shape

                                        # Coordenates
                                        xi, yi, an, al = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, an, al = int(xi * animg), int(yi * alimg), int(
                                            an * animg), int(al * alimg)

                                        # Width
                                        offsetan = (offsetx / 100) * an
                                        xi = int(xi - int(offsetan/2))
                                        an = int(an + offsetan)
                                        xf = xi + an

                                        # Height
                                        offsetal = (offsety / 100) * al
                                        yi = int(yi - offsetal)
                                        al = int(al + offsetal)
                                        yf = yi + al

                                        # Error < 0
                                        if xi < 0: xi = 0
                                        if yi < 0: yi = 0
                                        if an < 0: an = 0
                                        if al < 0: al = 0

                                    # Steps
                                    if step == 0:
                                        # Draw
                                        cv2.rectangle(frame, (xi, yi, an, al), (255, 0, 255), 2)
                                        # IMG Step0
                                        alis0, anis0, c = img_step0.shape
                                        frame[50:50 + alis0, 50:50 + anis0] = img_step0

                                        # IMG Step1
                                        alis1, anis1, c = img_step1.shape
                                        frame[50:50 + alis1, 1030:1030 + anis1] = img_step1

                                        #IMG Step2
                                        alis2, anis2, c = img_step2.shape
                                        frame[270:270 + alis2, 1030:1030 + anis2] = img_step2

                                        # Condiciones
                                        if x7 > x5 and x8 < x6:

                                            # Cont Parpadeos
                                            if longitud1 <= 10 and longitud2 <= 10 and parpadeo == False:  # Parpadeo
                                                conteo = conteo + 1
                                                parpadeo = True

                                            elif longitud1 > 10 and longitud2 > 10 and parpadeo == True:  # Seguridad parpadeo
                                                parpadeo = False

                                            # IMG check
                                            alich, anich, c = img_check.shape
                                            frame[165:165 + alich, 1105:1105 + anich] = img_check

                                            # Parpadeos
                                            # Conteo de parpadeos
                                            cv2.putText(frame, f'Parpadeos: {int(conteo)}', (1070, 375), cv2.FONT_HERSHEY_COMPLEX,0.5,
                                                        (255, 255, 255), 1)


                                            if conteo >= 3:
                                                # IMG check
                                                alich, anich, c = img_check.shape
                                                frame[385:385 + alich, 1105:1105 + anich] = img_check

                                                # Open Eyes
                                                if longitud1 > 14 and longitud2 > 14:
                                                    # Cut
                                                    cut = frameSave[yi:yf, xi:xf]
                                                    # Save Image Without Draw
                                                    cv2.imwrite(f"{OutFolderPathFace}/{RegUser}.png", cut)
                                                    # Cerramos
                                                    step = 1
                                        else:
                                            conteo = 0

                                    if step == 1:
                                        # Draw
                                        cv2.rectangle(frame, (xi, yi, an, al), (0, 255, 0), 2)
                                        # IMG check Liveness
                                        allich, anlich, c = img_liche.shape
                                        frame[50:50 + allich, 50:50 + anlich] = img_liche


                            # Close Window
                            close = pantalla2.protocol("WM_DELETE_WINDOW", Close_Windows)

            # Rendimensionamos el video
            frame = imutils.resize(frame, width=1280)

            # Convertimos el video
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            # Mostramos en el GUI
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, Log_Biometric)

        else:
            cap.release()

# Sign Biometric
def Sign_Biometric():
    global pantalla, pantalla3, conteo, parpadeo, img_info, step, UserName, prueba

    # Leemos la videocaptura
    if cap is not None:
        ret, frame = cap.read()

        # Frame Save
        frameCopy = frame.copy()

        # Resize
        frameFR = cv2.resize(frameCopy, (0, 0), None, 0.25, 0.25)

        # Color
        rgb = cv2.cvtColor(frameFR, cv2.COLOR_BGR2RGB)

        # RGB
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Show
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Si es correcta
        if ret == True:

            # Inference
            res = FaceMesh.process(frameRGB)

            # List Results
            px = []
            py = []
            lista = []
            r = 5
            t = 3

            # Resultados
            if res.multi_face_landmarks:
                # Iteramos
                for rostros in res.multi_face_landmarks:

                    # Draw Face Mesh
                    mpDraw.draw_landmarks(frame, rostros, FacemeshObject.FACEMESH_CONTOURS, ConfigDraw, ConfigDraw)

                    # Extract KeyPoints
                    for id, puntos in enumerate(rostros.landmark):

                        # Info IMG
                        al, an, c = frame.shape
                        x, y = int(puntos.x * an), int(puntos.y * al)
                        px.append(x)
                        py.append(y)
                        lista.append([id, x, y])

                        # 468 KeyPoints
                        if len(lista) == 468:
                            # Ojo derecho
                            x1, y1 = lista[145][1:]
                            x2, y2 = lista[159][1:]
                            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                            longitud1 = math.hypot(x2 - x1, y2 - y1)
                            #print(longitud1)

                            # Ojo Izquierdo
                            x3, y3 = lista[374][1:]
                            x4, y4 = lista[386][1:]
                            cx2, cy2 = (x3 + x4) // 2, (y3 + y4) // 2
                            longitud2 = math.hypot(x4 - x3, y4 - y3)
                            #print(longitud2)

                            # Parietal Derecho
                            x5, y5 = lista[139][1:]
                            # Parietal Izquierdo
                            x6, y6 = lista[368][1:]

                            # Ceja Derecha
                            x7, y7 = lista[70][1:]
                            # Ceja Izquierda
                            x8, y8 = lista[300][1:]

                            #cv2.circle(frame, (x5, y5), 2, (255, 0, 0), cv2.FILLED)
                            #cv2.circle(frame, (x6, y6), 2, (0, 0, 0), cv2.FILLED)
                            #cv2.circle(frame, (x7, y7), 2, (0, 255, 0), cv2.FILLED)
                            #cv2.circle(frame, (x8, y8), 2, (0, 255, 0), cv2.FILLED)

                            # Face Detect
                            faces = detector.process(frameRGB)

                            if faces.detections is not None:
                                for face in faces.detections:

                                    # bboxInfo - "id","bbox","score","center"
                                    score = face.score
                                    score = score[0]
                                    bbox = face.location_data.relative_bounding_box

                                    # Threshold
                                    if score > confThreshold:
                                        # Info IMG
                                        alimg, animg, c = frame.shape

                                        # Coordenates
                                        xi, yi, an, al = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, an, al = int(xi * animg), int(yi * alimg), int(
                                            an * animg), int(al * alimg)

                                        # Width
                                        offsetan = (offsetx / 100) * an
                                        xi = int(xi - int(offsetan/2))
                                        an = int(an + offsetan)
                                        xf = xi + an

                                        # Height
                                        offsetal = (offsety / 100) * al
                                        yi = int(yi - offsetal)
                                        al = int(al + offsetal)
                                        yf = yi + al

                                        # Error < 0
                                        if xi < 0: xi = 0
                                        if yi < 0: yi = 0
                                        if an < 0: an = 0
                                        if al < 0: al = 0

                                        # Steps
                                        if step == 0:
                                            # Draw
                                            cv2.rectangle(frame, (xi, yi, an, al), (255, 0, 255), 2)
                                            # IMG Step0
                                            alis0, anis0, c = img_step0.shape
                                            frame[50:50 + alis0, 50:50 + anis0] = img_step0

                                            # IMG Step1
                                            alis1, anis1, c = img_step1.shape
                                            frame[50:50 + alis1, 1030:1030 + anis1] = img_step1

                                            # IMG Step2
                                            alis2, anis2, c = img_step2.shape
                                            frame[270:270 + alis2, 1030:1030 + anis2] = img_step2

                                            # Condiciones
                                            if x7 > x5 and x8 < x6:

                                                # Cont Parpadeos
                                                if longitud1 <= 10 and longitud2 <= 10 and parpadeo == False:  # Parpadeo
                                                    conteo = conteo + 1
                                                    parpadeo = True

                                                elif longitud2 > 10 and longitud2 > 10 and parpadeo == True:  # Seguridad parpadeo
                                                    parpadeo = False

                                                # IMG check
                                                alich, anich, c = img_check.shape
                                                frame[165:165 + alich, 1105:1105 + anich] = img_check

                                                # Parpadeos
                                                # Conteo de parpadeos
                                                cv2.putText(frame, f'Parpadeos: {int(conteo)}', (1070, 375),
                                                            cv2.FONT_HERSHEY_COMPLEX, 0.5,
                                                            (255, 255, 255), 1)

                                                if conteo >= 3:
                                                    # IMG check
                                                    alich, anich, c = img_check.shape
                                                    frame[385:385 + alich, 1105:1105 + anich] = img_check

                                                    # Open Eyes
                                                    if longitud1 > 14 and longitud2 > 14:
                                                        step = 1
                                            else:
                                                conteo = 0

                                        if step == 1:
                                            # Draw
                                            cv2.rectangle(frame, (xi, yi, an, al), (0, 255, 0), 2)
                                            # IMG check Liveness
                                            allich, anlich, c = img_liche.shape
                                            frame[50:50 + allich, 50:50 + anlich] = img_liche

                                            # Find Faces
                                            faces = fr.face_locations(rgb)
                                            facescod = fr.face_encodings(rgb, faces)

                                            # Iteramos
                                            for facecod, faceloc in zip(facescod, faces):

                                                # Matching
                                                Match = fr.compare_faces(FaceCode, facecod)

                                                # Similitud
                                                simi = fr.face_distance(FaceCode, facecod)

                                                # Min
                                                min = np.argmin(simi)

                                                # User
                                                if Match[min]:
                                                    # UserName
                                                    UserName = clases[min].upper()

                                                    Profile()


                            # Close Window
                            close = pantalla3.protocol("WM_DELETE_WINDOW", Close_Windows2)

            # Rendimensionamos el video
            frame = imutils.resize(frame, width=1280)

            # Convertimos el video
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)

            # Mostramos en el GUI
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, Sign_Biometric)

        else:
            cap.release()


# Sign Function
def Sign():
    global LogUser, LogPass, OutFolderPath, cap, lblVideo, pantalla3, FaceCode, clases, images

    # DB Faces
    # Accedemos a la carpeta
    images = []
    clases = []
    lista = os.listdir(OutFolderPathFace)

    # Leemos los rostros del DB
    for lis in lista:
        # Leemos las imagenes de los rostros
        imgdb = cv2.imread(f'{OutFolderPathFace}/{lis}')
        # Almacenamos imagen
        images.append(imgdb)
        # Almacenamos nombre
        clases.append(os.path.splitext(lis)[0])

    # Face Code
    FaceCode = Code_Face(images)

    # 3° Ventana
    pantalla3 = Toplevel(pantalla)
    pantalla3.title("BIOMETRIC SIGN")
    pantalla3.geometry("1280x720")

    back2 = Label(pantalla3, image=imagenB, text="Back")
    back2.place(x=0, y=0, relwidth=1, relheight=1)

    # Video
    lblVideo = Label(pantalla3)
    lblVideo.place(x=0, y=0)

    # Elegimos la camara
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 1280)
    cap.set(4, 720)
    Sign_Biometric()


# Register Function
def Log():
    global RegName, RegUser, RegPass, InputNameReg, InputUserReg, InputPassReg, cap, lblVideo, pantalla2
    # Name, User, PassWord
    RegName, RegUser, RegPass = InputNameReg.get(), InputUserReg.get(), InputPassReg.get()

    if len(RegName) == 0 or len(RegUser) == 0 or len(RegPass) == 0:
        # Info incompleted
        print(" FORMULARIO INCOMPLETO ")

    else:
        # Info Completed
        # Check users
        UserList = os.listdir(PathUserCheck)
        # Name Users
        UserName = []
        for lis in UserList:
            # Extract User
            User = lis
            User = User.split('.')
            # Save
            UserName.append(User[0])

        # Check Names
        if RegUser in UserName:
            # Registred
            print("USUARIO REGISTRADO ANTERIORMENTE")

        else:
            # No Registred
            # Info
            info.append(RegName)
            info.append(RegUser)
            info.append(RegPass)

            # Save Info
            f = open(f"{OutFolderPathUser}/{RegUser}.txt", 'w')
            f.writelines(RegName + ',')
            f.writelines(RegUser + ',')
            f.writelines(RegPass + ',')
            f.close()

            # Clean
            InputNameReg.delete(0, END)
            InputUserReg.delete(0, END)
            InputPassReg.delete(0, END)

            # Ventana principal
            pantalla2 = Toplevel(pantalla)
            pantalla2.title("BIOMETRIC REGISTER")
            pantalla2.geometry("1280x720")

            back = Label(pantalla2, image=imagenB, text="Back")
            back.place(x=0, y=0, relwidth=1, relheight=1)

            # Video
            lblVideo = Label(pantalla2)
            lblVideo.place(x=0, y=0)
            #lblVideo.place(x=320, y=115)

            # Elegimos la camara
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap.set(3, 1280)
            cap.set(4, 720)
            Log_Biometric()

# Path
OutFolderPathUser = 'C:/Users/Daniel/Desktop/PrototipoFinal/Protofinoentregable/DataBase/Users'
PathUserCheck = 'C:/Users/Daniel/Desktop/PrototipoFinal/Protofinoentregable/DataBase/Users'
OutFolderPathFace = 'C:/Users/Daniel/Desktop/PrototipoFinal/Protofinoentregable/DataBase/Faces'

# List
info = []

# Variables
parpadeo = False
conteo = 0
muestra = 0
step = 0

# Margen
offsety = 30
offsetx = 20

# Umbral
confThreshold = 0.5
blurThreshold = 15

# Tool Draw
mpDraw = mp.solutions.drawing_utils
ConfigDraw = mpDraw.DrawingSpec(thickness=1, circle_radius=1) #Ajustamos la configuracion de dibujo

# Object Face Mesh
FacemeshObject = mp.solutions.face_mesh
FaceMesh = FacemeshObject.FaceMesh(max_num_faces=1) #Creamos el objeto (Ctrl + Click)

# Object Detect
FaceObject = mp.solutions.face_detection
detector = FaceObject.FaceDetection(min_detection_confidence= 0.5, model_selection=1)

# Img OpenCV
# Leer imagenes
img_info = cv2.imread("C:/Users/Daniel\Desktop/PrototipoFinal/Protofinoentregable/SetUp/mensaje.png")
img_check = cv2.imread("C:/Users/Daniel\Desktop/PrototipoFinal/Protofinoentregable/SetUp/check.png")
img_step0 = cv2.imread("C:/Users/Daniel\Desktop/PrototipoFinal/Protofinoentregable/SetUp/mensaje-2.png")
img_step1 = cv2.imread("C:/Users/Daniel\Desktop/PrototipoFinal/Protofinoentregable/SetUp/Paso1.png")
img_step2 = cv2.imread("C:/Users/Daniel\Desktop/PrototipoFinal/Protofinoentregable/SetUp/Paso2.png")
img_liche = cv2.imread("C:/Users/Daniel\Desktop/PrototipoFinal/Protofinoentregable/SetUp/mensaje-4.png")

# Ventana principal
pantalla = Tk()
pantalla.title("SECURE FACE-NE")
pantalla.geometry("1280x720")

# Fondo
imagenF = PhotoImage(file="C:/Users/Daniel/Desktop/PrototipoFinal/Protofinoentregable/SetUp/reconoce.png")
background = Label(image = imagenF, text = "Inicio")
background.place(x = 0, y = 0, relwidth = 1, relheight = 1)

# Fondo 2
imagenB = PhotoImage(file="C:/Users/Daniel/Desktop/PrototipoFinal/Protofinoentregable/SetUp/Fondo2.png")

# Input Text
# Register
# Name
# Definir el estilo de texto para los campos de entrada
text_font = font.Font(family="Arial", size=12, weight="bold", slant="roman")

InputNameReg = Entry(pantalla, font=text_font)
InputNameReg.place(x= 110, y = 320)
InputNameReg.config(bg="lightgray", fg="black", borderwidth=2, relief="groove")
# User
InputUserReg = Entry(pantalla, font=text_font)
InputUserReg.place(x= 110, y = 430)
InputUserReg.config(bg="lightgray", fg="black", borderwidth=2, relief="groove")
# Pass
InputPassReg = Entry(pantalla, font=text_font, show="*")
InputPassReg.place(x= 110, y = 540)
InputPassReg.config(bg="lightgray", fg="black", borderwidth=2, relief="groove")

# Botones
# Registro
imagenBR = PhotoImage(file="C:/Users/Daniel/Desktop/PrototipoFinal/Protofinoentregable/SetUp/registro-biometrico.png")
BtReg = Button(pantalla, text="Registro", image=imagenBR, height="40", width="200", command=Log)
BtReg.place(x = 300, y = 580)
BtReg.config(cursor="hand2")

# Inicio de sesion
imagenBL = PhotoImage(file="C:/Users/Daniel/Desktop/PrototipoFinal/Protofinoentregable/SetUp/acceso.png")
BtSign = Button(pantalla, text="Sign", image=imagenBL, height="40", width="200", command=Sign)
BtSign.place(x = 850, y = 580)
BtReg.config(cursor="hand2")


# Eject
pantalla.mainloop()