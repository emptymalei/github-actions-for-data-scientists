import click
from ufo_data.utils import BASE_URL, unified_dataframe_from_links


@click.command()
@click.option("--top", default=None, type=int, help="Only download from most recent months")
@click.option(
    "--target",
    default="nuforc_ufo_records.csv",
    help="Download to target file",
    required=False,
)
def download(top, target):
    """Download UFO records"""

    df = unified_dataframe_from_links(BASE_URL, top=top)
    print(df.head())
    df.to_csv(target, index=False)
