# Addon Info
bl_info = {
    "name": "FBX Exporter",
    "description": "Export scene to FBX",
    "author": "Wolf",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View 3D > Properties Panel",
    "support": "COMMUNITY",
    "category": "Import-Export"
    }


import bpy
import os
import sys
from bpy.props import StringProperty, PointerProperty
from bpy.types import PropertyGroup, Panel, Operator


# Panel
class ExporterPanelFBX(Panel):
	bl_space_type = "VIEW_3D"
	bl_context = "objectmode"
	bl_region_type = "UI"
	bl_category = "Export"
	bl_label = "Export to FBX"

	def draw(self, context):
		layout = self.layout
		scn = context.scene

		# Export Button
		split = layout.split()
		col = split.column(align=True)
		row = col.row(align=True)
		row.scale_y = 1.5
		row.operator("export.fbx", icon="EXPORT", text="Export")

		# Directory
		layout.prop(scn.exporterprops, "directory", text="")

		# File Name
		layout.prop(scn.exporterprops, "filename", text="Name")


# Export
class EXPORT_OT_FBX(Operator):
	bl_idname = "export.fbx"
	bl_label = "Export FBX"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		location = bpy.context.scene.exporterprops.directory
		filen = bpy.context.scene.exporterprops.filename
		loc = location + filen + ".fbx"
		if location == "":
			self.report({'ERROR'}, "Choose an output path")
		else:
			bpy.ops.object.select_all(action='SELECT')
			bpy.ops.export_scene.fbx(filepath=loc, use_selection=True)
			text = "File exported in: " + loc
			self.report({'INFO'}, text)
			bpy.ops.object.select_all(action='DESELECT')
			return{'FINISHED'}


# Properties
class FBXExporterProperties(PropertyGroup):
	directory : StringProperty(
		name="Path",
		description="Choose the path to save the file",
		default="",
		subtype='FILE_PATH'
		)

	filename : StringProperty(
		name="Filename",
		description="Choose the file name",
		default="Test"
		)


#################################################################################

classes = (
	ExporterPanelFBX,
	EXPORT_OT_FBX,
	FBXExporterProperties
	)

register, unregister = bpy.utils.register_classes_factory(classes)

# Register
def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.Scene.exporterprops = PointerProperty(type=FBXExporterProperties)
    
def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)
	del bpy.types.Scene.exporterprops

if __name__ == "__main__":
	register()
