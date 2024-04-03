if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import polars as pl 

pl.Config.restore_defaults()

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

    # These transformations need to be done in order - we cannot combine into a single replace_all
    data = data.with_columns(pl.col("botanical_name").str.replace_all(" ", "-").str.replace_all("\/", "-").str.replace_all("-&-", "-").str.replace_all("\.", "").str.replace_all("'", "").alias('botanical_name_html'))    
    data = data.with_columns([
        pl.format("https://www.rhs.org.uk/plants/{}/{}/details", "id", "botanical_name_html").alias("plant_url"),
        pl.lit('rhs').alias('source')
    ])
    data = data.drop("botanical_name_html")

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
