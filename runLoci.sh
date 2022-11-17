#  win
e:
cd E:\LociProjects
activate lociEnv
python main.py b.glb


# mac
conda activate lociEnv
cd /Users/harveyli/Documents/GitHub/Get_Metadata_from_glb-gltf
python main.py ./assets1/hat.glb original -g
python main.py ./assets1/hat.glb VC 10 -g
python main.py ./assets1/hat.glb VC 32 -g
python main.py ./assets1/hat.glb QD 12 -g
python main.py ./assets1/hat.glb QD 50 -g
