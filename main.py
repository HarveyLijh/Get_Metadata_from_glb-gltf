from gltflib import GLTF
import os
import trimesh
import sys

MESH_NAME = ''


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


def subdivide(mesh, numSubdivisions):
    if numSubdivisions == 0:
        return mesh
    else:
        numSubdivisions = numSubdivisions - 1
        return subdivide(mesh.subdivide(), numSubdivisions)


def subdivide_remesh(mesh, numSubdivisions):
    if numSubdivisions == 0:
        return mesh
    else:
        numSubdivisions = numSubdivisions - 1
        new_vertices, new_faces = trimesh.remesh.subdivide(
            mesh.vertices, mesh.faces, face_index=None, vertex_attributes=None, return_index=False)
        newMesh: trimesh.Trimesh = trimesh.Trimesh(
            vertices=new_vertices, faces=new_faces)
        return subdivide_remesh(newMesh, numSubdivisions)


def subdivide_to_size(mesh, numSubdivisions):
    if numSubdivisions == 0:
        return mesh
    else:
        numSubdivisions = numSubdivisions - 1
        new_vertices, new_faces = trimesh.remesh.subdivide_to_size(
            mesh.vertices, mesh.faces, max_edge=0.01, max_iter=10, return_index=False)
        newMesh: trimesh.Trimesh = trimesh.Trimesh(
            vertices=new_vertices, faces=new_faces)
        return subdivide_to_size(newMesh, numSubdivisions)

def exportToGLTF(mesh, filename='assets1\\'+MESH_NAME+'-remesh'+'.glb'):
    mesh.export(filename)
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: No .glb file specified')
    MESH_NAME = str(sys.argv[1])
    fileAddr = 'assets1\\'+MESH_NAME
    # get file size in byte, MB, KB, GB
    print(MESH_NAME+'\'s file size is :', getFileSize(fileAddr, roundDigit=2))

    mesh: trimesh.Trimesh = trimesh.load(fileAddr, force="mesh")
    new_vertices, new_faces = trimesh.remesh.subdivide(
        mesh.vertices, mesh.faces, face_index=None, vertex_attributes=None, return_index=False)
    
    for i in range(3):
        meshC = (subdivide(mesh, i+1))
        print("Subdivide %(times)d times, Faces#: %(faces)d, Vertices#: %(vertices)d" % {
              'times': i, 'faces': len(meshC.faces), 'vertices': len(meshC.vertices)})
    for i in range(3):
        meshC = (subdivide_remesh(mesh, i+1))
        print("Remsh.subdivide %(times)d times, Faces#: %(faces)d, Vertices#: %(vertices)d" % {
            'times': i, 'faces': len(meshC.faces), 'vertices': len(meshC.vertices)})
        
    for i in range(3):
        meshC = (subdivide_to_size(mesh, i+1))
        print("Remsh.subdivide_to_size %(times)d times, Faces#: %(faces)d, Vertices#: %(vertices)d" % {
            'times': i, 'faces': len(meshC.faces), 'vertices': len(meshC.vertices)})
