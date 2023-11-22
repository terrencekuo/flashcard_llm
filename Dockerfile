FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y \
    autoconf \
    automake \
    cmake \
    gcc \
    gcc-c++ \
    libtool \
    make \
    nasm \
    pkgconfig

WORKDIR ${LAMBDA_TASK_ROOT}

RUN pip3 install llama-cpp-python
RUN CMAKE_ARGS="-DLLAMA_AVX=OFF -DLLAMA_AVX2=OFF -DLLAMA_F16C=OFF -DLLAMA_FMA=OFF" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python --no-cache-dir

# Specify the name of your quantized model here
ENV MODEL_NAME=llama-2-7b-chat.Q4_K_M.gguf

# Copy the infrence code
COPY app.py ${LAMBDA_TASK_ROOT}

# Copy the model file
COPY ./${MODEL_NAME} ${LAMBDA_TASK_ROOT}/model/${MODEL_NAME}

# Set the CMD to your handler
CMD [ "app.handler" ] 
