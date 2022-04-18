# SoundboardBot

## Audio Clips

Audio clips are stored in a PVC, defined in k8s/pvc.yaml, that is mounted onto our deployment at /data/audio

## TODO:
- Store user clip information in a db instead of a yaml file
- Add way of adding custom clips for people by discord user command
- Maybe rework how clips are stored. Cause currently having more than one clip for a user isn't logical, and can't have a clip play only in certain channels ect.
