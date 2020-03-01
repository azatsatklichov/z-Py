import appsbf
import tempfile
import csv
import os
import string
import cgi
import copy
import base64
import re
from datetime import datetime, timedelta
from math import ceil

# Core
from appsbf.formatter import core_count_formatter
from appsbf.services.configuration import filter_loc_os_rel
from ..core import require_csrf_token
# Flask
from flask import (
	Blueprint, Markup,
	flash, request, redirect, url_for, make_response, session, abort,
	jsonify)
from flask import render_template as flask_render_template
from flask.ext.login import fresh_login_required, current_user
# Services
from appsbf.services.mongo_service import DB
from appsbf.services.app_service import app as flask_app
from ..services import json_response, cmdb
# lookups
from appsbf.model.lookups import LookupTab, LookupFieldTab
# Model
from ..model.model_sbf import SbfUpsertor, SbfRemover
from ..model import lookups
# Validators
from .validators import SbfValidator
# CSV
from appsbf.services.service_csvexport import encodeRow, prepareHeaders
# VMWare allocations
import xmlrpclib
# Pisa
from sbfprint import sbf_print
# rest
import requests
import json
# suds
import suds
from suds.sax.element import Element
# sbfexport
from sbfexport import (
	sbf_export_cluster, sbf_export_to_csv, sbf_export_general, sbf_export_oat,
	sbf_export_esm, sbf_export_error_xml, sbf_export_error, sbf_export_vm,
	sbf_export_sudo, sbf_export_osparams, sbf_export_pat
)
# validations
from appsbf.controllers.validators.sbf_util import extendList, merge_results, appendToList, getNewValue
from .validators import ClusterValidator
# Active Directory check for users and groups
from appsbf.model.ldapcli import EXTUserSearch, EXTexactGroupSearch
# Helpers
from appsbf.controllers.sbfhelpers import (
	has_mssql, has_informix, has_oracle, has_mysql,
	has_weblogic, has_websphere,
	get_number_of_cpu,
)
# Calendar
from business_calendar import Calendar
# Pricing
from appsbf.controllers.pricing import getPriceList
# Profile Settings
from .profile import Profile
from appsbf import app
from bson.son import SON
from appsbf.controllers.application.application_tab import ApplicationTab


logger = app.logger


def render_template(template_path, *args, **kwargs):
	return flask_render_template(
		template_path,
		debug=flask_app.config.get('DEBUG'),
		*args, **kwargs
	)

BP = Blueprint('sbfmanager', __name__, template_folder='../templates')

def get_service_now_codes(sbf):

	if not sbf.get('server_env'):
		raise Exception("Server environment not set for SBF #%s" % sbf['_id'])
	if not sbf.get('location'):
		raise Exception("Location not set for SBF #%s" % sbf['_id'])
	if not sbf.get('release'):
		raise Exception("Release not set for SBF #%s" % sbf['_id'])
	if not sbf.get('platform'):
		raise Exception("Platform not set for SBF #%s" % sbf['_id'])

	snenv = DB.SNEnvironmentCode.find_one({'_id' : sbf.get('server_env')})
	if not snenv:
		raise Exception("Service Now configuration does not contain %s for SBF #%s" % (sbf.get('server_env'), sbf['_id']), 'warning')

	cats = list(DB.SNCategoryCode.find({}).sort('_id', 1))

	for cat in cats:

		match = True

		for k,v in cat.items():
			if k != '_id' and k != 'code' and k != 'sys_id':

				regex = re.compile(v)
				if not regex.match(sbf.get(k, '')):
					match = False

		if match:
			environment_code = DB.SNEnvironmentCodeMapping.find_one({'_id': snenv.get('environment')})
			if environment_code:
				environment_code = int(environment_code['code'])
			return (cat['sys_id'], cat['code'], snenv['location'], snenv['folder'], snenv.get('prefix'), environment_code)

	raise Exception("Service Now configuration does not set for SBF #%s" % sbf['_id'])

def create_calendar(sbf):

	if sbf.get('location') == 'PRG':
		return Calendar(holidays=appsbf.app.config['CZ_HOLIDAYS'])
	elif sbf.get('location') == 'CBJ':
		return Calendar(holidays=appsbf.app.config['MY_HOLIDAYS'])
	elif sbf.get('location') == 'US':
		return Calendar(holidays=appsbf.app.config['US_HOLIDAYS'])
	else:
		return Calendar()


@BP.route('/sbflist/gsntask/gsn_configuration_item/', methods=['GET'])
@fresh_login_required
def gsn_configuration_item():

	page = int(request.args.get('page', 1))
	filters = dict((key, value) for key, value in request.args.iteritems() if 'filter_' in key and value != '')
	sbfids = list(filter(lambda x: x != 'undefined', (request.args.getlist('sbfid[]')) ))

	client = suds.client.Client(
				url=appsbf.app.config['GSN_URL']+'u_dhl_ci_hw_server.do?WSDL',
				username=appsbf.app.config['GSN_USER'],
				password=base64.b64decode(appsbf.app.config['GSN_PASSWD']))

	conf = DB.Conf.find_one({'_id' : 0})

	for sbfid in sbfids:
		sbf = DB.SBF.find_one({'_id':long(sbfid)})

		try:

			if not sbf:
				raise Exception("SBF #%s does not exist." % sbfid)

			if not sbf.get('server_hostname'):
				raise Exception("SBF #%s does not have hostname." % sbfid)

			if not sbf.get('com_rfc_no'):
				raise Exception("SBF #%s does not have commissioning RFC yet." % sbfid)

			if 'ci' in sbf:
				raise Exception("Configuration Item %s already created in past." % sbf['ci'], 'info')

			rfc_sys_id = cmdb.check_rfc_existence(sbf.get('RFC'))
			if not rfc_sys_id:
				raise Exception("%s does not exist in GSN." % sbf.get('RFC'))

			crfc_sys_id = cmdb.check_rfc_existence(sbf.get('com_rfc_no'))
			if not crfc_sys_id:
				raise Exception("Commissioning %s does not exist in GSN." % sbf.get('com_rfc_no'))

			sys_id, category_code, location, folder, prefix, environment = get_service_now_codes(sbf)
			u_search_code = ('-'.join([prefix, category_code, sbf['server_hostname']])).upper()

			url = appsbf.app.config['GSN_URL']+'api/now/table/u_dhl_ci_hw_server?sysparm_limit=10&sysparm_query=u_search_code=%s&sysparm_display_value=true&sysparm_fields=sys_id' % u_search_code

			response = requests.get(
				url=url,
				auth=(appsbf.app.config['GSN_USER'], base64.b64decode(appsbf.app.config['GSN_PASSWD'])),
				headers={"Accept" : "application/json"})

			respdict = response.json()

			if response.status_code == 200 and 'result' in respdict and len(respdict['result']) > 0 and 'sys_id' in respdict['result'][0]:
				u_search_code = u_search_code + "-" + sbfid.upper()

				url = appsbf.app.config['GSN_URL']+'api/now/table/u_dhl_ci_hw_server?sysparm_limit=10&sysparm_query=u_search_code=%s&sysparm_display_value=true&sysparm_fields=sys_id' % u_search_code

				response = requests.get(
					url=url,
					auth=(appsbf.app.config['GSN_USER'], base64.b64decode(appsbf.app.config['GSN_PASSWD'])),
					headers={"Accept" : "application/json"})

				respdict = response.json()

				if response.status_code == 200 and 'result' in respdict and len(respdict['result']) > 0 and 'sys_id' in respdict['result'][0]:
					raise Exception("Configuration Item %s already exists." % u_search_code, 'info')

			short_description = [x['service_name'] for x in sbf.get('service_names', [])]
			if sbf.get('citrix_silo_name'):
				short_description.append("CMDB Citrix silo name : " + sbf.get('citrix_silo_name', ''))
			elif sbf.get('server_usage'):
				short_description.append(sbf.get('server_usage'))

			ci_params = {
				'name' 				: sbf['server_hostname'].upper(),
				'u_search_code' 	: u_search_code,
				'u_folder' 			: folder,
				'category' 			: sys_id,
				'location' 			: location,
				'short_description' : ", ".join(short_description)
			}

			if environment:
				ci_params['u_environment'] = environment

			for iprow in sbf.get('hostname_allocs', []):
				if iprow.get('fqdn_hostname', '').lower() == sbf['server_hostname'].lower():
					ci_params['ip_address'] = iprow['ip']
				elif iprow.get('fqdn_hostname', '').lower() == sbf['server_hostname'].lower() + "-b":
					ci_params['u_ip_address2'] = iprow['ip']
				elif iprow.get('fqdn_hostname', '').lower() == sbf['server_hostname'].lower() + "-r":
					ci_params['u_ilo_ip_address'] = iprow['ip']
				elif iprow.get('fqdn_hostname', '').lower() == sbf['server_hostname'].lower() + "-c":
					ci_params['u_ilo_ip_address'] = iprow['ip']

			if sbf.get('location') == 'PRG':
				ci_params['u_cost_code'] = 'DCZISX'
			elif sbf.get('location') == 'CBJ':
				ci_params['u_cost_code'] = 'DMYXIS'
			elif sbf.get('location') == 'US':
				ci_params['u_cost_code'] = 'DSYXXX'

			if sbf.get('total_nr_of_cores') and sbf.get('cputype') and sbf.get('server_type') == "Physical":
				ci_params['u_cpus_installed'] = core_count_formatter.as_string(get_number_of_cpu(sbf))

			if sbf.get('total_nr_of_cores'):
				ci_params['u_cpu_cores'] = core_count_formatter.as_string(sbf.get('total_nr_of_cores'))

			if sbf.get('ram'):
				ci_params['u_memory_installed'] = 1024 * sbf.get('ram')

			remark = "CI created as per " + sbf.get('RFC')
			if sbf.get('com_remark'):
				remark += "\n" + sbf.get('com_remark')
			ci_params['u_remark'] = remark

			snModel = None
			if sbf.get('server_model'):
				snModel = DB.SNModelCode.find_one({'_id' : sbf['server_model'] })
			elif sbf.get('platform') == 'AS400':
				snModel = DB.SNModelCode.find_one({'_id' : 'IBM LPAR' })

			if snModel:
				if 'model_number' in snModel:
					ci_params['model_number'] = snModel['model_number']
				if 'model_id' in snModel:
					ci_params['model_id'] = snModel['model_id']
				if 'u_brand' in snModel:
					ci_params['u_brand'] = snModel['u_brand']

			if sbf.get('technicians_contact_name'):
				ci_params['owned_by'] = sbf.get('technicians_contact_name')

			u_network_name = [sbf['server_hostname']]
			if sbf.get('server_domain'):
				u_network_name.append(sbf.get('server_domain'))
			ci_params['u_network_name'] = ".".join(u_network_name).lower()

			rslt = client.service.insert(**ci_params)

			if 'sys_id' not in rslt:
				raise Exception("Problem when creating %s: %s" % (u_search_code, rslt))

			flash(u_search_code + ' was created.', 'success')

			upsertor = SbfUpsertor(sbf)
			upsertor.SetScalar('ci', u_search_code)
			upsertVal = upsertor.Execute()

			cmdb.create_ci_relations(rslt['sys_id'], sbf, rfc_sys_id, crfc_sys_id)
			result = cmdb.set_sbf_os_release(sbf, rslt['sys_id'])
			logger.info('result of set_sbf_os_release: {}'.format(result))

		except (suds.WebFault, TypeError, Exception) as e:

			if isinstance(e, suds.WebFault):
				e2 = Exception()
				e2.args = e.args
				e = e2

			if len(e.args) > 1 and e.args[1] == 'info':
				flash(e.args[0], 'info')
			elif len(e.args) > 1 and e.args[1] == 'warning':
				flash(e.args[0], 'warning')
			else:
				flash(e, 'danger')

	return redirect(url_for('sbfmanager.sbf', page=page, **filters))


@BP.route('/sbflist/gsntask/gsn_comm_request/', methods=['GET'])
@fresh_login_required
def gsn_comm_request():

	page = int(request.args.get('page', 1))
	filters = dict((key, value) for key, value in request.args.iteritems() if 'filter_' in key and value != '')
	sbfids = list(filter(lambda x: x != 'undefined', (request.args.getlist('sbfid[]')) ))

	rfcdict = {}
	rfcnotingsn = {}
	ctaskdict = {}

	for sbfid in sbfids:
		sbf = DB.SBF.find_one({'_id':long(sbfid)})

		if 'ctask_comm' in sbf:
			flash("Commissioning %s already created in past for SBF #%s" % (sbf['ctask_comm'], sbfid))
		elif sbf.get('fit_to_cloud',False):
			flash("Commissioning for SBF #%s cannot be created because it fits to Cloud server!" % (sbfid))
		else:

			if sbf and sbf.get("RFC"):

				if sbf["RFC"] not in rfcdict and sbf["RFC"] not in rfcnotingsn:

					url = appsbf.app.config['GSN_URL']+'api/now/table/change_request?sysparm_limit=10&sysparm_query=number=%s&sysparm_display_value=true&sysparm_fields=sys_id' % sbf["RFC"]

					response = requests.get(
						url=url,
						auth=(appsbf.app.config['GSN_USER'], base64.b64decode(appsbf.app.config['GSN_PASSWD'])),
						headers={"Accept" : "application/json"})

					respdict = response.json()

					if response.status_code == 200 and 'result' in respdict and len(respdict['result']) > 0 and 'sys_id' in respdict['result'][0]:
						rfcdict[sbf["RFC"]] = respdict['result'][0]['sys_id']
					else:
						rfcnotingsn[sbf["RFC"]] = True
						flash("%s does not exist in GSN." % sbf["RFC"], 'danger')

				if sbf["RFC"] in rfcdict:
					key = sbf["RFC"] \
						  + sbf.get('platform', '') \
						  + sbf.get('location', '') \
						  + sbf.get('server_type', '') \
						  + sbf.get('server_purpose', '') \
						  + sbf.get('server_env', '')
					ctaskdict.setdefault(key, []).append(sbf)

			else:
				flash("SBF #%s does not exist or does not have RFC assigned." % sbfid, 'danger')

	client = suds.client.Client(
				url=appsbf.app.config['GSN_URL']+'change_task.do?WSDL',
				username=appsbf.app.config['GSN_USER'],
				password=base64.b64decode(appsbf.app.config['GSN_PASSWD']))

	for sbflist in ctaskdict.values():

		cal = create_calendar(sbflist[0])

		short_description = 'ComReq ' + str(len(sbflist)) + (' servers:' if len(sbflist) > 1 else ' server:') \
								+ ' ' + sbflist[0].get('server_type', '') \
								+ ' ' + sbflist[0].get('platform', '') \
								+ ' ' + sbflist[0].get('location', '') \
								+ ' ' + sbflist[0].get('server_env', '')

		project = DB.Project.find_one({'_id' : long(sbflist[0]["projectid"])})

		description = ''
		if project.get('GSN_short_description'):
			description = project.get('GSN_short_description') + '\n\n'

		description += "Commission servers:\n"
		for sbf in sbflist:
			description += sbf.get('server_hostname', '<empty hostname>') + ": https://sbf.prg-dc.dhl.com/sbf/" + str(sbf['_id']) + "?action=detail\n"

		rslt = client.service.insert(
			state = 1,
			u_change_stage = 'build_and_test',
			change_request = rfcdict[sbflist[0]["RFC"]],
			u_task_type = "build",
			assignment_group = "22c0b75eed8e3c0006cb6139c8e6dce2",
			short_description = short_description,
			description = description,
			work_start = datetime.now(),
			work_end = cal.addbusdays(datetime.now(), 5))

		if 'number' in rslt:
			flash(rslt['number'] + ' "' + short_description + '" was created.', 'success')

			for sbf in sbflist:

				upsertor = SbfUpsertor(sbf)
				upsertor.SetScalar('ctask_comm', rslt['number'])
				upsertVal = upsertor.Execute()

		else:
			flash(rslt, 'danger')

	return redirect(url_for('sbfmanager.sbf', page=page, **filters))

