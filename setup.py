from setuptools import setup, find_packages

setup(
	name="apexaiassistant",
	version="0.0.1",
	description="Apex Erpnext Ai Assistant",
	author="Apexlogic Technology",
	author_email="info@apexlogicsoftware.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[
		"openai>=1.0.0"
	]
)
