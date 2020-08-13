from Drivers.Driver import Driver
from time import sleep
from picamera import PiCamera
from os import listdir
from os.path import expanduser
from os import makedirs
import subprocess

class Camera(Driver):
    def __init__(self):
        """
        Takes a picture
        """
        super().__init__("Camera")

        self.highRes = (3280, 2464)
        self.lowRes = (640, 480)
        self.pictureDirectoryPath = expanduser('~/Pictures')
        self.cam = None
        self.pictureNumber = 0

    def read(self):
        pass

    def takePicture(self):
        """
        Takes the picture
        """
        #the way to count folders in directory is len(os.listdir(path of directory to count in))
        #you have to import OS
        #This also counts files in the total, but with the file structure we came up with this shouldn't be a problem
        self.pictureNumber = len(listdir(self.pictureDirectoryPath))
        #count number of folders in directory, add 1 for current pic

        self.cam = PiCamera()
        self.cam.resolution = self.lowRes
        sleep(2)
        makedirs(self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/LowRes", exist_ok=True)
        self.cam.capture(self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/LowRes/LowResOriginal"+str(self.pictureNumber)+".jpg")
        self.cam.resolution = self.highRes
        makedirs(self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/HighRes", exist_ok=True)
        self.cam.capture(self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/HighRes/HighResOriginal"+str(self.pictureNumber)+".jpg")

    def compressLowResToFiles(self, pictureNumber):
        """
        Compresses the Low Res to files. Compresses with SSDV, converts from Hex to ASCII with xxd, splits into 128 byte files.
        """
        self.pictureNumber = pictureNumber
        #Set up paths for low res picture and creates the packets directory
        lowResOriginalPath = self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/LowRes/LowResOriginal"+str(self.pictureNumber)+".jpg"
        lowResSSDVPath = self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/LowRes/LowResOriginal"+str(self.pictureNumber)+".bin"
        lowResASCIIPath = self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/LowRes/LowResOriginal"+str(self.pictureNumber)+".txt"
        makedirs(self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/LowRes/Packets", exist_ok=True)
        lowResPacketPath = self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/LowRes/Packets/"


        ssdv_lowRes_picture = subprocess.run(["ssdv", "-e", lowResOriginalPath, lowResSSDVPath])
        xxd_lowRes_picture = subprocess.run(["xxd", lowResSSDVPath, lowResASCIIPath])
        split_lowRes_picture = subprocess.run(["split", "-b", "128", lowResASCIIPath, lowResPacketPath])

    def compressHighResToFiles(self,pictureNumber):
        """
        Compresses the Low Res to files. Compresses with SSDV, converts from Hex to ASCII with xxd, splits into 128 byte files.
        """
        self.pictureNumber = pictureNumber

        #Set up paths for high res picture and creates the packets directory
        highResOriginalPath = self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/HighRes/HighResOriginal"+str(self.pictureNumber)+".jpg"
        highResSSDVPath = self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/HighRes/HighResOriginal"+str(self.pictureNumber)+".bin"
        highResASCIIPath = self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/HighRes/HighResOriginal"+str(self.pictureNumber)+".txt"
        makedirs(self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/HighRes/Packets", exist_ok=True)
        highResPacketPath = self.pictureDirectoryPath+"/"+str(self.pictureNumber)+"/HighRes/Packets/"

        ssdv_highRes_picture = subprocess.run(["ssdv", "-e", highResOriginalPath, highResSSDVPath])
        xxd_highRes_picture = subprocess.run(["xxd", highResSSDVPath, highResASCIIPath])
        split_highRes_picture = subprocess.run(["split", "-b", "128", highResASCIIPath, highResPacketPath])

