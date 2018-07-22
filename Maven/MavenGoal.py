SNAPSHOT_VERSION_SUFFIX = '-SNAPSHOT'

class MavenGoal:
    def __init__(self):
        self.goal = 'mvn'
        self.append('--batch-mode')

    def pom_file(self, file_path):
        pom_path = '{}/pom.xml'.format(file_path)
        self.append_maven_arg('pomFile', pom_path)

    def zip_packaging(self):
        packaging = 'zip'
        self.append_maven_arg('packaging', packaging)

    def version_suffix(self, suffix):
        self.append_maven_arg('versionSuffix', suffix)

    def append_maven_arg(self, key, value):
        arg = '-D{}={}'.format(key, value)
        self.append(arg)

    def append(self, block):
        self.goal = ' '.join([self.goal, block])