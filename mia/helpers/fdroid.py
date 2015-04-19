"""
Helper functions dealing with F-Droid.
"""


def fdroid_get_app_lock_info(data, app_info):
    repo = None
    name = None
    package_name = None
    package_versioncode = None

    # Prepare a list of repositories to look into.
    repositories = [app_info['repo']]
    if 'fallback' in data[app_info['repo']]:
        repositories.append(data[app_info['repo']]['fallback'])

    for repo in repositories:
        for tag in data[repo]['tree'].findall('application'):
            if tag.get('id') and tag.get('id') == app_info['name']:
                name, package_name, package_versioncode = \
                    _fdroid_index_get_app_info(tag, app_info['versioncode'])

        # Only try the fallback repository if the application was not found.
        if package_name is not None:
            break

    if package_name is None and app_info['versioncode'] == 'latest':
        print(' - no such app: %s' % app_info['name'])
        return None
    elif package_name is None:
        print(' - no package: %s:%s' % (app_info['name'],
                                        app_info['versioncode']))
        return None

    return {
        'name': name,
        'repository_id': repo,
        'package_name': package_name,
        'package_versioncode': int(package_versioncode),
        'package_url': data[repo]['url'].strip('/') + '/' + package_name,
    }


def _fdroid_index_get_app_info(tag, target_versioncode):
    name = None
    apkname = None
    versioncode = None

    package = None
    if target_versioncode == 'latest':
        package = tag.find('package')
    else:
        for item in tag.findall('package'):
            versioncode = item.find('versioncode').text
            if int(versioncode) == int(target_versioncode):
                package = item
                break

    if package is not None:
        name = tag.find('name').text
        apkname = package.find('apkname').text
        versioncode = package.find('versioncode').text

    return name, apkname, versioncode

