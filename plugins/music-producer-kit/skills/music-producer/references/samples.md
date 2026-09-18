# Existing local samples

Read when the task needs an existing sample or the user asks what is available locally.
Use only the explicitly authorized sample directory. Do not scan the entire home directory or disk for a music-production request.
A Splice account or installed application does not grant API access, purchase permission or proof that a file has been licensed.

From the installed plugin directory, using the actual directory the user authorized:

```text
python skills/music-producer/scripts/sample_library.py SAMPLE_DIRECTORY --query "kick tight" --limit 12
```

Replace SAMPLE_DIRECTORY with the authorized directory, quoted when it contains spaces. Do not invent a default machine path.
The helper searches filenames and relative directory names with case-insensitive literal terms; all terms must occur. An empty query lists candidate files.
It recognizes WAV/WAVE, FLAC, AIFF/AIF and OGG filename extensions. This is file discovery, not audio-format validation or decoding.
It returns relative paths, sizes and a SHA256 of the returned files up to the 256 MiB hashing limit. Larger files explicitly lack a hash.
It scans at most 10,000 files, returns at most 100 matches, and reports incomplete scans, truncation and read problems rather than silently calling a partial result exhaustive.
The traversal skips symlinks and nested directory junctions. No sample is modified, copied, downloaded, uploaded or purchased.

## From a candidate file to an actual choice

Treat filename key/BPM/style labels as unverified clues. A file named kick.wav is not proof of a kick sound.
Compare candidates with playback or an actual analysis tool when one is available; never report hearing based on this helper's JSON.
Record the chosen file identity in the private song workspace. Do not commit sample filenames, ownership records or user paths to this public repo by default.
Load the selected file only through an actually exposed Live/MCP operation. A discovered path does not prove browser import or device loading succeeded.
After loading, verify the destination track/clip/device, playback boundaries and protected material.
Retain the source file and arrange collection into the Live project through a verified save/collection workflow.

When the requested sample is unavailable, use an already-owned instrument or report the gap. Do not consume Splice credits or buy a sound automatically.
The helper does not provide audio previews, BPM/key detection, a license checker, a Splice connector or automatic sound-quality ranking.
