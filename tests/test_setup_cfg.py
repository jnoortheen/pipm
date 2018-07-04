from pipm import setup_cfg
from six.moves import StringIO

setup_cfg_str = """\
[options]
install_requires = 
	py~=1.5.3

[options.extras_require]
dev = 
	django~=2.0.7
"""


def test__write_to_setup_cfg(chdir):
    config = setup_cfg.configparser.ConfigParser()
    config.read_string(setup_cfg_str)
    configDict = {
        'options': {
            'install_requires': ['py~=1.5.3'],
            'extras_require': {
                'dev': ['django~=2.0.7']
            }
        }
    }
    setup_cfg._write_to_setup_cfg(config, configDict, {'pkg': 'pkg~=1.11'}, env='')
    with StringIO() as f:
        config.write(f)
        assert """\
install_requires = 
	py~=1.5.3
	pkg~=1.11""" in f.getvalue()

    setup_cfg._write_to_setup_cfg(config, configDict, {'pkg2': 'pkg2~=1.11'}, env='dev')

    with StringIO() as f:
        config.write(f)
        print(f.getvalue())
        assert """\
install_requires = 
	py~=1.5.3
	pkg~=1.11

[options.extras_require]
dev = 
	django~=2.0.7
	pkg2~=1.11
""" in f.getvalue()