@BP.route('/sbflist/gsntask/gsn_build_db_request/', methods=['GET'])
@fresh_login_required
def gsn_build_db_request():

	cal = Calendar()

	page = int(request.args.get('page', 1))
	filters = dict((key, value) for key, value in request.args.iteritems() if 'filter_' in key and value != '')
	sbfids = list(filter(lambda x: x != 'undefined', (request.args.getlist('sbfid[]')) ))

	rfcdict = {}
	rfcnotingsn = {}
	ctaskdict = {}

	for sbfid in sbfids:
		sbf = DB.SBF.find_one({'_id':long(sbfid)})

		if 'ctask_db' in sbf:
			flash("Build DB %s already created in past for SBF #%s" % (sbf['ctask_db'], sbfid))
		else:

			if sbf and sbf.get("RFC"):

				if sbf["RFC"] not in rfcdict and sbf["RFC"] not in rfcnotingsn:

					url = appsbf.app.config['GSN_URL']+'api/now/table/change_request?sysparm_limit=10&sysparm_query=number=%s&sysparm_display_value=true&sysparm_fields=sys_id' % sbf["RFC"]

					response = requests.get(
						url=url,
						auth=(appsbf.app.config['GSN_USER'], base64.b64decode(appsbf.app.config['GSN_PASSWD'])),
						headers={"Accept" : "application/json"})

					respdict = response.json()

					if response.status_code == 200 and 'result' in respdict and len(respdict['result']) > 0 and 'sys_id' in respdict['result'][0]:
						rfcdict[sbf["RFC"]] = respdict['result'][0]['sys_id']
					else:
						rfcnotingsn[sbf["RFC"]] = True
						flash("%s does not exist in GSN." % sbf["RFC"], 'danger')

				if sbf["RFC"] in rfcdict:

					if has_mssql(sbf):
						ctaskdict.setdefault(sbf["RFC"] + "mssql", []).append(sbf)
					if has_oracle(sbf):
						ctaskdict.setdefault(sbf["RFC"] + "oracle", []).append(sbf)
					if has_informix(sbf):
						ctaskdict.setdefault(sbf["RFC"] + "informix", []).append(sbf)
					if has_mysql(sbf):
						ctaskdict.setdefault(sbf["RFC"] + "mysql", []).append(sbf)

			else:
				flash("SBF #%s does not exist or does not have RFC assigned." % sbfid, 'danger')

	client = suds.client.Client(
				url=appsbf.app.config['GSN_URL']+'change_task.do?WSDL',
				username=appsbf.app.config['GSN_USER'],
				password=base64.b64decode(appsbf.app.config['GSN_PASSWD']))

	for taskkey, sbflist in ctaskdict.items():

		if taskkey.endswith("mssql"):
			short_description = 'DB Build - MSSQL'
			assignment_group = '03976cb3878b2800f000675f2b434d8a'
		elif taskkey.endswith("oracle"):
			short_description = 'DB Build - Oracle'
			assignment_group = '8b976cb3878b2800f000675f2b434d85'
		elif taskkey.endswith("informix"):
			short_description = 'DB Build - Informix'
			assignment_group = '4f976cb3878b2800f000675f2b434d87'
		elif taskkey.endswith("mysql"):
			short_description = 'DB Build - MySQL'
			assignment_group = '561e561d3d47b500ddd53861825a5ead'

		short_description += ' on %s' % ", ".join([sbf.get('server_hostname') for sbf in sbflist])

		cis = []
		cifail = False

		project = DB.Project.find_one({'_id' : long(sbflist[0]["projectid"])})

		description = ''
		if project.get('GSN_short_description'):
			description = project.get('GSN_short_description') + '\n\n'

		description += short_description + "\n\nInstall, configure 'DB' according to SBF"

		for sbf in sbflist:

			if 'server_hostname' in sbf and sbf['server_hostname'] != '':
				url=appsbf.app.config['GSN_URL']+'api/now/table/u_dhl_ci_hw_server?sysparm_limit=10&sysparm_query=name=%s&sysparm_display_value=true&sysparm_fields=sys_id' % sbf['server_hostname']

				response = requests.get(
					url=url,
					auth=(appsbf.app.config['GSN_USER'], base64.b64decode(appsbf.app.config['GSN_PASSWD'])),
					headers={"Accept" : "application/json"})

				respdict = response.json()

				if response.status_code == 200 and 'result' in respdict and len(respdict['result']) > 0 and 'sys_id' in respdict['result'][0]:
					cis.append(respdict['result'][0]['sys_id'])
				else:
					flash("GSN Configuration Item for '%s' does not exist. CI has to exist before CTASK creation." % sbf['server_hostname'], 'danger')
					cifail = True

		if cifail:
			return redirect(url_for('sbfmanager.sbf', page=page, **filters))

		rslt = client.service.insert(
			state = 1,
			u_change_stage = 'build_and_test',
			change_request = rfcdict[sbflist[0]["RFC"]],
			u_task_type = "build",
			assignment_group = assignment_group,
			short_description = short_description,
			description = description,
			work_start = datetime.now(),
			work_end = cal.addbusdays(datetime.now(), 3 if taskkey.endswith("oracle") else 2),
			u_affected_cis = ','.join(cis))

		if 'number' in rslt:
			flash(rslt['number'] + ' "' + short_description + '" was created.', 'success')

			for sbf in sbflist:

				upsertor = SbfUpsertor(sbf)
				upsertor.SetScalar('ctask_db', rslt['number'])
				upsertVal = upsertor.Execute()

		else:
			flash(rslt, 'danger')

	if len(ctaskdict) == 0:
		flash('No Build Task created.', 'info')

	return redirect(url_for('sbfmanager.sbf', page=page, **filters))

@BP.route('/sbflist/gsntask/gsn_build_mw_request/', methods=['GET'])
@fresh_login_required
def gsn_build_mw_request():

	cal = Calendar()

	page = int(request.args.get('page', 1))
	filters = dict((key, value) for key, value in request.args.iteritems() if 'filter_' in key and value != '')
	sbfids = list(filter(lambda x: x != 'undefined', (request.args.getlist('sbfid[]')) ))

	rfcdict = {}
	rfcnotingsn = {}
	ctaskdict = {}

	for sbfid in sbfids:
		sbf = DB.SBF.find_one({'_id':long(sbfid)})

		if 'ctask_mw' in sbf:
			flash("Build Middleware %s already created in past for SBF #%s" % (sbf['ctask_mw'], sbfid))
		else:

			if sbf and sbf.get("RFC"):

				if sbf["RFC"] not in rfcdict and sbf["RFC"] not in rfcnotingsn:

					url = appsbf.app.config['GSN_URL']+'api/now/table/change_request?sysparm_limit=10&sysparm_query=number=%s&sysparm_display_value=true&sysparm_fields=sys_id' % sbf["RFC"]

					response = requests.get(
						url=url,
						auth=(appsbf.app.config['GSN_USER'], base64.b64decode(appsbf.app.config['GSN_PASSWD'])),
						headers={"Accept" : "application/json"})

					respdict = response.json()

					if response.status_code == 200 and 'result' in respdict and len(respdict['result']) > 0 and 'sys_id' in respdict['result'][0]:
						rfcdict[sbf["RFC"]] = respdict['result'][0]['sys_id']
					else:
						rfcnotingsn[sbf["RFC"]] = True
						flash("%s does not exist in GSN." % sbf["RFC"], 'danger')

				if sbf["RFC"] in rfcdict:

					mw = False
					for applist in [sbf.get('appl_applications_component', []), sbf.get('appl_applications_db', []), sbf.get('appl_applications_other', []), sbf.get('appl_applications_mw', [])]:
						for app in applist:
							if app.get('installed by') == 'GLOBAL-INFRA-MWARE' and app.get('man') is True:
								mw = True

					if mw:
						ctaskdict.setdefault(sbf["RFC"] + "mw", []).append(sbf)

			else:
				flash("SBF #%s does not exist or does not have RFC assigned." % sbfid, 'danger')

	client = suds.client.Client(
				url=appsbf.app.config['GSN_URL']+'change_task.do?WSDL',
				username=appsbf.app.config['GSN_USER'],
				password=base64.b64decode(appsbf.app.config['GSN_PASSWD']))

	for taskkey, sbflist in ctaskdict.items():

		short_description = 'MW Build on %s' % (", ".join([sbf.get('server_hostname') for sbf in sbflist]))

		cis = []
		cifail = False

		project = DB.Project.find_one({'_id' : long(sbflist[0]["projectid"])})

		description = ''
		if project.get('GSN_short_description'):
			description = project.get('GSN_short_description') + '\n\n'

		description += "MW Build:\n"

		for sbf in sbflist:

			if 'server_hostname' in sbf and sbf['server_hostname'] != '':
				url=appsbf.app.config['GSN_URL']+'api/now/table/u_dhl_ci_hw_server?sysparm_limit=10&sysparm_query=name=%s&sysparm_display_value=true&sysparm_fields=sys_id' % sbf['server_hostname']

				response = requests.get(
					url=url,
					auth=(appsbf.app.config['GSN_USER'], base64.b64decode(appsbf.app.config['GSN_PASSWD'])),
					headers={"Accept" : "application/json"})

				respdict = response.json()

				if response.status_code == 200 and 'result' in respdict and len(respdict['result']) > 0 and 'sys_id' in respdict['result'][0]:
					cis.append(respdict['result'][0]['sys_id'])
				else:
					flash("GSN Configuration Item for '%s' does not exist. CI has to exist before CTASK creation." % sbf['server_hostname'], 'danger')
					cifail = True

		if cifail:
			return redirect(url_for('sbfmanager.sbf', page=page, **filters))

		description += "\n"

		for sbf in sbflist:

			mv_description = []
			for applist in [sbf.get('appl_applications_component', []), sbf.get('appl_applications_db', []), sbf.get('appl_applications_other', []), sbf.get('appl_applications_mw', [])]:
				for app in applist:
					if app.get('installed by') == 'GLOBAL-INFRA-MWARE' and app.get('man') is True:
						mv_description.append(app.get('application') + ': ' + app.get('version', ''))
			description += sbf.get('server_hostname') + ": " + ", ".join(mv_description) + "\n\n"

		rslt = client.service.insert(
			state = 1,
			u_change_stage = 'build_and_test',
			change_request = rfcdict[sbflist[0]["RFC"]],
			u_task_type = "build",
			assignment_group = '56972cb3878b2800f000675f2b434dac',
			short_description = short_description,
			description = description,
			work_start = datetime.now(),
			work_end = cal.addbusdays(datetime.now(), 2),
			u_affected_cis = ','.join(cis))

		if 'number' in rslt:
			flash(rslt['number'] + ' "' + short_description + '" was created.', 'success')

			for sbf in sbflist:

				upsertor = SbfUpsertor(sbf)
				upsertor.SetScalar('ctask_mw', rslt['number'])
				upsertVal = upsertor.Execute()

		else:
			flash(rslt, 'danger')

	if len(ctaskdict) == 0:
		flash('No Build Task created.', 'info')

	return redirect(url_for('sbfmanager.sbf', page=page, **filters))

