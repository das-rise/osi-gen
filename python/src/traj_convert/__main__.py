from traj_convert.carla2traj import Carla2Traj

if __name__ == "__main__":
    import argparse
    from rich_argparse import RichHelpFormatter

    parser = argparse.ArgumentParser(
        description="Convert CARLA trajectory data to OmegaPrime-compliant OSI or OpenLabel format",
        epilog="""
Example usage: `python carla2traj.py traj.parquet osi 752 0.1.0 "" "Town01.xodr" -o output.osi`
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
        "format",
        type=str,
        choices=["osi", "openlabel"],
        help="Output format: 'osi' or 'openlabel'",
    )
    parser.add_argument(
        "arg1",
        type=int,
        help="For OSI: ISO country_code (int), For OpenLabel: dummy argument A",
    )
    parser.add_argument(
        "arg2",
        type=str,
        help="For OSI: version (X.Y.Z), For OpenLabel: dummy argument B",
    )
    parser.add_argument(
        "arg3",
        type=str,
        nargs="?",
        default=None,
        help="For OSI: proj_string (str) (optional for OpenLabel)",
    )
    parser.add_argument(
        "arg4",
        type=str,
        nargs="?",
        default=None,
        help="For OSI: map_reference (str) (optional for OpenLabel)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output file path (default: auto-generated based on format)",
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
        if args.format == "osi":
            output_path = f"trajectory_osi_{datetime_str}.osi"
        else:
            output_path = f"trajectory_openlabel_{datetime_str}.json"
    else:
        output_path = args.output

    # Convert based on selected format
    if args.format == "osi":
        if args.arg3 is None or args.arg4 is None:
            parser.error(
                "OSI format requires all 4 arguments: country_code, version, proj_string, map_reference"
            )

        from traj2osi import Traj2OSI  # Assuming this import exists

        converter_args = {
            "country_code": args.arg1,
            "version": args.arg2,
            "proj_string": args.arg3,
            "map_reference": args.arg4,
        }

        print("Converting to OSI format with:")
        print(f"  country_code: {args.arg1}")
        print(f"  version: {args.arg2}")
        print(f"  proj_string: {args.arg3}")
        print(f"  map_reference: {args.arg4}")

        traj.convert(Traj2OSI, output_path, converter_args)

    else:  # openlabel
        from traj2openlabel import Traj2OpenLabel  # Assuming this import exists

        converter_args = {"dummy_a": args.arg1, "dummy_b": args.arg2}

        print("Converting to OpenLabel format with dummy arguments:")
        print(f"  A: {args.arg1}")
        print(f"  B: {args.arg2}")

        traj.convert(Traj2OpenLabel, output_path, converter_args)

    print(f"Conversion complete! Output saved to: {output_path}")
