import carla
from typing import Tuple


class Carla2Traj:

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

    def _convert_coord_to_osi_x(self, x: float) -> float:
        return 0
    
    def _convert_coord_to_osi_y(self, y: float) -> float:
        return 0
    
    def _convert_coord_to_osi_z(self, z: float) -> float:
        return 0
    
    def _convert_carlaVector3D_to_osi(self, vector: carla.Vector3D) -> Tuple[float, float, float]:
        x_osi = self._convert_coord_to_osi_x(vector.x)
        y_osi = self._convert_coord_to_osi_y(vector.y)
        z_osi = self._convert_coord_to_osi_z(vector.z)
        return (x_osi, y_osi, z_osi)

    def add_map_reference(self, map_reference: str):
        self.map_reference = map_reference

    def add_country_code(self, country_code: int):
        self.country_code = country_code

    def add_version_major(self, version_major: int):
        self.version_major = version_major

    def add_version_minor(self, version_minor: int):
        self.version_minor = version_minor

    def add_version_patch(self, version_patch: int):
        self.version_patch = version_patch

    def add_proj_frame_offset_position(self, proj_frame_offset_position: tuple):
        self.proj_frame_offset_position = proj_frame_offset_position

    def add_proj_frame_offset_yaw(self, proj_frame_offset_yaw: float):
        self.proj_frame_offset_yaw = proj_frame_offset_yaw

    def add_proj_string(self, proj_string: str):
        self.proj_string = proj_string


    # TODO: add traffic lights