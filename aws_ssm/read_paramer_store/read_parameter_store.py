from boto3.session import Session


def read_parameter_store(ssm_client: Session.client, ssm_parameter_name: str) -> dict:
    try:
        param = ssm_client.get_parameter(Name=ssm_parameter_name, WithDecryption=True)
        return param["Parameter"]["Value"]
    except ssm_client.exceptions.ParameterNotFound as e:
        print("Error reading parameter store: " + str(e))
        raise
