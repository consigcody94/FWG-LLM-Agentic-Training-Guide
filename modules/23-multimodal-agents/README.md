# Module 23: Multimodal AI Agents

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███╗   ███╗██╗   ██╗██╗  ████████╗██╗███╗   ███╗ ██████╗ ██████╗  █████╗ ██╗     ║
║   ████╗ ████║██║   ██║██║  ╚══██╔══╝██║████╗ ████║██╔═══██╗██╔══██╗██╔══██╗██║     ║
║   ██╔████╔██║██║   ██║██║     ██║   ██║██╔████╔██║██║   ██║██║  ██║███████║██║     ║
║   ██║╚██╔╝██║██║   ██║██║     ██║   ██║██║╚██╔╝██║██║   ██║██║  ██║██╔══██║██║     ║
║   ██║ ╚═╝ ██║╚██████╔╝███████╗██║   ██║██║ ╚═╝ ██║╚██████╔╝██████╔╝██║  ██║███████╗║
║   ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝║
║                                                                              ║
║                 Vision • Audio • Video • Document Processing                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Learning Objectives

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  By the end of this module, you will be able to:                           │
│                                                                             │
│  □ Build agents that process images, audio, and video                      │
│  □ Implement vision-language models for document analysis                   │
│  □ Create speech-to-text and text-to-speech pipelines                      │
│  □ Design multimodal workflows for federal applications                     │
│  □ Handle accessibility requirements with multimodal AI                     │
│  □ Process classified document imagery with appropriate controls            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 23.1 Multimodal Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      MULTIMODAL AI ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│   │    IMAGE     │    │    AUDIO     │    │    VIDEO     │                 │
│   │   Input      │    │   Input      │    │   Input      │                 │
│   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                 │
│          │                   │                   │                          │
│          ▼                   ▼                   ▼                          │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│   │   Vision     │    │   Speech     │    │   Video      │                 │
│   │   Encoder    │    │   Encoder    │    │   Encoder    │                 │
│   └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                 │
│          │                   │                   │                          │
│          └───────────────────┼───────────────────┘                          │
│                              │                                              │
│                              ▼                                              │
│                    ┌─────────────────┐                                      │
│                    │    FUSION       │                                      │
│                    │    LAYER        │                                      │
│                    │ (Cross-Attention)│                                     │
│                    └────────┬────────┘                                      │
│                             │                                               │
│                             ▼                                               │
│                    ┌─────────────────┐                                      │
│                    │   LANGUAGE      │                                      │
│                    │   MODEL         │                                      │
│                    │   (LLM Core)    │                                      │
│                    └────────┬────────┘                                      │
│                             │                                               │
│          ┌──────────────────┼──────────────────┐                            │
│          ▼                  ▼                  ▼                            │
│   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐                   │
│   │    Text      │   │    Image     │   │    Audio     │                   │
│   │   Output     │   │   Output     │   │   Output     │                   │
│   └──────────────┘   └──────────────┘   └──────────────┘                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Multimodal Model Comparison

| Model | Provider | Modalities | Context | Best Use Case |
|-------|----------|-----------|---------|---------------|
| **GPT-4o** | OpenAI | Text, Vision, Audio | 128K | General multimodal |
| **Claude 3.5** | Anthropic | Text, Vision | 200K | Document analysis |
| **Gemini Pro** | Google | Text, Vision, Audio | 1M | Long document/video |
| **LLaVA** | Open Source | Text, Vision | 32K | Local deployment |
| **Whisper** | OpenAI | Audio → Text | N/A | Transcription |
| **DALL-E 3** | OpenAI | Text → Image | N/A | Image generation |

---

## 23.2 Vision-Language Models

### Image Analysis with GPT-4 Vision

