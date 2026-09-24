from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


client = QdrantClient(path = './qdrant_local_db')

collection_name = "new_collection"


if not client.collection_exists(collection_name):
    client.create_collection(
    collection_name = collection_name,
    vectors_config= VectorParams (size = 1024, distance= Distance.COSINE),
)