@BP.route('/sbflist/gsntask/gsn_build_backup_request/', methods=['GET'])
@fresh_login_required
def gsn_build_backup_request():

	cal = Calendar()

	page = int(request.args.get('page', 1))
	filters = dict((key, value) for key, value in request.args.iteritems() if 'filter_' in key and value != '')
	sbfids = list(filter(lambda x: x != 'undefined', (request.args.getlist('sbfid[]')) ))

	rfcdict = {}
	rfcnotingsn = {}
	ctaskdict = {}

	for sbfid in sbfids:
		sbf = DB.SBF.find_one({'_id':long(sbfid)})

		if 'ctask_backup' in sbf:
			flash("Build Backup %s already created in past for SBF #%s" % (sbf['ctask_backup'], sbfid))
		else:

			if sbf and sbf.get("RFC"):

				if sbf["RFC"] not in rfcdict and sbf["RFC"] not in rfcnotingsn:

					url = appsbf.app.config['GSN_URL']+'api/now/table/change_request?sysparm_limit=10&sysparm_query=number=%s&sysparm_display_value=true&sysparm_fields=sys_id' % sbf["RFC"]

					response = requests.get(
						url=url,
						auth=(appsbf.app.config['GSN_USER'], base64.b64decode(appsbf.app.config['GSN_PASSWD'])),
						headers={"Accept" : "application/json"})

					respdict = response.json()

					if response.status_code == 200 and 'result' in respdict and len(respdict['result']) > 0 and 'sys_id' in respdict['result'][0]:
						rfcdict[sbf["RFC"]] = respdict['result'][0]['sys_id']
					else:
						rfcnotingsn[sbf["RFC"]] = True
						flash("%s does not exist in GSN." % sbf["RFC"], 'danger')

				if sbf["RFC"] in rfcdict:

					if sbf.get('location') == 'PRG' or sbf.get('location') == 'CBJ' or sbf.get('location') == 'US':
						ctaskdict.setdefault(sbf["RFC"] + sbf.get('location'), []).append(sbf)

			else:
				flash("SBF #%s does not exist or does not have RFC assigned." % sbfid, 'danger')

	client = suds.client.Client(
				url=appsbf.app.config['GSN_URL']+'change_task.do?WSDL',
				username=appsbf.app.config['GSN_USER'],
				password=base64.b64decode(appsbf.app.config['GSN_PASSWD']))

	for taskkey, sbflist in ctaskdict.items():

		short_description = 'Configure Backups on %s' % ", ".join([sbf.get('server_hostname') for sbf in sbflist])

		cis = []
		cifail = False

		project = DB.Project.find_one({'_id' : long(sbflist[0]["projectid"])})

		description = ''
		if project.get('GSN_short_description'):
			description = project.get('GSN_short_description') + '\n\n'

		dbbackup = []

		for sbf in sbflist:

			if has_mssql(sbf) or has_oracle(sbf) or has_informix(sbf) or has_mysql(sbf):
				dbbackup.append(sbf.get('server_hostname'))

			if 'server_hostname' in sbf and sbf['server_hostname'] != '':
				url=appsbf.app.config['GSN_URL']+'api/now/table/u_dhl_ci_hw_server?sysparm_limit=10&sysparm_query=name=%s&sysparm_display_value=true&sysparm_fields=sys_id' % sbf['server_hostname']

				response = requests.get(
					url=url,
					auth=(appsbf.app.config['GSN_USER'], base64.b64decode(appsbf.app.config['GSN_PASSWD'])),
					headers={"Accept" : "application/json"})

				respdict = response.json()

				if response.status_code == 200 and 'result' in respdict and len(respdict['result']) > 0 and 'sys_id' in respdict['result'][0]:
					cis.append(respdict['result'][0]['sys_id'])
				else:
					flash("GSN Configuration Item for '%s' does not exist. CI has to exist before CTASK creation." % sbf['server_hostname'], 'danger')
					cifail = True

		if cifail:
			return redirect(url_for('sbfmanager.sbf', page=page, **filters))

		description += "FS Backup: " + ", ".join([sbf.get('server_hostname') for sbf in sbflist]) + "\n\n"
		if len(dbbackup) > 0:
			description += "DB Backup: " + ", ".join(dbbackup) + "\n\n"

		if sbflist[0]['location'] == "PRG":
			assignment_group = 'ce68976afdf8a000b150d1a19ec2810c' # EMEA-TOOLS.BACKUP&RESTORE
		elif sbflist[0]['location'] == "CBJ":
			assignment_group = 'f8793da3a9d30580b32ac9299cf59110' # GLOBAL-OPS.BACKUP
		elif sbflist[0]['location'] == "US":
			assignment_group = 'f8793da3a9d30580b32ac9299cf59110' # GLOBAL-OPS.BACKUP

		rslt = client.service.insert(
			state = 1,
			u_change_stage = 'build_and_test',
			change_request = rfcdict[sbflist[0]["RFC"]],
			u_task_type = "build",
			assignment_group = assignment_group,
			short_description = short_description,
			description = description,
			work_start = datetime.now(),
			work_end = cal.addbusdays(datetime.now(), 2),
			u_affected_cis = ','.join(cis))

		if 'number' in rslt:
			flash(rslt['number'] + ' "' + short_description + '" was created.', 'success')

			for sbf in sbflist:

				upsertor = SbfUpsertor(sbf)
				upsertor.SetScalar('ctask_backup', rslt['number'])
				upsertVal = upsertor.Execute()

		else:
			flash(rslt, 'danger')

	if len(ctaskdict) == 0:
		flash('No Build Task created.', 'info')

	return redirect(url_for('sbfmanager.sbf', page=page, **filters))

@BP.route('/sbflist/gsntask/gsn_build_mon_request/', methods=['GET'])
@fresh_login_required
def gsn_build_mon_request():

	page = int(request.args.get('page', 1))
	filters = dict((key, value) for key, value in request.args.iteritems() if 'filter_' in key and value != '')
	sbfids = list(filter(lambda x: x != 'undefined', (request.args.getlist('sbfid[]')) ))

	rfcdict = {}
	rfcnotingsn = {}
	ctaskdict = {}

	for sbfid in sbfids:
		sbf = DB.SBF.find_one({'_id':long(sbfid)})

		if 'ctask_mon' in sbf:
			flash("Build Monitoring %s already created in past for SBF #%s" % (sbf['ctask_mon'], sbfid))
		else:

			if sbf and sbf.get("RFC"):

				if sbf["RFC"] not in rfcdict and sbf["RFC"] not in rfcnotingsn:

					url = appsbf.app.config['GSN_URL']+'api/now/table/change_request?sysparm_limit=10&sysparm_query=number=%s&sysparm_display_value=true&sysparm_fields=sys_id' % sbf["RFC"]

					response = requests.get(
						url=url,
						auth=(appsbf.app.config['GSN_USER'], base64.b64decode(appsbf.app.config['GSN_PASSWD'])),
						headers={"Accept" : "application/json"})

					respdict = response.json()

					if response.status_code == 200 and 'result' in respdict and len(respdict['result']) > 0 and 'sys_id' in respdict['result'][0]:
						rfcdict[sbf["RFC"]] = respdict['result'][0]['sys_id']
					else:
						rfcnotingsn[sbf["RFC"]] = True
						flash("%s does not exist in GSN." % sbf["RFC"], 'danger')

				if sbf["RFC"] in rfcdict:

					if sbf.get('location') == 'PRG' or sbf.get('location') == 'CBJ' or sbf.get('location') == 'US':
						ctaskdict.setdefault(sbf["RFC"] + sbf.get('location'), []).append(sbf)

			else:
				flash("SBF #%s does not exist or does not have RFC assigned." % sbfid, 'danger')

	client = suds.client.Client(
				url=appsbf.app.config['GSN_URL']+'change_task.do?WSDL',
				username=appsbf.app.config['GSN_USER'],
				password=base64.b64decode(appsbf.app.config['GSN_PASSWD']))

	for taskkey, sbflist in ctaskdict.items():

		cal = create_calendar(sbflist[0])

		short_description = 'Configure OVO on %s' % (", ".join([sbf.get('server_hostname') for sbf in sbflist]))

		cis = []
		cifail = False

		project = DB.Project.find_one({'_id' : long(sbflist[0]["projectid"])})

		description = ''
		if project.get('GSN_short_description'):
			description = project.get('GSN_short_description') + '\n\n'

		description += "Configure OVO\n\nServer Details:\n"

		for sbf in sbflist:

			if 'server_hostname' in sbf and sbf['server_hostname'] != '':
				url=appsbf.app.config['GSN_URL']+'api/now/table/u_dhl_ci_hw_server?sysparm_limit=10&sysparm_query=name=%s&sysparm_display_value=true&sysparm_fields=sys_id' % sbf['server_hostname']

				response = requests.get(
					url=url,
					auth=(appsbf.app.config['GSN_USER'], base64.b64decode(appsbf.app.config['GSN_PASSWD'])),
					headers={"Accept" : "application/json"})

				respdict = response.json()

				if response.status_code == 200 and 'result' in respdict and len(respdict['result']) > 0 and 'sys_id' in respdict['result'][0]:
					cis.append(respdict['result'][0]['sys_id'])
				else:
					flash("GSN Configuration Item for '%s' does not exist. CI has to exist before CTASK creation." % sbf['server_hostname'], 'danger')
					cifail = True

		if cifail:
			return redirect(url_for('sbfmanager.sbf', page=page, **filters))

		description += "\n"

		for sbf in sbflist:

			mv_description = []
			for applist in [sbf.get('appl_applications_component', []), sbf.get('appl_applications_db', []), sbf.get('appl_applications_other', []), sbf.get('appl_applications_mw', [])]:
				for app in applist:
					if app.get('installed by') == 'GLOBAL-INFRA-MWARE' and app.get('man') is True:
						mv_description.append(app.get('application') + ': ' + app.get('version', ''))
			if len(mv_description) > 0:
				description += sbf.get('server_hostname') + " Middleware: " + ", ".join(mv_description) + "\n\n"

		for sbf in sbflist:

			if has_mssql(sbf):
				description += sbf.get('server_hostname') + " Database: " + "MSSQL\n"
			if has_oracle(sbf):
				description += sbf.get('server_hostname') + " Database: " + "Oracle\n"
			if has_informix(sbf):
				description += sbf.get('server_hostname') + " Database: " + "Informix\n"
			if has_mysql(sbf):
				description += sbf.get('server_hostname') + " Database: " + "MySQL\n"

		for sbf in sbflist:

			if sbf.get('cluster') and sbf.get('clusterId'):
				cluster = DB.Cluster.find_one({'_id':sbf.get('clusterId')})
				if cluster and cluster.get('cluster_type'):
					description += "\nHostname %s is part of the %s cluster type.\n" % (sbf.get('server_hostname'), cluster.get('cluster_type'))

		if sbflist[0]['location'] == "PRG":
			assignment_group = 'b568df2afdf8a000b150d1a19ec28199'
		elif sbflist[0]['location'] == "CBJ":
			assignment_group = '8668172afdf8a000b150d1a19ec28118'
		elif sbflist[0]['location'] == "US":
			assignment_group = '63b0a6ee153cb140ddd5e446db491cdb'

		rslt = client.service.insert(
			state = 1,
			u_change_stage = 'build_and_test',
			change_request = rfcdict[sbflist[0]["RFC"]],
			u_task_type = "build",
			assignment_group = assignment_group,
			short_description = short_description,
			description = description,
			work_start = datetime.now(),
			work_end = cal.addbusdays(datetime.now(), 2),
			u_affected_cis = ','.join(cis))

		if 'number' in rslt:
			flash(rslt['number'] + ' "' + short_description + '" was created.', 'success')

			for sbf in sbflist:

				upsertor = SbfUpsertor(sbf)
				upsertor.SetScalar('ctask_mon', rslt['number'])
				upsertVal = upsertor.Execute()

		else:
			flash(rslt, 'danger')

	if len(ctaskdict) == 0:
		flash('No Build Task created.', 'info')

	return redirect(url_for('sbfmanager.sbf', page=page, **filters))

@BP.route('/sbflist/gsntask/gsn_build_completed_request/', methods=['GET'])
@fresh_login_required
def gsn_build_completed_request():

	page = int(request.args.get('page', 1))
	filters = dict((key, value) for key, value in request.args.iteritems() if 'filter_' in key and value != '')
	sbfids = list(filter(lambda x: x != 'undefined', (request.args.getlist('sbfid[]')) ))

	delayed_why = request.args.get('delayed_why')
	work_start = datetime.strptime(request.args.get('workstart'), '%Y/%m/%d') if request.args.get('workstart') else datetime.now()

	rfcdict = {}
	rfcnotingsn = {}
	ctaskdict = {}


	for sbfid in sbfids:
		sbf = DB.SBF.find_one({'_id':long(sbfid)})

		#if sbf.has_key('ctask_are') and sbf.get('ctask_are') == 0:
		#	flash("Build 'Completed' already created in past for SBF #%s" % (sbfid))
		#else:
		upsertor = SbfUpsertor(sbf)
		upsertor.SetScalar('ctask_are',0)
		upsertor.SetScalar('aredate', work_start)
		upsertor.SetScalar('delayed_why', delayed_why)
		upsertVal = upsertor.Execute()

	return redirect(url_for('sbfmanager.sbf', page=page, **filters))
