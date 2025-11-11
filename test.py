from carla2traj import Carla2Traj
from traj2x import Traj2OSI

traj = Carla2Traj.from_file("../synergies-carla-scenic/RiRun/traj_20251111_134532.parquet")  # Load existing trajectory data

traj.convert(Traj2OSI, "output.osi", converter_args={"country_code": 752, "version": "0.1.0"})  # Convert and save to OSI format