import os

pathRoot = os.getenv('NAME')
if pathRoot == 'DEP':
    domainName = 'https://nextreadsbackend.azurewebsites.net'
else:
    domainName = 'https://localhost:80'