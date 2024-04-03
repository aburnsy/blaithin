if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
from kafka import KafkaProducer
import json

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """


    topic = 'rhs_urls'
    producer = KafkaProducer(
        bootstrap_servers='kafka:29092',
    )


    print(f"Shape of df to be sent via kafka: {data.shape}")

    for row in data.rows(named=True):
        message = {
            'id': row['id'],
            'plant_url': row['plant_url'],
            'botanical_name': row['botanical_name'],
        }
        producer.send(topic, json.dumps(message).encode('utf-8'))