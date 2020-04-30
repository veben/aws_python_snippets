import sys

from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from awsglue.transforms import Join
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

# ARGUMENTS ##############################################################################
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'result_bucket_path', 'base', 'table_v1', 'table_v2'])
job_name = args['JOB_NAME']
result_bucket_path = args['result_bucket_path']
base = args['base']
tables = [args['table_v1'], args['table_v2']]
##########################################################################################

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

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(job_name, args)


pokemons_v1 = glueContext.create_dynamic_frame.from_catalog(database=base, table_name=tables[0])
pokemons_v2 = glueContext.create_dynamic_frame.from_catalog(database=base, table_name=tables[1])

combined_dataframe = Join.apply(pokemons_v1, pokemons_v2, id_field, id_field) \
    .select_fields(columns).toDF().orderBy(id_field).repartition(1)
combined_dynamicframe = DynamicFrame.fromDF(combined_dataframe, glueContext, "partitioned_df")

glueContext.write_dynamic_frame.from_options(frame=combined_dynamicframe,
                                             connection_type="s3",
                                             connection_options={"path": result_bucket_path},
                                             format="csv")

job.commit()
