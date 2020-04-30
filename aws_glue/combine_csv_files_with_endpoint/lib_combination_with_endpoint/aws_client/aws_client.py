from pyspark.context import SparkContext
from pyspark.sql import DataFrame
from pyspark.sql.utils import AnalysisException

from awsglue import DynamicFrame
from awsglue.context import GlueContext
from awsglue.transforms import Join
from lib_combination_with_endpoint.conf_utils.conf_utils import get_database_name, get_table_v2_name, \
    get_table_v1_name, get_final_columns_names


def get_glue_context() -> GlueContext:
    return GlueContext(SparkContext.getOrCreate())


def create_dynamic_frame(glue_context: GlueContext, database_name: str, table_name: str) -> DynamicFrame:
    return glue_context.create_dynamic_frame.from_catalog(database=database_name, table_name=table_name)


def join_df_data(df1: DynamicFrame, df2: DynamicFrame, attr1_name: str, attr2_name: str) -> DynamicFrame:
    return Join.apply(df1, df2, attr1_name, attr2_name)


def define_pokemons_final_df(glue_context: GlueContext) -> DataFrame:
    database = get_database_name()

    pokemons_v1_df = create_dynamic_frame(glue_context, database, get_table_v1_name()) \
        .drop_fields(['species_id', 'is_default'])
    pokemons_v2_df = create_dynamic_frame(glue_context, database, get_table_v2_name()) \
        .drop_fields(['name'])

    id_field = 'id'
    return join_df_data(pokemons_v1_df, pokemons_v2_df, id_field, id_field) \
        .select_fields(get_final_columns_names()) \
        .toDF() \
        .orderBy(id_field)


def display_dynamic_frame_data(dynamic_frame: DynamicFrame):
    dynamic_frame.show()


def display_dynamic_frame_schema(dynamic_frame: DynamicFrame):
    dynamic_frame.printSchema()


def write_df_to_s3_bucket(data_frame: DataFrame, folder_path: str):
    try:
        data_frame.repartition(1).write.csv(folder_path, header="true")
    except AnalysisException:
        print(f"There is already a result file in remote folder {folder_path}")
        # raise
