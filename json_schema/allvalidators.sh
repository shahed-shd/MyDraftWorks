schema="$1"
instance="$2"

echo "SCHEMA: $schema"
echo "INSTANCE: $instance"

echo "Validating . . ."

echo "-------------------- justify --------------------"
justify-cli/justify -s $schema -i $instance     # Needs to clone the justify-cli repo

echo "-------------------- yajsv --------------------"
yajsv -s $schema $instance

echo "-------------------- ajv --------------------"
ajv --verbose -s $schema -d $instance

echo "-------------------- jsonschema --------------------"
jsonschema -i $instance $schema

echo "-------------------- Done --------------------"
