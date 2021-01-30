# defaultdict supports multimap (multiple values for the same key)
from collections import defaultdict
import hashlib
import os
import sys




# Provides:
# Finds files of the same size
# List of file paths that are identical
class FileDeduplicator:

    # Interface ----------------------------------
    def __init__(self):
        self.name = "FileDeduplicator: "

        # 64kb chunks for file hashing
        self.BUFFER_SIZE = 65536

        print(self.name + "Initializing")

    # Returns a list of file sizes, each with a list of filenames of that size
    # In: root directory
    # Out: ex: [{10, {file1, file2}}, {20, {file3}} ]
    def getSizeBasedFiles(self, rootDir):
        print(self.name + "Getting files based on size from root dir: " + rootDir)

        if not os.path.exists(rootDir):
            print(self.name + "[" + rootDir + "] does not exist")
            return []

        sizedFilesDict = defaultdict(set)

        for rootDir1, _, files in os.walk(rootDir):
            pathedFiles = [rootDir1 + os.sep + file for file in files]

            # TODO: add try-catch for FileNotFoundError
            # Ignore symlinks
            [sizedFilesDict[os.path.getsize(file)].add(file) for file in pathedFiles if not os.path.islink(file)]

        return sizedFilesDict


    # Returns list of file sizes with multiple file paths
    # In: root directory
    # Out: ex: [{10, {a.txt, b.txt}}, {400, {c.txt, d.txt}}]
    def getSameSizedFiles(self, rootDir):
        print(self.name + "Getting same-sized files from root dir: " + rootDir)

        sizeBasedFiles = self.getSizeBasedFiles(rootDir)
        return {size: files for (size, files) in sizeBasedFiles.items() if len(files) > 1}


    def getDuplicateFiles(self, sameSizedFiles):
        print(self.name + "Getting possible duplicate files from " + str(len(sameSizedFiles)) + " file sizes")

        return {}


    def writeOutputFile(self, sameSizedFiles, outputFile):
        print(self.name + "Writing " + str(len(sameSizedFiles)) + " possible duplicate file clusters to output file: " + outputFile)

        with open(outputFile, "w") as out:
            {self._printSize(out, size, paths) for (size, paths) in sorted(sameSizedFiles.items(), reverse=True)}



    # Private ------------------------------------

    def _printSize(self, out, size, paths):
        print(self.name + "Printing file size: " + str(size))
        print(size, file=out)

        {self._printHash(out, path) for path in paths}

        print(file=out)


    def _printHash(self, out, path):
        fileHash = self._getFileHash(path)

        print("  ", fileHash, path, file=out)



    def _getFileHash(self, filePath):
        sha256 = hashlib.sha256()

        # From: https://stackoverflow.com/a/22058673
        with open(filePath, 'rb') as file:
            dataChunk = file.read(self.BUFFER_SIZE)

            while dataChunk:
                sha256.update(dataChunk)
                dataChunk = file.read(self.BUFFER_SIZE)

        return sha256.hexdigest()



# --------- Main --------------------

if '__main__' == __name__:
    rootDir = ""

    dedup = FileDeduplicator()

    sameSizedFiles = dedup.getSameSizedFiles(rootDir)
    
    dedup.writeOutputFile(sameSizedFiles, "/home/builder/RAM/dedup-" + os.path.basename(os.path.dirname(rootDir)) + ".txt")

    # print(dedup.getDuplicateFiles(sameSizedFiles))