'''
@BP.route('/sbflist/gsntask/gsn_build_completed_request/', methods=['GET'])
@fresh_login_required
def gsn_build_completed_request():

	page = int(request.args.get('page', 1))
	filters = dict((key, value) for key, value in request.args.iteritems() if 'filter_' in key and value != '')
	sbfids = list(filter(lambda x: x != 'undefined', (request.args.getlist('sbfid[]')) ))

	delayed_why = request.args.get('delayed_why')
	work_start = datetime.strptime(request.args.get('workstart'), '%Y/%m/%d') if request.args.get('workstart') else datetime.now()

	rfcdict = {}
	rfcnotingsn = {}
	ctaskdict = {}


	for sbfid in sbfids:
		sbf = DB.SBF.find_one({'_id':long(sbfid)})

		if 'ctask_are' in sbf:
			flash("Build 'Completed' %s already created in past for SBF #%s" % (sbf['ctask_are'], sbfid))
		else:


			if sbf and sbf.get("RFC"):

				if sbf["RFC"] not in rfcdict and sbf["RFC"] not in rfcnotingsn:

					url = appsbf.app.config['GSN_URL']+'api/now/table/change_request?sysparm_limit=10&sysparm_query=number=%s&sysparm_display_value=true&sysparm_fields=sys_id' % sbf["RFC"]

					response = requests.get(
						url=url,
						auth=(appsbf.app.config['GSN_USER'], base64.b64decode(appsbf.app.config['GSN_PASSWD'])),
						headers={"Accept" : "application/json"})

					respdict = response.json()

					if response.status_code == 200 and 'result' in respdict and len(respdict['result']) > 0 and 'sys_id' in respdict['result'][0]:
						rfcdict[sbf["RFC"]] = respdict['result'][0]['sys_id']
					else:
						rfcnotingsn[sbf["RFC"]] = True
						flash("%s does not exist in GSN." % sbf["RFC"], 'danger')

				if sbf["RFC"] in rfcdict:

					if sbf.get('server_type'):
						if sbf.get('location') == 'PRG' or sbf.get('location') == 'CBJ' or sbf.get('location') == 'US':
							ctaskdict.setdefault(sbf["RFC"] + sbf.get('location') + sbf.get('server_type'), []).append(sbf)

			else:
				flash("SBF #%s does not exist or does not have RFC assigned." % sbfid, 'danger')

	client = suds.client.Client(
				url=appsbf.app.config['GSN_URL']+'change_task.do?WSDL',
				username=appsbf.app.config['GSN_USER'],
				password=base64.b64decode(appsbf.app.config['GSN_PASSWD']))

	for taskkey, sbflist in ctaskdict.items():

		short_description = 'ARE completed - %s servers' % sbflist[0]['server_type']

		cis = []
		cifail = False

		project = DB.Project.find_one({'_id' : long(sbflist[0]["projectid"])})

		description = short_description
		if project.get('GSN_short_description'):
			description += '\n\n' + project.get('GSN_short_description')

		for sbf in sbflist:

			if 'server_hostname' in sbf and sbf['server_hostname'] != '':

				url=appsbf.app.config['GSN_URL']+'api/now/table/u_dhl_ci_hw_server?sysparm_limit=10&sysparm_query=name=%s&sysparm_display_value=true&sysparm_fields=sys_id' % sbf['server_hostname']

				response = requests.get(
					url=url,
					auth=(appsbf.app.config['GSN_USER'], base64.b64decode(appsbf.app.config['GSN_PASSWD'])),
					headers={"Accept" : "application/json"})

				respdict = response.json()

				if response.status_code == 200 and 'result' in respdict and len(respdict['result']) > 0 and 'sys_id' in respdict['result'][0]:
					cis.append(respdict['result'][0]['sys_id'])
				else:
					flash("GSN Configuration Item for '%s' does not exist. CI has to exist before CTASK creation." % sbf['server_hostname'], 'danger')
					cifail = True

		if cifail:
			return redirect(url_for('sbfmanager.sbf', page=page, **filters))

		if sbflist[0]['location'] == "PRG":
			assignment_group = '4669db6afdf8a000b150d1a19ec281e0'
		elif sbflist[0]['location'] == "CBJ":
			assignment_group = 'bd695baafdf8a000b150d1a19ec28174'
		elif sbflist[0]['location'] == "US":
			assignment_group = 'd6a4cd85e8cb35003d92de4cd7ab24da'

		if delayed_why:
			u_special_instructions = "%d\nDelayed why: %s\n" % (len(cis), delayed_why)
		else:
			u_special_instructions = len(cis)

		rslt = client.service.insert(
			state = 110,
			u_change_stage = 'build_and_test',
			change_request = rfcdict[sbflist[0]["RFC"]],
			u_task_type = "build",
			assignment_group = assignment_group,
			short_description = short_description,
			description = description,
			work_start = work_start,
			work_end = work_start + timedelta(seconds=1),
			u_affected_cis = ','.join(cis),
			close_notes = "Server build completed, servers handed over to customer.",
			u_close_code = 'implemented',
			u_special_instructions = u_special_instructions)

		if 'number' in rslt:
			flash(rslt['number'] + ' "' + short_description + '" was created.', 'success')

			for sbf in sbflist:

				upsertor = SbfUpsertor(sbf)
				upsertor.SetScalar('ctask_are', rslt.get('number',0))
				upsertor.SetScalar('aredate', work_start)
				upsertor.SetScalar('delayed_why', delayed_why)
				upsertVal = upsertor.Execute()

		else:
			flash(rslt, 'danger')


	if len(ctaskdict) == 0:
		flash('No Build Task created.', 'info') #MM: TASK 142545: point (5) deactivated temporarily, no ctask creation possible:

	return redirect(url_for('sbfmanager.sbf', page=page, **filters))
'''

# protected by user certificates on the apache
@BP.route('/sbf-exp-ipcontrol/', methods=['GET'])
def sbf_exp_ipcontrol():

	hostname = request.args.get('hostname')
	if hostname is None or len(hostname) == 0:
		return json_response({
			'message' 	: "No valid hostname data provided",
			'error' 	: 404
		}, 404)

	#url="http://prgdca-lab-ipcmgr01.dhl.com:8080/inc-ws/services/Exports?wsdl"
	url="https://ipcontrol.dhl.com/inc-ws/services/Exports?wsdl"
	client = suds.client.Client(url, username=appsbf.app.config['IPCONTROL_USER'], password=base64.b64decode(appsbf.app.config['IPCONTROL_PASSWD']), timeout=360)

	rslt_init = client.service.initExportDevice(filter="name begins '{}'".format(hostname))

	sid = Element('sessionID')
	sid.set("SOAP-ENV:actor", "http://schemas.xmlsoap.org/soap/actor/next")
	sid.set("SOAP-ENV:mustUnderstand", "0")
	sid.set("xsi:type", "soapenc:long")
	sid.applyns(ns=('ns1','http://xml.apache.org/axis/session'))
	sid.setText(client.last_received().getChild('soapenv:Envelope').getChild('soapenv:Header').getChild('ns1:sessionID').getText())

	client.set_options(soapheaders=sid)
	rslt_exec = client.service.exportDevice(context=rslt_init)

	if rslt_exec is not None:

		hostnameIPlist = []
		for wsdevice in rslt_exec:
			hostnameIP = { 'hostname' : wsdevice.hostname }
			if len(wsdevice.interfaces) > 0 and len(wsdevice.interfaces[0].ipAddress) > 0:
				hostnameIP['ipAddress'] = wsdevice.interfaces[0].ipAddress[0]
			hostnameIPlist.append(hostnameIP)

		for hostnameIP in hostnameIPlist:

			client.set_options(soapheaders=None)
			context = client.service.initExportChildBlock(query="ipaddress='{}'".format(hostnameIP['ipAddress']), includeFreeBlocks=False)
			sid.setText(client.last_received().getChild('soapenv:Envelope').getChild('soapenv:Header').getChild('ns1:sessionID').getText())
			client.set_options(soapheaders=sid)
			blocks = client.service.exportChildBlock(context=context)

			for block in blocks:
				if block.childBlock.blockStatus == "Deployed":

					if str(block.childBlock.blockSize).isdigit():
						nlen = int(str(block.childBlock.blockSize))
						if nlen >= 0 and nlen <= 32:
							hostnameIP['netmask'] = '.'.join([str((0xffffffff << (32 - nlen) >> i) & 0xff) for i in [24, 16, 8, 0]])

					if block.childBlock.userDefinedFields:
						for udf in block.childBlock.userDefinedFields:
							if udf.startswith("vname="):
								hostnameIP['vname'] = udf[6:]
							elif udf.startswith("vno="):
								hostnameIP['vno'] = udf[4:]

					if block.subnetPolicy.defaultGateway:
						hostnameIP['gateway'] = block.subnetPolicy.defaultGateway
	else:
		hostnameIPlist = []

	return json_response(hostnameIPlist)

@BP.route('/_ajax/search/IPControl/exportDevice', methods=['GET'])
@fresh_login_required
def ipcontrol_export_device():
	return sbf_exp_ipcontrol()

@BP.route('/_ajax/ad_check', methods=['GET'])
@fresh_login_required
def ad_check():

	succUsers = []
	failUsers = []
	succGroups = []
	failGroups = []

	user_domains = request.args.getlist('user_domain[]')
	user_logins = request.args.getlist('user_login[]')
	group_domains = request.args.getlist('group_domain[]')
	group_names = request.args.getlist('group_name[]')

	try:

		for i in range(len(user_logins)):
			rec = EXTUserSearch(appsbf.app, user_logins[i], exact=True, domain=user_domains[i])

			if rec:
				succUsers.append(user_logins[i])
			else:
				failUsers.append(user_logins[i])

		for i in range(len(group_names)):
			rec = EXTexactGroupSearch(appsbf.app, group_names[i], group_domains[i])

			if rec:
				succGroups.append(group_names[i])
			else:
				failGroups.append(group_names[i])

		return json_response({'succ_users':succUsers, 'fail_users':failUsers, 'succ_groups':succGroups, 'fail_groups':failGroups})

	except Exception as e:
		error_message = e.message.get('desc')
		return json_response({'errors' : [error_message]}, 400)

@BP.route('/_ajax/vmware/allocate', methods=['GET'])
@fresh_login_required
def vmware_allocate():

	conf = DB.Conf.find_one({'_id' : 0})

	sbfid 			= request.args.get('sbfid')
	hostname 		= request.args.get('hostname')
	ram 			= request.args.get('ram')
	total_nr_of_cores = request.args.get('total_nr_of_cores')
	os_hdd_size 	= request.args.get('os_hdd_size') or 0
	data_hdd_size 	= request.args.get('data_hdd_size')
	data_sizes 		= request.args.getlist('data_sizes[]')
	data_disk_groups = request.args.getlist('data_disk_groups[]')
	vlans 			= request.args.getlist('vlans[]')
	platform 		= request.args.get('platform')
	release 		= request.args.get('release')
	project 		= request.args.get('project')
	location 		= request.args.get('location')
	purpose 		= request.args.get('purpose')
	application 	= request.args.get('application')
	server_env		= request.args.get('server_env')
	server_model	= request.args.get('server_model')
	clusterId 		= request.args.get('clusterId')

	app_cluster_nodes = []
	if clusterId:
		cluster = DB.Cluster.find_one({'_id':long(clusterId)})
		app_cluster_nodes = cluster.get('cluster_ACNodes') or []

	sbf = DB.SBF.find_one({'_id':long(sbfid)})

	data_hdd = []

	if platform == "Windows" and len(data_sizes) > 0:
		for xgb in data_sizes:
			if xgb.strip() != '':

				try:
					xgb = round(float(xgb), 2)
				except Exception as e:
					return json_response({'errors' : ["data drive value '{}' can't be converted to float GB number".format(xgb)]}, 400)

				data_hdd.append(xgb)
	else:
		# disk groups summary
		dgs = {}
		for i, xgb in enumerate(data_sizes):

			if xgb.strip() != '':

				try:
					xgb = float(xgb)
				except Exception as e:
					return json_response({'errors' : ["data drive value '{}' can't be converted to float GB number".format(xgb)]}, 400)

				dg = data_disk_groups[i]
				if dg in dgs:
					dgs[dg] += xgb
				else:
					dgs[dg] = xgb

		for k,v in dgs.items():
			data_hdd.append(int(ceil(v)))

	if len(data_hdd) == 0 and data_hdd_size != "":
		data_hdd.append(int(data_hdd_size))

	if sbfid is not None:

		server_proxy = xmlrpclib.ServerProxy('http://czchows226.prg-dc.dhl.com/xmlrpc/')

		try:

			params = [
				'029qonalmq10uo0hiofxca',									# string
				int(sbfid),													# int
				hostname,													# string
				0 if ram == "" else int(ram),								# int
				0 if total_nr_of_cores == "" else int(total_nr_of_cores),	# int
				int(os_hdd_size),											# int
				data_hdd,													# array
				vlans,														# array
				string.lower(platform),										# string
				release,													# string
				conf['server-rooms'].get(location, {}).get(purpose, ""),	# string
				application,												# string
				project,													# string
				app_cluster_nodes,											# array
				server_env,													# string
				server_model,												# string
				has_mysql(sbf),												# bool
			]

			print "xmlrpc call start timestamp"
			rslt = server_proxy.vmware.allocate(*params)
			print "xmlrpc call end timestamp"
			return json_response(rslt)

		except Exception as e:
			print "xmlrpc call exception timestamp"
			return json_response({'errors' : [cgi.escape("{}".format(e))]}, 400)

	return json_response({'errors' 	: ["No valid data provided for {} and {}".format(sbfid, hostname)]}, 400)

@BP.route('/_csv/export/commissioned_sbfs', methods=['GET'])
@fresh_login_required
def commissioned_sbfs():

	commissioned = DB.SBF.inline_map_reduce(
		'''
			function ()
			{
				if ('location' in this && 'server_type' in this && 'phase' in this)
				{
					if (this.phase != 'proposal' && this.phase != 'draft' && this.phase != 'aip' && 'build' in this.phase_change)
					{
						var key = {
							'location' : this.location,
							'server_type' : this.server_type,
							'com_finish_year' : this.phase_change.build.getFullYear(),
							'com_finish_month' : this.phase_change.build.getMonth()+1
						}

						emit(key, 1)
					}
				}
			}
		''',
		'''
			function (key, counts)
			{
				for (var i = 0, sum=0; i < counts.length; i++) {
					sum += counts[i]
				}
				return sum
			}
		''')

	commDict = { (x['_id']['location'], x['_id']['server_type'], int(x['_id']['com_finish_month']), int(x['_id']['com_finish_year'])) : int(x['value']) for x in commissioned }

	rowLst = sorted(set(list((x['_id']['location'], x['_id']['server_type']) for x in commissioned)))
	colLst = sorted(set(list((int(x['_id']['com_finish_year']), int(x['_id']['com_finish_month'])) for x in commissioned)))

	f = tempfile.NamedTemporaryFile(delete=False)
	csvwriter = csv.writer(f)

	csvwriter.writerow(["", "Commissioned Servers Report - Server is counted here with date when it went to the Build phase."])
	csvwriter.writerow([])

	line=["{}/{}".format(x[1],x[0]) for x in colLst]
	line.insert(0, "")
	csvwriter.writerow(encodeRow(line))

	for row in rowLst:
		line = ["{} {}".format(row[0], row[1])]
		for col in colLst:
			if (row[0],row[1],col[1],col[0]) in commDict:
				line.append(commDict[(row[0],row[1],col[1],col[0])])
			else:
				line.append(0)
		csvwriter.writerow(encodeRow(line))

	f.close()

	body = open(f.name, 'r').read()
	response = make_response(body, 200)
	for header, value in prepareHeaders( "SBF_commissioned_"+datetime.now().strftime("%m-%d-%Y_%H-%M"), len(body)).items():
		response.headers[header] = value

	f.close()
	os.unlink(f.name)
	return response

