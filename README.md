switchbin GStreamer element
===========================

This is a new GStreamer element for automatically switching between groups of elements,
called "paths", according to input caps. Paths are child objects, which are accessed by
the GstChildProxy interface (which switchbin implements).


Whenever new input caps are encountered at the switchbin's sinkpad, the first path with
matching caps is picked. The paths are looked at in order: path #0's caps are looked at
first, checked against the new input caps with `gst_caps_can_intersect()`, and if its
return value is TRUE, path #0 is picked. Otherwise, path #1's caps are looked at etc.
If no path matches, an error is reported.


In this example, if the data is raw PCM audio with 44.1 kHz, a volume element is used
for reducing the audio volume to 10%. Otherwise, it is just passed through. So, a
44.1 kHz MP3 will sound quiet, a 48 kHz MP3 will be at full volume.

    gst-launch-1.0 uridecodebin uri=<URI> ! switchbin num-paths=2 \
      path0::element="audioconvert ! volume" path0::caps="audio/x-raw, rate=44100" \
      path1::element="identity" path1::caps="ANY" ! \
      autoaudiosink

This example's path #1 is a fallback "catch-all" path. Its caps are "ANY" caps,
so any input caps will match against this. A catch-all path with an identity element
is useful for cases where certain kinds of processing should only be done for specific
formats, like the example above (it applies volume only to 44.1 kHz PCM audio).


It is also possible to have paths which do not let data through. These behave like
the "valve" element with its "drop" property set to TRUE. This example lets only
PCM audio data through to the audio sink branch:

    gst-launch-1.0 uridecodebin uri=<URI> ! tee name=t  \
      t. ! queue ! switchbin num-paths=2 \
        path0::element="identity" path0::caps="audio/x-raw" \
        path1::caps="ANY" ! pulsesink async=false \
      t. ! queue ! fakesink sync=true

This will send data to the fakesink. If it is audio/x-raw data, it will also send it
to the pulsesink. path1's element is not set, which means it remains NULL.

NOTE: This feature is not 100% defined yet. It has these issues:

1. Any sink placed after a switchbin that contains such a "drop path" must have
   its "async" property set to FALSE, otherwise the preroll never ends (because
   the sink expects data to finish its state change to PAUSED).

2. If an element queues up in-band events like "stream-start", these events may not
   be turned to messages by the pipeline. stream-start events for example need
   to be received by all sinks before a stream-start message is posted. Base classes
   like GstAudioDecoder can queue up buffers and in-band events (and stream-start
   is an in-band, or "serialized", event). Since in case of a drop path, no data
   flows through to the sink, such a queue won't be emptied, and the stream-start
   event remains stuck inside.


Known issues
------------

Aside from the drop path issues mentioned above, currently there are the following
known problems:

1. Path elements must have one "src" and one "sink" pad, and these must be always-pads.
   Request- and sometimes-pads are not supported yet.

2. gst-launch command lines may cause problems with their element property specifiers.
   This is because for unknown reasons, a description like `path0::element="audioconvert ! volume"`
   isn't turned into one GstBin containing the audioconvert and volume elements; instead,
   a GstPipeline is created, which can lead to problems. This was already
   [reported as a bug](https://bugzilla.gnome.org/show_bug.cgi?id=763457).
