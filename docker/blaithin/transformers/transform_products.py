if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test
import polars as pl
from rapidfuzz.utils import default_process


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    data = pl.DataFrame(data).with_columns(
        pl.col("product_name")
        .str.replace("\(G\) ?\d+.*", "")
        .str.replace(" Stem \d+\s?\w+.+", "")
        .str.replace(" ?\(\d+-?\d*cm.+", "")
        .str.replace(" ?-? \d+\.?\d* ?L.+", "")
        .str.replace(" \d+ ?cm ?.*", "")
        .str.replace(" ?-? \d+ ?-\d+.*", "")
        .str.replace(" \d+\.?\d*L.*", "")
        .str.replace(" \d+ ?-?p?P?ack.*", "")
        .str.replace(" Standard Tree.*", "")
        .str.replace(" Half Standard.*", "")
        .str.replace(" High Standard.*", "")
        .str.replace(" ?–?-? \d\/\d s?S?tandard.*", "")
        .str.replace(" x ?\d+.*", "")
        .str.replace(" \d+ x .*", "")
        .str.replace(" h?H?\d+-?x?W?\d*cm.*", "")
        .str.replace("[M|m]ulti-?[S|s]tem.*", "")
        .str.replace("\d[F|f]t.*", "")
        .str.replace("[b|B]are [r|R]oot.*", "")
        .str.replace(" [p|P]\d+.*", "")
        .str.replace(" \d+ltr.*", "")
        .str.replace(" \d+\/?\d+ ?cm", "")
        .str.replace(" ?H?D?\d.*[C|c][M|m].*", "")
        .str.replace(" Special Offer", "")
        .str.replace(" Specimen.*", "")
        .str.replace(" [m|M]ulti-?[B|b]all.*", "")
        .str.replace(" ?\(.*\) ?", "")
        .str.replace(" [B|b]all", "")
        .str.replace(" [H|h]edge", "")
        .str.replace(" ?[C|c]onical", "")
        .str.replace(" ?[T|t]opiary", "")
        .str.replace(" ?[T|t]opiary", "")
        .str.replace(" [P|p]yramid$", "")
        # virens Ball 40
        # Leave very last
        .str.replace("\d+ x ", "")
        .str.replace("\d+.*", "")
        .str.split("/")
        .list.first()
        .str.replace(" pleached", "")
        .str.replace(" [Ss]pirals?", "")
        .str.replace(" [Cc]ones?", "")
        .str.replace(" Lollipop$", "")
        .str.replace(" [Ss]tandards?", "")
        .str.replace(" [Hh]alf-? ?[Ss]tandards?", "")
        .str.replace(" ?[Ss]tandard [Ee]spalier", "")
        .str.replace(" ?Standard Tree", "")
        .str.replace(" [Ss]tandards?", "")
        .str.replace("[Ee]spalier", "")
        .map_elements(lambda s: default_process(s))
        .str.replace("  ", " ")
        .str.replace("  ", " ")
        .str.strip()
        .alias("product_name_cleansed")
    )
    # data = data.filter(pl.col("product_name_cleansed").str.contains("espalier")).to_pandas()
    # data = data.sample(1000).to_pandas()
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