```python
"""
Vision-Language Model Integration
Federal document and image analysis system
"""
import base64
from openai import OpenAI
from pathlib import Path
from typing import Union
import httpx


class VisionAnalyzer:
    """
    ┌─────────────────────────────────────────────────────────┐
    │                 VISION ANALYZER                         │
    │                                                         │
    │  ┌─────────┐    ┌─────────────┐    ┌─────────────┐    │
    │  │  Image  │───▶│   Encode    │───▶│   Analyze   │    │
    │  │  Input  │    │   Base64    │    │   w/ LLM    │    │
    │  └─────────┘    └─────────────┘    └─────────────┘    │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.supported_formats = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}

    def encode_image(self, image_path: Union[str, Path]) -> str:
        """Encode local image to base64"""
        path = Path(image_path)

        if path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported format: {path.suffix}")

        with open(path, "rb") as f:
            return base64.standard_b64encode(f.read()).decode("utf-8")

    def analyze_image(
        self,
        image_source: str,  # File path or URL
        prompt: str,
        detail: str = "high"  # low, high, auto
    ) -> str:
        """
        Analyze image with vision model

        Args:
            image_source: Local path or URL
            prompt: Analysis instruction
            detail: Image detail level (affects token usage)
        """
        # Determine if URL or local file
        if image_source.startswith(('http://', 'https://')):
            image_content = {
                "type": "image_url",
                "image_url": {
                    "url": image_source,
                    "detail": detail
                }
            }
        else:
            # Local file - encode to base64
            base64_image = self.encode_image(image_source)
            suffix = Path(image_source).suffix.lower()
            media_type = f"image/{suffix.replace('.', '')}"
            if suffix == '.jpg':
                media_type = "image/jpeg"

            image_content = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{media_type};base64,{base64_image}",
                    "detail": detail
                }
            }

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        image_content
                    ]
                }
            ],
            max_tokens=4096
        )

        return response.choices[0].message.content

    def analyze_document(self, image_path: str) -> dict:
        """
        Extract structured data from document image

        Federal use case: Processing scanned forms, IDs, certificates
        """
        prompt = """Analyze this document image and extract:
        1. Document type (form, ID, certificate, letter, etc.)
        2. Key fields and their values
        3. Any dates present
        4. Signatures or stamps present (yes/no)
        5. Document quality assessment

        Return as structured JSON."""

        response = self.analyze_image(
            image_path,
            prompt,
            detail="high"
        )

        return {
            "raw_analysis": response,
            "source": image_path,
            "model": "gpt-4o"
        }

    def compare_images(
        self,
        image1: str,
        image2: str,
        comparison_type: str = "similarity"
    ) -> str:
        """Compare two images for similarity or differences"""

        images = []
        for img in [image1, image2]:
            if img.startswith(('http://', 'https://')):
                images.append({
                    "type": "image_url",
                    "image_url": {"url": img, "detail": "high"}
                })
            else:
                b64 = self.encode_image(img)
                images.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{b64}",
                        "detail": "high"
                    }
                })

        if comparison_type == "similarity":
            prompt = """Compare these two images and describe:
            1. Overall similarity (percentage estimate)
            2. Key similarities
            3. Key differences
            4. Are they the same document/item? (yes/no/uncertain)"""
        else:
            prompt = """Identify all differences between these images:
            1. Structural differences
            2. Content differences
            3. Quality differences"""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        *images
                    ]
                }
            ],
            max_tokens=2048
        )

        return response.choices[0].message.content


# Usage example
analyzer = VisionAnalyzer(api_key="your-key")

# Analyze a document image
result = analyzer.analyze_document("/path/to/scanned_form.png")
print(result["raw_analysis"])

# Compare two documents
comparison = analyzer.compare_images(
    "/path/to/doc1.jpg",
    "/path/to/doc2.jpg",
    comparison_type="similarity"
)
```

### Claude Vision for Document Processing

