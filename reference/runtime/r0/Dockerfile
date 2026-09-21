FROM public.ecr.aws/ubuntu/ubuntu@sha256:f4da486bc9b357039b00eb68d03fdbda5570525a5c14f56907d75fd5aa204f8f

ARG DEBIAN_FRONTEND=noninteractive
ARG PYTHON_VERSION=3.12.14
ARG PYTHON_SHA256=5c8462af5790baf43a321a1559dbe0db06d1be4300fb85fb53c40060668e548a

RUN sed -i \
        's|http://archive.ubuntu.com/ubuntu|http://mirrors.tuna.tsinghua.edu.cn/ubuntu|g; s|http://security.ubuntu.com/ubuntu|http://mirrors.tuna.tsinghua.edu.cn/ubuntu|g' \
        /etc/apt/sources.list.d/ubuntu.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        libbz2-dev \
        libffi-dev \
        libgdbm-dev \
        liblzma-dev \
        libncursesw5-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        tk-dev \
        uuid-dev \
        xz-utils \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl --fail --location --silent --show-error \
        "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tar.xz" \
        --output /tmp/python.tar.xz \
    && echo "${PYTHON_SHA256}  /tmp/python.tar.xz" | sha256sum --check --strict \
    && mkdir /tmp/python-source \
    && tar --extract --xz --file /tmp/python.tar.xz \
        --directory /tmp/python-source --strip-components=1 \
    && cd /tmp/python-source \
    && ./configure --prefix="/opt/cpython-${PYTHON_VERSION}" --with-ensurepip=install \
    && make -j4 \
    && make install \
    && rm -rf /tmp/python-source /tmp/python.tar.xz

ENV PATH="/opt/cpython-3.12.14/bin:${PATH}" \
    OPENBLAS_NUM_THREADS=1 \
    OMP_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    PYTHONHASHSEED=0 \
    PYTHONDONTWRITEBYTECODE=1

COPY reference/requirements-canonical.txt /opt/pvfactors-r0/requirements-canonical.txt
COPY reference/requirements-linux-cp312.lock /opt/pvfactors-r0/requirements-linux-cp312.lock

RUN python3.12 -m pip install --no-cache-dir --require-hashes \
        --requirement /opt/pvfactors-r0/requirements-linux-cp312.lock \
    && python3.12 -m pip install --no-cache-dir \
        attrs==26.1.0 \
        jsonschema==4.25.1 \
        jsonschema-specifications==2025.9.1 \
        referencing==0.37.0 \
        rpds-py==2026.6.3 \
        typing-extensions==4.16.0

WORKDIR /workspace
