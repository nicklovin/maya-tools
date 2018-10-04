import maya.cmds as cmds

curve_list = []


def arc_tool(cv_count=30):
    ''' Arc Visualizer Tool

    Args:
        cv_count(int): the number of frames that the user would like to
            visualize.  The curve will show half way forward and backward on a
            curve the arc of the movement
    '''
    global sel
    sel = cmds.ls(selection=True)[0]

    if not sel:
        cmds.warning('Could not find selection!')
        return

    starting_time = cmds.currentTime(query=True)
    backward_timeline = starting_time - (cv_count / 2)
    forward_timeline = starting_time + (cv_count / 2)

    position_list = []

    for i in range(cv_count):
        point = [i, 0, 0]
        position_list.append(point)

    points = tuple(position_list)

    global path_curve, position_frame_values_list, time_slider_max
    path_curve = cmds.curve(point=points,
                            degree=1,
                            name='arc_CRV')
    cmds.setAttr(path_curve + '.dispCV', 1)

    # get list of attributes that are keyed
    # query the all values of the attribute at each frame
    # append all values into a list
    # assign these values based on cmds.currentTime() to cv's on a curve

    position_frame_values_list = []

    time_slider_min = cmds.playbackOptions(query=True, minTime=True)
    time_slider_max = cmds.playbackOptions(query=True, maxTime=True)
    time_slider_range = time_slider_max - time_slider_min + 1

    frame_displacement = 1
    i = 0
    for frame in range(int(time_slider_range)):
        cmds.currentTime(time_slider_min + i)
        trans = cmds.xform(sel, query=True, translation=True, ws=True)
        position_frame_values_list.append(trans)
        frame_displacement = frame_displacement + 1
        i = i + 1

    frame_range = []

    a = (cv_count / 2)
    while backward_timeline <= forward_timeline:
        list_frame = starting_time - a
        frame_range.append(list_frame)
        backward_timeline = backward_timeline + 1
        a = a - 1

    for cv in range(cv_count):
        # in list frame_range, we have the frame number to assign to the cv
        # then pulls from the position_frame_values_list to get the values for
        # the object at that frame
        list_index_value = int(frame_range[cv] + 1)
        if list_index_value >= time_slider_max:
            cv_position = position_frame_values_list[int(time_slider_max - 1)]
        else:
            cv_position = position_frame_values_list[list_index_value]
        cmds.xform(path_curve + '.cv[' + str(cv) + ']',
                   translation=(cv_position[0], cv_position[1], cv_position[2]),
                   worldSpace=True)

    cmds.currentTime(starting_time)

    # setup the refresh condition
    global time_change, new_cv_count
    new_cv_count = cv_count

    time_change = cmds.scriptJob(
        event=['timeChanged', 'cv_refresh(path_curve, new_cv_count)'])
    curve_list.append(path_curve)


def cv_refresh(curve_update, cv_count):
    starting_time = cmds.currentTime(query=True)
    backward_timeline = starting_time - (cv_count / 2)
    forward_timeline = starting_time + (cv_count / 2)

    new_frame_range = []
    a = (cv_count / 2)
    while backward_timeline <= forward_timeline:
        list_frame = starting_time - a
        new_frame_range.append(list_frame)
        backward_timeline = backward_timeline + 1
        a = a - 1

    for cv in range(cv_count):
        # in list frame_range, we have the frame number to assign to the cv
        # then pulls from the position_frame_values_list to get the values for
        # the object at that frame
        list_index_value = int(new_frame_range[cv] + 1)
        if list_index_value >= time_slider_max:
            cv_position = position_frame_values_list[int(time_slider_max - 1)]
        else:
            cv_position = position_frame_values_list[list_index_value]
        cmds.xform(curve_update + '.cv[' + str(cv) + ']',
                   translation=(cv_position[0], cv_position[1], cv_position[2]),
                   worldSpace=True)


def kill_refresh():
    cmds.scriptJob(kill=time_change, force=True)
    if curve_list:
        cmds.delete(curve_list)
