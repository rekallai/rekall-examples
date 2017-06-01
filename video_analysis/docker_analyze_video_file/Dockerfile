FROM alpine:3.6
ENV REKALL_API_KEY ''
ENV REKALL_AGENT_ID ''
RUN apk update
RUN apk add python py-requests
ADD . /code
WORKDIR /code
ENTRYPOINT ["python", "analyze_video_file.py"]
