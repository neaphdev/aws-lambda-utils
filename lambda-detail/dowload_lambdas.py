import boto3


def get_lambda_function_description(
    function_name: str,
    profile_name: str = "bdev",
):
    # Create a Lambda client

    try:
        if profile_name:
            session = boto3.Session(profile_name=profile_name)
        else:
            session = boto3.Session()
        # Initialize a session using Amazon Lambda in a specific region
        client = session.client("lambda", region_name="us-east-1")  # Ensure this is the same region as your Lambda function

        # Get the function configuration
        response = client.get_function_configuration(FunctionName=function_name)

        # Print the function description
        description = response.get("Description", "No description available.")
        return description

    except client.exceptions.ResourceNotFoundException:
        return f"Function {function_name} not found."

    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    # open file
    lambdas = [
        "prod_compartir-resultado-v3_app-bim-3-1-10",
        "prod_inicio-cambio-cuenta-general-v3_app-bim-3-1-10",
        "prod_cambio-cuenta-face-bio-v8_app-bim-3-1-10",
        "prod_status-cambio-cuenta-bio-v3_app-bim-3-1-10",
        "prod_generateqr-v4_app-bim-3-1-8",
        "iniciocuentadniprod-iniciocuentadniprod-5ERFVS42FLI",
        "prod_poner-plata-cuenta-dni-v2_app-bim_v4",
        "confirmappcuentadniprod-confirmappcuentadniprod-1LF4SPUVDF9L1",
        "prod_compartir-resultado-v3_app-bim-3-1-10",
        "promocion-bimer-prod",
        "consultarinfoappbimprod-consultarinfoappbimprod-1LWGMP8XPKW7W",
        "prod_compra-v2_app-bim_v4",
    ]
    descriptions = []
    for function_name in lambdas:

        # Replace 'your-lambda-function-name' with your actual Lambda function name

        description = get_lambda_function_description(function_name)
        descriptions.append((function_name, description))
        print(function_name, description)