@BP.route('/_csv/export/decommissioned_sbfs', methods=['GET'])
@fresh_login_required
def decommissioned_sbfs():

	decommissioned = DB.SBF.inline_map_reduce(
		'''
			function ()
			{
				if ('location' in this && 'server_type' in this && 'phase_change' in this && 'phase' in this)
				{
					if (this.phase == 'decommission' && 'decommission' in this.phase_change)
					{
						var key = {
							'location' : this.location,
							'server_type' : this.server_type,
							'decom_finish_year' : this.phase_change.decommission.getFullYear(),
							'decom_finish_month' : this.phase_change.decommission.getMonth()+1
						}

						emit(key, 1)
					}
				}
			}
		''',
		'''
			function (key, counts)
			{
				for (var i = 0, sum=0; i < counts.length; i++) {
					sum += counts[i]
				}
				return sum
			}
		''')

	decommDict = { (x['_id']['location'], x['_id']['server_type'], int(x['_id']['decom_finish_month']), int(x['_id']['decom_finish_year'])) : int(x['value']) for x in decommissioned }

	rowLst = sorted(set(list((x['_id']['location'], x['_id']['server_type']) for x in decommissioned)))
	colLst = sorted(set(list((int(x['_id']['decom_finish_year']), int(x['_id']['decom_finish_month'])) for x in decommissioned)))

	f = tempfile.NamedTemporaryFile(delete=False)
	csvwriter = csv.writer(f)

	csvwriter.writerow(["", "Decommissioned Servers Report - Server is counted here with date when it went to the Decommissioned phase."])
	csvwriter.writerow([])

	line=["{}/{}".format(x[1],x[0]) for x in colLst]
	line.insert(0, "")
	csvwriter.writerow(encodeRow(line))

	for row in rowLst:
		line = ["{} {}".format(row[0], row[1])]
		for col in colLst:
			if (row[0],row[1],col[1],col[0]) in decommDict:
				line.append(decommDict[(row[0],row[1],col[1],col[0])])
			else:
				line.append(0)
		csvwriter.writerow(encodeRow(line))

	f.close()

	body = open(f.name, 'r').read()
	response = make_response(body, 200)
	for header, value in prepareHeaders( "SBF_decommissioned_"+datetime.now().strftime("%m-%d-%Y_%H-%M"), len(body)).items():
		response.headers[header] = value

	f.close()
	os.unlink(f.name)
	return response

@BP.route('/_csv/export/released_sbfs', methods=['GET'])
@fresh_login_required
def released_sbfs():
	'''released servers into production'''
	to_production = DB.SBF.inline_map_reduce(
		'''
			function () {
				if ('location' in this && 'server_type' in this && 'phase' in this)
				{
					if (this.phase != 'proposal' && this.phase != 'draft' && this.phase != 'aip' && this.phase != 'build' &&
						'prod' in this.phase_change)
					{
						var key = {
							'location' : this.location,
							'server_type' : this.server_type,
							'prod_finish_year' : this.phase_change.prod.getFullYear(),
							'prod_finish_month' : this.phase_change.prod.getMonth()+1
						}

						emit(key, 1);
					}
				}
			}
		''',
		'''
			function (key, counts)
			{
				for (var i = 0, sum=0; i < counts.length; i++) {
					sum += counts[i];
				}
				return sum;
			}
		''')

	prodDict = { (x['_id']['location'], x['_id']['server_type'], int(x['_id']['prod_finish_month']), int(x['_id']['prod_finish_year'])) : int(x['value']) for x in to_production }

	rowLst = sorted(set(list((x['_id']['location'], x['_id']['server_type']) for x in to_production)))
	colLst = sorted(set(list((int(x['_id']['prod_finish_year']), int(x['_id']['prod_finish_month'])) for x in to_production)))

	f = tempfile.NamedTemporaryFile(delete=False)
	csvwriter = csv.writer(f)

	csvwriter.writerow(["", "Released Servers Report - Server is counted here with date when it went to the Production phase."])
	csvwriter.writerow([])

	line=["{}/{}".format(x[1],x[0]) for x in colLst]
	line.insert(0, "")
	csvwriter.writerow(encodeRow(line))

	for row in rowLst:
		line = ["{} {}".format(row[0], row[1])]
		for col in colLst:
			if (row[0],row[1],col[1],col[0]) in prodDict:
				line.append(prodDict[(row[0],row[1],col[1],col[0])])
			else:
				line.append(0)
		csvwriter.writerow(encodeRow(line))

	f.close()

	body = open(f.name, 'r').read()
	response = make_response(body, 200)
	for header, value in prepareHeaders( "SBF_released_"+datetime.now().strftime("%m-%d-%Y_%H-%M"), len(body)).items():
		response.headers[header] = value

	f.close()
	os.unlink(f.name)
	return response

@BP.route('/_csv/export/cpu_types_sbfs', methods=['GET'])
@fresh_login_required
def cpu_types_sbfs():

	mapFunction = '''

		function () {

			if ('platform' in this && 'server_model' in this && 'cputype' in this && 'total_nr_of_cores' in this)
			{
				var key = {
					'platform' : this.platform,
					'server_model' : this.server_model,
					'cpu_type' : this.cputype
				}

				var val = Math.round(100 * (parseFloat(this.total_nr_of_cores) / parseFloat(this.cputype.split('-')[0]))) / 100;
				if (isNaN(val))
					val = parseFloat(this.total_nr_of_cores)
				if (isNaN(val))
					val = 0;

				emit(key, val)
			}
		}
	'''

	reduceFunction = '''

		function (key, values) {

			var total = 0.0;
			for (var i = values.length - 1; i >= 0; i--) {
				total += values[i]
			}

			total = parseFloat(total)
			if (isNaN(total))
				total = 0

			return total
		}
	'''

	cpu_type_export_month = request.args.get('cpu_type_export_month')

	headerLine = None
	if cpu_type_export_month:

		year1, month1 = cpu_type_export_month.split('/')
		year2 = year1
		month2 = int(month1) + 1
		if month2 > 12:
			month2 = 1
			year2 = int(year1) + 1

		headerLine = ['Report for', '{}/{}'.format(month1, year1)]

		dateStart = datetime.strptime('{}-{}-01'.format(year1, month1), '%Y-%m-%d')
		dateEnd = datetime.strptime('{}-{}-01'.format(year2, month2), '%Y-%m-%d')

		query = {
			'phase' : { '$in' : ['build', 'prod'] },
			'$or' : [
				{'phase_change.build' : {
					'$gte' : dateStart,
					'$lt' : dateEnd
				}},
				{'phase_change.oat' : {
					'$gte' : dateStart,
					'$lt' : dateEnd
				}},
				{'phase_change.prod' : {
					'$gte' : dateStart,
					'$lt' : dateEnd
				}}
			]
		}

		serverCPUcounts = DB.SBF.inline_map_reduce(
			mapFunction,
			reduceFunction,
			query = query)

	else:

		serverCPUcounts = DB.SBF.inline_map_reduce(
			mapFunction,
			reduceFunction,
			query = {
				'phase' : { '$in' : ['build', 'prod'] }
			})

	serverCPUcountsDict = { (x['_id']['platform'], x['_id']['server_model'], x['_id']['cpu_type']) : float(x['value']) for x in serverCPUcounts }

	rowLst = sorted(set(list((x['_id']['platform'], x['_id']['server_model']) for x in serverCPUcounts)))
	colLst = sorted(set(list(x['_id']['cpu_type'] for x in serverCPUcounts)))

	def toNumberCPU(x):
		try:
			x = int(x.split('-')[0])
		except Exception:
			return 1000
		return x

	colLst = sorted(set(list(x['_id']['cpu_type'] for x in serverCPUcounts)), key=toNumberCPU)

	f = tempfile.NamedTemporaryFile(delete=False)
	csvwriter = csv.writer(f)

	csvwriter.writerow(["", "CPU Type Report - Number of CPU's of servers in Build or Production phase."])
	if cpu_type_export_month:
		csvwriter.writerow(headerLine)
	csvwriter.writerow([])

	line=[x for x in colLst]
	line.insert(0, "")
	csvwriter.writerow(encodeRow(line))

	for row in rowLst:
		line = ["{} {}".format(row[0], row[1])]
		for col in colLst:
			if (row[0],row[1],col) in serverCPUcountsDict:
				line.append(serverCPUcountsDict[(row[0],row[1],col)])
			else:
				line.append(0)
		csvwriter.writerow(encodeRow(line))

	f.close()

	body = open(f.name, 'r').read()
	response = make_response(body, 200)
	for header, value in prepareHeaders( "SBF_cpu_types_"+datetime.now().strftime("%m-%d-%Y_%H-%M"), len(body)).items():
		response.headers[header] = value

	f.close()
	os.unlink(f.name)
	return response

@BP.route('/_csv/export/server_models_sbfs', methods=['GET'])
@fresh_login_required
def server_models_sbfs():

	mapFunction = '''

		function () {

			if ('platform' in this && 'server_model' in this)
			{
				if ('build' in this.phase_change)
				{
					var key = {
						'platform' : this.platform,
						'server_model' : this.server_model,
						'year' : this.phase_change.build.getFullYear(),
						'month' : this.phase_change.build.getMonth()+1
					}

					if (this.phase == 'build' || this.phase == 'prod' || this.phase == 'decommission')
						emit(key, 1)
				}
			}
		}
	'''
	reduceFunction = '''

		function (key, counts)
		{
			for (var i = 0, sum=0; i < counts.length; i++) {
				sum += counts[i]
			}
			return sum
		}
	'''

	serverModels = DB.SBF.inline_map_reduce(
		mapFunction,
		reduceFunction,
		query = {
			'phase' : { '$in' : ['build', 'prod', 'decommission'] }
		})

	serverModelsDict = { (x['_id']['platform'], x['_id']['server_model'], int(x['_id']['month']), int(x['_id']['year'])) : int(x['value']) for x in serverModels }

	rowLst = sorted(set(list((x['_id']['platform'], x['_id']['server_model']) for x in serverModels)))
	colLst = sorted(set(list((int(x['_id']['year']), int(x['_id']['month'])) for x in serverModels)))

	f = tempfile.NamedTemporaryFile(delete=False)
	csvwriter = csv.writer(f)

	csvwriter.writerow(["", "Server Models Report - Server is counted here with date when it went to the Build phase."])
	csvwriter.writerow([])

	line=["{}/{}".format(x[1],x[0]) for x in colLst]
	line.insert(0, "")
	csvwriter.writerow(encodeRow(line))

	for row in rowLst:
		line = ["{} {}".format(row[0], row[1])]
		for col in colLst:
			if (row[0],row[1],col[1],col[0]) in serverModelsDict:
				line.append(serverModelsDict[(row[0],row[1],col[1],col[0])])
			else:
				line.append(0)
		csvwriter.writerow(encodeRow(line))

	f.close()

	body = open(f.name, 'r').read()
	response = make_response(body, 200)
	for header, value in prepareHeaders( "SBF_models_"+datetime.now().strftime("%m-%d-%Y_%H-%M"), len(body)).items():
		response.headers[header] = value

	f.close()
	os.unlink(f.name)
	return response

@BP.route('/_csv/export/sbfs', methods=['GET'])
@fresh_login_required
def export_sbfs():

	_, profile_settings = Profile.get_active_SBF_profile()
	filters=dict((key, value) for key, value in request.args.iteritems() if 'filter_' in key and value != '')
	# remove on export sorting 'cause of RAM limitation
	sbfs, _, lastUpdate, clusters, projects = get_sbfs_rows_from_profile(profile_settings, 'all', filters, sortme=False)

	f = tempfile.NamedTemporaryFile(delete=False)
	csvwriter = csv.writer(f)
	for line in _prepareSBFsLines(sbfs, clusters, projects, lastUpdate):
		csvwriter.writerow(encodeRow(line))
	f.close()

	body = open(f.name, 'r').read()
	response = make_response(body, 200)
	for header, value in prepareHeaders( "SBF_list_"+datetime.now().strftime("%m-%d-%Y_%H-%M"), len(body)).items():
		response.headers[header] = value

	f.close()
	os.unlink(f.name)
	return response

