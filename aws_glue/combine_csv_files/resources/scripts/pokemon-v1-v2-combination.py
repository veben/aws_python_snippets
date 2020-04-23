import sys

from pyspark.context import SparkContext

from awsglue.transforms import Join
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

columns = [
  'id',
  'identifier',
  'generation',
  'first_type',
  'second_type',
  'legendary',
  'base_experience',
  'attack',
  'defense',
  'hp',
  'speed'
]

id_field = 'id'

result_bucket_path = "s3://aws-glue-pokemon-tmp/csv_file_result_job"

pokemons_v1 = glueContext.create_dynamic_frame.from_catalog(database = "pokemons", table_name = "pokemons_v1")
pokemons_v2 = glueContext.create_dynamic_frame.from_catalog(database = "pokemons", table_name = "pokemons_v2")

combined_dataframe = Join.apply(pokemons_v1, pokemons_v2, id_field, id_field).select_fields(columns).toDF().orderBy(id_field).repartition(1)
combined_dynamicframe = DynamicFrame.fromDF(partitioned_dataframe, glueContext, "partitioned_df")

glueContext.write_dynamic_frame.from_options(frame = partitioned_dynamicframe, connection_type = "s3", connection_options = {"path": result_bucket_path}, format = "csv")

job.commit()