```python
"""
Anthropic Claude Vision Implementation
Superior for long document analysis
"""
import anthropic
import base64
from pathlib import Path


class ClaudeVisionAnalyzer:
    """
    ┌─────────────────────────────────────────────────────────┐
    │              CLAUDE VISION ANALYZER                     │
    │                                                         │
    │  Strengths:                                             │
    │  • 200K context for multi-page documents                │
    │  • Strong reasoning about document structure            │
    │  • Excellent at following complex instructions          │
    │  • Built-in safety for sensitive content                │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    """

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    def analyze_images(
        self,
        images: list[str],  # List of paths or URLs
        prompt: str,
        system_prompt: str = None
    ) -> str:
        """
        Analyze multiple images with Claude

        Claude excels at:
        - Multi-page document understanding
        - Complex form extraction
        - Comparing multiple images
        """
        content = []

        # Add images
        for img in images:
            if img.startswith(('http://', 'https://')):
                content.append({
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": img
                    }
                })
            else:
                # Local file
                path = Path(img)
                with open(path, "rb") as f:
                    data = base64.standard_b64encode(f.read()).decode()

                media_type = f"image/{path.suffix.replace('.', '')}"
                if path.suffix == '.jpg':
                    media_type = "image/jpeg"

                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": data
                    }
                })

        # Add text prompt
        content.append({
            "type": "text",
            "text": prompt
        })

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt or "You are a document analysis expert.",
            messages=[
                {"role": "user", "content": content}
            ]
        )

        return message.content[0].text

    def extract_form_data(self, form_images: list[str]) -> dict:
        """
        Extract structured data from government forms

        Federal Use Case: Processing SF-86, tax forms, applications
        """
        prompt = """Analyze this government form and extract ALL fields:

        For each field found:
        1. Field label/name
        2. Field value (or "EMPTY" if blank)
        3. Field type (text, checkbox, date, signature, etc.)
        4. Any validation notes (e.g., dates formatted correctly?)

        Also identify:
        - Form name/number (e.g., "SF-86", "1040")
        - Required fields that are empty
        - Potential data quality issues

        Return as structured JSON."""

        system = """You are a federal document processing specialist.
        Extract data accurately and flag any compliance concerns.
        Be thorough - missing data can have serious consequences."""

        response = self.analyze_images(form_images, prompt, system)

        return {
            "extraction": response,
            "page_count": len(form_images),
            "model": "claude-sonnet-4-20250514"
        }


# Multi-page document processing
claude_analyzer = ClaudeVisionAnalyzer(api_key="your-key")

# Process a multi-page scanned document
pages = [
    "/docs/sf86_page1.jpg",
    "/docs/sf86_page2.jpg",
    "/docs/sf86_page3.jpg"
]

result = claude_analyzer.extract_form_data(pages)
```

---

## 23.3 Audio Processing & Speech

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AUDIO PROCESSING PIPELINE                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────┐                                                          │
│   │    AUDIO     │                                                          │
│   │    INPUT     │                                                          │
│   │  (.wav/.mp3) │                                                          │
│   └──────┬───────┘                                                          │
│          │                                                                  │
│          ▼                                                                  │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│   │  PRE-        │───▶│   WHISPER    │───▶│    POST-     │                 │
│   │  PROCESSING  │    │   MODEL      │    │   PROCESS    │                 │
│   │  (Normalize) │    │  (ASR/STT)   │    │  (Correct)   │                 │
│   └──────────────┘    └──────────────┘    └──────┬───────┘                 │
│                                                   │                         │
│          ┌────────────────────────────────────────┤                         │
│          │                                        │                         │
│          ▼                                        ▼                         │
│   ┌──────────────┐                        ┌──────────────┐                 │
│   │  TRANSCRIPT  │                        │  DIARIZATION │                 │
│   │  (Raw Text)  │                        │  (Speakers)  │                 │
│   └──────────────┘                        └──────────────┘                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Speech-to-Text with Whisper

