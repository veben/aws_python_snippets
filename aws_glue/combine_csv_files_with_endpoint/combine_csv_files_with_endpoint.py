from lib_combination_with_endpoint.aws_client.aws_client import get_glue_context, define_pokemons_final_df, \
    write_df_to_s3_bucket
from lib_combination_with_endpoint.conf_utils.conf_utils import get_s3_result_folder_path


def main():
    write_df_to_s3_bucket(define_pokemons_final_df(get_glue_context()), get_s3_result_folder_path())


if __name__ == "__main__":
    main()