def _prepareSBFsLines(sbfs, clusters, projects, lastUpdate):
	lines = []
	lines.append(
		[
			'SBF ID',
			'Phase',
			'Hostname',
			'RFC',
			'RFC Description',
			'Requestor',
			'Change Coordinator',
			'CRM Proposal Number',
			'BSO',
			'RSO',
			'CRFC',
			'Comm. Start',
			'Comm. Finish',
			'Location',
			'Server Environment',
			'Platform',
			'Release',
			'HW',
			'Usage',
			'VLAN',
			'Total Nr of Cores',
			'CPU',
			'RAM',
			'HDD OS',
			'HDD Data',
			'Storage',
			'ARE Date',
			'ARE completed',
			'Fit to Cloud',
			'Shared',
			'Cluster'
		]
	)

	for sbf in sbfs:

		project = projects.get(sbf.get('projectid')) or {}
		line = []

		line.append(sbf.get('_id'))
		line.append(lookups.LookupPhase.Phases.get(sbf.get('phase')))
		line.append(sbf.get('server_hostname'))
		line.append(project.get('RFC'))
		line.append(project.get('GSN_short_description'))
		line.append(project.get('GSN_dv_u_requested_by'))
		line.append(project.get('GSN_dv_u_change_coordinator'))
		line.append(project.get('GSN_u_spot_quote_number'))
		line.append(project.get('GSN_u_sap_build_sales_order_number'))
		line.append(project.get('GSN_u_sap_run_sales_order_number'))
		line.append(sbf.get('com_rfc_no'))

		if sbf.get('com_start'):
			line.append(datetime.strptime(sbf.get('com_start'), '%Y/%m/%d').strftime(('%d/%b/%Y')))
		else:
			line.append('')

		if sbf.get('com_finish'):
			line.append(datetime.strptime(sbf.get('com_finish'), '%Y/%m/%d').strftime(('%d/%b/%Y')))
		else:
			line.append('')

		line.append((sbf.get('location', '') + ' ' + sbf.get('server_purpose', '')).strip())
		line.append(sbf.get('server_env', ''))
		line.append(sbf.get('platform'))
		line.append(sbf.get('release'))
		line.append(sbf.get('server_model'))
		line.append(sbf.get('citrix_silo_name') if sbf.get('server_usage') == 'CMDB Citrix silo name' else sbf.get('server_usage'))
		line.append(sbf.get('vlan-type'))
		line.append(sbf.get('total_nr_of_cores'))
		line.append(sbf.get('cputype'))
		line.append(sbf.get('ram'))

		if sbf.get('os_hdd_size_real'):
			line.append(str(sbf.get('os_hdd_size_real')) + "GB")
		else:
			line.append('')

		if sbf.get('data_hdd_size_real'):
			line.append(str(sbf.get('data_hdd_size_real')) + "GB")
		else:
			line.append('')

		storage=[]
		if sbf.get('tier0-in') is not None:
			storage.append("T0 " + str(sbf.get('tier0-in')) + "GB")
		if sbf.get('tier1-in') is not None:
			storage.append("T1 " + str(sbf.get('tier1-in')) + "GB")
		if sbf.get('tier2-in') is not None:
			storage.append("T2 " + str(sbf.get('tier2-in')) + "GB")
		if sbf.get('tier3-in') is not None:
			storage.append("T3 " + str(sbf.get('tier3-in')) + "GB")
		if sbf.get('tier4-in') is not None:
			storage.append("T4 " + str(sbf.get('tier4-in')) + "GB")
		line.append(' '.join(storage))

		if sbf.get('aredate'):
			line.append(sbf.get('aredate', '').strftime('%d/%b/%Y'))
		else:
			line.append('')


		line.append(sbf.get('delayed_why'))

		if sbf.get('fit_to_cloud') is not None:
			if sbf.get('fit_to_cloud') == True:
				if sbf.get('fit_to_cloud_attribute') == 'FULL':
					line.append('YES F')
				if sbf.get('fit_to_cloud_attribute') == 'PARTIAL':
					line.append('YES P')
				else:
					line.append('')
			else:
				line.append('NO')
		else:
			line.append('')

		cluster = clusters.get(sbf['_id'])
		if sbf.get('cluster') is not None and cluster is not None:

			clusterstr = []

			if cluster.get('cluster_HASharedTier0Size', False):
				clusterstr.append("T0HA " + str(cluster.get('cluster_HASharedTier0Size')) + 'GB')

			if cluster.get('cluster_HASharedTier1Size', False):
				clusterstr.append("T1HA " + str(cluster.get('cluster_HASharedTier1Size')) + 'GB')

			if cluster.get('cluster_HASharedTier2Size', False):
				clusterstr.append("T2HA " + str(cluster.get('cluster_HASharedTier2Size')) + 'GB')

			if cluster.get('cluster_DRSharedTier0Size', False):
				clusterstr.append("T0DR " + str(cluster.get('cluster_DRSharedTier0Size')) + 'GB')

			if cluster.get('cluster_DRSharedTier1Size', False):
				clusterstr.append("T1DR " + str(cluster.get('cluster_DRSharedTier1Size')) + 'GB')

			if cluster.get('cluster_DRSharedTier2Size', False):
				clusterstr.append("T2DR " + str(cluster.get('cluster_DRSharedTier2Size')) + 'GB')

			line.append(' '.join(clusterstr))

		else:
			line.append('')

		if sbf.get('cluster') is not None and cluster is not None:

			clusterstr = ['#' + str(cluster.get('_id'))]
			if cluster.get('cluster_type') is not None:
				clusterstr.append(cluster.get('cluster_type'))
			if cluster.get('cluster_hasHA') is True:
				clusterstr.append("HA")
			if cluster.get('cluster_hasDR') is True:
				clusterstr.append("DR")
			if cluster.get('cluster_hasAC') is True:
				clusterstr.append("AC")

			line.append(' '.join(clusterstr))
		else:
			line.append("No")

		lines.append(line)

	return lines


@BP.route('/sbf/pricing/<sbfid>', methods=['GET'])
@fresh_login_required
def pricing(sbfid):

	prev_url = request.args.get('prev_url')
	sbf = DB.SBF.find_one(long(sbfid))
	conf = DB.Conf.find_one({'_id' : 0})
	projecttitle=sbf.get('RFC', 'Project #' + sbf.get('projectid'))

	priceLog, priceList, priceDesc = getPriceList(sbf, conf)

	return render_template(
		'sbfmanager/pricing.html',
		projecttitle=projecttitle,
		sbfid=sbfid,
		priceList=priceList,
		priceLog=priceLog,
		priceDesc=priceDesc,
		prev_url=prev_url
	)

@BP.route('/sbf/history/<sbfid>', methods=['GET'])
@fresh_login_required
def history(sbfid):

	tab = request.args.get('tab')
	prev_url = request.args.get('prev_url')

	if sbfid != '!new':
		sbf = DB.SBF.find_one(long(sbfid))
		projecttitle=sbf.get('RFC', 'Project #' + sbf.get('projectid'))

		auditLog=list(DB.AuditLog.find({ "where": "SBF", "pk" : long(sbfid) }).sort('when', -1))
		auditLog.extend(list(DB.AuditLog.find({ "where": "Cluster", "pk" : sbf.get('clusterId', -1L) }).sort('when', -1)))
		auditLog = sorted(auditLog, key=lambda k: k['when'], reverse=True)

		if tab is not None and tab != "":
			filteredLog = copy.deepcopy(auditLog)
			for idx, log in enumerate(auditLog):
				for action, content in log['what'].items():
					for fieldname in content.keys():
						if LookupFieldTab(fieldname.split('__')[0]) != tab:
							del filteredLog[idx]['what'][action][fieldname]
			auditLog=filteredLog
	else:
		projecttitle = ""
		auditLog = []

	return render_template(
		'sbfmanager/auditlog.html',
		projecttitle=projecttitle,
		sbfid=sbfid,
		tab=tab,
		tabs=LookupTab.Tabs,
		auditLog=auditLog,
		prev_url=prev_url
	)

@BP.route('/sbf/<sbfid>', methods=['GET', 'POST'])
@BP.route('/sbf/', methods=['GET','POST'])
@fresh_login_required
def sbf(sbfid=None):

	page = int(request.args.get('page', 1))
	filters = dict((key, value) for key, value in request.args.iteritems() if 'filter_' in key and value != '')

	pagesize = request.args.get('sbflist-pagesize')

	if request.method == 'GET':
		action = request.args.get('action')

		if action == 'detail':
			return sbf_GET_detail(
				sbfid=sbfid,
				page=page,
				filters=filters)

		if action == 'print':
			return sbf_print(
				sbfid=sbfid)

		return sbf_GET_list_profile(
			pagesize=int(pagesize) if pagesize else -1,
			page=page,
			filters=filters)

	elif request.method == 'POST':

		action = request.form.get('action')
		if sbfid is not None:
			action = request.form.get('!action')
			if action == 'nextphase':
				return sbf_POST_setphase(sbfid, (1))
			elif action == 'prevphase':
				return sbf_POST_setphase(sbfid, (-1))

		if action == 'clone':
			return sbf_POST_clone(
				sbfid=request.form['sbfid'],
				cloneToProject=request.form.get('cloneToProject') or request.form.get('cloneToProposal'),
				numberOfClones=request.form.get('numberOfClones', 1),
				page=page,
				filters=filters)

		elif action == 'delete':
			return sbf_POST_delete(
				sbfid=request.form['sbfid'],
				page=page,
				filters=filters)

	raise RuntimeError("Invalid state reached.")


class ProjectLockedException(Exception):
	pass


def sbf_clone(sbfid, cloneToProject, numberOfClones="1"):
	sbf = DB.SBF.find_one({'_id' : long(sbfid)})

	if not re.match('^\d+$', numberOfClones):
		flash(Markup(
			'Count of clones must be a number between 1 and 100. You entered "{}" which is not a number'.format(numberOfClones)
		), 'danger')
		return

	numberOfClones = int(numberOfClones)
	if numberOfClones < 1 or numberOfClones > 100:
		flash(Markup(
			'Count of clones must be a number between 1 and 100. You entered {}.'.format(numberOfClones)
		), 'danger')
		return

	if cloneToProject is None:
		cloneToProject = sbf['projectid']

	project = DB.Project.find_one({'_id' : long(cloneToProject)})

	if project.get('project_lock'):
		flash("Project #{} is locked.".format(cloneToProject), 'danger')
		raise ProjectLockedException()

	sbf['projectid'] = cloneToProject
	if project.get('RFC'):
		sbf['RFC'] = project['RFC']
		sbf['phase'] = 'draft'
	else:
		sbf['phase'] = 'proposal'
	#sbf['are_completed'] = 'NO'

	sbf.pop('_id')
	sbf.pop('Stamp')
	sbf.pop('_optlock')
	sbf.pop('hostname_allocs', None)
	sbf.pop('com_rfc_no', None)
	sbf.pop('com_start', None)
	sbf.pop('com_finish', None)

	sbf.pop('esx_virtual_server_loc', None)
	sbf.pop('clone_template', None)
	sbf.pop('cust_spec', None)
	sbf.pop('san_system_drive_locs', None)
	sbf.pop('san_data_drive_locs', None)

	sbf.pop('clusterId', None)
	sbf.pop('cluster', None)

	sbf.pop('comments-row', None)
	if sbf.get('server_hostname') is not None:
		sbf['server_hostname'] = "clone-of-" + sbf.get('server_hostname')

	sbf.pop('attachments-row', None)
	for oracleRow in sbf.get('oracle-row', []):
		oracleRow.pop('oracle_attach_row', None)

	sbf.pop('ci', None)
	sbf.pop('ctask_comm', None)
	sbf.pop('ctask_db', None)
	sbf.pop('ctask_mw', None)
	sbf.pop('ctask_backup', None)
	sbf.pop('ctask_mon', None)
	sbf.pop('aredate', None)
	sbf.pop('delayed_why', None)


	sbf_message_parts = []
	for clone_round in xrange(0, numberOfClones):
		upsertor = SbfUpsertor({})
		for key, value in sbf.iteritems():
			upsertor.SetScalar(key, value)

		ret = upsertor.Execute()
		cloned_sbf = ret.get('value') or sbf
		if ret.get('ok') != 1:
			flash(ret.get('err'), ret.get('alert'))
			return
		else:
			upsertor = SbfUpsertor(cloned_sbf)
			upsertor.SetScalar('server_hostname', 'tbd{}'.format(cloned_sbf['_id']))
			ret = upsertor.Execute()
			if ret.get('ok') != 1:
				flash(ret.get('err'), ret.get('alert'))
				return
			else:
				sbf_message_part = '<a href="{clone_url}">#{clone_id}</a>'.format(
						clone_id=cloned_sbf['_id'],
						clone_url=url_for('sbfmanager.sbf', sbfid=cloned_sbf['_id'], action='detail'),
					)
				sbf_message_parts.append(sbf_message_part)

	# increment sbfs_count in the Project
	project_id = long(sbf['projectid'])
	update_project_sbfs_count(project_id)

	flash(Markup(
		'SBF <a href="{orig_url}">#{orig_id}</a> ' \
		'cloned to SBF {sbf_parts} in project <a href="{project_url}">#{project_id}</a>.'.format(
			orig_id=sbfid,
			orig_url=url_for('sbfmanager.sbf', sbfid=sbfid, action='detail'),
			sbf_parts=', '.join(sbf_message_parts),
			project_id=sbf['projectid'],
			project_url=url_for('projectmanager.project', projectid=sbf['projectid']),
		),
	), 'success')


def sbf_POST_clone(sbfid, cloneToProject, numberOfClones, page, filters):
	try:
		sbf_clone(sbfid, cloneToProject, numberOfClones)
	except ProjectLockedException:
		return redirect(url_for('sbfmanager.sbf', page=page, **filters))
	else:
		return redirect(url_for('sbfmanager.sbf', page=page, **filters))


