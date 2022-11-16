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

# simplify mesh using Vertex clustering
# lower the degree value, more the simplification
# http://www.open3d.org/docs/release/tutorial/geometry/mesh.html#Mesh-simplification
def simplifyMeshVC(mesh, degree=32) -> o3d.geometry.TriangleMesh:
    voxel_size = max(mesh.get_max_bound() - mesh.get_min_bound()) / degree
    mesh_smp = mesh.simplify_vertex_clustering(
        voxel_size=voxel_size,
        contraction=o3d.geometry.SimplificationContraction.Average)
    return mesh_smp

# simplify mesh using Quadric Decimation
# lower the num_of_triangle value, more the simplification
# http://www.open3d.org/docs/release/tutorial/geometry/mesh.html#Mesh-simplification
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
    
    # check arguments and file existence
    if len(sys.argv) < 2:
        raise Exception('Error: No .glb file specified!')
    fileAddr = str(sys.argv[1])
    if len(sys.argv) < 3:
        raise Exception('Error: No operation specified!')
    operation = str(sys.argv[2])
    
    if os.path.exists(fileAddr) == False:
        raise Exception('Error: File not found!')
        
    # get file size in byte, MB, KB, GB
    print(fileAddr+'\'s file size is :', getFileSize(fileAddr, roundDigit=2))

    # load and preprocess mesh
    print(f'Loading mesh {fileAddr} ...')
    mesh = o3d.io.read_triangle_mesh(fileAddr)
    
    
    # origMesh = o3d.data.BunnyMesh()
    # mesh = o3d.io.read_triangle_mesh(origMesh.path)
    
    
    mesh.compute_vertex_normals()

    
    # handle operations
    if operation == 'original':
        o3d.io.write_triangle_mesh('original.glb', mesh)
        print(f'Visualizing original mesh...')
        visualizeMesh(mesh)
        exit(0)
        
    if operation == 'VC':
        if len(sys.argv) < 4:
            raise Exception('Error: VC operation has no degree specified!')
        degree = int(sys.argv[3])
        mesh_smp_VC = simplifyMeshVC(mesh, degree)
        o3d.io.write_triangle_mesh(f'VC_{degree}.glb', mesh_smp_VC)
        print(f'Visualizing simplified mesh using simplify_vertex_clustering ...')
        visualizeMesh(mesh_smp_VC)
        exit(0)
    
    if operation == 'QD':
        if len(sys.argv) < 4:
            raise Exception('Error: QD operation has no degree specified!')
        degree = int(sys.argv[3])
        num_of_triangles = len(mesh.triangles)
        mesh_smp_QD = simplifyMeshQD(mesh, num_of_triangles=int(num_of_triangles/degree))
        o3d.io.write_triangle_mesh(f'QD_{degree}.glb', mesh_smp_QD)
        print(f'Visualizing simplified mesh using simplify_quadric_decimation ...')
        visualizeMesh(mesh_smp_QD)
        exit(0)
        
    
    raise Exception('Error: Operation not found')
