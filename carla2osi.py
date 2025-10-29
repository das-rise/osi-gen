import carla


class Carla2OSI:

    def __init__(
        self,
        map_reference: str,
        country_code: int,
        version_major: int,
        version_minor: int,
        version_patch: int,
        proj_frame_offset_position: tuple,
        proj_frame_offset_yaw: float,
        proj_string: str,
    ):
        self.map_reference = map_reference
        self.country_code = country_code
        self.version_major = version_major
        self.version_minor = version_minor
        self.version_patch = version_patch
        self.proj_frame_offset_position = proj_frame_offset_position
        self.proj_frame_offset_yaw = proj_frame_offset_yaw
        self.proj_string = proj_string

    def process_world_snapshot(self, world_snapshot: carla.WorldSnapshot):

        timestamp = world_snapshot.timestamp

        for actor_snapshot in world_snapshot:
            # Process each actor snapshot
            movingobject_id_value = actor_snapshot.id

            movingobject_base_dimension_x = None
            movingobject_base_dimension_y = None
            movingobject_base_dimension_z = None

            movingobject_base_position_x = None
            movingobject_base_position_y = None
            movingobject_base_position_z = None

            movingobject_base_orientation_x = None
            movingobject_base_orientation_y = None
            movingobject_base_orientation_z = None

            movingobject_base_velocity = None
            movingobject_base_acceleration = None

            movingobject_type = None  # Other, Vehicle, Pedestrian, Animal

            movingobject_vehicleclassification_type = None  # Other, car, delivery van, semitrailer, trailer, motorbike, bicycle, bus, tram, train, wheelchair, standup scooter
            movingobject_vehicleclassification_role = None  # Other, civil, ambulance, fire, police, public transport, road assistance, garbage collection, road construction, military

    
    # TODO: add traffic lights