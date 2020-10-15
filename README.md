![Layer-8-Logo-Wide](https://user-images.githubusercontent.com/8293038/96061566-93d8af00-0e61-11eb-8b84-3fd207290be2.png)

# ConvertHound
Convert [BloodHound](https://github.com/BloodHoundAD/BloodHound) zip files to nmap xml for use in reporting software. Created by [Cory Wolff](https://github.com/cwolff411) from [Layer 8 Security](https://layer8security.com)

### Installation
`git clone https://github.com/layer8secure/converthound`

### Usage
`python3 converthound.py convert BLOODHOUND_ZIP_FILE`

Should work without additional dependencies.

Takes an BLOODHOUND ZIP FILE and outputs an nmap xml file of the discovered hosts and a csv file of discovered usernames. Outputs to the ./converthound directory.

![ConvertHound](https://user-images.githubusercontent.com/8293038/96060567-df3d8e00-0e5e-11eb-9587-60c5144e18bf.png)


### About

Built as an easy way to convert BloodHound output files into data that can be imported into reporting software like Dradis and Plextrac.

When a BloodHound zip file is converted two files are generated and placed in the `./converthound` folder:

1. **ORIGINAL_FILE_NAME**_computers.xml
2. **ORIGINAL_FILE_NAME**_users.csv

The resulting xml file follows nmap DTD formatting and can be imported to any reporting software that supports nmap xml output. This file will include the hostname found during the SharpHound scan. No additional host info is included at this time. The second generated file is a csv listing all users that were found from SharpHound. This users file will include username, firstname, domain, email, title, and home directory if found.

This is v1. Pull requests and collaboration welcomed.

### Author
- [Cory Wolff](https://github.com/cwolff411) - Senior Security Consultant at [Layer 8 Security](https://layer8security.com)

### Roadmap
- Add additional host info to xml output
- Support additional output formats
- Create csv of hosts with OS, open ports, etc

For additional feature requests please submit an [issue](https://github.com/layer8secure/ConvertHound/issues/new) and add the `enhancement` tag.

### License
[MIT License](https://opensource.org/licenses/MIT)