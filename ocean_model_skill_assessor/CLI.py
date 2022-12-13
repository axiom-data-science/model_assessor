"""
Command Line Interface.
"""

import argparse

import ocean_model_skill_assessor as omsa


# https://sumit-ghosh.com/articles/parsing-dictionary-key-value-pairs-kwargs-argparse-python/
class ParseKwargs(argparse.Action):
    """With can user can input dicts on CLI."""

    def __call__(self, parser, namespace, values, option_string=None):
        """With can user can input dicts on CLI."""
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split("=")
            # catch list case
            if "[" in value and "]" in value:
                value = value.strip("][").split(",")
            getattr(namespace, self.dest)[key] = value


def main():
    """Parser method."""

    parser = argparse.ArgumentParser()

    parser.add_argument("action", help="What action to take? Options: make_catalog, proj_path, vocabs, run.")
    parser.add_argument(
        "--project_name",
        help="All saved items will be stored in a subdirectory call `project_name` in the user application cache.",
    )
    
    # make_catalog options
    parser.add_argument(
        "--catalog_type",
        help="Which type of catalog to make? Options: erddap, axds, local.",
    )

    parser.add_argument(
        "--kwargs",
        nargs="*",
        action=ParseKwargs,
        default={},
        help="Input keyword arguments for the catalog. Available options are specific to the `catalog_type`. Dictionary-style input. More information on options can be found in `omsa.main.make_catalog` docstrings. Format for list items is e.g. standard_names='[sea_water_practical_salinity,sea_water_temperature]'.",
    )

    parser.add_argument(
        "--kwargs_search",
        nargs="*",
        action=ParseKwargs,
        default={},
        help="Input keyword arguments for the search specification. Dictionary-style input. More information on options can be found in `omsa.main.make_catalog` docstrings. Format for list items is e.g. standard_names='[sea_water_practical_salinity,sea_water_temperature]'.",
    )

    parser.add_argument("--catalog_name", help="Catalog name, with or without suffix of yaml.")
    parser.add_argument("--vocab_names", nargs="*", help="Name of vocabulary file, must be in the vocab user directory.")


    # run options
    parser.add_argument("--catalog_names", nargs="*", help="Which catalogs, by name, to use? For example: catalog1 catalog2")
    parser.add_argument("--key", help="Key from vocab representing the variable to compare.")
    parser.add_argument("--model_path", help="Path for model output.")
    parser.add_argument("--ndatasets", type=int, help="Max number of datasets from input catalog(s) to use.")


    args = parser.parse_args()

    # Make a catalog.
    if args.action == "make_catalog":
        omsa.make_catalog(
            catalog_type=args.catalog_type,
            project_name=args.project_name,
            catalog_name=args.catalog_name,
            kwargs=args.kwargs,
            kwargs_search=args.kwargs_search,
            vocab=args.vocab_names,
            save_cat=True,
        )

    # Print path for project name.
    elif args.action == "proj_path":
        print(omsa.PROJ_DIR(args.project_name))

    # Print available vocabularies.
    elif args.action == "vocabs":
        print([path.stem for path in omsa.VOCAB_DIR.glob("*")])

    # Run model-data comparison.
    elif args.action == "run":
        omsa.main.run(
            project_name=args.project_name,
            catalog_names=args.catalog_names,
            vocabs=args.vocab_names,
            key=args.key,
            model_path=args.model_path,
            ndatasets=args.ndatasets,
        )
