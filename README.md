
# Rekall Examples

In this repository you can find several examples on how to use the Rekall API. With [Rekall](http://rekall.ai/) you can use an intuitive drag and drop interface to build a custom model and have it up and running within minutes. Rekall integrates with several popular image repositories, which makes training your model a breeze.

Comprehensive developer documentation can be found at:

[http://developer.rekall.ai/](developer.rekall.ai)

## Image Classification

### Classify File

This example uploads a file, and then classifies that file using a public [Indoor VS Outdoor classification model](http://rekall.ai/dominiek/models/scene-types)

```bash
python image_recognition/classify_file.py
```

### Classify URL

Using the same model, but classify an image URL instead of a file:

```bash
python image_recognition/classify_url.py
```

### Build model from folder of images

This example uses the images in `files/indoor_vs_outdoor` and build an "Indoor VS Outdoor" classifier:

```bash
python image_recognition/build_model.py
```

## Video Analysis

### Analyze Video URL

Uses a public [Kitchen Items Model](http://rekall.ai/dominiek/models/kitchen-items) to identify different objects in a kitchen. This example gets the full analysis and summary of a video analysis.

```bash
python video_analysis/classify_url.py
```

### Analyze Video File in Docker

Here's an example of uploading a video file and performing a time series analysis in Docker.

Build the Docker image:

```bash
cd video_analysis/docker_analyze_video_file
docker build -t analyze_video_file .
cd ../../
```

Analyze a video file using Dockerized client:

```bash
docker run \
  --env REKALL_API_KEY=d37011ad9010e67ed4cf8b2ec71952db \
  --env REKALL_AGENT_ID=592e270165e46500297a15a2 \
  --volume `pwd`/files:/files \
  -it analyze_video_file /files/my-kitchen.mp4 "My Kitchen"
```

_Note: For Enterprise customers we offer fully network isolated Docker containers. Contact sales@rekall.ai_
