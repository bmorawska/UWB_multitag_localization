from pypozyx import PozyxSerial, get_first_pozyx_serial_port, PositionError, SingleRegister, FilterData, DeviceList

serial_port = get_first_pozyx_serial_port()
if serial_port is not None:
    pozyx = PozyxSerial(serial_port)
else:
    print("No Pozyx port was found")
    exit(-1)

number_of_anchors = SingleRegister()
pozyx.getNumberOfAnchors(number_of_anchors)
print(f"Visible anchors:\t{number_of_anchors}")

anchor_list = DeviceList(list_size=number_of_anchors[0])
pozyx.getPositioningAnchorIds(anchor_list)
print(f"Anchros ids:\t\t{anchor_list}.")


algorithm = SingleRegister()
pozyx.getPositionAlgorithm(algorithm)
if algorithm == 0:
    algorithm = "POSITIONING_ALGORITHM_UWB_ONLY"
elif algorithm == 3:
    algorithm = "POSITIONING_ALGORITHM_NONE"
elif algorithm == 4:
    algorithm = "POSITIONING_ALGORITHM_TRACKING"
print(f"Positioning algorithm:\t{algorithm}")

position_dimension = SingleRegister()
pozyx.getPositionDimension(position_dimension)
if position_dimension == 1:
    position_dimension = "DIMENSION_2_5D"
elif position_dimension == 2:
    position_dimension = "DIMENSION_2D"
elif position_dimension == 3:
    position_dimension = "DIMENSION_3D"
print(f"Position dimension:\t{position_dimension}")

position_error = PositionError()
pozyx.getPositionError(position_error)
print(f"Position error:\t\t{position_error}")


filter_data = FilterData()
pozyx.getPositionFilterData(filter_data)
print(f"Filter data:\t\t{filter_data}")
