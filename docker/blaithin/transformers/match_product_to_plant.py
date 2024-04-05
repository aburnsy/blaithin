if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test
import polars as pl
from rapidfuzz import process
from rapidfuzz.distance import Levenshtein
from rapidfuzz.utils import default_process

# from thefuzz import process
# from rapidfuzz import fuzz

# from rapidfuzz.distance import Levenshtein, JaroWinkler


@transformer
def transform(plants, products, *args, **kwargs):
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
    # Specify your transformation logic here

    plant_values = plants.select("name").to_series(0).unique().to_list()

    matched_products = (
        products
        # .filter(pl.col('product_name') == 'Euonymous japonicus')
        # .sample(10)
        .with_columns(
            pl.col("product_name")
            .map_elements(
                lambda product_name: process.extractOne(
                    product_name,
                    # plant_list,
                    [
                        plant
                        for plant in plant_values
                        if (
                            any(
                                default_process(product_name.split()[0]) == e
                                for e in plant.split()
                            )
                        )
                    ],
                    scorer=Levenshtein.normalized_similarity,
                    score_cutoff=0.25,
                    processor=lambda s: default_process(s),
                )
            )
            .alias("match")
        )
        .with_columns(pl.col("match").list.get(0).alias("name"))
        .drop("match")
        .with_columns(
            pl.when(pl.col("name").is_null())
            .then(
                pl.col("product_name").map_elements(
                    lambda product_name: process.extractOne(
                        product_name,
                        plant_values,
                        scorer=Levenshtein.normalized_similarity,
                        score_cutoff=0.60,
                        processor=lambda s: default_process(s),
                    )
                )
            )
            .otherwise(None)
            .alias("match")
        )
        .with_columns(pl.col("match").list.get(0).alias("name2"))
        .drop("match")
        .with_columns(
            pl.when(pl.col("name").is_null())
            .then(pl.col("name2"))
            .otherwise(pl.col("name"))
            .alias("name")
        )
        .drop("name2")
        .join(
            plants,
            on="name",
            how="inner",
        )  # Only return matches on products from rhs website
        .unique()
    )

    return matched_products


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
