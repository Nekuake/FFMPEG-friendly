from tkinter import Tk, filedialog, messagebox
import os
import os.path
import shutil
import requests
import zipfile


class Carpetas:
    ruta = str()

    def __init__(self, rutaReferencia):
        self.ruta = rutaReferencia

    def inicializacionConcat(self):
        listOfFile = os.listdir(str(self.ruta))
        allFiles = list()
        with open('lista.txt', 'w') as f:
            for entry in listOfFile:
                rutadearchivo = os.path.join(self.ruta, entry)
                if not os.path.isdir(rutadearchivo):
                    allFiles.append(rutadearchivo)
                    for x in allFiles:
                        f.writelines('file ' + '"' + x + '"\n')
            f.close()
            with open('lista.txt', 'r') as fin:
                data = fin.read().splitlines(True)
            with open('lista.txt', 'w') as fout:
                fout.writelines(data[1:])


class Conversion:
    rutaFFMPEG = str()

    def __init__(self):
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

    def concat(self):
        carpeta = Carpetas(
            filedialog.askdirectory(title="Seleccionar carpeta contenedora de los archivos a concatenar..."))
        carpeta.inicializacionConcat()
        rutaLista = str(str(os.getcwd()) + "\lista.txt")
        rutaSalida = filedialog.asksaveasfile(title="Dónde guardar el archivo final")
        # ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.wav
        messagebox.showinfo("Concatenación iniciada", "Por favor, espere, el tiempo de espera puede variar según el "
                                                      "tamaño del archivo, la velocidad del disco duro o si el "
                                                      "archivo esá localizado en una ubicación de red. Si nota que "
                                                      "tarda mucho tiempo, puede probar, de cara a futuras "
                                                      "conversiones, a variar algunos de esos factores. Tenga en "
                                                      "cuenta que si la conversión da error, se avisará, por lo que "
                                                      "no cierre el programa.")

        comando = os.popen(self.rutaFFMPEG + " -hide_banner" + " -f" + " concat" + " -safe" + " 0" + ' -y -i "' +
                           rutaLista + '" -c ' + 'copy "' + rutaSalida.name + '"')
        messagebox.showinfo("Concatenación completada", "Puedes encontrar el archivo en " + rutaSalida.name)
        os.remove("lista.txt")
        comando.read()


print("FFMPEG Wrapper goes brummmm")
root = Tk()
root.withdraw()
root.attributes('-topmost', True)
conversor = Conversion()
conversor.concat()
input("Pulse intro para cerrar>>")
exit(0)
