from tkinter import Tk, filedialog, messagebox
import os
import os.path
import shutil
import requests
import sys
from pyunpack import Archive


class Carpetas:

    def __init__(self, reference_path):
        self.ruta = reference_path

    def init_concat(self):
        list_of_file = os.listdir(str(self.ruta))
        all_files = list()
        with open('lista.txt', 'w') as f:
            for entry in list_of_file:
                rutadearchivo = os.path.join(self.ruta, entry)
                if not os.path.isdir(rutadearchivo):
                    all_files.append(rutadearchivo)
                    for x in all_files:
                        f.writelines('file ' + '"' + x + '"\n')
            f.close()
            with open('lista.txt', 'r') as fin:
                data = fin.read().splitlines(True)
            with open('lista.txt', 'w') as fout:
                fout.writelines(data[1:])


class Conversion:
    rutaFFMPEG = str()

    def __init__(self):
        # Importar FFMPEG
        if not os.path.isfile('ffmpeg.exe'):
            messagebox.showinfo("FFMPEG BINARY NOT FOUND", "Since the FFMPEG executable is not found, you will "
                                                           " will have to be downloaded. Please make sure you "
                                                           "have an active and functional internet connection. "
                                                           "This may take a few seconds, please wait. ")

            link = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.7z"
            file_name = "ffmpeg.7zip"
            with open(file_name, "wb") as f:
                print("Downloading %s" % file_name)
                response = requests.get(link, stream=True)
                total_length = response.headers.get('content-length')
                if total_length is None:
                    f.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=2048):
                        dl += len(data)
                        f.write(data)
                        done = int(50 * dl / total_length)
                        sys.stdout.write("\r[%s%s] " % ('=' * done, ' ' * (50 - done)))
                        sys.stdout.write(str(round(dl / 1048576, 2)) + " MBytes of " + str(
                            round(total_length / 1048576, 2)) + " MBytes")
                        sys.stdout.flush()

            Archive('ffmpeg.7z').extractall("\\temp")

            try:
                shutil.copyfile((os.getcwd() + "\\temp\\ffmpeg-5.0-essentials_build\\bin\\ffmpeg.exe"),
                                str(os.getcwd() + "\\ffmpeg.exe"))
            except:
                raise Exception(
                    "Can't find the extracted folder. Please, place ffmpeg.exe in the same folder as the script.")
            # shutil.rmtree(os.getcwd() + "\\temp")
            os.remove("ffmpeg.zip")
            messagebox.showinfo("FFMPEG downloaded", "FFMPEG downloaded successfully")
        self.rutaFFMPEG = str('"' + os.getcwd() + '\\ffmpeg.exe"')

    def concat(self):
        carpeta = Carpetas(
            filedialog.askdirectory(title="Select folder of files to concat..."))
        carpeta.init_concat()
        list_path = str(str(os.getcwd()) + "\\lista.txt")
        output_path = filedialog.asksaveasfile(title="Save output file...")
        # ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.wav
        messagebox.showinfo("Concat started", "Please wait, the waiting time may vary depending on the "
                                              "file size, hard disk speed or if the "
                                              "file is located in a network location. If you notice that "
                                              " takes a long time, you can try, for future "
                                              " conversions, to vary some of these factors. Keep in "
                                              " note that if the conversion fails, a warning will be given, so "
                                              "do not close the program.")

        command = os.popen(self.rutaFFMPEG + " -hide_banner" + " -f" + " concat" + " -safe" + " 0" + ' -y -i "' +
                           list_path + '" -c ' + 'copy "' + output_path.name + '"')
        messagebox.showinfo("Concatenación completada", "Puedes encontrar el archivo en " + output_path.name)
        os.remove("lista.txt")
        command.read()


print("FFMPEG concat")
root = Tk()
root.withdraw()
root.attributes('-topmost', True)
conversor = Conversion()
conversor.concat()
input("Press intro to exit>>")
exit(0)