def filter_query(active_profile, filters=None):
	sbf_profile_columns = active_profile.get('columns',{})
	query = dict()
	if filters:
		query.update(dict((key.split('_', 1)[1], value) for key, value in filters.iteritems() if key == 'filter_projectid'))

	technicians_contact_name__map__project = sbf_profile_columns.get('technicians_contact_name:map:project',{}).get('filter',None)

	def get_sbf_owner(sbf_owner):
		my_projects = DB.Project.find({'RFC': {'$exists': True},
                                        '$or': [{'GSN_dv_u_requested_by': {'$regex': sbf_owner, '$options': 'i'}},
                                                {"GSN_dv_u_change_coordinator": {'$regex': sbf_owner, '$options': 'i'}}]},{'_id': 1})
		project_list = list(my_projects)
		projects_ids = [ (str(x.get('_id',''))) for x in project_list ]
		query.update({'$or': [{'technicians_contact_name': {'$regex': sbf_owner, '$options': 'i'}},
							  {'Stamp.CreationUser.Name': {'$regex': sbf_owner, '$options': 'i'}},
                              {'projectid': {'$in': projects_ids}}]})
		sbf_owner_add = sbf_profile_columns.pop('technicians_contact_name:map:project')
		return sbf_owner_add

	sbf_owner_add = get_sbf_owner(technicians_contact_name__map__project) if technicians_contact_name__map__project else None


	#location filter (location + server_purpose)
	location = sbf_profile_columns.get('location',{}).get('filter',None)

	def get_location(location):
		location_serverpurpose = location.split()
		if len(location_serverpurpose) > 1:
			query.update({	'location': {'$options':'i','$regex': location_serverpurpose[0]},
						'server_purpose':  {'$options':'i','$regex': location_serverpurpose[1]}})
		else:
			query.update({'$or': [	{'location': {'$options':'i','$regex': location_serverpurpose[0]}},
									{'server_purpose': {'$options':'i','$regex': location_serverpurpose[0]}}]})

		location_add = sbf_profile_columns.pop('location')
		return location_add

	location_add = get_location(location) if location else None
	#fit_to_coud flag
	fit_to_cloud_add = None
	fit_to_cloud = sbf_profile_columns.get('fitCloud',{}).get('filter',None)

	def get_fit_to_cloud(fit_to_cloud):
		if fit_to_cloud == 'NO':
			query.update({ 'fit_to_cloud': False })
		elif fit_to_cloud == 'YES F':
			query.update({ 'fit_to_cloud': True, 'fit_to_cloud_attribute': 'FULL'})
		elif fit_to_cloud == 'YES P':
			query.update({ 'fit_to_cloud': True, 'fit_to_cloud_attribute': 'PARTIAL'})
		else:
			pass
		return query

	if fit_to_cloud:
		return_cloud = get_fit_to_cloud(fit_to_cloud)
		if return_cloud:
			fit_to_cloud_add = sbf_profile_columns.pop('fitCloud')
	#as400
	cluster_add = None
	clusterId = sbf_profile_columns.get('clusterId',{}).get('filter', None)

	def get_cluster_complex_filter(clusterId):
	# 	# 347 HA DR AC Windows
		# split
		clusterId = clusterId.replace('#','')
		cluster_values = clusterId.split()

		clusterNo = None
		HA = None
		DR = None
		AC = None
		platf = None

		query_cluster = dict()

		for value in cluster_values:
			try:
				clusterNo = int(value)
				query_cluster.update({'_id': clusterNo })
				continue
			except Exception:
				pass
			if 'HA' == value.upper():
				query_cluster.update({'cluster_hasHA': True})
			elif 'DR' == value.upper():
				query_cluster.update({'cluster_hasDR': True})
			elif 'AC' == value.upper():
				query_cluster.update({'cluster_hasAC': True})
			elif (value.upper() in ['LINUX','HP-UX','WINDOWS', 'AIX', 'AS400']):
				query_cluster.update({'cluster_platform': { '$regex': value, '$options': 'i'}})
			elif (value.upper()  in ['VCS','MCS','ORACLE','STANDALONE','ASM','RAC','CFS','VXFS']):
				if query_cluster.has_key('cluster_type'):
					prev_val = query_cluster.get('cluster_type',{})
					new_val = ' '.join((prev_val.get('$regex'), value))
				else:
					new_val = value
				query_cluster.update({'cluster_type': {'$regex': new_val, '$options': 'i'}})

		return query_cluster

	if clusterId:
		query_cluster = get_cluster_complex_filter(clusterId)
		if query_cluster:
			clusters = DB.Cluster.find(query_cluster,{'_id': 1})
			clusters_sbfID = map(lambda x: x.get('_id'), list(clusters))
			as_cluster = {'$or': [{'as_clusterId': {'$in': clusters_sbfID}}, {'clusterId': {'$in': clusters_sbfID}}]}
			query.update(dict(as_cluster))
			cluster_add = sbf_profile_columns.pop('clusterId')

	int_types = (int, long)
	for key, value in sbf_profile_columns.iteritems():
		filter_value = value.get('filter')
		if isinstance(filter_value, bool):
			query[key] = filter_value or {'$in': [False, None]}
		elif not isinstance(value.get('filter',0), int_types) and 'date' not in key:
			query[key] = { '$regex': filter_value, '$options': 'i'}
		elif isinstance(value.get('filter',''), int_types) and key != 'filter_clusterId':
			query[key] = int(filter_value)
		elif 'date' in key and 'filter' in value and (
			isinstance(value.get('filter',''), unicode) or isinstance(value.get('filter',''), str)
		):
			query[key] = {
				'$gte':datetime.strptime(filter_value, '%Y/%m/%d'),
				'$lt':datetime.strptime(filter_value, '%Y/%m/%d') + timedelta(days=1),
			}
	sbfs = DB.SBF.find(query)

	if fit_to_cloud_add: sbf_profile_columns['fitCloud']=fit_to_cloud_add
	if cluster_add: sbf_profile_columns['clusterId']=cluster_add
	if location_add: sbf_profile_columns['location']=location_add
	if sbf_owner_add: sbf_profile_columns['technicians_contact_name:map:project']=sbf_owner_add
	return sbfs

def sort_by_phase_with_filter(sbfs_project, asc_desc = 'asc'):
	try:
		sorting_priority = {"proposal", "aip", "build", "prod", "decommission"}
		clone_sbfs_project = sbfs_project.clone()
		object_map = {p["phase"]: p for p in list(clone_sbfs_project)}
		objects = [object_map.get(phase,None) for phase in sorting_priority]
		return objects
	except:
		return sbfs_project

def sort_query(sbfs, active_profile, projectFilter = False):
	sbf_profile_columns = active_profile.get('columns',{})

	isAnySortingOn = dict( (key, value.get('sort')) for (key, value) in sbf_profile_columns.iteritems() if value.get('sort', '') in ['asc','desc'] )

	if any(isAnySortingOn):
		if isAnySortingOn.has_key('phase'):
			asc_or_desc = 1 if isAnySortingOn['phase'][0]=='asc' else -1
			sbfs.sort([('phase_num', asc_or_desc)])
		else:
			sort_map = map(lambda(k,v): (k, +1 if v=='asc' else -1), isAnySortingOn.iteritems())
			sbfs.sort(sort_map)

	else:
		sbfs.sort([("Stamp.CreationDate", -1)])

	return sbfs

