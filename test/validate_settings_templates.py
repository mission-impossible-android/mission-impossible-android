import yamale

schema = yamale.make_schema('./docs/schema.yaml')

data = yamale.make_data('./docs/target.settings.yaml')
yamale.validate(schema, data)

data = yamale.make_data('./mia/templates/mia-default/settings.yaml')
yamale.validate(schema, data)
