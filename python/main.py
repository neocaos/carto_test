# import libraries
import sys
import os
from cartoframes.auth import set_default_credentials
from cartoframes import to_carto
from datetime import datetime
from urllib.parse import urlparse
from geopandas import GeoDataFrame

from utils import (
    get_file,
    get_geodataframe_from_file,
    get_geodataframe_from_geojson,
    is_arg_file,
    is_arg_url,
)

# we set our Credentials to carto.
set_default_credentials("creds.json")


# Main method, which will be executed once module is called
def main(args):
    print("Running ETL pipeline to Ingest Spatial Data")
    print("Number of arguments:", len(args), "arguments.")

    # We iterate over arguments, and we check if they're a request or a file
    for index, arg in enumerate(args):
        print("argument: " + str(arg) + " with index :" + str(index))

        now = datetime.now()
        date_time = now.strftime("%Y%m%d%H%M")
        dataset_name = ""

        # We can set up how many rows to upload to carto by setting up an Environment Variable (row_limit)
        row_limit = int(os.environ.get("row_limit", 10))
        try:
            is_file = is_arg_file(arg)
            is_url = is_arg_url(arg)

            if not is_file and not is_url:
                raise Exception("Argument must be a local file or a url")

            if is_file:
                file = arg
                _, dataset_name = os.path.split(file)
                geodataframe = get_geodataframe_from_file(arg)
            else:  # It's a endpoint or request
                file = get_file(arg)
                dataset_name = urlparse(arg).path.replace("/", "_").strip("_")
                geodataframe = get_geodataframe_from_geojson(arg)

            if isinstance(geodataframe, GeoDataFrame):
                to_carto(
                    geodataframe.head(row_limit),
                    f"{date_time}_{dataset_name}",
                    if_exists="replace",
                )

        except Exception as e:
            print("Some Exception has raised in the arg: " + arg)
            print(str(e))


# We pass all the arguments to the method except the module itself.
if __name__ == "__main__":
    main(sys.argv[1:])