def sort_by_phase_only(asc_desc = 'asc', active_profile=None, filters=None, page = 1):
	'''
	sorting in direction asc: proposal->aip->build->prod->decommission
	:param sbfs:
	:param asc_desc:
	'''
	def get_phase_filter(active_profile, filters):
		if active_profile is None: return
		sbf_profile_columns = active_profile.get('columns',{})

		query = dict()
		if filters:
			query.update(dict((key.split('_', 1)[1], value) for key, value in filters.iteritems() if key == 'filter_projectid'))

		cluster_add = None
		clusterId = sbf_profile_columns.get('clusterId',{}).get('filter', None)
		if clusterId:
			as_cluster = {'$or': [{'as_clusterId': clusterId},{'clusterId': clusterId}]}
			query.update(dict(as_cluster))
			cluster_add = sbf_profile_columns.pop('clusterId')

		query.update((key, { '$regex': val.get('filter'), '$options': 'i'}) for key, val in sbf_profile_columns.iteritems() if not isinstance(val.get('filter',0), (int, long))
					and 'date' not in key)
		query.update(dict((key, int(val.get('filter'))) for key, val in sbf_profile_columns.iteritems() if isinstance(val.get('filter',''), (int, long)) and key != 'filter_clusterId'))

		query.update(dict((key, {'$gte':datetime.strptime(value.get('filter'), '%Y/%m/%d'),
							'$lt':datetime.strptime(value.get('filter'), '%Y/%m/%d')+timedelta(days=1)})
					for key, value in sbf_profile_columns.iteritems() if 'date' in key and 'filter' in value and (isinstance(value.get('filter',''),unicode)
																					or isinstance(value.get('filter',''), str) ) ))

		if cluster_add: sbf_profile_columns['clusterId']=cluster_add
		return query

	def get_page_query(sbfs_list, page):
		pagesize = Profile.get_SBF_pages()

		if page != 'all':
			nrSkipRecords = int(pagesize * (page - 1))
			count = 0
			try:
					count = len(sbfs_list)
					sbfs = sbfs_list[nrSkipRecords:nrSkipRecords+pagesize]
					return count, sbfs
			except:
				return len(sbfs_list), sbfs_list
		else:
			return len(sbfs_list),sbfs_list

	try:
		sbfs = DB.SBF.find()
		filtered_query = get_phase_filter(active_profile, filters)
		keys = filtered_query.keys()

		pipeline = [
		{
		"$project": {
			"_id":1,
			"phase":1,
			"phase_new": {
				"$cond": { "if": {"$eq": ["$phase", 'proposal']}, "then": 1,
						"else":
							{
							"$cond": {
								"if": {"$eq": ["$phase", 'draft']}, "then": 2,
								"else":
								{
									"$cond": {
										"if": {"$eq": ["$phase", 'aip']}, "then": 3,
										"else":
										{
										"$cond": {
											"if": {"$eq": ["$phase", 'build']}, "then": 4,
											"else":
											{
											"$cond": {
												"if": {"$eq": ["$phase", 'prod']}, "then": 5,
												"else": 6
												}
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
		},
		{ "$match": filtered_query
		},
		{ "$sort": { "phase_new": 1 if asc_desc == 'asc' else -1 }}]

		dictproject = pipeline[0].get('$project')
		if any(dictproject):
			for key in filtered_query.keys():
				dictproject.update({key: 1})

		result = sbfs.collection.aggregate(pipeline)

		#guaranteed compatibility: monika
		#mongo V3 returns pymongo.command_cursor.CommandCursor, V2 returns dict
		new_sbfs = result.get("result") if isinstance(result, dict) else result

		if new_sbfs:
			# due to performance
			count, p_sbfs = get_page_query(new_sbfs, page)
			object_map = { orig_sbf["_id"]: orig_sbf for orig_sbf in sbfs}
			#objects = [object_map[id.get("_id")] for id in new_sbfs ]
			objects = [object_map[id.get("_id")] for id in p_sbfs ]
			return count, objects
		else:
			return sbfs.count(), sbfs
	except:
		return sbfs.count(), sbfs

def page_query(sbfs, page = 1):

	pagesize = Profile.get_SBF_pages()

	if page != 'all':
		nrSkipRecords = int(pagesize * (page - 1))
		count = 0
		try:
			if isinstance(sbfs, list):
				count = len(sbfs)
				if count > nrSkipRecords:
					sbfs = sbfs[nrSkipRecords:nrSkipRecords+pagesize]
				return count, sbfs
			else:
				if sbfs.count() > nrSkipRecords:
					sbfs.skip(nrSkipRecords).limit(pagesize)
				return sbfs.count(), sbfs
		except:
			return (len(sbfs), sbfs) if isinstance(sbfs, list) else (sbfs.count(), sbfs)
	else:
		return (len(sbfs),sbfs) if isinstance(sbfs, list) else (sbfs.count(), sbfs)

def get_sbfs_rows_from_profile(activated_profile, page, filters, sortme = True):

	sbf_profile_columns = activated_profile.get('columns',{})

	count = 0

	# Filter
	sbfs = filter_query(activated_profile, filters)
	# Sort
	if sortme: sbfs = sort_query(sbfs, activated_profile, True if filters else False)
	# Pagination
	count, sbfs = page_query(sbfs, page)

	# Get data from database
	sbfs = list(sbfs)

	# Modification timestamp
	lastUpdate = dict((lu.get('_id'), lu.get('Stamp',{}).get('ChangingDate') or lu.get('Stamp',{}).get('CreationDate','')) for lu in sbfs)

	clusters_all = { sbf['_id'] : DB.Cluster.find_one({'_id' : sbf['clusterId']}) for sbf in sbfs if sbf.get('cluster') is True and sbf.get('clusterId') is not None }
	clusters_as400 = { sbf['_id'] : DB.Cluster.find_one({'_id' : sbf['as_clusterId']}) for sbf in sbfs if sbf.get('as_cluster') is True and sbf.get('as_clusterId') is not None }
	clusters = dict(clusters_all, **clusters_as400)


	projectids = set(list(sbf.get('projectid', -1) for sbf in sbfs))
	projects = { projectid : DB.Project.find_one({'_id' : long(projectid)}) for projectid in projectids }

	return (sbfs, count, lastUpdate, clusters, projects)

# get site after saving profile to DB, select profile
# switch profile
def sbf_GET_list_profile(pagesize, page, filters):

	profile_name, profile_settings = Profile.get_active_SBF_profile()

	if pagesize != -1:
		Profile.set_SBF_pages(pagesize)

	sbfs, count, lastUpdate, clusters, _ = get_sbfs_rows_from_profile(profile_settings, page, filters)

	project = {}
	rfcfilter = {}
	if filters.get('filter_projectid') is not None:
		project = DB.Project.find_one({'_id' : long(filters.get('filter_projectid'))})
		rfcfilter={'filter__id:int' : filters.get('filter_projectid')}

	urls = { sbf['_id']: url_for('sbfmanager.sbf', sbfid=sbf['_id'], page=page, **filters) for sbf in sbfs }

	return render_template(
		'sbfmanager/sbflist.html',
		sbfs=sbfs,
		project=project,
		lastUpdate=lastUpdate,
		clusters=clusters,
		page=page,
		count=count,
		filters=filters,
		rfcfilter=rfcfilter,
		urls=urls,
		pagesize=Profile.get_SBF_pages(),
		custom_profile_settings=profile_settings if profile_name=='custom' else {}
		)


def sbf_GET_detail(sbfid, page, filters):

	if sbfid == '!new':
		sbf = {"_id" : '!new'}
	else:
		sbf = DB.SBF.find_one({"_id" : long(sbfid)})
		if sbf is None:
			abort(404)

	conf = DB.Conf.find_one({'_id' : 0})
	loc_os_rel = filter_loc_os_rel(conf['loc-os-rel'], current_user.in_roles(['admin', 'exc']), sbf.get('location'), sbf.get('release'))
	hw = conf['hardware']
	storage = conf['disk_layout']
	disk_layout = conf['disk_layout']
	timezones = conf['timezone']
	infx = conf['informix']
	dbs = conf['db-tabs']
	oracle = conf['oracle']
	user_shell = conf['user_shell']
	server_env = conf['server_env']
	file_system = conf['FSType']
	parent_root_autogen = list(conf.get('Storage_tab',[]).get('parent_root_autogen','').keys())

	projectid = long(sbf.get('projectid', filters.get('filter_projectid')))
	project = DB.Project.find_one({'_id' : projectid })
	url=url_for('sbfmanager.sbf', sbfid=sbfid, action="detail", page=page, **filters)
	accessDict=DB.Access.find_one({'_id' : 0})
	appver = { x['_id']['application'] + ' ' + x['_id']['platform'] : x['version'] for x in DB.AppVer.find({})}

	## configuration initialization ##
	ApplicationTab.init_array_in_installed_db_for_all_releases()
	installed_by = ApplicationTab.db_config

	return render_template(
		'sbfmanager/sbfdetail.html',
		project=project,
		sbf=sbf,
		page=page,
		filters=filters,
		tabs=LookupTab.Tabs,
		conf=dict(conf),
		loc_os_rel=loc_os_rel,
		hw=hw,
		storage=storage,
		disk_layout=disk_layout,
		timezones=timezones,
		infx=infx,
		dbs=dbs,
		oracle=oracle,
		user_shell=user_shell,
		server_env=server_env,
		accessDict=accessDict,
		rfcfilter={'filter__id:int' : projectid},
		url=url,
		appver=appver,
		file_system=file_system,
		parent_root_autogen=parent_root_autogen,
		installed_by=installed_by)

def sbf_POST_delete(sbfid, page, filters):

	sbf = DB.SBF.find_one({'_id' : long(sbfid)})
	if sbf is not None:
		project_id = long(sbf.get("projectid", None))
		sbfRemover = SbfRemover(long(sbfid))
		ret = sbfRemover.Execute()
		if ret.get('ok') != 1:
			# delete sbfs_count from project
			flash(ret.get('err'), ret.get('alert'))
		else:
			update_project_sbfs_count(project_id)
			flash('SBF {} removed'.format(sbfid), 'success')

	return redirect(url_for('sbfmanager.sbf', page=page, **filters))

def isValidationWithoutError(result):
	if result is True:
		return True
	if "errors" in result:
		if not result["errors"]:
			return True
	return False


#@require_csrf_token()
def sbf_POST_setphase(sbfid, delta):
	page = int(request.args.get('page', 1))
	filters = dict((key, value) for key, value in request.args.iteritems() if 'filter_' in key and value != '')

	resultSP = switchPhase(sbfid, delta=delta)
	for field, notification_type in {
		'errors': 'danger',
		'warnings': 'warnings',
		'info': 'info',
		'success': 'success',
	}.items():
		for result in resultSP.get(field) or []:
				flash(result, notification_type)
	#flash(resultSP.get('fieldErrors', ''), 'danger')

	if resultSP.get('ok') != 1:
		return redirect(url_for('sbfmanager.sbf', sbfid=sbfid, page=page, action='detail', **filters))
		#return json_response(resultSP, 400)
	return redirect(url_for('sbfmanager.sbf', sbfid=sbfid, page=page, action='detail', **filters))


def add_middleware_relation_to_ci(sbf):
	from appsbf.services.cmdb_lookup_service import lookup_cmdb_ids

	cmdb_ids = lookup_cmdb_ids(sbf)
	warnings = []
	if not cmdb_ids:
		return {}
	try:
		rfc_sys_id = cmdb.check_rfc_existence(sbf.get('RFC'))
		if not rfc_sys_id:
			warnings.append("{} does not exist in GSN.".format(sbf.get('RFC')))
		else:
			crfc_sys_id = cmdb.check_rfc_existence(sbf.get('com_rfc_no'))
			if not crfc_sys_id:
				warning_msg = "Commissioning {} does not exist in GSN.".format(sbf.get('com_rfc_no'))
				warnings.append(warning_msg)
				logger.warning(warning_msg)
			else:
				for item_search_code in cmdb_ids:
					logger.info('Checking of existence of item with search code "{}"'.format(item_search_code))
					sys_id = cmdb.check_searchcode_existence('u_dhl_ci_sw', item_search_code)
					if not sys_id:
						warning_msg = "Item {} does not exist in GSN.".format(item_search_code)
						warnings.append(warning_msg)
						logger.warning(warning_msg)
					else:
						server_sys_id = cmdb.check_server_existence(sbf)
						if not server_sys_id:
							warning_msg = "SBF #{} CI does not exist in GSN.".format(sbf['_id'])
							warnings.append(warning_msg)
							logger.warning(warning_msg)
						else:
							result = cmdb.create_sbf_relation(
								sys_id, server_sys_id, rfc_sys_id, crfc_sys_id,
								relation_type="Contains::Installed on"
							)
							logger.info(result)
		if warnings:
			return {"warnings": warnings}
	except Exception as e:
		message = "'{}' raised when trying to connect to CMDB".format(e)
		logger.critical(message)
		import traceback
		traceback.print_exc()
		return {"errors": [message]}
	else:
		return {"info": ["Relation for '{}' middleware was created on CMDB".format(item_search_code)]}


def write_validation_result(newObj, result):
	newUpsertor = SbfUpsertor(newObj)
	result_copy = copy.copy(result)
	for field in ('success', 'info', 'value'):
		if field in result_copy:
			result_copy.pop(field)
	newUpsertor.SetScalar("Validation", result_copy)
	validationUpdRslt = newUpsertor.Execute()
	newObj = validationUpdRslt.get('value') or newObj
	newObj['Validation'] = result
	return newObj


def switchPhase(sbfid, delta):

	if delta == 0:
		return {'ok' : 1, 'info' : ['SBF already has requested phase.']}

	origObj = DB.SBF.find_one({'_id' : long(sbfid)})
	if origObj is None:
		return {'ok' : 0, 'errors' : ['Couldn\'t find SBF with id "{}".'.format(sbfid)]}

	upsertor 		= SbfUpsertor(origObj)
	currentPhase 	= origObj.get('phase')
	allPhases		= lookups.LookupPhase.Phases
	allPhasesKeys 	= allPhases.keys()

	if delta > 0:
		result = {}
		valid = validateSbfClusterSG(sbfid)
		if valid is not True and len(valid.get('errors', [])) > 0:
			result['errors']	  = extendList(result.get('errors'), valid.get('errors'))
			result['warnings']	= extendList(result.get('warnings'), valid.get('warnings',[]))
			result['fieldErrors'] =  merge_results(result.get('fieldErrors', {}), valid.get('fieldErrors', {}))
			result['ok']		  = 0
			result['info']		= appendToList(result.get('info',[]), 'Unable to change phase - there are some validation errors.')
			write_validation_result(origObj, result)
			return result

	if currentPhase is None:
		return {'ok' : -1, 'errors' : ['Phase not set. Save data first.']}

	currentPhaseIndex = allPhasesKeys.index(currentPhase)
	newPhaseIndex = currentPhaseIndex + delta

	if newPhaseIndex < 0 or newPhaseIndex > len(allPhasesKeys)-1:
		return {'ok' : -1, 'errors' : ['Phase index out of range. Refresh data please.']}

	newPhase = allPhasesKeys[newPhaseIndex]

	def can_switch_phase_right(currentPhase, nextPhase):
		access = DB.Access.find_one({ 'from' : currentPhase, 'to' : nextPhase })
		if not access:
			return False
		for role in current_user.Roles:
			if role in access.get('roles'):
				return True
		return False

	if not can_switch_phase_right(currentPhase, newPhase):
		return {'ok' : 0, 'warnings' : ['You are not allowed to switch phase to "{}".'.format(allPhases.get(newPhase))]}

	upsertor.SetScalar('phase', newPhase)
	upsertor.SetScalar('phase_num', lookups.LookupPhase.Phases_num.get(newPhase))
	upsertor.SetScalar('phase_change.' + newPhase, datetime.now())
	upsertor.SetScalar('phase_leave.' + currentPhase, datetime.now())
	resU = upsertor.Execute()
	if resU.get('ok') != 1:
		if resU.get('alert') == 'info':
			return {'ok' : 1, 'errors' : [resU.get('err')]}
		else:
			return {'ok' : 0, 'errors' : [resU.get('err')]}

	result = {'ok' : 1, 'success' : ['SBF phase changed to "{}"'.format(allPhases.get(newPhase))]}

	if newPhase == 'prod' and newPhaseIndex > currentPhaseIndex:
		result = merge_results(result, add_middleware_relation_to_ci(origObj))

	return result

@BP.route('/ui-sbf-exp/<sbfid>', methods=['GET', 'POST'])
@BP.route('/ui-sbf-exp/', methods=['GET','POST'])
@fresh_login_required
def sbf_export_ui(sbfid=None):
	return sbf_export(sbfid)

@BP.route('/sbf-exp-locations/', methods=['GET'])
def sbf_export_locs():

	server_env_dict = DB.Conf.find_one({'_id' : 0})['server_env']
	rooms_dict = DB.Conf.find_one({'_id' : 0})['server_rooms']
	locations = set()
	rooms = {}

	for server_purpose, support_level_dict in server_env_dict.items():
		for support_level, locations_dict in support_level_dict.items():
			for location, server_env_list in locations_dict.items():
				for server_env in server_env_list:
					locations.add(location + ' ' + server_env if location != server_env else location)

	for location, server_env_dict in rooms_dict.items():
		for server_env, rooms_list in server_env_dict.items():
			rooms[location + ' ' + server_env if location != server_env else location] = sorted(rooms_list)

	resp = json_response({'locations' : sorted(list(locations)), 'rooms': rooms}, 200)
	resp.headers["Content-Disposition"] = "attachment; filename=locations.json"
	return resp

@BP.route('/sbf-exp/<sbfid>', methods=['GET', 'POST'])
@BP.route('/sbf-exp/', methods=['GET','POST'])
# @fresh_login_required
def sbf_export(sbfid=None):

	if not sbfid:
		sbfid = int(request.args.get('sbfid', 0))
	server_hostname = request.args.get('hostname',None)
	fileformat = request.args.get('format',"csv")
	project_id = request.args.get('projectid',None)
	if project_id:
		project_id = long(project_id)
	rfc = request.args.get('rfc',None)

	content	= request.args.get('content',None)

	if content != "license":
		if not sbfid and not server_hostname:
			if content in ["cluster","general","oat"] :
				fileformat = "xml"
			return sbf_export_error(fileformat,"Invalid parameters: id or hostname expected")

	if content == "cluster":
		return sbf_export_cluster(server_hostname, sbfid)
	elif content == "general":
		return sbf_export_general(server_hostname, sbfid)
	elif content == "vm":
		return sbf_export_vm(server_hostname, sbfid)
	elif content == "sudo":
		return sbf_export_sudo(server_hostname, sbfid)
	elif content == "osparams":
		return sbf_export_osparams(server_hostname, sbfid)
	elif content == "oat":
		return sbf_export_oat(
				hostname=server_hostname,
				sbfid = sbfid
				)
	elif any(content in s for s in ["users","groups","storage","license"]):
		return sbf_export_to_csv(
				hostname=server_hostname,
				sbfid=sbfid,
				content=content,
				projectid = project_id,
				rfc = rfc
				)
	elif content == "esm":
		return sbf_export_esm(
				hostname=server_hostname,
				sbfid = sbfid
				)
	elif content == "pat":
		return sbf_export_pat(
				hostname=server_hostname,
				sbfid = sbfid
				)

	return sbf_export_error(fileformat, "Invalid parameters")

@BP.route('/info.php', methods=['GET'])
@BP.route('/info', methods=['GET'])
# @fresh_login_required
def sbf_info_oat():
	hostname = request.args.get('hostname',None)
	sbfid = request.args.get('sbfid',None)
	if not hostname and not sbfid:
		return sbf_export_error_xml("Invalid parameters: hostname or SBF id is expected")

	if request.method == 'GET':
		return sbf_export_oat(
				hostname=hostname,
				sbfid = sbfid
				)

	return sbf_export_error_xml("Unknown command")

def validateSbfClusterSG(sbfid, data={}):
	res = True
	result = {'errors' : [], 'warnings' : [], 'fieldErrors' : {}, 'fieldWarnings' : {}}

	### Validate
	valid 		= True
	origSbfObj 	= {} if sbfid == "!new" else DB.SBF.find_one({'_id' : long(sbfid)})
	clusterId 	= getNewValue('clusterId', origSbfObj, data)

	sbfErr = False

	## SBF
	sbfValidator= SbfValidator(data, origSbfObj)
	resV 		= sbfValidator.Validate()
	if resV is not True:
		valid = False
		# update result with validation result
		result['fieldErrors'] 	= merge_results(result.get('fieldErrors', {}), resV)
		result['errors'] 		= appendToList(result.get('errors'), 'There are some errors in SBF fields.')
		sbfErr = True
		result['warnings'] 		= extendList(result.get('warnings'), resV.get('warnings',[]))

	if resV is True or (isinstance(resV, dict) and not resV.get('fatal_error')):
		#do post validation if not fatal error
		resultPost = sbfValidator.PostValidate()
		if resultPost is not True:
			valid = False
			# update result with validation result
			result['fieldErrors'] 	= merge_results(result.get('fieldErrors', {}), resultPost['fieldErrors'])
			result['errors'] 		= result['errors'] + resultPost['errors']
			result['fieldWarnings'] 	= merge_results(result.get('fieldWarnings', {}), resultPost['fieldWarnings'])
			result['warnings'] 		= result['warnings'] + resultPost['warnings']

			if not sbfErr and (result['fieldErrors'] or result['errors']):
				result['errors'] = appendToList(result.get('errors'), 'There are some errors in SBF fields.')


	clusterId = getNewValue('clusterId', origSbfObj, data)
	origClusterObj 	= DB.Cluster.find_one({'_id' : long(clusterId)}) if clusterId is not None else None

	## Cluster
	if origClusterObj is not None:
		clusterValidator= ClusterValidator(data, origClusterObj)

		resCV 			= clusterValidator.Validate()
		if resCV is not True:
			valid = False
			# update result with validation result
			result['fieldErrors'] 	= merge_results(result.get('fieldErrors', {}), resCV)
			result['errors'] 		= appendToList(result.get('errors'), 'There are some errors in Cluster fields')

	if valid is not True:
		return result
	return True

def update_project_sbfs_count(project_id):
	project = DB.Project.find_one({'_id' : project_id })
	if project is not None:
		sbfs_count = DB.SBF.find({"projectid": str(project_id)},{"_id": 1}).count() or 0;
		DB.Project.update({'_id' : project_id}, {'$set' : {'sbfs_count' : sbfs_count }})


@BP.route('/_ajax/SBF/service/add', methods=['POST'])
@fresh_login_required
def sbf_add_service_to_multiple_sbf():
	selected_sbfs = request.form.get('selectedSBFs')
	selected_service = request.form.get('selectedService')
	if selected_sbfs == '':
		sbf_list = []
	else:
		sbf_list = selected_sbfs.split(',')
	sbf_list_ints = [int(sbf_id) for sbf_id in sbf_list]

	sbfs = list(DB.SBF.find({'_id': {'$in': sbf_list_ints}}))

	for sbf in sbfs:
		current_service_names = sbf.get('service_names', [])
		plain_names = [r['service_name'] for r in current_service_names]

		if selected_service not in plain_names:
			upsertor = SbfUpsertor(sbf)
			upsertor.PushItem('service_names', {'service_name': selected_service})
			upsertVal = upsertor.Execute()

	return jsonify(result=[])
