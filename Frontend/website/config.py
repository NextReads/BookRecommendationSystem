import os

pathRoot = os.getenv('NAME')
if pathRoot == 'DEP':
    domainName = 'https://nextreadsbackend.azurewebsites.net'
else:
    domainName = 'http://localhost:80'

print('domainName: ', domainName)