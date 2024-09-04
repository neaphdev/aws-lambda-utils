from pathlib import Path

import toml
import yaml


class CloudFormationLoader(yaml.SafeLoader):
    def construct_ref(self, node):
        return {"Ref": node.value}

    def construct_get_att(self, node):
        return {"Fn::GetAtt": node.value.split(".")}

    def construct_sub(self, node):
        return {"Fn::Sub": node.value}


CloudFormationLoader.add_constructor("!Ref", CloudFormationLoader.construct_ref)
CloudFormationLoader.add_constructor("!GetAtt", CloudFormationLoader.construct_get_att)
CloudFormationLoader.add_constructor("!Sub", CloudFormationLoader.construct_sub)


def load_toml_config(file_path):
    with open(file_path, "r") as f:
        return toml.load(f)


def load_yaml_template(file_path):
    with open(file_path, "r") as f:
        return yaml.load(f, Loader=CloudFormationLoader)


def save_yaml_template(data, file_path):
    with open(file_path, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)


def update_template(template, config, gen_bashdebug=True):
    parameters = config["dev"]["deploy"]["parameters"]
    parameter_overrides: dict = parameters.get("parameter_overrides", [])
    stack_name = parameters.get("stack_name")
    if gen_bashdebug:
        # save  string command as .sh
        command_debug = f"sam.cmd sync --watch --template template-dev.yaml --profile mid-nc-dev-developer --stack-name {stack_name} --no-dependency-layer"
        with open("debug.sh", "w") as f:
            f.write(command_debug)

    for override in parameter_overrides:
        key, value = override.split("=", 1)
        if key in template.get("Parameters", {}):
            template["Parameters"][key]["Default"] = value

    resources = template.get("Resources", {})
    for resource in resources.values():
        if resource.get("Type") == "AWS::Serverless::Function":
            properties = resource.get("Properties", {})
            if "Runtime" in properties:
                properties["Runtime"] = template["Parameters"]["Runtime"]["Default"]
            if "Layers" in properties:
                properties["Layers"] = template["Parameters"]["LayerList"]["Default"].split(",")

    return template


def generate_static_template(toml_path, template_path, output_path):
    config = load_toml_config(toml_path)
    template = load_yaml_template(template_path)
    updated_template = update_template(template, config)
    save_yaml_template(updated_template, output_path)
    print(f"Static template saved to {output_path}")


if __name__ == "__main__":
    try:
        script_dir = Path().resolve()
        print("Location where the file is executed: ", script_dir)
        toml_file_path = script_dir / "samconfig.toml"
        yaml_template_path = script_dir / "template.yaml"
        output_template_path = script_dir / "template-dev.yaml"

        generate_static_template(toml_file_path, yaml_template_path, output_template_path)
    except Exception as e:
        print(f"Error al generar archivo: {e}")
