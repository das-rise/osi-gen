from traj_convert.carla2traj import Carla2Traj

if __name__ == "__main__":
    import argparse
    from rich_argparse import RichHelpFormatter

    parser = argparse.ArgumentParser(
        description="Convert CARLA trajectory data to OmegaPrime-compliant OSI format",
        epilog="""
Example usage: `python -m traj_convert traj.parquet 752 0.1.0 "" "Town01.xodr" -o output.osi`
To generate the CARLA trajectory parquet file, please confer the README.md in this repository.
        """,
        formatter_class=RichHelpFormatter,
    )
    parser.add_argument(
        "parquet_file",
        type=str,
        help="Path to the input parquet file containing trajectory data",
    )
    parser.add_argument(
        "country_code",
        type=int,
        help="ISO country code (int, e.g. 276 for Germany, 840 for USA)",
    )
    parser.add_argument(
        "version",
        type=str,
        help="OSI version string (X.Y.Z)",
    )
    parser.add_argument(
        "proj_string",
        type=str,
        nargs="?",
        default="",
        help="PROJ coordinate transformation string (default: empty)",
    )
    parser.add_argument(
        "map_reference",
        type=str,
        nargs="?",
        default="",
        help="Map reference, e.g. an OpenDRIVE file name (default: empty)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output file path (default: auto-generated with timestamp)",
    )

    args = parser.parse_args()

    # Load trajectory data from parquet file
    print(f"Loading trajectory data from {args.parquet_file} ...", end=" ")
    traj = Carla2Traj.from_file(args.parquet_file)
    print(f"Loaded {traj.df.height} frames.")

    # Determine output path
    if args.output is None:
        from datetime import datetime

        datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"trajectory_osi_{datetime_str}.osi"
    else:
        output_path = args.output

    from traj_convert.traj2osi import Traj2OSI

    converter_args = {
        "country_code": args.country_code,
        "version": args.version,
        "proj_string": args.proj_string,
        "map_reference": args.map_reference,
    }

    print("Converting to OSI format with:")
    print(f"  country_code: {args.country_code}")
    print(f"  version: {args.version}")
    print(f"  proj_string: {args.proj_string}")
    print(f"  map_reference: {args.map_reference}")

    traj.convert(Traj2OSI, output_path, converter_args)

    print(f"Conversion complete! Output saved to: {output_path}")
