from traj import TrajDF
import betterosi

class Traj2X:
    def __call__(self, traj_df: TrajDF, output_path: str):
        pass


class Traj2OpenLabel(Traj2X):
    def __call__(self, traj_df: TrajDF, output_path: str):
        # Implement conversion to OpenLabel format
        pass


class Traj2OSI(Traj2X):
    def __call__(self, traj_df: TrajDF, output_path: str):
        # Implement conversion to OSI format as defined in https://github.com/ika-rwth-aachen/omega-prime/blob/main/docs/omega_prime_specification.md
        pass