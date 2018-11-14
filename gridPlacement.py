import maya.cmds as cmds
from random import randint


def build_grid():
    """
    Creates a plane to act as a grid for the set_to_grid function.  Also creates
    a Heads Up Display to feed instructions.

    Returns:
        A polyPlane named 'placementGrid'.

    """
    cmds.polyPlane(name='placementGrid')
    if cmds.headsUpDisplay('HUD_grid_message', exists=True):
        cmds.headsUpDisplay('HUD_grid_message', remove=True)
    cmds.headsUpDisplay('HUD_grid_message',
                        section=6,
                        block=1,
                        blockSize='large',
                        label='Adjust polyPlane parameters to fit the needs of '
                              'the grid.  Then select the objects to constrain '
                              'to the grid.',
                        labelFontSize='large',
                        labelWidth=100)


def set_to_grid(grid='placementGrid', input_objects=[], step=1):
    """
    Sets objects/rigs/etc. to points on a selected or created grid.  Select all
    objects that should be constrained to the grid before executing.  If not
    using the default grid funciton to build your grid (custom grid), then
    select the grid object after selecting the input objects.

    Args:
        grid (str): Assign a grid object by its name.  If none given or the
            default name does not exist, then the last object in the selection
            list will be used.
        input_objects (list[str]): Assign objects to be constrained to the grid.
        step (int): Assign a step count for the grid placement if desired.

    """
    if not input_objects:
        input_objects = cmds.ls(selection=True)
    if not cmds.objExists(grid):
        grid = cmds.ls(selection=True)[-1]

    # Kill HUD if created from previous command
    if cmds.headsUpDisplay('HUD_grid_message', exists=True):
        cmds.headsUpDisplay('HUD_grid_message', remove=True)

    # Dependency checks
    if not input_objects:
        cmds.warning('No selection found! Select all objects to constrain to '
                     'the grid.')
        return
    if not grid:
        cmds.warning('No grid selection found! If object "placementGrid" does '
                     'not exist, create a polyPlane and add it to selection '
                     'after objects to be constrained')
        return

    vertex_count = cmds.polyEvaluate(grid, vertex=True)

    print (len(input_objects) * step), vertex_count
    if (len(input_objects) * step) > vertex_count:
        cmds.warning('Grid is not large enough to constrain all selected '
                     'objects! Overflow objects will be ignored.')

    for vertex in range(0, vertex_count):
        locator = cmds.spaceLocator(name='gridPoint_%s_LOC' % str(vertex))
        vertex_position = cmds.xform(grid + '.vtx[' + str(vertex * step) + ']',
                                     query=True,
                                     translation=True,
                                     worldSpace=True)
        cmds.xform(locator,
                   translation=[vertex_position[0],
                                vertex_position[1],
                                vertex_position[2]],
                   worldSpace=True)
        cmds.parent(locator, grid)
        cmds.pointConstraint(locator, input_objects[vertex])

        if vertex >= (len(input_objects) - 1) or \
                input_objects[vertex + 1] == grid or \
                (vertex + 1) * step >= vertex_count:
            break


def kill_message():
    """
    Kills the Heads Up Display message created by the build_grid command if it
        still exists.  Function serves as a backup if it isn't deleted by
        another command.

    """
    if cmds.headsUpDisplay('HUD_grid_message', exists=True):
        cmds.headsUpDisplay('HUD_grid_message', remove=True)


def assign_dot_color():
    selection = cmds.ls(selection=True)
    for item in selection:
        dot_color = randint(1, 15)
        cmds.setAttr(item + '.dotColor', dot_color)
