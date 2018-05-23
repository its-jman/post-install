import requests
from lxml import html
from ansible.module_utils.basic import AnsibleModule

def main():
    ans_module = AnsibleModule(
        argument_spec = dict(
            repo=dict(required=True, type='str'),
        )
    )

    repo = ans_module.params['repo']
    resp = requests.get('https://api.github.com/repos/{}/releases/latest'.format(repo))
    tag_name = resp.json()["tag_name"]

    ans_module.exit_json(
        changed=True, # Always true. Future, detect currently installed version, and allow for updating.
        val=tag_name
        # initial=versions
    )

if __name__ == '__main__':
    main()
