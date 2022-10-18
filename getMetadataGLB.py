from gltflib import GLTF
import os

MESH_NAME = 'pbnik.glb'


def writeToRecord(data, filename=''):
    f = open(MESH_NAME + '-' + filename+'.txt', 'a')
    f = open(MESH_NAME + '-' + filename+'.txt', 'w')
    f.write(formatOutput(str(data))+'\n\n')
    f.close()


def formatOutput(data):
    return str(data).replace(', ', ',\n').replace('{', '{\n').replace('}', '\n}').replace('[', '[\n').replace(']', '\n]').replace('(', '(\n').replace(')', '\n)')


def getFileSize(filename, roundDigit=2):
    size = os.path.getsize(filename)
    if(size == 0):
        return '0 byte'
    if(size == 1):
        return '1 byte'
    if(size > 1024):
        size = size/1024
        if(size > 1024):
            size = size/1024
            return str(round(size, roundDigit))+' MB'
        else:
            return str(round(size, roundDigit))+' KB'
    if(size > 1024):
        size = size/1024
        return str(round(size, roundDigit))+' MB'
    if(size > 1024):
        size = size/1024
        return str(round(size, roundDigit))+' GB'
    return str(round(size, roundDigit))+' bytes'


if __name__ == '__main__':
    fileAddr = 'assets1\\'+MESH_NAME
    # get file size in byte, MB, KB, GB
    print(MESH_NAME+'\'s file size is :', getFileSize(fileAddr, roundDigit=2))

    # get metadata from glb file
    glb = GLTF.load(fileAddr)
    data = glb.model
    images_data = data.images
    materials_data = data.materials
    meshes_data = data.meshes
    scenes_data = data.scenes
    textures_data = data.textures

    # print metadata
    print('# of Materials:', len(materials_data))
    print('# of Meshes:', len(meshes_data))
    print('# of Scenes:', len(scenes_data))
    print('# of Images:', len(images_data))
    print('# of Textures:', len(textures_data))

    # record metadata details to txt file
    # writeToRecord(materials_data, 'materials_data')
    # writeToRecord(meshes_data, 'meshes_data')
    # writeToRecord(scenes_data, 'scenes_data')
    # writeToRecord(images_data, 'images_data')
    # writeToRecord(textures_data, 'textures_data')
