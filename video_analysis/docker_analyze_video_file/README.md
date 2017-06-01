
# Analyze Video File in Docker

Here's an example of uploading a video file and performing a time series analysis in Docker.

Build the Docker image:

```bash
cd docker_analyze_video_file
docker build -t analyze_video_file .
```

Analyze a video file using Dockerized client:

```bash
docker run \
  --env REKALL_API_KEY=d37011ad9010e67ed4cf8b2ec71952db \
  --env REKALL_AGENT_ID=592e270165e46500297a15a2 \
  --volume `pwd`/../../files:/files \
  -it analyze_video_file /files/my-kitchen.mp4 "My Kitchen"
```

_Note: For Enterprise customers we offer fully network isolated Docker containers. Contact sales@rekall.ai_
