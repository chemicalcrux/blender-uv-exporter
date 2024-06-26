import struct
from typing import Dict, Iterator, List, NamedTuple, Tuple

import bmesh
import bpy
from mathutils import Vector

from .context_managers import EnsureGeonodes

from . import props, ui, library
from .export import perform_export


class UV_Link_Libraries(bpy.types.Operator):
    bl_idname = "attribute_exporter.link_library"
    bl_label = "Link Library"
    bl_description = "Link data that the add-on depends on."

    def execute(self, context: bpy.types.Context):
        with bpy.data.libraries.load(library.BLEND_PATH, link=True) as (data_from, data_to):
            data_to.node_groups = data_from.node_groups

        print(library.get_vertex_node_tree())
        return {"FINISHED"}


class UV_Export(bpy.types.Operator):
    bl_idname = "attribute_exporter.export"
    bl_label = "Export Data"
    bl_description = "Export the currently selected package."

    def execute(self, context: bpy.types.Context):
        package = ui.get_current_package(context)

        try:
            perform_export(context, package)
        except ValueError as e:
            self.report({"ERROR"}, str(e))

        return {"FINISHED"}


class UV_Export_All(bpy.types.Operator):
    bl_idname = "attribute_exporter.export_all"
    bl_label = "Export All Data"
    bl_description = "Export every package."

    def execute(self, context: bpy.types.Context):
        for package in context.scene.attribute_exporter_packages:
            perform_export(context, package)

        return {"FINISHED"}


class UV_Refresh(bpy.types.Operator):
    bl_idname = "attribute_exporter.refresh"
    bl_label = "Refresh Attribute Choices"
    bl_description = "Re-calculate the list of attributes you can pick from."

    def execute(self, context: bpy.types.Context):
        props.refresh_attribute_choices(self, context)
        return {"FINISHED"}
