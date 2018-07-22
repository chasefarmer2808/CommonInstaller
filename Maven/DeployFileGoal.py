from Maven.MavenGoal import MavenGoal, SNAPSHOT_VERSION_SUFFIX

SNAPSHOT_URL = 'http://localhost:8081/repository/maven-snapshots/'
RELEASE_URL = 'http://localhost:8081/repository/maven-releases/'

class DeployFileGoal(MavenGoal):
    def __init__(self, destination):
        super(DeployFileGoal, self).__init__()

        if destination is 'local':
            self.append('install:install-file')
        else:
            self.append('deploy:deploy-file')

            if destination is 'snapshot':
                self.version_suffix(SNAPSHOT_VERSION_SUFFIX)
                self.url(SNAPSHOT_URL)
            else:
                self.url(RELEASE_URL)

    def file(self, file_path, file_name):
        full_path = '{}/target/{}'.format(file_path, file_name)
        self.append_maven_arg('file', full_path)

    # Id of repositories defined within the <server> tags in the settings.xml
    def repo_id(self, id):
        self.append_maven_arg('repositoryId', id)

    def url(self, url):
        self.append_maven_arg('url', url)
