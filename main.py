from tkinter import Tk, filedialog, messagebox
import os
import os.path
import shutil
import requests
import zipfile
from colorama import init, Fore, Back, Style

class Conversion:
    rutaFFMPEG = str()
    rutaArchivoIn = str()

    def __init__(self):
        # Importar FFMPEG
        if not os.path.isfile('ffmpeg.exe'):
            messagebox.showinfo("EJECUTABLE FFMPEG NO ENCONTRADO", "Al no encontrarse el ejecutable de FFMPEG, se va "
                                                                   "a tener que descargar. Por favor, asegurate de "
                                                                   "tener conexión a internet activa y funcional. "
                                                                   "Esto puede tomar unos segundos, espera, por favor. ")
            peticionDescargaFFMPEG = requests.get("https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
                                                  allow_redirects=True)
            open('ffmpeg.zip', 'wb').write(peticionDescargaFFMPEG.content)
            with zipfile.ZipFile("ffmpeg.zip", "r") as zip_ref:
                zip_ref.extractall(os.getcwd() + "\\temp")
            shutil.copyfile((os.getcwd() + "\\temp\\ffmpeg-4.4-essentials_build\\bin\\ffmpeg.exe"),
                            str(os.getcwd() + "\\ffmpeg.exe"))
            shutil.rmtree(os.getcwd() + "\\temp")
            os.remove("ffmpeg.zip")
            messagebox.showinfo("FFMPEG descargado", "Se ha descargado correctamente FFMPEG.")
        self.rutaFFMPEG = str('"' + os.getcwd() + '\\ffmpeg.exe"')
        # Importar archivo a trimear
        self.rutaArchivoIn = str(
            '"' + (filedialog.askopenfile(title="Selecciona archivo de vídeo a trimear. Tiene que ser MP4 y no ProRes").name) + '"')

    def trim(self, timeIn, timeOut, rutaSalida):
        # ffmpeg -ss [start] -i in.mp4 -to [end] -c copy -copyts out.mp4

        comando = os.popen(
            self.rutaFFMPEG + " -hide_banner -loglevel error -stats -ss " + timeIn + " -y -i " + self.rutaArchivoIn + " -to " + timeOut + " -c copy -copyts " + rutaSalida.name)
        comando.read()


print("FFMPEG Wrapper goes brummmm")
root = Tk()
root.withdraw()
root.attributes('-topmost', True)
messagebox.showinfo("Por favor, leeme detenidamente", "Este programa sirve para separar secciones de un archivo de "
                                                      "vídeo de manera rápida ya que no se lleva a cabo una "
                                                      "recodificación como en Premiere. El funcionamiento es el "
                                                      "siguiente: \n·Primero se comprueba si FFMPEG está descargado, "
                                                      "en caso de no estarlo, se descarga y extrae automáticamente, "
                                                      "el usuario no tiene que hacer nada. \n·Después se preguntan "
                                                      "cuántas secciones hacer del vídeo. No hay límite \n ·Entonces, "
                                                      "archivo por archivo, se preguntan los puntos de entrada y "
                                                      "salida de cada uno de los nuevos archivos y dónde guardarlos y "
                                                      "con qué nombre. Es importante acordarse de añadir en los "
                                                      "nombres el formato, por ejemplo, .mp4 o .mov. Tenga en cuenta "
                                                      "que se se crean archivos vacío antes de la conversión para "
                                                      "reservar el nombre de archivo. Que aparezca el archivo no "
                                                      "significa que ya esté terminado. \n·Una vez se hayan "
                                                      "determinado los parametros de cada uno de los archivos "
                                                      "finales, la conversión se hará automáticamente. En el terminal "
                                                      "o consola (la ventana negra) aparecerán datos y error si lo "
                                                      "hubiera, así como un aviso cuando se terminen todas las "
                                                      "conversiones.")
conversor = Conversion()
timestamps = {
    "in": list(str()),
    "out": list(str()),
    "file": list(str()),
}
ciclos = int(input("¿Cuántos cortes a llevar a cabo?"))
for x in range(ciclos):
    print("Configurando archivo número " + str(x + 1))
    timestamps["in"].append(input("Entrada (ej. 00:00:00)>>"))
    timestamps["out"].append(input("Final (ej. 00:00:00)>>"))
    timestamps["file"].append(filedialog.asksaveasfile(title="Guardar archivo número " + str(x + 1)))
for x in range(ciclos):

    print("-------------------------------------------------\n"
          "Conversión número " + str(x + 1))
    conversor.trim(timestamps["in"][x], timestamps["out"][x], timestamps["file"][x])
print(Fore.GREEN + 'CONVERSIÓN TERMINADA')
input(Fore.RESET + "Pulse intro para cerrar>>")
exit(0)
