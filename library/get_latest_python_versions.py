import requests
from lxml import html
from ansible.module_utils.basic import AnsibleModule

PY_URL = 'https://www.python.org/ftp/python/{}/Python-{}.tar.xz'

class Version:
    def __init__(self, version):
        self.version = version
        self.str_split = version.split('.')
        self.split = list(map(lambda x: int(x), self.str_split))
        self.len = len(self.split)

    def is_major(self, major):
        return self.split[0] == major

    def __getitem__(self, key):
        if self.len > key:
            return self.split[key]
        else:
            return 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0
    def __gt__(self, other):
        return self.__cmp__(other) > 0
    def __eq__(self, other):
        return self.__cmp__(other) == 0
    def __le__(self, other):
        return self.__cmp__(other) <= 0
    def __ge__(self, other):
        return self.__cmp__(other) >= 0
    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __cmp__(self, other):
        max_range = max(self.len, other.len)
        for v in range(max_range):
            if self[v] == other[v]:
                continue
            elif self[v] < other[v]:
                return -1
            elif self[v] > other[v]:
                return 1
        return 0

    def __str__(self):
        return self.version

    def __repr__(self):
        return self.version


def _get_remote_versions():
    remote_source = requests.get('https://www.python.org/ftp/python/')
    tree = html.fromstring(remote_source.content)

    lxml_links = tree.xpath('//a')
    links = map(lambda x: x.text_content(), lxml_links)

    versions = filter(lambda x: x[0].isdigit(), links)
    versions = list(versions)

    remote_versions = map(lambda x: Version(x.rstrip('/').strip()), versions)
    remote_versions = list(remote_versions)
    return remote_versions


def _get_matching_major_versions(version, remote_versions):
    matching = filter(lambda x: x.is_major(version), remote_versions)
    return list(matching)


def file_exists(location):
    resp = requests.head(location)
    return (resp.status_code == 200)


def _get_functional_url(versions):
    for i in range(len(versions) - 1, 0, -1):
        v = versions[i]

        url = PY_URL.format(v, v)
        if file_exists(url):
            return url
    return ''


def main():
    ans_module = AnsibleModule(
        argument_spec = dict(
            versions        = dict(required=True, type='list'),
        )
    )
    log = []

    versions = ans_module.params['versions']
    remote_versions = _get_remote_versions()

    matching_versions = map(
        lambda x: _get_matching_major_versions(x, remote_versions),
        versions
    )
    matching_versions = map(lambda x: sorted(x), matching_versions)

    install_urls = map(lambda x: _get_functional_url(x), matching_versions)


    ans_module.exit_json(
        changed=True, # Always true. Future, detect currently installed version, and allow for updating.
        val=install_urls,
        log=log,
        initial=versions
    )

if __name__ == '__main__':
    main()
