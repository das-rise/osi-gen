from traj import TrajDF
from polars import DataFrame
from typing import Generator, Any

NANOS_PER_SECOND = 1_000_000_000


class Traj2X:
    """Base class for trajectory format converters."""

    def __init__(self, traj_df: TrajDF):
        self._traj_df = traj_df

    def __call__(self, output_path: str):
        pass

    def _traverse_frames(self) -> Generator[DataFrame, Any, None]:
        # Generator to traverse the trajectory DataFrame frame by frame
        for frame, frame_data in self._traj_df.sort("frame").group_by("frame"):
            yield frame_data


class Traj2OpenLabel(Traj2X):
    """Converter to OpenLabel format."""

    def __call__(self, output_path: str):
        # Implement conversion to OpenLabel format
        pass


class Traj2OSI(Traj2X):
    """Converter to OSI format as specified in SYNERGIES OmegaPrime, https://github.com/ika-rwth-aachen/omega-prime/blob/main/docs/omega_prime_specification.md."""

    def __init__(
        self, traj_df: TrajDF, country_code: int, version: str, proj_string: str = ""
    ):
        super().__init__(traj_df)
        self._country_code = country_code
        self._version_major, self._version_minor, self._version_patch = map(
            int, version.split(".")
        )
        self._proj_string = proj_string

    def __call__(self, output_path: str):
        # Implement conversion to OSI format as defined in https://github.com/ika-rwth-aachen/omega-prime/blob/main/docs/omega_prime_specification.md
        import betterosi

        with betterosi.Writer(output_path) as writer_osi:
            for frame_data in self._traverse_frames():
                # for now, we only register moving objects
                moving_objects = []
                for object in frame_data.iter_rows(named=True):
                    base = betterosi.BaseMoving(
                        dimension=betterosi.Dimension3D(
                            length=object["dimension_x"],
                            width=object["dimension_y"],
                            height=object["dimension_z"],
                        ),
                        position=betterosi.Vector3D(
                            x=object["position_x"],
                            y=object["position_y"],
                            z=object["position_z"],
                        ),
                        orientation=betterosi.Orientation3D(
                            roll=object["orientation_x"],
                            pitch=object["orientation_y"],
                            yaw=object["orientation_z"],
                        ),
                        velocity=betterosi.Vector3D(
                            x=object["velocity"][0],
                            y=object["velocity"][1],
                            z=object["velocity"][2],
                        ),
                        acceleration=betterosi.Vector3D(
                            x=object["acceleration"][0],
                            y=object["acceleration"][1],
                            z=object["acceleration"][2],
                        ),
                    )
                    # TODO: fix type and vehicle classification mapping
                    moving_objects.append(
                        betterosi.MovingObject(
                            id=betterosi.Identifier(object["movingobject_id"]),
                            type=betterosi.MovingObjectType.UNKNOWN,
                            vehicle_classification=betterosi.MovingObjectVehicleClassification(
                                type=betterosi.MovingObjectVehicleClassificationType.UNKNOWN,
                                role=betterosi.MovingObjectVehicleClassificationRole.UNKNOWN,
                            ),
                        )
                    )
                # Create frame
                timestamp = frame_data["timestamp"][0]
                timestamp_seconds = int(timestamp)
                timestamp_nanos = int(
                    (timestamp - timestamp_seconds) * NANOS_PER_SECOND
                )

                ground_truth_frame = betterosi.GroundTruth(
                    version=betterosi.InterfaceVersion(
                        version_major=self._version_major,
                        version_minor=self._version_minor,
                        version_patch=self._version_patch,
                    ),
                    country_code=self._country_code,
                    timestamp=betterosi.Timestamp(
                        seconds=timestamp_seconds, nanos=timestamp_nanos
                    ),
                    moving_object=moving_objects,
                    host_vehicle_id=betterosi.Identifier(
                        0
                    ),  # assuming no host vehicle for now
                )

                writer_osi.add(ground_truth_frame)