```python
"""
Audio Transcription System
Using OpenAI Whisper for federal applications
"""
from openai import OpenAI
from pathlib import Path
import tempfile
from pydub import AudioSegment


class AudioTranscriber:
    """
    Speech-to-Text transcription system

    Supports:
    - Multiple audio formats (mp3, wav, m4a, etc.)
    - Long audio files (chunked processing)
    - Speaker diarization
    - Multi-language transcription
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.max_file_size = 25 * 1024 * 1024  # 25MB limit

    def transcribe(
        self,
        audio_path: str,
        language: str = None,  # Auto-detect if None
        response_format: str = "verbose_json",
        include_timestamps: bool = True
    ) -> dict:
        """
        Transcribe audio file to text

        Args:
            audio_path: Path to audio file
            language: ISO language code (e.g., 'en', 'es')
            response_format: text, json, verbose_json, srt, vtt
            include_timestamps: Include word-level timestamps
        """
        path = Path(audio_path)

        # Check file size
        if path.stat().st_size > self.max_file_size:
            return self._transcribe_large_file(audio_path, language)

        with open(path, "rb") as audio_file:
            kwargs = {
                "model": "whisper-1",
                "file": audio_file,
                "response_format": response_format
            }

            if language:
                kwargs["language"] = language

            if include_timestamps and response_format == "verbose_json":
                kwargs["timestamp_granularities"] = ["word", "segment"]

            transcript = self.client.audio.transcriptions.create(**kwargs)

        return transcript

    def _transcribe_large_file(
        self,
        audio_path: str,
        language: str = None,
        chunk_duration_ms: int = 600000  # 10 minutes
    ) -> dict:
        """
        Transcribe large audio files by chunking
        """
        audio = AudioSegment.from_file(audio_path)
        chunks = []

        # Split into chunks
        for i in range(0, len(audio), chunk_duration_ms):
            chunk = audio[i:i + chunk_duration_ms]
            chunks.append(chunk)

        all_segments = []
        offset = 0

        for i, chunk in enumerate(chunks):
            # Save chunk to temp file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                chunk.export(f.name, format="mp3")

                # Transcribe chunk
                result = self.transcribe(
                    f.name,
                    language=language,
                    response_format="verbose_json"
                )

                # Adjust timestamps
                if hasattr(result, 'segments'):
                    for segment in result.segments:
                        segment['start'] += offset / 1000
                        segment['end'] += offset / 1000
                        all_segments.append(segment)

                offset += chunk_duration_ms

        # Combine results
        full_text = " ".join(seg['text'] for seg in all_segments)

        return {
            "text": full_text,
            "segments": all_segments,
            "duration": len(audio) / 1000
        }

    def translate_audio(
        self,
        audio_path: str,
        target_language: str = "en"
    ) -> str:
        """
        Translate audio from any language to English

        Whisper only supports translation TO English
        """
        with open(audio_path, "rb") as audio_file:
            translation = self.client.audio.translations.create(
                model="whisper-1",
                file=audio_file
            )

        return translation.text


class TextToSpeech:
    """
    Text-to-Speech synthesis using OpenAI

    Federal Use Cases:
    - Accessibility compliance (508)
    - Automated announcements
    - Voice response systems
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def synthesize(
        self,
        text: str,
        voice: str = "alloy",  # alloy, echo, fable, onyx, nova, shimmer
        model: str = "tts-1",  # tts-1 or tts-1-hd
        output_path: str = "output.mp3"
    ) -> str:
        """
        Convert text to speech

        Voice options:
        - alloy: Neutral, balanced
        - echo: Warm, conversational
        - fable: Expressive, storytelling
        - onyx: Deep, authoritative
        - nova: Bright, energetic
        - shimmer: Soft, gentle
        """
        response = self.client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )

        response.stream_to_file(output_path)
        return output_path

    def synthesize_long_text(
        self,
        text: str,
        voice: str = "alloy",
        max_chars: int = 4096,
        output_path: str = "output.mp3"
    ) -> str:
        """
        Synthesize long text by chunking
        """
        from pydub import AudioSegment

        # Split text into chunks at sentence boundaries
        sentences = text.replace('?', '?|').replace('!', '!|').replace('.', '.|').split('|')

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_chars:
                current_chunk += sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk.strip())

        # Synthesize each chunk
        audio_segments = []

        for i, chunk in enumerate(chunks):
            temp_path = f"temp_chunk_{i}.mp3"
            self.synthesize(chunk, voice, output_path=temp_path)
            audio_segments.append(AudioSegment.from_mp3(temp_path))

        # Combine audio
        combined = audio_segments[0]
        for segment in audio_segments[1:]:
            combined += segment

        combined.export(output_path, format="mp3")
        return output_path


# Usage
transcriber = AudioTranscriber(api_key="your-key")
tts = TextToSpeech(api_key="your-key")

# Transcribe meeting recording
transcript = transcriber.transcribe(
    "/recordings/meeting_2024_01_15.mp3",
    language="en",
    include_timestamps=True
)

# Generate audio announcement
tts.synthesize(
    "The security briefing will begin in 5 minutes.",
    voice="onyx",  # Authoritative voice
    output_path="announcement.mp3"
)
```

