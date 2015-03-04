import os 

def findFilelist(extension, rootDir = '..'):
    fileList = []

    for root, subFolders, files in os.walk(rootDir):
        for file in files:
            if file.find(extension) != -1:
                fileList.append(file)

    return fileList

if __name__ == '__main__':
    
    footFileList = findFilelist('.kicad_mod')
    footprints = '\n'.join(footFileList)

    with open('footprints.txt', 'w') as f:
        f.write(footprints)

    modFileList = findFilelist('.lib')
    modules = '\n'.join(modFileList)

    with open('modules.txt', 'w') as f:
        f.write(modules)
