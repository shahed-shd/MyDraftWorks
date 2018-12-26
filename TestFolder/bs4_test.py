import pprint

from bs4 import BeautifulSoup


with open('anis_fb_profile.html', 'r') as fp:
	soup = BeautifulSoup(fp, 'html.parser')

id_val_list = ["work", "education", "skills", "living", "contact-info", "basic-info", "nicknames", "relationship", "family", "bio", "year-overviews", "quote"]

info_dict = {}


# ---------- work, education ----------
def parse_list_section(sec_name):
	section = soup.find(id=sec_name)
	dzs = section.find_all(class_='dz')

	section_list = []
	for dz in dzs:
		ea = dz.find(class_='ea')
		eds = dz.find_all(class_='ed')
		section_list.append({'institution': ea.text, 'info': [ed.text for ed in eds]})
	info_dict[sec_name] = section_list


# ---------- skills ----------
def parse_skills_info():
	skills = soup.find(id='skills')
	skills.find(class_='ci').text
	info_dict.update(skills=skills.find(class_='ci').text)


# ---------- living, contact-info, basic-info, nicknames ----------
def parse_tabled_section(sec_name):
	info_dict[sec_name] = {}

	section = soup.find(id=sec_name)
	tbls = section.find_all('table')

	for tbl in tbls:
		trs = tbl.find_all('tr')

		for tr in trs:
			eo = tr.find(class_='eo')
			eq = tr.find(class_='eq')

			if eo and eq:
				info_dict[sec_name][eo.text] = eq.text


# ---------- family ----------
def parse_family_members():
	family = soup.find(id='family')
	dws = family.find_all(class_='dw')

	member_list = []
	for dw in dws:
		cm = dw.find(class_='cm')
		cp = dw.find(class_='cp')
		member_list.append({'member': cm.text, 'relation': cp.text})
	info_dict['family'] = member_list


# ---------- bio, quote ----------
def parse_single_string_info(sec_name):
	section = soup.find(id=sec_name)
	dw = section.find(class_='dw')
	info_dict[sec_name] = dw.text


def parse_year_overviews():
	year_overviews = soup.find(id='year-overviews')
	dp = year_overviews.find(class_='dp')
	fcs = dp.find_all(class_='fa fb fc')

	print("HERE", fcs)
	
	year_overviews_list = []
	for fc in fcs:
		cc = fc.find(class_='cc')
		cqs = fc.find_all(class_='cq')
		year_overviews_list.append({'year': cc.text, 'events': [cq.text for cq in cqs]})
	info_dict.update({'year-overviews': year_overviews_list})


parse_list_section('work')
parse_list_section('education')
parse_skills_info()
parse_tabled_section('living')
parse_tabled_section('contact-info')
parse_tabled_section('basic-info')
parse_tabled_section('nicknames')
parse_family_members()
parse_single_string_info('bio')
parse_year_overviews()
parse_single_string_info('quote')

pprint.pprint(info_dict)