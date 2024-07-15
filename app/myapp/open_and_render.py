# import os
# import sys

# blender_path = "E:\Projects\Python\Ivan\blender-3.2.2\3.2\python\bin"
# sys.path.append(blender_path)
# os.environ["PYTHONPATH"] = blender_path



import bpy
import sys

def main(blend_file_path):
    # Load the Blender file
    bpy.ops.wm.open_mainfile(filepath=blend_file_path)

    # Render with multiple instances
    bpy.ops.object.gpu_instance_render()

if __name__ == "__main__":
    # Assuming the Blender file path is the last argument passed to the script
    blend_file_path = sys.argv[-1]
    main(blend_file_path)