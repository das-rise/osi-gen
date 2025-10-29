import carla
from typing import Tuple


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

        # Process each actor snapshot
        for actor_snapshot in world_snapshot:
            
            movingobject_id_value = actor_snapshot.id
            # use this id to get the actor bounding box from the list of all actors, world.get_actors()

            movingobject_base_dimension_x = None
            movingobject_base_dimension_y = None
            movingobject_base_dimension_z = None
            # use actor id from snapshot to get bounding box dimensions

            movingobject_base_position_x = None
            movingobject_base_position_y = None
            movingobject_base_position_z = None
            # actor_snapshot.get_transform().location

            movingobject_base_orientation_x = None
            movingobject_base_orientation_y = None
            movingobject_base_orientation_z = None
            # actor_snapshot.get_transform().rotation

            movingobject_base_velocity = None
            # actor_snapshot.get_velocity()
            movingobject_base_acceleration = None
            # actor_snapshot.get_acceleration()

            movingobject_type = None  # Other, Vehicle, Pedestrian, Animal

            movingobject_vehicleclassification_type = None  # Other, car, delivery van, semitrailer, trailer, motorbike, bicycle, bus, tram, train, wheelchair, standup scooter
            movingobject_vehicleclassification_role = None  # Other, civil, ambulance, fire, police, public transport, road assistance, garbage collection, road construction, military

    def _convert_geometry_to_osi_x(self, x: float) -> float:
        return 0
    
    def _convert_geometry_to_osi_y(self, y: float) -> float:
        return 0
    
    def _convert_geometry_to_osi_z(self, z: float) -> float:
        return 0
    
    def _convert_geometry_to_osi_carlaVector3D(self, vector: carla.Vector3D) -> Tuple[float, float, float]:
        x_osi = self._convert_geometry_to_osi_x(vector.x)
        y_osi = self._convert_geometry_to_osi_y(vector.y)
        z_osi = self._convert_geometry_to_osi_z(vector.z)
        return (x_osi, y_osi, z_osi)


    # TODO: add traffic lights