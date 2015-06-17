from glob import glob
import sys
import yamale

schema = yamale.make_schema('./docs/schema.yaml')

data = yamale.make_data('./docs/current.settings.yaml')
yamale.validate(schema, data)

templates = glob('mia/templates/*/settings.yaml')
for template in templates:
    sys.stdout.write('Checking %s against schema... ' % template)
    data = yamale.make_data(template)
    yamale.validate(schema, data)
    print("done!")
