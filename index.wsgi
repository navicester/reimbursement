import sys
import os.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'reimbursement.settings'
sys.path.append(os.path.join(os.path.dirname(__file__),'reimbursement'))
if not 'SERVER_SOFTWARE' in os.environ: # sae
	root = os.path.dirname(__file__)
	sys.path.insert(0, os.path.join(root, 'site-packages'))

from reimbursement import wsgi

application = sae.create_wsgi_app(wsgi.application)


#def application(environ, start_response):
#    start_response('200 ok', [('content-type', 'text/plain')])
#    return ['Hello, SAE!']