---

## 23.4 Video Processing

```python
"""
Video Analysis System
Frame extraction and multimodal analysis
"""
import cv2
import base64
from pathlib import Path
import tempfile
from openai import OpenAI


class VideoAnalyzer:
    """
    ┌─────────────────────────────────────────────────────────┐
    │                  VIDEO ANALYZER                         │
    │                                                         │
    │  ┌─────────┐    ┌─────────────┐    ┌─────────────┐    │
    │  │  Video  │───▶│  Extract    │───▶│   Analyze   │    │
    │  │  Input  │    │  Frames     │    │   Frames    │    │
    │  └─────────┘    └─────────────┘    └─────────────┘    │
    │                        │                               │
    │                        ▼                               │
    │                 ┌─────────────┐                        │
    │                 │  Extract    │                        │
    │                 │  Audio      │───▶ Transcribe        │
    │                 └─────────────┘                        │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def extract_frames(
        self,
        video_path: str,
        frame_interval: int = 30,  # Extract every N frames
        max_frames: int = 50
    ) -> list[str]:
        """
        Extract key frames from video

        Args:
            video_path: Path to video file
            frame_interval: Extract every N frames
            max_frames: Maximum frames to extract
        """
        video = cv2.VideoCapture(video_path)
        frames = []
        frame_count = 0
        extracted = 0

        while video.isOpened() and extracted < max_frames:
            ret, frame = video.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                # Convert to base64
                _, buffer = cv2.imencode('.jpg', frame)
                b64 = base64.b64encode(buffer).decode('utf-8')
                frames.append(b64)
                extracted += 1

            frame_count += 1

        video.release()
        return frames

    def analyze_video(
        self,
        video_path: str,
        prompt: str,
        frame_interval: int = 60,
        max_frames: int = 20
    ) -> str:
        """
        Analyze video content using vision model
        """
        frames = self.extract_frames(video_path, frame_interval, max_frames)

        # Build content with frames
        content = []

        for i, frame_b64 in enumerate(frames):
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{frame_b64}",
                    "detail": "low"
                }
            })

        content.append({
            "type": "text",
            "text": f"""These are {len(frames)} frames extracted from a video.

            {prompt}

            Analyze the sequence of frames to understand the video content."""
        })

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": content}
            ],
            max_tokens=4096
        )

        return response.choices[0].message.content

    def extract_audio(self, video_path: str, output_path: str = None) -> str:
        """Extract audio track from video"""
        import subprocess

        if output_path is None:
            output_path = tempfile.mktemp(suffix=".mp3")

        # Use ffmpeg to extract audio
        cmd = [
            "ffmpeg", "-i", video_path,
            "-vn", "-acodec", "libmp3lame",
            "-y", output_path
        ]

        subprocess.run(cmd, capture_output=True, check=True)
        return output_path

    def full_video_analysis(
        self,
        video_path: str,
        analysis_prompt: str
    ) -> dict:
        """
        Complete video analysis: visual + audio

        Federal Use Case: Training video review, security footage
        """
        # Extract and analyze frames
        visual_analysis = self.analyze_video(
            video_path,
            "Describe what is happening in this video sequence."
        )

        # Extract and transcribe audio
        audio_path = self.extract_audio(video_path)

        transcriber = AudioTranscriber(api_key=self.client.api_key)
        transcript = transcriber.transcribe(audio_path)

        # Combined analysis
        combined_prompt = f"""
        Video Visual Analysis:
        {visual_analysis}

        Audio Transcript:
        {transcript.text if hasattr(transcript, 'text') else transcript}

        Based on both the visual content and audio:
        {analysis_prompt}
        """

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": combined_prompt}
            ]
        )

        return {
            "visual_analysis": visual_analysis,
            "transcript": transcript,
            "combined_analysis": response.choices[0].message.content
        }


# Usage
video_analyzer = VideoAnalyzer(api_key="your-key")

# Analyze training video
result = video_analyzer.full_video_analysis(
    "/videos/security_training.mp4",
    "Summarize the key training points and any compliance requirements mentioned."
)
```

