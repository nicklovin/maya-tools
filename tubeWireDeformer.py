import maya.cmds as cmds


def build_tube_wire(vertex_circumference, wire_name='test_wire',
                    lowpoly_crv=True):
    """
    Builds a curve through the inside center of a tube/cylinder geometry, that
    can be used to deform the geometry as a wire.

    Input the number of vertexes that go around the circumference of the tube,
    then select the tube geo and run command.

    Args:
        vertex_circumference (int): Input the number of vertices around the
            selected tube.
        wire_name (str): Name for the returned wire curve.
        lowpoly_crv (bool): Condition to build a low poly duplicate of the curve
            to control and manipulate geo with smoother results.

    """
    vert_selection = cmds.ls(selection=True)[0]
    vert_count = cmds.polyEvaluate(vert_selection, vertex=True)

    temp_geo = cmds.duplicate(vert_selection)[0]
    # 2018 specific command
    cmds.meshReorder(temp_geo + '.vtx[0]',
                     temp_geo + '.vtx[1]',
                     temp_geo + '.vtx[' + str(vertex_circumference) + ']')

    locator_list = []
    locator_kill_list = []

    index = 0
    index_end = vertex_circumference - 1
    while index <= vert_count:
        cmds.select(clear=True)
        if index == 0:
            # meshReorder command causes issues with the first two vertex loops,
            # so they are paired together as one loop for curve evaluation
            index_end = index_end + vertex_circumference
        cmds.select('%s.vtx[%s:%s]' %
                    (temp_geo, str(index), str(index_end)))
        temp_cluster = cmds.cluster()
        position_locator = cmds.spaceLocator()[0]
        locator_shape = position_locator.replace('locator', 'locatorShape')
        cluster_xform = cmds.getAttr(temp_cluster[1] + '.origin')[0]
        cmds.xform(position_locator, translation=cluster_xform, worldSpace=True)
        cmds.delete(temp_cluster)
        locator_kill_list.append(position_locator)
        locator_list.append(locator_shape + '.worldPosition[0]')

        index = index + vertex_circumference
        if index == 1:
            # Continuation for combining the first two vertex loops
            continue
        index_end = index_end + vertex_circumference
        # Loop breaker for testing
        if index > 2000 or index == 0:
            break

    locator_values_list = []
    for shape in locator_list:
        world_position = cmds.getAttr(shape)[0]
        # print world_position
        locator_values_list.append(world_position)
    # Last loop carries only 1 vertex, value is deleted.
    del locator_values_list[-1]

    tube_curve = cmds.curve(degree=1,
                            point=locator_values_list,
                            name=wire_name + '_CRV')
    cmds.delete(temp_geo, locator_kill_list)

    if lowpoly_crv:
        # Creates a more manageable low-poly curve that deforms the original
        low_tube_curve = cmds.rebuildCurve(tube_curve,
                                           replaceOriginal=False,
                                           name=wire_name + 'lowpoly_CRV',
                                           degree=3,
                                           spans=4,
                                           rebuildType=0,
                                           constructionHistory=False)
        cmds.wire(tube_curve, wire=low_tube_curve)
    cmds.wire(vert_selection, wire=tube_curve)
