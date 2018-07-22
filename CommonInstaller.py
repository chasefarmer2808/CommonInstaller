""""
Use Cases
1. Create an artifact for my project using 7zip. (This should not be the common installer's responsibility)
2. Install my artifact to my local maven repository.
3. Publish my artifact to a remote snapshot repository.
4. Publish my artifact to a remote release repository.
5. Pull down the latest release version of a specified artifact.
6. Pull down the latest snapshot version of a specific artifact.
7. Specify a config file to handle a bulk pull of artifacts.
"""

import argparse
import subprocess
import os

from Maven.DeployFileGoal import DeployFileGoal


def execute(cmd):
    print(cmd)
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, err = process.communicate()

    if err:
        console_print(err)
    else:
        console_print(output)


def console_print(txt):
    print(txt.decode('utf-8'))


class CommonInstaller:
    def __init__(self, base_dir, local, snapshot, release):
        self.project_base_dir = 'C:/Users/chase/OneDrive/Documents/Github/{}'.format(base_dir)
        self.repo = self.determine_repo(local, snapshot, release)

    def determine_repo(self, local, snapshot, release):
        if local:
            return 'local'

        if snapshot:
            return 'snapshot'

        if release:
            return 'release'

    def publish(self, artifact, repo_id):
        # Assume the path leading to the base dir is stored in an env var called SPACESW_HOME.
        # Assume the zipped artifact is located in base_dir/target.
        # Use maven install-file goal to publish the zip to Nexus.
        # Example: mvn deploy:deploy-file -DpomFile=base_dir/pom.xml -DrepositoryId=nexus -Durl=<nexus url> -Dfile=target/project.zip -DgeneratePom=false
        # Need to figure out how to switch between release, snapshot, and local repo.
        # if release or snapshot, must require repo url

        goal = DeployFileGoal(self.repo)
        goal.pom_file(self.project_base_dir)
        goal.file(self.project_base_dir, artifact)
        goal.repo_id(repo_id)
        goal.zip_packaging()

        execute(goal.goal)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--publish', action='store_true')
    parser.add_argument('--local', action='store_true', default=False)
    parser.add_argument('--snapshot', action='store_true', default=False)
    parser.add_argument('--release', action='store_true', default=False)
    parser.add_argument('--base_dir')
    parser.add_argument('--artifact')
    parser.add_argument('--repo_id', default='nexus')
    args = parser.parse_args()

    ci = CommonInstaller(args.base_dir, args.local, args.snapshot, args.release)

    if args.publish:
        ci.publish(args.artifact, args.repo_id)