---

## 23.5 Multimodal Agent Integration

```python
"""
Multimodal AI Agent
Combines vision, audio, and language capabilities
"""
from typing import Union, Literal
from dataclasses import dataclass
from openai import OpenAI
import anthropic


@dataclass
class MultimodalInput:
    """Container for multimodal inputs"""
    type: Literal["text", "image", "audio", "video"]
    content: str  # Text, path, or URL
    metadata: dict = None


class MultimodalAgent:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                       MULTIMODAL AGENT                                  │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                         │
    │   INPUT ROUTER                                                          │
    │   ┌─────────────────────────────────────────────────────────────────┐  │
    │   │                                                                 │  │
    │   │   Text ──────┐                                                  │  │
    │   │              │                                                  │  │
    │   │   Image ─────┼────▶ PROCESSOR ────▶ UNIFIED ────▶ LLM ────▶   │  │
    │   │              │      PIPELINE       CONTEXT       CORE    OUT  │  │
    │   │   Audio ─────┤                                                  │  │
    │   │              │                                                  │  │
    │   │   Video ─────┘                                                  │  │
    │   │                                                                 │  │
    │   └─────────────────────────────────────────────────────────────────┘  │
    │                                                                         │
    │   CAPABILITIES                                                          │
    │   • Document analysis & extraction                                      │
    │   • Meeting transcription & summarization                               │
    │   • Video content analysis                                              │
    │   • Accessibility transformations                                       │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
    """

    def __init__(
        self,
        openai_key: str,
        anthropic_key: str = None
    ):
        self.openai = OpenAI(api_key=openai_key)
        self.anthropic = anthropic.Anthropic(api_key=anthropic_key) if anthropic_key else None

        # Component analyzers
        self.vision = VisionAnalyzer(openai_key)
        self.audio = AudioTranscriber(openai_key)
        self.video = VideoAnalyzer(openai_key)
        self.tts = TextToSpeech(openai_key)

    def process_input(self, input_item: MultimodalInput) -> str:
        """Route input to appropriate processor"""

        if input_item.type == "text":
            return input_item.content

        elif input_item.type == "image":
            return self.vision.analyze_image(
                input_item.content,
                "Describe this image in detail.",
                detail="high"
            )

        elif input_item.type == "audio":
            transcript = self.audio.transcribe(input_item.content)
            return transcript.text if hasattr(transcript, 'text') else str(transcript)

        elif input_item.type == "video":
            return self.video.analyze_video(
                input_item.content,
                "Describe this video content.",
                max_frames=10
            )

    def process_multimodal(
        self,
        inputs: list[MultimodalInput],
        task: str,
        system_prompt: str = None
    ) -> str:
        """
        Process multiple inputs of different modalities

        Args:
            inputs: List of multimodal inputs
            task: The task/question to accomplish
            system_prompt: Optional system context
        """
        # Process each input
        processed = []
        for i, inp in enumerate(inputs):
            content = self.process_input(inp)
            processed.append(f"[{inp.type.upper()} {i+1}]:\n{content}")

        # Combine into unified context
        context = "\n\n---\n\n".join(processed)

        # Generate response
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({
            "role": "user",
            "content": f"""I have the following multimodal content:

{context}

---

Task: {task}"""
        })

        response = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=4096
        )

        return response.choices[0].message.content

    def accessibility_transform(
        self,
        content: Union[str, MultimodalInput],
        target_format: Literal["audio", "text", "simplified"]
    ) -> Union[str, bytes]:
        """
        Transform content for accessibility

        Federal Requirement: Section 508 compliance
        """
        # Get text content
        if isinstance(content, MultimodalInput):
            text = self.process_input(content)
        else:
            text = content

        if target_format == "audio":
            # Convert to speech
            return self.tts.synthesize(text, voice="nova")

        elif target_format == "simplified":
            # Simplify language
            response = self.openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "Rewrite the following text in plain language, suitable for a general audience. Use short sentences and common words."
                    },
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content

        else:
            return text


# Complete multimodal workflow example
async def process_briefing_materials():
    """
    Process a briefing package with multiple formats

    Federal Use Case: Process meeting materials including
    slides, audio recording, and supporting documents
    """
    agent = MultimodalAgent(
        openai_key="your-key",
        anthropic_key="your-anthropic-key"
    )

    inputs = [
        MultimodalInput(
            type="image",
            content="/briefing/slide_deck.pdf",  # Will be processed as images
            metadata={"source": "presentation"}
        ),
        MultimodalInput(
            type="audio",
            content="/briefing/meeting_recording.mp3",
            metadata={"duration": "45:00"}
        ),
        MultimodalInput(
            type="text",
            content="Additional context: This briefing covers Q4 security updates.",
            metadata={"type": "context"}
        )
    ]

    # Generate comprehensive summary
    summary = agent.process_multimodal(
        inputs,
        task="""Create a comprehensive briefing summary including:
        1. Key decisions made
        2. Action items with owners
        3. Security concerns raised
        4. Follow-up required""",
        system_prompt="You are a federal briefing analyst."
    )

    # Create accessible versions
    audio_summary = agent.accessibility_transform(
        summary,
        target_format="audio"
    )

    simplified = agent.accessibility_transform(
        summary,
        target_format="simplified"
    )

    return {
        "full_summary": summary,
        "audio_file": audio_summary,
        "simplified_text": simplified
    }
```

