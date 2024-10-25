FROM google/cloud-sdk:slim

RUN apt-get update && \
    apt-get -y install curl \
    iputils-ping \
    tar \
    jq \
    ca-certificates \
    unzip \
    default-mysql-client

WORKDIR /runner

RUN GH_RUNNER_VERSION=$(curl --silent "https://api.github.com/repos/actions/runner/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/' | sed 's/v//g') && \
    curl -o actions.tar.gz --location "https://github.com/actions/runner/releases/download/v${GH_RUNNER_VERSION}/actions-runner-linux-x64-${GH_RUNNER_VERSION}.tar.gz" && \
    tar -zxf actions.tar.gz && \
    rm -f actions.tar.gz && \
    ./bin/installdependencies.sh

# install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256" && \
    echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# install kustomize
RUN curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh"  | bash
RUN ln -s /runner/kustomize /usr/local/sbin/kustomize

COPY ./container-files/entrypoint.sh .
RUN chmod +x entrypoint.sh

RUN useradd -m ghrunner -d /home/ghrunner  && chown -R ghrunner: /runner && chown -R ghrunner: /home/ghrunner
USER ghrunner
ENTRYPOINT ["/runner/entrypoint.sh"]
