import carla
import polars as pl
from typing import Tuple

class Carla2Traj:

    def __init__(self, world: carla.World, debug: bool = False):
        self._world = world
        self._debug = debug
        self.df = pl.DataFrame(schema={
            'frame': pl.Int64,
            'timestamp': pl.Float64,
            'movingobject_id': pl.Int64,
            'dimension_x': pl.Float64,
            'dimension_y': pl.Float64,
            'dimension_z': pl.Float64,
            'position_x': pl.Float64,
            'position_y': pl.Float64,
            'position_z': pl.Float64,
            'orientation_x': pl.Float64,
            'orientation_y': pl.Float64,
            'orientation_z': pl.Float64,
            'velocity': pl.Float64,
            'acceleration': pl.Float64,
            'type': pl.Utf8,
            'vehicleclassification_type': pl.Utf8,
            'vehicleclassification_role': pl.Utf8
        })

        self._first_frame = None

    def process_world_snapshot(self, world_snapshot: carla.WorldSnapshot):

        timestamp = world_snapshot.timestamp.elapsed_seconds
        frame_number = self._get_frame(world_snapshot)

        # Process each actor snapshot
        for actor_snapshot in world_snapshot:
            
            movingobject_id_value = actor_snapshot.id
            actor = self._get_actor(movingobject_id_value)

            actor_type = self._get_type_from_carla_actor(actor)
            if actor_type is None:
                continue  # Skip unknown actor types

            bounding_box_extent = self._get_extent_from_carla_bounding_box(actor.bounding_box)
            dimension_x = bounding_box_extent[0]
            dimension_y = bounding_box_extent[1]
            dimension_z = bounding_box_extent[2]
            # use actor id from snapshot to get bounding box dimensions

            position_x = actor_snapshot.get_transform().location.x
            position_y = actor_snapshot.get_transform().location.y
            position_z = actor_snapshot.get_transform().location.z

            orientation_x = actor_snapshot.get_transform().rotation.pitch
            orientation_y = actor_snapshot.get_transform().rotation.yaw
            orientation_z = actor_snapshot.get_transform().rotation.roll

            velocity = actor_snapshot.get_velocity().length()
            acceleration = actor_snapshot.get_acceleration().length()

            vehicleclassification_type = None 
            vehicleclassification_role = None

            # Append data to DataFrame
            new_row = {
                'frame': frame_number,
                'timestamp': timestamp,
                'movingobject_id': movingobject_id_value,
                'dimension_x': dimension_x,
                'dimension_y': dimension_y,
                'dimension_z': dimension_z,
                'position_x': position_x,
                'position_y': position_y,
                'position_z': position_z,
                'orientation_x': orientation_x,
                'orientation_y': orientation_y,
                'orientation_z': orientation_z,
                'velocity': velocity,
                'acceleration': acceleration,
                'type': actor_type or 'Other',
                'vehicleclassification_type': vehicleclassification_type or 'Other',
                'vehicleclassification_role': vehicleclassification_role or 'Other'
            }

            if self._debug:
                print(f"[CARLA2TRAJ] Processed actor ID {movingobject_id_value} at timestamp {timestamp}")
                print(new_row['frame'])

    def _get_frame(self, world_snapshot: carla.WorldSnapshot) -> int: 
        # Calculate frame number in current run by subtracting first frame of this run
        # (Carla has a global frame counter counting from when the simulator was started)
        if self._first_frame is None:
            self._first_frame = world_snapshot.frame  
        return world_snapshot.frame - self._first_frame

    def _get_actor(self, actor_id: int) -> carla.Actor:
        try:
            return [actor for actor in self._world.get_actors() if actor.id == actor_id][0]
        except IndexError:
            raise ValueError(f"No actor found with ID {actor_id}")
        
    def _get_extent_from_carla_bounding_box(self, bounding_box: carla.BoundingBox) -> Tuple[float, float, float]:
        """Convert CARLA bounding box extent to OSI dimensions (x, y, z).
        
        Args:
            bounding_box: CARLA bounding box

        Returns:
            Extents in OSI coordinates as (ext_x, ext_y, ext_z)
        """
        extent = bounding_box.extent
        # The bounding box vector in carla is half-extent, so double it
        return tuple(2 * abs(coord) for coord in self._convert_carlaVector3D_to_osi(extent))
        
    def _get_type_from_carla_actor(self, actor: carla.Actor) -> str:
        TYPES = ["Other", "Vehicle", "Pedestrian", "Animal"]
        type_id = actor.type_id
        if type_id.split(".")[0] == "vehicle":
            return "Vehicle"

    def _convert_coord_to_osi_x(self, x: float) -> float:
        return x
    
    def _convert_coord_to_osi_y(self, y: float) -> float:
        return y
    
    def _convert_coord_to_osi_z(self, z: float) -> float:
        return z
    
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