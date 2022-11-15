from gltflib import GLTF
import os
import open3d as o3d
import sys
import copy
import numpy as np

MESH_NAME = ''


def getFileSize(filename, roundDigit=2) -> float:
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


def exportToGLB(mesh, filename='assets1\\'+MESH_NAME+'-remesh'+'.glb')  -> None:
    o3d.io.write_triangle_mesh(filename, mesh)

# simplify mesh using Vertex clustering
# lower the degree value, more the simplification
def simplifyMeshVC(mesh, degree=32) -> o3d.geometry.TriangleMesh:
    voxel_size = max(mesh.get_max_bound() - mesh.get_min_bound()) / degree
    print(f'voxel_size = {voxel_size:e}')
    mesh_smp = mesh.simplify_vertex_clustering(
        voxel_size=voxel_size,
        contraction=o3d.geometry.SimplificationContraction.Average)
    return mesh_smp

# simplify mesh using Quadric Decimation
# lower the num_of_triangle value, more the simplification
def simplifyMeshQD(mesh, num_of_triangles) -> o3d.geometry.TriangleMesh:
    mesh_smp = mesh.simplify_quadric_decimation(
        target_number_of_triangles=num_of_triangles)
    return mesh_smp


def visualizeMesh(mesh) -> None:
    print(
        f'Simplified mesh has {len(mesh.vertices)} vertices and {len(mesh.triangles)} triangles'
    )
    o3d.visualization.draw_geometries([mesh])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: No .glb file specified')
    MESH_NAME = str(sys.argv[1])
    fileAddr = 'assets1\\'+MESH_NAME
    # get file size in byte, MB, KB, GB
    print(MESH_NAME+'\'s file size is :', getFileSize(fileAddr, roundDigit=2))

    # load mesh
    origMesh = o3d.data.BunnyMesh()
    # preprocess the mesh
    mesh = o3d.io.read_triangle_mesh(origMesh.path)
    mesh.compute_vertex_normals()

    visualizeMesh(mesh)
    mesh_smp_VC = simplifyMeshVC(mesh, degree=64)
    visualizeMesh(mesh_smp_VC)
    
    num_of_triangles = len(mesh.triangles)
    degree = 10
    mesh_smp_QD = simplifyMeshQD(mesh, num_of_triangles=int(num_of_triangles/degree))
    visualizeMesh(mesh_smp_QD)