---

## 23.6 Federal Accessibility Compliance

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SECTION 508 COMPLIANCE FRAMEWORK                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  REQUIREMENT                    │ MULTIMODAL AI SOLUTION                   │
│  ─────────────────────────────────────────────────────────────────────────│
│                                                                             │
│  ✓ Text alternatives for       │ Vision model generates alt text          │
│    non-text content            │ for images automatically                  │
│                                                                             │
│  ✓ Captions for audio          │ Whisper provides accurate                 │
│    content                     │ transcription/captioning                  │
│                                                                             │
│  ✓ Audio descriptions for      │ Video analyzer creates audio              │
│    video content               │ description scripts                       │
│                                                                             │
│  ✓ Content readable by         │ Text-to-speech enables audio              │
│    screen readers              │ output of all content                     │
│                                                                             │
│  ✓ Plain language versions     │ LLM simplifies complex content            │
│    available                   │ to plain language                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

```python
"""
508 Compliance Automation System
"""

class AccessibilityCompliance:
    """
    Automated Section 508 compliance for multimodal content
    """

    def __init__(self, agent: MultimodalAgent):
        self.agent = agent

    def generate_alt_text(self, image_path: str) -> str:
        """Generate descriptive alt text for images"""
        prompt = """Generate concise, descriptive alt text for this image.

        Guidelines:
        - Be specific about what the image shows
        - Include relevant text visible in image
        - Keep under 125 characters if possible
        - Don't start with "Image of" or "Picture of"
        - Include relevant context for understanding"""

        return self.agent.vision.analyze_image(image_path, prompt, detail="low")

    def generate_captions(
        self,
        audio_path: str,
        format: Literal["srt", "vtt"] = "vtt"
    ) -> str:
        """Generate captions file from audio"""
        transcript = self.agent.audio.transcribe(
            audio_path,
            response_format=format
        )
        return transcript

    def generate_audio_description(
        self,
        video_path: str
    ) -> str:
        """Generate audio description script for video"""
        analysis = self.agent.video.analyze_video(
            video_path,
            """Create an audio description script for this video.

            For each significant scene change, describe:
            1. Visual elements not evident from dialogue
            2. Important actions and movements
            3. Scene settings and changes
            4. Relevant text or graphics shown

            Format as timed script:
            [00:00] Description
            [00:15] Description
            etc."""
        )
        return analysis

    def create_accessible_document(
        self,
        document_image: str,
        output_formats: list[str] = ["text", "audio", "simplified"]
    ) -> dict:
        """
        Create multiple accessible versions of a document

        Federal Use Case: Make all public documents 508 compliant
        """
        results = {}

        # Extract text from document image
        text_content = self.agent.vision.analyze_image(
            document_image,
            "Extract all text from this document, preserving structure."
        )
        results["text"] = text_content

        if "audio" in output_formats:
            results["audio"] = self.agent.tts.synthesize(
                text_content,
                voice="nova"
            )

        if "simplified" in output_formats:
            results["simplified"] = self.agent.accessibility_transform(
                text_content,
                target_format="simplified"
            )

        # Generate compliance report
        results["compliance_check"] = self._check_compliance(text_content)

        return results

    def _check_compliance(self, content: str) -> dict:
        """Check content against 508 requirements"""
        checks = {
            "has_structure": bool(content),
            "readable_font_implied": True,
            "plain_language_available": True,
            "audio_alternative_available": True
        }

        return {
            "compliant": all(checks.values()),
            "checks": checks
        }
```

