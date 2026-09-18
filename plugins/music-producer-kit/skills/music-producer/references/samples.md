# Use the user's actual local samples

Use for sound selection from an explicitly supplied local folder, including downloaded Splice files. Do not scan entire drives by default.
Metadata inspection is not listening, similarity search, audio quality grading, transcription or account access.

## Read-only path

From the installed plugin directory, with the user's real private paths substituted:

```text
python skills/music-producer/scripts/sample_library.py scan "D:/My Samples" --output "D:/Song Workspace/samples.json"
python skills/music-producer/scripts/sample_library.py find "D:/Song Workspace/samples.json" "kick"
python skills/music-producer/scripts/sample_library.py inspect "D:/My Samples" "Drums/kick.wav"
```

These paths are illustrations, not assumptions about this user's machine. The output parent directory must already exist.
The scanner skips links/junctions, hidden subdirectories and unselected extensions. It records unreadable files as issues and explicitly reports when its file limit truncates a scan.
It reads sample rate, channels, frame count, duration, format and subtype using SoundFile. These are header observations, not a full waveform integrity check.
Search matches filename/path terms literally, ignoring case. It does not infer that a file sounds good or matches the reference artist.
The inspect step reopens the selected current file and computes its SHA256. A saved inventory can be stale; recheck the file before importing it into Live.
No command decodes waveforms for analysis, plays audio, writes a sample, follows external links, downloads, uploads or consumes credits.

## Boundaries and handoff

Keep the inventory outside the installed plugin, sample root and public repository. It contains private paths and names.
Filename BPM/key labels are unverified hints: this tool returns no detected BPM or key. Local presence does not establish a sample license; use the user's records.
Choose a role and articulation before searching. Reuse a suitable owned sound; do not assume a purchase is needed when no filename matches.
Once a file is selected, pass its validated path to an actually available Live loader. Do not invent a load-sample MCP command.
An instrumental or one-shot file does not acquire a lyric language from its name. Japanese kanji, Korean filenames and English loanwords remain valid.

## Implementation basis

SoundFile 0.13.1 supplies cross-platform audio header reading, including floating-point WAV. It and its dependencies must be installed before this helper runs.
Official documentation: https://python-soundfile.readthedocs.io/en/0.13.1/
This link is attribution/documentation, not a runtime download path. Reuse the library instead of implementing a RIFF/FLAC/AIFF parser.
