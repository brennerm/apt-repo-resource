## Concourse CI APT repository resource
This Concourse CI resource will check for updated versions of a package in an APT repository.

## Usage
The resource will provide at least the following two files:
- $resource_dir/package: contains the name of the package
- $resource_dir/version: contains the version of the package

If the parameter "download_deb" is set to True the .deb file will be available as well.
It's name can be found in "$resource_dir/filename".

## Example
```yaml
resource_types:
  - name: apt-package
    type: docker-image
    source:
      repository: brennerm/apt-repo-resource
      tag: latest

resources:
  - name: gitlab-deploy
    type: git
    source:
      uri: git@gitlab.company.com:ansible/gitlab-deploy.git
  - name: gitlab-package
    type: apt-package
    source:
      repositories:
        - deb https://packages.gitlab.com/gitlab/gitlab-ce/ubuntu/ xenial main
      package: gitlab-ce
      
jobs:
  - plan:
      - get: docker-package-xenial
        trigger: true
      - get: gitlab-deploy
      - task: deploy gitlab
        config:
          image_resource:
            type: docker-image
            source:
              repository: ansible
              tag: latest
          platform: linux
          inputs:
            - name: gitlab-deploy
            - name: gitlab-package
          run:
            path: /bin/bash
            args:
              - -c
              - |
                cd gitlab-deploy
                ansible-playbook -e "version=$(cat ../gitlab-package/version)" gitlab.yml
```