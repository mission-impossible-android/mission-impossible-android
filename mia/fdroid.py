"""
Helper functions dealing with F-Droid.
"""


class MiaFDroid(object):
    @classmethod
    def fdroid_get_app_lock_info(cls, data, app_info):
        repo = None
        app_lock_info = None

        # Prepare a list of repositories to look into.
        repositories = [app_info['repo']]
        if 'fallback' in data[app_info['repo']]:
            repositories.append(data[app_info['repo']]['fallback'])

        for repo in repositories:
            # TODO: Improve detection!
            for tag in data[repo]['tree'].findall('application'):
                if tag.get('id') != app_info['id']:
                    continue

                app_lock_info = \
                    cls._fdroid_index_get_app_info(tag, app_info['versioncode'])

            # Only try the fallback repository if the application was not found.
            if app_lock_info is not None:
                break

        if app_lock_info is None and app_info['versioncode'] == 'latest':
            print(' - no such app: %s' % app_info['id'])
            return None
        elif app_lock_info is None:
            msg = ' - no package: %s:%s'
            print(msg % (app_info['id'], app_info['versioncode']))
            return None

        app_lock_info['package_url'] = '%s/%s' % (
            data[repo]['url'].strip('/'),
            app_lock_info['package_name']
        )
        app_lock_info['repository'] = repo
        app_lock_info['type'] = app_info.get('type', 'user')

        return app_lock_info

    @staticmethod
    def _fdroid_index_get_app_info(tag, target_versioncode):
        """
        :type tag: xml.etree.ElementTree.Element
        :type target_versioncode: str
        :rtype: dict
        """
        package = None
        if target_versioncode == 'latest':
            package = tag.find('package')
        else:
            for item in tag.findall('package'):
                package_versioncode = item.find('versioncode').text
                if int(package_versioncode) == int(target_versioncode):
                    package = item
                    break

        if package is None:
            return None

        return {
            'id': tag.find('id').text,
            'name': tag.find('name').text,
            'package_name': package.find('apkname').text,
            'package_versioncode': package.find('versioncode').text,
            'hash': package.find('hash').text,
            'hash_type': package.find('hash').get('type'),
        }
