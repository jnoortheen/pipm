from six.moves import StringIO

from pipm import setup_cfg


def test__write_to_setup_cfg(chdir, config, config_parsed):
    setup_cfg._write_to_setup_cfg(config, config_parsed, {'pkg': 'pkg~=1.11'}, env='')
    with StringIO() as f:
        config.write(f)
        assert """\
install_requires = 
	py~=1.5.3
	pkg~=1.11""" in f.getvalue()


    setup_cfg._write_to_setup_cfg(config, config_parsed, {'pkg2': 'pkg2~=1.11'}, env='dev')

    with StringIO() as f:
        config.write(f)
        print(f.getvalue())
        assert """\
install_requires = 
	py~=1.5.3
	pkg~=1.11

[options.extras_require]
dev = 
	pkg2~=1.11
""" in f.getvalue()
