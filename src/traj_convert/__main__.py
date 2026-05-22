from traj_convert.carla2traj import Carla2Traj
from datetime import datetime, timezone

def timestamp_now_dataprov() -> str:
    """Returns the current timestamp in ISO 8601 format for use with dataprov."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

if __name__ == "__main__":
    import sys, time

    started_at = timestamp_now_dataprov()

    if sys.version_info < (3, 10):
        print(
            f"Error: The traj_convert CLI requires Python 3.10 or later "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).",
            file=sys.stderr,
        )
        sys.exit(1)

    import argparse
    from rich_argparse import RichHelpFormatter

    parser = argparse.ArgumentParser(
        description="Convert CARLA trajectory data to OmegaPrime-compliant OSI format",
        epilog="""
Example usage: `python -m traj_convert traj.parquet 752 0.1.0 "" "Town01.xodr" -o output.osi`
To generate the CARLA trajectory parquet file, please confer the `README.md` of the `osi-gen` repository.
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
    parser.add_argument(
        "--omega-prime",
        action="store_true",
        default=False,
        help="Output an OmegaPrime-compliant MCAP file with embedded OpenDRIVE map. "
        "The map_reference argument must be a valid path to an .xodr file.",
    )
    parser.add_argument(
        "--input-provenance",
        type=str,
        default=None,
        help="Path to an input provenance file (dataprov JSON) to link in the provenance chain.",
    )

    args = parser.parse_args()

    # Load trajectory data from parquet file
    print(f"Loading trajectory data from {args.parquet_file} ...", end=" ")
    traj = Carla2Traj.from_file(args.parquet_file)
    print(f"Loaded {traj.df.height} frames.")

    # Determine output path and extension
    if args.output is None:
        from datetime import datetime

        datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = ".mcap" if args.omega_prime else ".osi"
        output_path = f"trajectory_osi_{datetime_str}{ext}"
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

    if args.omega_prime:
        import tempfile
        import os
        import omega_prime

        if not args.map_reference:
            parser.error("--omega-prime requires map_reference to be a valid path to an .xodr file.")

        # Write OSI to a temporary file, then convert to OmegaPrime MCAP
        with tempfile.NamedTemporaryFile(suffix=".osi", delete=False) as tmp:
            tmp_osi_path = tmp.name

        try:
            traj.convert(Traj2OSI, tmp_osi_path, converter_args)
            print(f"Creating OmegaPrime MCAP with embedded map from {args.map_reference} ...")
            recording = omega_prime.Recording.from_file(
                tmp_osi_path, map_path=args.map_reference, validate=False, parse_map=False, apply_proj=False
            )
            recording.to_mcap(output_path)
        finally:
            os.unlink(tmp_osi_path)
    else:
        traj.convert(Traj2OSI, output_path, converter_args)

    # Provenance tracking

    from dataprov import ProvenanceChain
    import hashlib
    from importlib.metadata import PackageNotFoundError, metadata

    unique_hash = hashlib.sha256(
        (str(vars(args)) + str(time.time_ns())).encode()
    ).hexdigest()
    tool_name = "rirun"
    try:
        meta = metadata(tool_name)
        tool_version = meta["Version"]
    except PackageNotFoundError:
        tool_version = "unknown"
    entity_id = tool_name + "_" + unique_hash[:8]

    chain = ProvenanceChain.create(
        entity_id=entity_id,
        initial_source=args.parquet_file,
        description="Conversion of CARLA trajectory data to OSI format using traj_convert",
        tags=["osi-gen", "traj_convert", "carla2osi", "conversion", "provenance", "Synergies"],
    )

    input_files = [args.parquet_file] + ([args.map_reference] if args.omega_prime else [])
    input_formats = ["parquet"] + (["xodr"] if args.omega_prime else [])
    input_prov = None
    if args.input_provenance:
        input_prov = [args.input_provenance] + ([None] if args.omega_prime else [])

    chain.add(
        started_at=started_at,
        ended_at=timestamp_now_dataprov(),
        tool_name=tool_name,
        tool_version=tool_version,
        arguments=" ".join(sys.argv[1:]),
        operation="Conversion from carla trajectory parquet to OSI format" + (" with OmegaPrime MCAP output" if args.omega_prime else ""),
        inputs=input_files,
        input_formats=input_formats,
        input_provenance_files=input_prov,
        outputs=[output_path],
        output_formats=["mcap" if args.omega_prime else "osi"],
    )

    print(f"Conversion complete! Output saved to: {output_path}")
