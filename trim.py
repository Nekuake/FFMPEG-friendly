from tkinter import Tk, filedialog, messagebox
import os
import os.path
import shutil
import requests
from colorama import Fore
import sys
from pyunpack import Archive


class Conversion:
    rutaFFMPEG = str()
    rutaArchivoIn = str()

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
                        sys.stdout.write(str(round(dl/1048576, 2)) + " MBytes of " + str(round(total_length/1048576,2))+ " MBytes")
                        sys.stdout.flush()

            Archive('ffmpeg.7z').extractall("\\temp")

            try:
                shutil.copyfile((os.getcwd() + "\\temp\\ffmpeg-5.0-essentials_build\\bin\\ffmpeg.exe"),
                                str(os.getcwd() + "\\ffmpeg.exe"))
            except:
                raise Exception(
                    "Can't find the extracted folder. Please, place ffmpeg.exe in the same folder as the script.")
            #shutil.rmtree(os.getcwd() + "\\temp")
            os.remove("ffmpeg.zip")
            messagebox.showinfo("FFMPEG downloaded", "FFMPEG downloaded successfully")
        self.rutaFFMPEG = str('"' + os.getcwd() + '\\ffmpeg.exe"')
        # Importar archivo a trimear
        self.rutaArchivoIn = str(
            '"' + filedialog.askopenfile(
                title="Select input file:").name + '"')

    def trim(self, time_in, time_out, output_path):
        # ffmpeg -ss [start] -i in.mp4 -to [end] -c copy -copyts out.mp4

        comando = os.popen(
            self.rutaFFMPEG + " -hide_banner -loglevel error -stats -ss " + time_in + " -y -i " + self.rutaArchivoIn + " -to " + time_out + " -c copy -copyts " + output_path.name)
        comando.read()


print("FFMPEG Trim")
root = Tk()
root.withdraw()
root.attributes('-topmost', True)
messagebox.showinfo("Please read", "This program is used to separate sections of a "
                                   "video file in a fast way since no "
                                   " re-encoding as in Premiere. It works as follows "
                                   " following: \n-First it checks if FFMPEG is downloaded, "
                                   "If it is not, it is downloaded and extracted automatically, "
                                   "The user does not have to do anything. \nThen they are asked "
                                   "how many sections to make of the video. There is no limit"
                                   "file by file, you ask for the entry and exit points "
                                   "output of each of the new files and where to save them and "
                                   "with what name. It is important to remember to add in the "
                                   " names the format, for example, .mp4 or .mov. Please note "
                                   " that empty files are created before the conversion to "
                                   "reserve the file name. If the file does not appear "
                                   " means that it is already finished. \n-Once you have "
                                   "Once the parameters for each of the final files "
                                   "final files, the conversion will be done automatically. In the terminal "
                                   "or console (the black window) will display data and error if "
                                   "and a warning when all the conversions are completed."
                                   "conversions are completed.")


conversor = Conversion()
timestamps = {
    "in": list(str()),
    "out": list(str()),
    "file": list(str()),
}
ciclos = int(input("How many output sections to make?"))
for x in range(ciclos):
    print("Configuring " + str(x + 1))
    timestamps["in"].append(input("Input (ej. 00:00:00)>>"))
    timestamps["out"].append(input("Output (ej. 00:00:00)>>"))
    timestamps["file"].append(filedialog.asksaveasfile(title="Save file number " + str(x + 1)))
for x in range(ciclos):
    print("-------------------------------------------------\n"
          "Triming number  " + str(x + 1))
    conversor.trim(timestamps["in"][x], timestamps["out"][x], timestamps["file"][x])
print(Fore.GREEN + 'CONVERTION FINISHED')
input(Fore.RESET + "Press Enter to exit")
exit(0)