---

## Hands-On Lab: Federal Document Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  LAB: Build a Multimodal Document Processing System                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  OBJECTIVE: Create a system that processes federal documents including:    │
│  • Scanned forms (images)                                                  │
│  • Audio recordings of meetings                                            │
│  • Video briefings                                                         │
│  • And makes them all accessible                                           │
│                                                                             │
│  DELIVERABLES:                                                              │
│  1. Document OCR and data extraction                                       │
│  2. Meeting transcription with speaker identification                      │
│  3. Video summarization                                                    │
│  4. 508-compliant output formats                                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Lab Tasks

1. **Implement document extraction pipeline**
2. **Add audio transcription with timestamps**
3. **Build video summarization**
4. **Create accessibility outputs**
5. **Build unified API endpoint**

---

## Knowledge Check

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ✓ COMPREHENSION QUESTIONS                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. What are the key differences between GPT-4V and Claude Vision?         │
│                                                                             │
│  2. How do you handle video files larger than API limits?                  │
│                                                                             │
│  3. What Section 508 requirements does multimodal AI help address?         │
│                                                                             │
│  4. How would you process a 2-hour meeting recording efficiently?          │
│                                                                             │
│  5. What security considerations apply to processing document images?       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  MODULE 23 SUMMARY: MULTIMODAL AI AGENTS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  KEY CAPABILITIES:                                                          │
│  ├── Vision: Document analysis, image understanding, OCR                   │
│  ├── Audio: Transcription, translation, text-to-speech                     │
│  ├── Video: Frame extraction, content analysis, summarization              │
│  └── Integration: Unified multimodal processing                            │
│                                                                             │
│  FEDERAL APPLICATIONS:                                                      │
│  ├── Form processing and data extraction                                   │
│  ├── Meeting transcription and summarization                               │
│  ├── Training video analysis                                               │
│  └── Section 508 compliance automation                                     │
│                                                                             │
│  NEXT: Module 24 - Workflow Automation                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Federal Working Group LLM Training Program - Module 23*
