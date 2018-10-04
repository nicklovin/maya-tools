import maya.cmds as cmds


def assign_even_weights(vertex_circumference, upper_joint, lower_joint,
                        reorder_vertices=[]):
    """
    Assign even skin weight values to a pipe or tube geo shape for smooth, even
    deformations.

    Select the geo object with an active skin cluster, then execute.

    Args:
        vertex_circumference: Assign number of vertices the go around the
            circumference of the tube/pipe geo.
        upper_joint: The first joint with influence on the pipe.
        lower_joint: The second joint with influence on the pipe.
        reorder_vertices (list[str]): Vertex numbers for the renumbering at the
            lower end of the tube/pipe.  The first two vertices should be
            adjacent points at the base of the geo along the circumference.  The
            third vertex should be a perpendicular point in the direction of the
            upper pipe.
            List should be written as ['.vtx[a]', '.vtx[b]', '.vtx[c]']

    Returns:
        percent_list (dictionary): A dictionary of vertex loops and the
            corresponding weight values applied to the joints.  Can be used to
            diagnose issues and check for correct weight applications.

    """
    # Establish the shape node with the skin cluster
    vert_selection = cmds.ls(selection=True, shapes=True)
    if not vert_selection:
        vert_selection = cmds.listRelatives(children=True)
    # Skin cluster
    selection_skin = cmds.listConnections(vert_selection,
                                          source=True,
                                          exactType=True,
                                          type='skinCluster')[0]
    # Must use ONLY one shape value, otherwise it will do the sum of the list
    total_vertices = cmds.polyEvaluate(vert_selection[0], vertex=True)

    # Fractions for percent value assignments on vertices
    vertex_percent = 1 / (float(total_vertices) / float(vertex_circumference))
    inverse_percent = 1 - vertex_percent

    # Temp geo object for the mesh reordering (work with referenced files)
    temp_geo = cmds.duplicate(vert_selection)[0]

    # If no vertex values are given, a best guess will be made (not recommended)
    if not reorder_vertices:
        # 2018 specific command
        cmds.meshReorder(temp_geo + '.vtx[0]',
                         temp_geo + '.vtx[1]',
                         temp_geo + '.vtx[' + str(vertex_circumference) + ']')
    cmds.meshReorder(temp_geo + reorder_vertices[0],
                     temp_geo + reorder_vertices[1],
                     temp_geo + reorder_vertices[2])
    skin = cmds.skinCluster(temp_geo, upper_joint, lower_joint, tsb=True)[0]

    # Dictionary for returned keys and values if debugging needed later
    percent_list = {}
    # Mutable percent variable
    new_percent = vertex_percent
    index = 0
    index_end = vertex_circumference - 1
    while index <= total_vertices:
        verts = '%s.vtx[%s:%s]' % (temp_geo, str(index), str(index_end))
        cmds.skinPercent(skin, verts,
                         transformValue=[(lower_joint, inverse_percent),
                                         (upper_joint, new_percent)])
        percent_list[verts] = [new_percent, inverse_percent]

        new_percent = new_percent + vertex_percent
        inverse_percent = 1 - new_percent

        index_end = index_end + vertex_circumference
        index = index + vertex_circumference

        if not cmds.objExists(verts):
            cmds.warning('Function is evaluating more vertices than exist!  '
                         'Returned weights may not be correct.')
            break

    # Copy new weights to original geo; Mesh reorder no longer required
    cmds.copySkinWeights(sourceSkin=skin, destinationSkin=selection_skin,
                         noMirror=True)
    cmds.delete(temp_geo)
    return percent_list
